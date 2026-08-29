#!/usr/bin/env python3
"""Fetch and decode Bitcoin transaction payloads without third-party packages.

The default transport is mempool.space's public REST API.  Set BITCOIN_CLI to
the path of bitcoin-cli (and optionally BITCOIN_CLI_ARGS) to read from a local
Bitcoin Core node instead.  Every run retains the raw transaction or block
bytes next to the reconstructed payload.
"""

from __future__ import annotations

import argparse
import base64
import binascii
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zlib


API_BASE = os.environ.get("BITCOIN_API", "https://mempool.space/api").rstrip("/")
USER_AGENT = "BitcoinWiki-on-chain-reconstructor/1.0"


class DecodeError(RuntimeError):
    pass


def read_varint(data: bytes, offset: int) -> tuple[int, int]:
    if offset >= len(data):
        raise DecodeError("unexpected end of data while reading varint")
    marker = data[offset]
    if marker < 0xFD:
        return marker, offset + 1
    sizes = {0xFD: 2, 0xFE: 4, 0xFF: 8}
    size = sizes[marker]
    end = offset + 1 + size
    if end > len(data):
        raise DecodeError("truncated varint")
    return int.from_bytes(data[offset + 1 : end], "little"), end


def take(data: bytes, offset: int, size: int) -> tuple[bytes, int]:
    end = offset + size
    if end > len(data):
        raise DecodeError(f"truncated byte field: need {size} bytes at {offset}")
    return data[offset:end], end


def parse_tx(data: bytes, offset: int = 0) -> tuple[dict, int]:
    start = offset
    version_bytes, offset = take(data, offset, 4)
    segwit = offset + 1 < len(data) and data[offset] == 0 and data[offset + 1] != 0
    marker_flag = b""
    if segwit:
        marker_flag, offset = take(data, offset, 2)

    vin_count, offset = read_varint(data, offset)
    vins = []
    vin_serialized = []
    for _ in range(vin_count):
        vin_start = offset
        prev_hash, offset = take(data, offset, 32)
        prev_vout, offset = take(data, offset, 4)
        script_len, offset = read_varint(data, offset)
        script, offset = take(data, offset, script_len)
        sequence, offset = take(data, offset, 4)
        vin_serialized.append(data[vin_start:offset])
        vins.append(
            {
                "prev_txid": prev_hash[::-1].hex(),
                "prev_vout": int.from_bytes(prev_vout, "little"),
                "script": script,
                "sequence": int.from_bytes(sequence, "little"),
                "witness": [],
            }
        )

    vout_count_offset = offset
    vout_count, offset = read_varint(data, offset)
    vout_count_serialized = data[vout_count_offset:offset]
    vouts = []
    vout_serialized = []
    for n in range(vout_count):
        vout_start = offset
        value, offset = take(data, offset, 8)
        script_len, offset = read_varint(data, offset)
        script, offset = take(data, offset, script_len)
        vout_serialized.append(data[vout_start:offset])
        vouts.append({"n": n, "value": int.from_bytes(value, "little"), "script": script})

    if segwit:
        for vin in vins:
            item_count, offset = read_varint(data, offset)
            witness = []
            for _ in range(item_count):
                item_len, offset = read_varint(data, offset)
                item, offset = take(data, offset, item_len)
                witness.append(item)
            vin["witness"] = witness

    locktime, offset = take(data, offset, 4)
    full = data[start:offset]
    if segwit:
        stripped = version_bytes + encode_varint(vin_count) + b"".join(vin_serialized)
        stripped += vout_count_serialized + b"".join(vout_serialized) + locktime
    else:
        stripped = full
    txid = hashlib.sha256(hashlib.sha256(stripped).digest()).digest()[::-1].hex()
    wtxid = hashlib.sha256(hashlib.sha256(full).digest()).digest()[::-1].hex()
    return {
        "version": int.from_bytes(version_bytes, "little", signed=True),
        "segwit": segwit,
        "marker_flag": marker_flag,
        "vin": vins,
        "vout": vouts,
        "locktime": int.from_bytes(locktime, "little"),
        "raw": full,
        "stripped": stripped,
        "txid": txid,
        "wtxid": wtxid,
    }, offset


