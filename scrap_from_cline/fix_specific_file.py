#!/usr/bin/env python3

# This script converts the test_canlog_250403-1-1.log to candump-2025-04-03_142614.log
# ensuring the correct format with consistency in parentheses usage

import os

# Input and output files
input_file = "GACHACON_log/test_canlog_250403-1-1.log"
output_file = "GACHACON_log/candump-2025-04-03_142614.log"

# Function to convert a single line
def convert_line(line):
    line = line.strip()
    
    # Extract timestamp - handle both formats
    if line.startswith('('):
        # With parentheses already
        closing_paren = line.find(')')
        if closing_paren == -1:
            return line
        
        timestamp = line[1:closing_paren]
        rest = line[closing_paren+1:].strip()
    else:
        # Without parentheses
        closing_paren = line.find(')')
        if closing_paren == -1:
            return line
        
        timestamp = line[:closing_paren]
        rest = line[closing_paren+1:].strip()
    
    # Parse the rest of the line
    parts = rest.split()
    if len(parts) < 3 or parts[0] != "vcan0" or '[' not in parts[2]:
        return line
    
    can_id = parts[1]
    data_start = rest.find(']')
    if data_start == -1:
        return line
    
    data = rest[data_start+1:].strip()
    data_no_spaces = ''.join(data.split())
    
    # Create new line in target format
    return f"({timestamp}) vcan0 {can_id}#{data_no_spaces}"

# Process the file
with open(input_file, 'r') as infile:
    lines = [line.strip() for line in infile.readlines()]

converted_lines = [convert_line(line) for line in lines]

with open(output_file, 'w') as outfile:
    for line in converted_lines:
        outfile.write(line + '\n')

print(f"File converted successfully. Output saved to {output_file}")
