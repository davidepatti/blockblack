# Bitcoin blockchain trivia reconstruction scripts

The folder contains `52` executable `slide-XX-*.sh` entry points, one for every
content slide from `3` through `54` in
`bitcoin-blockchain-trivia-and-fun-facts.pptx`. The scripts retrieve raw
transaction or block bytes, parse Bitcoin's binary serialization, isolate the
relevant script or witness carrier, concatenate its chunks in chain order, and
write both the untouched bytes and a decoded artifact.

## Requirements

- a Unix-like shell;
- Python `3.10` or newer from the standard system installation;
- either internet access to `https://mempool.space/api` or a synchronized
  Bitcoin Core node.

No Python packages are required.

## Run one slide

```sh
./slide-08-len-sassaman-memorial.sh
```

The default output is `./reconstructed/slide-08/`. To select another location:

```sh
./slide-08-len-sassaman-memorial.sh /tmp/len-memorial
```

Every result directory contains:

- the downloaded raw transaction or block in binary and hexadecimal form;
- `payload.raw`, the exact byte stream selected by the slide recipe;
- the reconstructed text, image, audio, document, archive, or diagnostic file;
- `transaction-summary.txt` when transactions are involved;
- `result.json`, recording the carrier, chunk count, output name, and caveats.

The runner never executes reconstructed programs, HTML, JavaScript, BASIC, or
archives. It writes archival bytes for inspection, which is important because
confirmed content can still be malicious.

## Read from Bitcoin Core instead of a public API

```sh
BITCOIN_CLI=/usr/local/bin/bitcoin-cli \
BITCOIN_CLI_ARGS='-rpcwallet=research' \
./slide-03-genesis-headline.sh
```

`BITCOIN_CLI_ARGS` is optional. A pruned node may not retain every historical
block required by this collection.

## Important boundaries

- Slides `4` and `5` describe historically meaningful payments rather than an
  arbitrary embedded file. Their scripts therefore preserve and summarize the
  canonical raw transactions instead of inventing a payload.
- Historic fake-address encodings can include ordinary payment or change
  outputs around the artifact. Recipes record any skipped chunks explicitly.
- Encrypted payloads remain encrypted; the script reconstructs ciphertext but
  cannot supply an unknown passphrase.
- Ordinal and other application-layer labels are not Bitcoin consensus data.
  The scripts parse witness bytes directly and do not rely on inscription IDs.
- Slide `39` reconstructs only what Bitcoin actually contains: signed root
  metadata and a `d6…@POT` pointer. The playable Pac-Man payload is referenced
  on Potcoin, so the script does not mislabel it as Bitcoin-resident HTML.
- Slide `54` is the largest job. It scans blocks `904,530–904,881`, fetches them
  concurrently when using the public API, records every contributing txid in
  `sermon-index.tsv`, and orders thousands of tagged `OP_RETURN` fragments.
  A local node is still the faster and more reproducible route.
- Copyrighted material is reconstructed only by an explicit user-run command;
  it is not bundled in this repository.

## Mapping and implementation

`manifest.json` is the auditable slide-to-chain map. `lib/bitcoin_payload.py`
contains the dependency-free transaction/block parser and carrier decoders.
`run-slide.sh` is the common runner used by the slide-specific entry points.

The implementation covers coinbase text, transaction summaries, legacy fake
public-key and fake-address storage, input-script pushes, P2SH publications,
`OP_RETURN`, SegWit witness bytes, Taproot inscription envelopes, legacy
Satoshi Uploader headers, and recursive AtomSea/EMBII links. File carving trims
known JPEG, PNG, PDF, MP3, and archive endings so padding bytes remain visible
in `payload.raw` without contaminating the reconstructed file.