def encode_varint(value: int) -> bytes:
    if value < 0xFD:
        return bytes([value])
    if value <= 0xFFFF:
        return b"\xfd" + value.to_bytes(2, "little")
    if value <= 0xFFFFFFFF:
        return b"\xfe" + value.to_bytes(4, "little")
    return b"\xff" + value.to_bytes(8, "little")


def parse_block(data: bytes) -> dict:
    if len(data) < 81:
        raise DecodeError("block is too short")
    header = data[:80]
    count, offset = read_varint(data, 80)
    txs = []
    for _ in range(count):
        tx, offset = parse_tx(data, offset)
        txs.append(tx)
    if offset != len(data):
        raise DecodeError(f"block parser left {len(data) - offset} trailing bytes")
    block_hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1].hex()
    return {"header": header, "hash": block_hash, "tx": txs, "raw": data}


def script_pushes(script: bytes, start: int = 0) -> list[bytes]:
    pushes = []
    i = start
    while i < len(script):
        op = script[i]
        i += 1
        if 1 <= op <= 75:
            size = op
        elif op == 0x4C:
            if i >= len(script):
                break
            size = script[i]
            i += 1
        elif op == 0x4D:
            if i + 2 > len(script):
                break
            size = int.from_bytes(script[i : i + 2], "little")
            i += 2
        elif op == 0x4E:
            if i + 4 > len(script):
                break
            size = int.from_bytes(script[i : i + 4], "little")
            i += 4
        else:
            continue
        if i + size > len(script):
            break
        pushes.append(script[i : i + size])
        i += size
    return pushes


def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    acceptable = sum(1 for b in data if b in (9, 10, 13) or 32 <= b < 127)
    return acceptable / len(data)


def p2pkh_payload_chunks(tx: dict, dust_only: bool = False) -> list[bytes]:
    """Return the 20-byte hashes carried by P2PKH outputs.

    Historical P2FKH encoders used many equal-valued dust outputs for data and
    one differently valued P2PKH output for change.  When ``dust_only`` is
    true, select the most frequent output value; ties prefer the lowest value.
    This removes change without assuming that it appears at a fixed position.
    """
    candidates: list[tuple[int, bytes]] = []
    for out in tx["vout"]:
        script = out["script"]
        if len(script) == 25 and script[:3] == b"\x76\xa9\x14" and script[-2:] == b"\x88\xac":
            candidates.append((out["value"], script[3:23]))
    if not dust_only or len(candidates) < 2:
        return [chunk for _, chunk in candidates]
    counts = Counter(value for value, _ in candidates)
    maximum = max(counts.values())
    payload_value = min(value for value, count in counts.items() if count == maximum)
    return [chunk for value, chunk in candidates if value == payload_value]


def extract_stream(tx: dict, stream: str) -> tuple[bytes, list[bytes]]:
    chunks: list[bytes] = []
    if stream == "coinbase":
        chunks = [tx["vin"][0]["script"]] if tx["vin"] else []
    elif stream == "opreturn":
        for out in tx["vout"]:
            script = out["script"]
            if script[:1] == b"\x6a":
                chunks.extend(script_pushes(script, 1))
    elif stream == "p2pkh":
        chunks = p2pkh_payload_chunks(tx)
    elif stream == "p2pkh-dust":
        chunks = p2pkh_payload_chunks(tx, dust_only=True)
    elif stream == "p2sh":
        for out in tx["vout"]:
            script = out["script"]
            if len(script) == 23 and script[:2] == b"\xa9\x14" and script[-1:] == b"\x87":
                chunks.append(script[2:22])
    elif stream == "p2pk":
        for out in tx["vout"]:
            script = out["script"]
            pushes = script_pushes(script)
            if script[-1:] == b"\xac" and pushes:
                chunks.extend(pushes)
    elif stream == "outputs":
        for out in tx["vout"]:
            chunks.extend(script_pushes(out["script"]))
    elif stream == "multisig":
        for out in tx["vout"]:
            script = out["script"]
            if script[-1:] == b"\xae":
                chunks.extend(script_pushes(script))
    elif stream == "inputs":
        for vin in tx["vin"]:
            chunks.extend(script_pushes(vin["script"]))
    elif stream == "input-text":
        for vin in tx["vin"]:
            for chunk in script_pushes(vin["script"]):
                stripped = chunk.strip(b"\x00 \t\r\n")
                if not stripped:
                    continue
                padded = chunk.startswith(b"\x00") or chunk.endswith(b"\x00")
                if padded and printable_ratio(stripped) >= 0.80:
                    chunks.append(stripped)
    elif stream == "input-raw":
        chunks = [vin["script"] for vin in tx["vin"]]
    elif stream == "witness":
        for vin in tx["vin"]:
            chunks.extend(vin["witness"])
    elif stream == "inscription":
        chunks = extract_inscriptions(tx)
    elif stream == "auto":
        inscriptions = extract_inscriptions(tx)
        if inscriptions:
            chunks = inscriptions
        else:
            opreturns = extract_stream(tx, "opreturn")[1]
            p2pkh = extract_stream(tx, "p2pkh")[1]
            output_chunks = extract_stream(tx, "outputs")[1]
            input_chunks = extract_stream(tx, "inputs")[1]
            witness_chunks = extract_stream(tx, "witness")[1]
            if opreturns:
                chunks = opreturns
            elif len([chunk for chunk in output_chunks if len(chunk) >= 32]) >= 2:
                chunks = output_chunks
            elif len(p2pkh) >= 2:
                chunks = p2pkh
            elif input_chunks and printable_ratio(b"".join(input_chunks)) > 0.35:
                chunks = input_chunks
            else:
                chunks = witness_chunks
    else:
        raise DecodeError(f"unknown stream: {stream}")
    return b"".join(chunks), chunks


