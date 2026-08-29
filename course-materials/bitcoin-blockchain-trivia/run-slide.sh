#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
NAME=$(basename -- "$0")

case "$NAME" in
  slide-[0-9][0-9]-*.sh) SLIDE=$(printf '%s' "$NAME" | cut -c 7-8) ;;
  run-slide.sh)
    if [ "$#" -lt 1 ]; then
      echo "usage: $0 SLIDE_NUMBER [OUTPUT_DIRECTORY]" >&2
      exit 2
    fi
    SLIDE=$1
    case "$SLIDE" in 0*) SLIDE=${SLIDE#0} ;; esac
    SLIDE=$(printf '%02d' "$SLIDE")
    shift
    ;;
  *)
    echo "cannot infer a slide number from $NAME" >&2
    exit 2
    ;;
esac

if [ "$#" -gt 0 ]; then
  OUTPUT_DIR=$1
else
  OUTPUT_DIR=$PWD/reconstructed/slide-$SLIDE
fi

exec python3 "$SCRIPT_DIR/lib/bitcoin_payload.py" \
  --manifest "$SCRIPT_DIR/manifest.json" \
  --slide "$SLIDE" \
  --out "$OUTPUT_DIR"
