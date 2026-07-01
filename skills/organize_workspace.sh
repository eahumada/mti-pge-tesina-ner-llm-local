#!/bin/bash

# skills/organize_workspace.sh
# This script reorganizes files into categorized directories based on a provided mapping.

set -e

# Define the target base directory for organized files
TARGET_BASE="doc/organized"
mkdir -p "$TARGET_BASE"

# Create a temporary file to store the mapping
MAPPING_FILE="organize_mapping.txt"
touch "$MAPPING_FILE"

echo "Starting reorganization..."

while IFS='|' read -r source_file category; do
    if [[ -n "$source_file" && -n "$regex" ]]; then
        # Create the specific category directory
        DEST_DIR="$TARGET_BASE/$category"
        mkdir -p "$DEST_DIR"

        echo "Moving $source_file to $DEST_DIR"

        # Move the original file if it exists
        if [[ -f "$source_file" ]]; then
            mv "$source_file" "$DEST_DIR/"
        fi

        # Also move the .md version if it exists (assuming same name + .md)
        MD_FILE="${source_file%.*}.md"
        if [[ -f "$MD_FILE" ]]; then
            mv "$MD_FILE" "$DEST_DIR/"
        fi
    fi
done < "$MAPPING_FILE"

# Clean up the mapping file
rm "$MAPPING_FILE"

echo "Reorganization complete. Files are located in $TARGET_BASE"