def extract_inscriptions(tx: dict) -> list[bytes]:
    results = []
    for vin in tx["vin"]:
        for item in vin["witness"]:
            marker = item.find(b"\x00\x63\x03ord")
            if marker < 0:
                continue
            script = item[marker + 2 :]
            pushes = script_pushes(script)
            try:
                ord_index = pushes.index(b"ord")
            except ValueError:
                continue
            after = pushes[ord_index + 1 :]
            if not after:
                continue
            # Ord envelopes place the body after an empty field separator.  A
            # push parser omits OP_0, so concatenate all non-MIME pushes after
            # the metadata fields and keep only the largest coherent suffix.
            candidates = [p for p in after if len(p) > 2 and b"/" not in p[:40]]
            if candidates:
                results.append(b"".join(candidates))
    return results


def local_cli() -> list[str] | None:
    executable = os.environ.get("BITCOIN_CLI")
    if not executable:
        return None
    return [executable, *shlex.split(os.environ.get("BITCOIN_CLI_ARGS", ""))]


def run_cli(*args: str) -> str:
    cmd = local_cli()
    if not cmd:
        raise DecodeError("BITCOIN_CLI is not set")
    proc = subprocess.run([*cmd, *args], check=True, text=True, capture_output=True)
    return proc.stdout.strip()


def http_get(path: str, binary: bool = False) -> bytes | str:
    url = f"{API_BASE}{path}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
                return body if binary else body.decode("utf-8").strip()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt < 3:
                time.sleep(1.5 * (attempt + 1))
    raise DecodeError(f"failed to fetch {url}: {last_error}")


def fetch_tx_hex(txid: str) -> str:
    if local_cli():
        return run_cli("getrawtransaction", txid)
    return str(http_get(f"/tx/{txid}/hex"))


def fetch_block_hash(height: int) -> str:
    if local_cli():
        return run_cli("getblockhash", str(height))
    return str(http_get(f"/block-height/{height}"))


def fetch_block_raw(block_hash: str) -> bytes:
    if local_cli():
        return bytes.fromhex(run_cli("getblock", block_hash, "0"))
    return bytes(http_get(f"/block/{block_hash}/raw", binary=True))


def write_raw_tx(txid: str, out_dir: Path) -> dict:
    hex_text = fetch_tx_hex(txid)
    raw = bytes.fromhex(hex_text)
    tx, consumed = parse_tx(raw)
    if consumed != len(raw):
        raise DecodeError(f"transaction parser left {len(raw) - consumed} trailing bytes")
    (out_dir / f"{txid}.tx.hex").write_text(hex_text + "\n", encoding="ascii")
    (out_dir / f"{txid}.tx.bin").write_bytes(raw)
    return tx


