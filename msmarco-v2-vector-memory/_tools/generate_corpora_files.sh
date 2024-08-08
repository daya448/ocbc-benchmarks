#!/bin/bash

# Check if DIR is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 DIR"
  exit 1
fi

DIR=$1

# Create the tmp directory if it doesn't exist
mkdir -p "$DIR/tmp"

# Loop through all files in the DIR named cohere-documents-0<n>.json, with <n> between 4 and 6
for FILE in "$DIR"/cohere-documents-0{4..6}.json; do
  if [ -f "$FILE" ]; then
    # Split each file into files with 1 million lines under DIR/tmp
    split -l 1000000 "$FILE" "$DIR/tmp/$(basename "$FILE" .json)-"
  fi
done

# Loop through all files in DIR/tmp and keep track of iteration number, starting with index 1
i=1
for TMP_FILE in "$DIR/tmp"/*; do
  if [ -f "$TMP_FILE" ]; then
    # Create a directory DIR/msmarco-memory-<i>
    DEST_DIR="$DIR/msmarco-memory-$i"
    mkdir -p "$DEST_DIR"

    # Move the file to DIR/msmarco-memory-<i>/msmarco-memory-documents-<i>.json
    DEST_FILE="$DEST_DIR/msmarco-memory-documents-$i.json"
    mv "$TMP_FILE" "$DEST_FILE"

    # Compress the file using bzip2 and keep the original file
    bzip2 -k "$DEST_FILE"

    i=$((i + 1))
  fi
done

# Delete the tmp directory
rm -rf "$DIR/tmp"

echo "Processing complete."
