#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "$#" -lt 1 ]; then
  echo "usage: $0 TRIVIA_NAME [OUTPUT_DIRECTORY]" >&2
  exit 2
fi

TRIVIA=$1
shift
case "$TRIVIA" in
  ''|*[!a-z0-9-]*)
    echo "invalid trivia name: $TRIVIA" >&2
    exit 2
    ;;
esac

if [ "$#" -gt 0 ]; then
  OUTPUT_DIR=$1
else
  OUTPUT_DIR=$PWD/reconstructed/$TRIVIA
fi

exec python3 "$SCRIPT_DIR/lib/bitcoin_payload.py" \
  --manifest "$SCRIPT_DIR/manifest.json" \
  --trivia "$TRIVIA" \
  --out "$OUTPUT_DIR"