def trim_payload(data: bytes, recipe: dict) -> bytes:
    if recipe.get("nul_to_newline"):
        data = data.replace(b"\x00", b"\n")
    if recipe.get("trim_before"):
        marker = recipe["trim_before"].encode("utf-8")
        index = data.find(marker)
        if index >= 0:
            data = data[index:]
    if recipe.get("trim_after"):
        marker = recipe["trim_after"].encode("utf-8")
        index = data.find(marker)
        if index >= 0:
            data = data[: index + len(marker)]
    if recipe.get("trim_after_last"):
        marker = recipe["trim_after_last"].encode("utf-8")
        index = data.rfind(marker)
        if index >= 0:
            data = data[: index + len(marker)]
    strip = int(recipe.get("strip_bytes", 0))
    if strip:
        data = data[strip:]
    if recipe.get("trim_magic"):
        markers = [b"%PDF", b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF87a", b"GIF89a", b"ID3", b"-----BEGIN PGP", b"\x1f\x8b", b"PK\x03\x04"]
        locations = [(data.find(marker), marker) for marker in markers]
        locations = [item for item in locations if item[0] >= 0]
        if locations:
            data = data[min(locations, key=lambda item: item[0])[0] :]
    if recipe.get("trim_known_end"):
        if data.startswith(b"\xff\xd8\xff"):
            end = data.find(b"\xff\xd9", 3)
            if end >= 0:
                data = data[: end + 2]
        elif data.startswith(b"\x89PNG\r\n\x1a\n"):
            end = data.find(b"IEND")
            if end >= 4 and end + 8 <= len(data):
                data = data[: end + 8]
        elif data.startswith((b"GIF87a", b"GIF89a")):
            end = data.find(b"\x3b", 6)
            if end >= 0:
                data = data[: end + 1]
        elif data.startswith(b"%PDF"):
            end = data.rfind(b"%%EOF")
            if end >= 0:
                data = data[: end + 5]
    if recipe.get("rstrip_nul"):
        data = data.rstrip(b"\x00")
    return data


def yenc_decode(data: bytes) -> bytes:
    begin = data.find(b"=ybegin")
    if begin < 0:
        raise DecodeError("no yEnc header found")
    first_newline = data.find(b"\n", begin)
    end = data.find(b"=yend", first_newline + 1)
    if first_newline < 0 or end < 0:
        raise DecodeError("incomplete yEnc payload")
    encoded = data[first_newline + 1 : end].replace(b"\r", b"").replace(b"\n", b"")
    decoded = bytearray()
    i = 0
    while i < len(encoded):
        value = encoded[i]
        i += 1
        if value == 61 and i < len(encoded):
            value = (encoded[i] - 64) & 0xFF
            i += 1
        decoded.append((value - 42) & 0xFF)
    return bytes(decoded)


def decode_data_url(data: bytes) -> tuple[bytes, str] | None:
    match = re.search(br"data:([^;,\s]+);base64,([A-Za-z0-9+/=\r\n]+)", data)
    if not match:
        return None
    mime = match.group(1).decode("ascii", "replace")
    decoded = base64.b64decode(re.sub(br"\s+", b"", match.group(2)), validate=False)
    extension = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "audio/mpeg": ".mp3",
        "text/html": ".html",
    }.get(mime, ".bin")
    return decoded, extension


def sniff_extension(data: bytes) -> str:
    signatures = [
        (b"%PDF", ".pdf"),
        (b"\x89PNG\r\n\x1a\n", ".png"),
        (b"\xff\xd8\xff", ".jpg"),
        (b"GIF87a", ".gif"),
        (b"GIF89a", ".gif"),
        (b"ID3", ".mp3"),
        (b"-----BEGIN PGP", ".asc"),
        (b"\x1f\x8b", ".gz"),
        (b"PK\x03\x04", ".zip"),
    ]
    for signature, extension in signatures:
        if data.startswith(signature):
            return extension
    if printable_ratio(data) > 0.78:
        return ".txt"
    return ".bin"


