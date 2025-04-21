#!/usr/bin/env python3
import re
import sys

if len(sys.argv) != 3:
    print("Usage: python3 convert_canlog.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Regular expressions to match both format types
pattern1 = r'\((\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)'  # With parentheses
pattern2 = r'(\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)'   # Without opening parenthesis

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        
        # Try to match with parentheses format first
        match1 = re.match(pattern1, line)
        if match1:
            timestamp, can_id, _, data = match1.groups()
            data_without_spaces = data.replace(" ", "")
            # Ensure consistent format with parentheses
            new_line = f"({timestamp}) vcan0 {can_id}#{data_without_spaces}\n"
            outfile.write(new_line)
            continue
            
        # Try to match without opening parenthesis
        match2 = re.match(pattern2, line)
        if match2:
            timestamp, can_id, _, data = match2.groups()
            data_without_spaces = data.replace(" ", "")
            # Ensure consistent format with parentheses
            new_line = f"({timestamp}) vcan0 {can_id}#{data_without_spaces}\n"
            outfile.write(new_line)
            continue
            
        # If no match, copy the line as is
        outfile.write(line + '\n')

# Now do a second pass to fix any remaining inconsistencies
with open(output_file, 'r') as infile:
    lines = infile.readlines()

with open(output_file, 'w') as outfile:
    for line in lines:
        line = line.strip()
        # Check if the line starts with a timestamp not in parentheses
        timestamp_pattern = r'^(\d+\.\d+)\) vcan0 ([0-9A-F]+)#(.+)$'
        match = re.match(timestamp_pattern, line)
        if match:
            timestamp, can_id, data = match.groups()
            # Rewrite with proper parentheses
            fixed_line = f"({timestamp}) vcan0 {can_id}#{data}\n"
            outfile.write(fixed_line)
        else:
            outfile.write(line + '\n')

print(f"Conversion complete. Output saved to {output_file}")
