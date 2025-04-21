#!/bin/bash

# Remove existing output file if it exists
rm -f GACHACON_log/candump-2025-04-03_142614.log

# Process each line of the input file and fix the format
while IFS= read -r line; do
  # Check if the line starts with a timestamp without parentheses
  if [[ $line =~ ^([0-9]+\.[0-9]+)\) ]]; then
    # Extract the timestamp and the rest of the line
    timestamp="${BASH_REMATCH[1]}"
    rest_of_line="${line#*) }"
    # Write the fixed line with proper parentheses
    echo "($timestamp) $rest_of_line" >> GACHACON_log/candump-2025-04-03_142614.log
  else
    # Line already has correct format, just copy it
    echo "$line" >> GACHACON_log/candump-2025-04-03_142614.log
  fi
done < <(./convert_canlog.py GACHACON_log/test_canlog_250403-1-1.log /dev/stdout)

echo "Conversion complete. Output saved to GACHACON_log/candump-2025-04-03_142614.log"