def write_strings_report(data: bytes, out_dir: Path, minimum: int = 4) -> None:
    lines = []
    for match in re.finditer(rb"[\x09\x0a\x0d\x20-\x7e]{%d,}" % minimum, data):
        text = match.group(0).decode("ascii", "replace")
        lines.append(f"{match.start():08x}\t{text}")
    (out_dir / "printable-strings.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def carve_known_files(data: bytes, out_dir: Path) -> list[str]:
    markers = [
        (b"%PDF", ".pdf"),
        (b"\x89PNG\r\n\x1a\n", ".png"),
        (b"\xff\xd8\xff", ".jpg"),
        (b"GIF87a", ".gif"),
        (b"GIF89a", ".gif"),
        (b"ID3", ".mp3"),
        (b"\x1f\x8b", ".gz"),
        (b"PK\x03\x04", ".zip"),
    ]
    outputs = []
    for marker, extension in markers:
        start = data.find(marker)
        if start < 0:
            continue
        carved = data[start:]
        if extension == ".jpg":
            end = carved.find(b"\xff\xd9", 3)
            if end >= 0:
                carved = carved[: end + 2]
        path = out_dir / f"carved-{start:08x}{extension}"
        path.write_bytes(carved)
        outputs.append(path.name)
    return outputs


def save_decoded(data: bytes, recipe: dict, out_dir: Path) -> Path:
    decode_mode = recipe.get("decode", "auto")
    filename = recipe.get("filename", "payload")
    decoded = data
    extension = ""
    if decode_mode == "yenc":
        decoded = yenc_decode(data)
    elif decode_mode == "base64":
        result = decode_data_url(data)
        if not result:
            raise DecodeError("no base64 data URL found")
        decoded, extension = result
    elif decode_mode == "text":
        decoded = data.decode("utf-8", "replace").encode("utf-8")
        extension = ".txt"
    elif decode_mode == "latin1":
        decoded = data.decode("latin-1").encode("utf-8")
        extension = ".txt"
    elif decode_mode == "auto":
        if b"=ybegin" in data and b"=yend" in data:
            decoded = yenc_decode(data)
        else:
            result = decode_data_url(data)
            if result:
                decoded, extension = result
    elif decode_mode != "none":
        raise DecodeError(f"unknown decode mode: {decode_mode}")

    if not extension:
        extension = sniff_extension(decoded)
    if Path(filename).suffix:
        output = out_dir / filename
    else:
        output = out_dir / f"{filename}{extension}"
    output.write_bytes(decoded)
    return output


def transaction_summary(tx: dict) -> str:
    lines = [
        f"txid: {tx['txid']}",
        f"wtxid: {tx['wtxid']}",
        f"version: {tx['version']}",
        f"segwit: {tx['segwit']}",
        f"inputs: {len(tx['vin'])}",
        f"outputs: {len(tx['vout'])}",
        f"output total (sats): {sum(out['value'] for out in tx['vout'])}",
        "",
    ]
    for out in tx["vout"]:
        lines.append(f"vout {out['n']}: {out['value']} sats script={out['script'].hex()}")
    return "\n".join(lines) + "\n"


def reconstruct_transactions(recipe: dict, out_dir: Path) -> tuple[bytes, dict]:
    all_chunks = []
    tx_summaries = []
    stream = recipe.get("stream", "auto")
    for txid in recipe.get("txids", []):
        tx = write_raw_tx(txid, out_dir)
        tx_summaries.append(transaction_summary(tx))
        payload, chunks = extract_stream(tx, stream)
        if recipe.get("satoshi_uploader"):
            if len(payload) < 8:
                raise DecodeError(f"Satoshi uploader payload in {txid} is shorter than its header")
            declared_size = int.from_bytes(payload[:4], "little")
            end = 8 + declared_size
            if end > len(payload):
                raise DecodeError(
                    f"Satoshi uploader payload in {txid} declares {declared_size} bytes "
                    f"but only {len(payload) - 8} follow the header"
                )
            all_chunks.append(payload[8:end])
        else:
            all_chunks.extend(chunks)
    skip = int(recipe.get("skip_chunks", 0))
    take_count = recipe.get("take_chunks")
    selected = all_chunks[skip:]
    if take_count is not None:
        selected = selected[: int(take_count)]
    if recipe.get("printable_chunks_min") is not None:
        threshold = float(recipe["printable_chunks_min"])
        selected = [
            chunk.rstrip(b"\x00")
            for chunk in selected
            if printable_ratio(chunk.rstrip(b"\x00")) >= threshold
        ]
    separator = recipe.get("chunk_separator", "").encode("utf-8")
    data = trim_payload(separator.join(selected), recipe)
    (out_dir / "transaction-summary.txt").write_text("\n".join(tx_summaries), encoding="utf-8")
    metadata = {"chunks_found": len(all_chunks), "chunks_used": len(selected), "stream": stream}
    return data, metadata


def reconstruct_atomsea(recipe: dict, out_dir: Path) -> tuple[bytes, dict]:
    """Reassemble an AtomSea/EMBII object from its on-chain root index.

    The root's equal-valued P2PKH dust outputs contain an ASCII list of leaf
    transaction IDs.  Each leaf's equal-valued P2PKH outputs carry the next
    contiguous section of the object.  No Bitfossil or other off-chain index is
    consulted: the root transaction is the index.
    """
    root_txid = recipe.get("root_txid") or recipe.get("txids", [None])[0]
    if not root_txid:
        raise DecodeError("AtomSea recipe requires root_txid or one txid")
    root = write_raw_tx(root_txid, out_dir)
    root_chunks = p2pkh_payload_chunks(root, dust_only=True)
    root_index = b"".join(root_chunks)
    (out_dir / "atomsea-root-index.raw").write_bytes(root_index)
    (out_dir / "atomsea-root-index.txt").write_text(
        root_index.decode("ascii", "replace"), encoding="utf-8"
    )

    foreign_links: set[tuple[str, str]] = set()

    def linked_txids(index_bytes: bytes) -> list[str]:
        links: list[str] = []
        local_seen = set()
        candidates: list[bytes] = []
        repeated = re.match(
            br"^([0-9A-Fa-f]{64})[^0-9A-Za-z\s][0-9]{1,18}[^0-9A-Za-z\s]\1(?:\r?\n|$)",
            index_bytes,
        )
        if repeated:
            candidates.append(repeated.group(1))
        # The protocol's remaining links are CRLF-delimited, bare txids.  Do
        # not treat every 64-hex substring as a link: signed AtomSea metadata
        # may also contain non-transaction content hashes.
        for line in index_bytes.splitlines():
            line = line.strip()
            if re.fullmatch(br"[0-9A-Fa-f]{64}", line):
                candidates.append(line)
        # Later Apertus roots wrap links in a normal file record named LNK:
        # LNK<delimiter><decimal byte count><delimiter><txid[@CHAIN]...>.
        # Parse the declared content length so a SHA-256 proof hash elsewhere
        # in signed metadata is never mistaken for a transaction ID.
        for match in re.finditer(
            br"LNK[^0-9A-Za-z\s]([0-9]{1,30})[^0-9A-Za-z\s]", index_bytes
        ):
            size = int(match.group(1))
            content = index_bytes[match.end() : match.end() + size]
            for line in content.splitlines():
                link = re.search(br"([0-9A-Fa-f]{64})(?:@([A-Za-z0-9]+))?", line)
                if not link:
                    continue
                txid = link.group(1)
                chain = link.group(2)
                if chain and chain.upper() not in (b"BTC", b"BITCOIN"):
                    foreign_links.add(
                        (txid.decode("ascii").lower(), chain.decode("ascii").upper())
                    )
                else:
                    candidates.append(txid)
        for candidate in candidates:
            txid = candidate.decode("ascii").lower()
            if txid not in local_seen:
                links.append(txid)
                local_seen.add(txid)
        return links

    def is_nested_index(index_bytes: bytes) -> bool:
        # A nested index starts with a txid, punctuation, a decimal byte count,
        # punctuation, and the same txid again.  This is deliberately stricter
        # than merely finding hashes in arbitrary prose.
        match = re.match(
            br"^([0-9A-Fa-f]{64})[^0-9A-Za-z\s][0-9]{1,18}[^0-9A-Za-z\s]\1(?:\r?\n|$)",
            index_bytes,
        )
        if match is not None:
            return True
        return b"LNK|" in index_bytes[:512] and bool(linked_txids(index_bytes))

    maximum = int(recipe.get("max_links", 4096))
    maximum_depth = int(recipe.get("max_depth", 8))
    summaries = ["ROOT\n" + transaction_summary(root)]
    link_log: list[str] = []
    total_chunks = 0
    total_links = 0
    current_index = root_index
    ordered_links = linked_txids(current_index)
    data = root_index
    depth = 0
    fetched = set()
    while ordered_links:
        if depth >= maximum_depth:
            raise DecodeError(f"AtomSea index exceeded recursion limit {maximum_depth}")
        if total_links + len(ordered_links) > maximum:
            raise DecodeError(
                f"AtomSea object exceeds linked-transaction safety limit {maximum}"
            )
        (out_dir / f"atomsea-level-{depth:02d}-index.raw").write_bytes(current_index)
        assembled: list[bytes] = []
        for index, txid in enumerate(ordered_links, start=1):
            if txid in fetched:
                raise DecodeError(f"AtomSea index repeats transaction across levels: {txid}")
            fetched.add(txid)
            tx = write_raw_tx(txid, out_dir)
            link_log.append(f"{depth}\t{index}\t{txid}")
            summaries.append(
                f"LEVEL {depth} ITEM {index}/{len(ordered_links)}\n" + transaction_summary(tx)
            )
            chunks = p2pkh_payload_chunks(tx, dust_only=True)
            total_chunks += len(chunks)
            assembled.extend(chunks)
        total_links += len(ordered_links)
        data = b"".join(assembled)
        depth += 1
        if not is_nested_index(data):
            break
        current_index = data
        ordered_links = linked_txids(current_index)

    (out_dir / "atomsea-links.tsv").write_text(
        "depth\tposition\ttxid\n" + "\n".join(link_log) + ("\n" if link_log else ""),
        encoding="ascii",
    )
    (out_dir / "atomsea-foreign-links.tsv").write_text(
        "txid\tchain\n"
        + "\n".join(f"{txid}\t{chain}" for txid, chain in sorted(foreign_links))
        + ("\n" if foreign_links else ""),
        encoding="ascii",
    )
    data = trim_payload(data, recipe)
    (out_dir / "transaction-summary.txt").write_text("\n".join(summaries), encoding="utf-8")
    return data, {
        "root_txid": root_txid,
        "linked_transactions": total_links,
        "index_depth": depth,
        "foreign_links": len(foreign_links),
        "chunks_used": total_chunks if total_links else len(root_chunks),
        "stream": "atomsea-p2pkh-dust",
    }


def reconstruct_block(recipe: dict, out_dir: Path) -> tuple[bytes, dict]:
    block_hash = recipe.get("block_hash")
    if not block_hash:
        block_hash = fetch_block_hash(int(recipe["height"]))
    raw = fetch_block_raw(block_hash)
    (out_dir / f"{block_hash}.block.bin").write_bytes(raw)
    block = parse_block(raw)
    (out_dir / f"{block_hash}.block.hex").write_text(raw.hex() + "\n", encoding="ascii")
    coinbase = block["tx"][0]
    stream = recipe.get("stream", "coinbase")
    if stream == "block-opreturns":
        chunks = []
        for tx in block["tx"]:
            chunks.extend(extract_stream(tx, "opreturn")[1])
        data = b"\n".join(chunks)
    else:
        data, chunks = extract_stream(coinbase, stream)
    data = trim_payload(data, recipe)
    metadata = {"block_hash": block_hash, "transactions": len(block["tx"]), "stream": stream}
    return data, metadata


def scan_block_matching_opreturns(data: bytes, pattern: re.Pattern[str]) -> list[tuple[str, bytes, str]]:
    """Scan a raw block for matching OP_RETURN records without materializing it.

    Current blocks contain thousands of unrelated transactions.  This parser
    advances over their fields, retains only matching OP_RETURN payloads, and
    computes a txid only for transactions that actually match.
    """
    if len(data) < 81:
        raise DecodeError("block is too short")
    tx_count, offset = read_varint(data, 80)
    results: list[tuple[str, bytes, str]] = []
    for _ in range(tx_count):
        tx_start = offset
        _, offset = take(data, offset, 4)
        segwit = offset + 1 < len(data) and data[offset] == 0 and data[offset + 1] != 0
        if segwit:
            _, offset = take(data, offset, 2)
        vin_count, offset = read_varint(data, offset)
        for _ in range(vin_count):
            _, offset = take(data, offset, 36)
            script_len, offset = read_varint(data, offset)
            _, offset = take(data, offset, script_len)
            _, offset = take(data, offset, 4)
        vout_count, offset = read_varint(data, offset)
        matched: list[tuple[str, bytes]] = []
        for _ in range(vout_count):
            _, offset = take(data, offset, 8)
            script_len, offset = read_varint(data, offset)
            script, offset = take(data, offset, script_len)
            if script[:1] == b"\x6a":
                for payload in script_pushes(script, 1):
                    text_value = payload.decode("utf-8", "ignore")
                    match = pattern.match(text_value)
                    if match:
                        matched.append((match.group(0), payload[len(match.group(0)) :]))
        if segwit:
            for _ in range(vin_count):
                item_count, offset = read_varint(data, offset)
                for _ in range(item_count):
                    item_len, offset = read_varint(data, offset)
                    _, offset = take(data, offset, item_len)
        _, offset = take(data, offset, 4)
        if matched:
            tx, consumed = parse_tx(data, tx_start)
            if consumed != offset:
                raise DecodeError("targeted scanner and transaction parser disagree on length")
            results.extend((key, payload, tx["txid"]) for key, payload in matched)
    if offset != len(data):
        raise DecodeError(f"targeted block scanner left {len(data) - offset} trailing bytes")
    return results


def reconstruct_sermon(recipe: dict, out_dir: Path) -> tuple[bytes, dict]:
    pattern = re.compile(recipe.get("match", r"^(08|09|10)JULY[0-9]{4}"))
    pieces: list[tuple[str, bytes, str]] = []
    heights = list(range(int(recipe["start_height"]), int(recipe["end_height"]) + 1))

    def scan_height(height: int) -> list[tuple[str, bytes, str]]:
        block_hash = fetch_block_hash(height)
        raw = fetch_block_raw(block_hash)
        if recipe.get("retain_blocks"):
            (out_dir / f"block-{height}-{block_hash}.bin").write_bytes(raw)
        return scan_block_matching_opreturns(raw, pattern)

    workers = max(1, min(int(recipe.get("workers", 6)), 12))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_height, height): height for height in heights}
        completed = 0
        for future in as_completed(futures):
            pieces.extend(future.result())
            completed += 1
            if completed % 50 == 0 or completed == len(heights):
                print(f"Scanned {completed}/{len(heights)} blocks", file=sys.stderr)
    pieces.sort(key=lambda item: (int(item[0][:2]), int(item[0][-4:])))
    index_lines = [f"{key}\t{txid}" for key, _, txid in pieces]
    (out_dir / "sermon-index.tsv").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    data = b"".join(piece for _, piece, _ in pieces)
    return data, {
        "pieces": len(pieces),
        "blocks_scanned": len(heights),
        "range": [recipe["start_height"], recipe["end_height"]],
    }


