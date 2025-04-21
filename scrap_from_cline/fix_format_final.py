#!/usr/bin/env python3

import re

# Input and output files
input_file = "GACHACON_log/test_canlog_250403-1-1.log"
output_file = "GACHACON_log/candump-2025-04-03_142614.log"

# Read the input file
with open(input_file, 'r') as f:
    content = f.readlines()

# Open output file for writing
with open(output_file, 'w') as outfile:
    for line in content:
        line = line.strip()
        
        # Extract timestamp with or without parentheses
        if line.startswith('('):
            # Format: (timestamp) vcan0 ID [len] data
            match = re.match(r'\((\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)', line)
            if match:
                timestamp, can_id, _, data = match.groups()
                data_no_spaces = ''.join(data.split())
                outfile.write(f"({timestamp}) vcan0 {can_id}#{data_no_spaces}\n")
            else:
                print(f"Warning: Could not parse line with parentheses: {line}")
                outfile.write(line + '\n')
        else:
            # Format: timestamp) vcan0 ID [len] data
            match = re.match(r'(\d+\.\d+)\)\s+vcan0\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)', line)
            if match:
                timestamp, can_id, _, data = match.groups()
                data_no_spaces = ''.join(data.split())
                outfile.write(f"({timestamp}) vcan0 {can_id}#{data_no_spaces}\n")
            else:
                print(f"Warning: Could not parse line without parentheses: {line}")
                outfile.write(line + '\n')

print(f"Conversion completed successfully. Output saved to {output_file}")
