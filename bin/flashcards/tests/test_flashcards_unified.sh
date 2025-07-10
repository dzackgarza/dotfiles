#!/bin/bash
set -e

# Test script for flashcards_unified.py
SAMPLEDIR="$(dirname "$0")/../sample_flashcards"
OUTDIR="$(dirname "$0")/output"
SCRIPT="$(dirname "$0")/../flashcards_unified.py"

mkdir -p "$OUTDIR"

# Run the unified script on the sample directory
echo "Running flashcards_unified.py on $SAMPLEDIR..."
python3 "$SCRIPT" "$SAMPLEDIR" --output "$OUTDIR/test_deck.apkg" --copy-images

if [ -f "$OUTDIR/test_deck.apkg" ]; then
  echo "Test passed: Deck created at $OUTDIR/test_deck.apkg"
else
  echo "Test failed: Deck not created."
  exit 1
fi