def run_recipe(manifest_path: Path, slide: str, out_dir: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    key = str(int(slide))
    if key not in manifest["slides"]:
        raise DecodeError(f"slide {slide} is not present in {manifest_path}")
    recipe = manifest["slides"][key]
    out_dir.mkdir(parents=True, exist_ok=True)
    kind = recipe.get("kind", "transaction")
    if kind in ("transaction", "transaction-summary"):
        data, metadata = reconstruct_transactions(recipe, out_dir)
    elif kind == "atomsea":
        data, metadata = reconstruct_atomsea(recipe, out_dir)
    elif kind == "block":
        data, metadata = reconstruct_block(recipe, out_dir)
    elif kind == "height-range-opreturn":
        data, metadata = reconstruct_sermon(recipe, out_dir)
    else:
        raise DecodeError(f"unsupported recipe kind: {kind}")

    (out_dir / "payload.raw").write_bytes(data)
    write_strings_report(data, out_dir)
    carved_files = carve_known_files(data, out_dir)
    if kind == "transaction-summary":
        output = out_dir / "transaction-summary.txt"
    else:
        output = save_decoded(data, recipe, out_dir)
    metadata.update(
        {
            "slide": int(slide),
            "title": recipe.get("title"),
            "kind": kind,
            "output": output.name,
            "raw_payload_bytes": len(data),
            "carved_files": carved_files,
            "note": recipe.get("note", ""),
        }
    )
    (out_dir / "result.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Slide {int(slide):02d}: {recipe.get('title', '')}")
    print(f"Output: {output}")
    print(f"Raw payload: {out_dir / 'payload.raw'}")
    if recipe.get("note"):
        print(f"Note: {recipe['note']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--slide", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        run_recipe(args.manifest, args.slide, args.out)
    except (DecodeError, OSError, ValueError, binascii.Error, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
