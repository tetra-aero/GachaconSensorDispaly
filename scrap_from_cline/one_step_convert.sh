#!/bin/bash

# Input and output files
INPUT_FILE="GACHACON_log/test_canlog_250403-1-1.log"
OUTPUT_FILE="GACHACON_log/candump-2025-04-03_142614.log"

# Remove the output file if it exists
rm -f "$OUTPUT_FILE"

# Process each line, ensuring proper formatting
while IFS= read -r line; do
    # Extract timestamp, ID, and data
    if [[ $line =~ ^\(([0-9]+\.[0-9]+)\)[[:space:]]+vcan0[[:space:]]+([0-9A-F]+)[[:space:]]+\[[0-9]+\][[:space:]]+(.+)$ ]]; then
        # Line with parentheses around timestamp
        timestamp="${BASH_REMATCH[1]}"
        id="${BASH_REMATCH[2]}"
        data="${BASH_REMATCH[3]}"
        # Remove spaces from data
        data_no_spaces=$(echo "$data" | tr -d ' ')
        # Write in target format
        echo "($timestamp) vcan0 $id#$data_no_spaces" >> "$OUTPUT_FILE"
    elif [[ $line =~ ^([0-9]+\.[0-9]+)\)[[:space:]]+vcan0[[:space:]]+([0-9A-F]+)[[:space:]]+\[[0-9]+\][[:space:]]+(.+)$ ]]; then
        # Line without parentheses around timestamp
        timestamp="${BASH_REMATCH[1]}"
        id="${BASH_REMATCH[2]}"
        data="${BASH_REMATCH[3]}"
        # Remove spaces from data
        data_no_spaces=$(echo "$data" | tr -d ' ')
        # Write in target format with parentheses
        echo "($timestamp) vcan0 $id#$data_no_spaces" >> "$OUTPUT_FILE"
    else
        # Line doesn't match expected format, copy as is
        echo "Warning: Could not parse line: $line"
        echo "$line" >> "$OUTPUT_FILE"
    fi
done < "$INPUT_FILE"

echo "Conversion complete. Output saved to $OUTPUT_FILE"
