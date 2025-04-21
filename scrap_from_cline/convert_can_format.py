#!/usr/bin/env python3
import re
import sys

input_file = "GACHACON_log/test_canlog_250403-1-1.log"
output_file = "GACHACON_log/candump-2025-04-03_142614.log"

# Use direct approach to ensure all lines are formatted correctly

# Process the output file in a two-stage approach
# First stage: Convert the original format to the new format
with open(input_file, 'r') as infile:
    lines = []
    for line in infile:
        line = line.strip()
        # Match both formats: with or without parentheses
        match_with_paren = re.match(r'\((\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)', line)
        match_without_paren = re.match(r'(\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)', line)
        
        if match_with_paren:
            timestamp, can_id, _, data = match_with_paren.groups()
            data_without_spaces = ''.join(data.split())
            new_line = f"({timestamp}) vcan0 {can_id}#{data_without_spaces}"
            lines.append(new_line)
        elif match_without_paren:
            timestamp, can_id, _, data = match_without_paren.groups()
            data_without_spaces = ''.join(data.split())
            new_line = f"({timestamp}) vcan0 {can_id}#{data_without_spaces}"
            lines.append(new_line)
        else:
            print(f"Warning: Could not parse line: {line}")
            lines.append(line)

# Write the processed lines to the output file
with open(output_file, 'w') as outfile:
    for line in lines:
        outfile.write(line + '\n')

print(f"Conversion complete. Output saved to {output_file}")
