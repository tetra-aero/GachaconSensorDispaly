#!/usr/bin/env python3
"""
CAN Log Format Converter

This script converts CAN logs from the format:
 (1743657974.805083)  vcan0  00003001   [2]  00 00

to:
(1743657974.805083) vcan0 00003001#0000
"""

import re
import sys
import os

def convert_line(line):
    """
    Convert a single line from the original format to the new format.
    """
    # Skip empty lines or lines that don't match the expected format
    if not line.strip():
        return ""
    
    # Regular expression to match the CAN log format
    pattern = r'\s*\((\d+\.\d+)\)\s+(\w+)\s+([0-9A-F]+)\s+\[(\d+)\]\s+((?:[0-9A-F]{2}\s*)+)'
    
    match = re.match(pattern, line)
    if not match:
        return ""  # Skip lines that don't match the format
    
    # Extract components
    timestamp = match.group(1)
    interface = match.group(2)
    can_id = match.group(3)
    byte_count = int(match.group(4))
    
    # Get hex data without spaces
    hex_data = match.group(5).strip().replace(' ', '')
    
    # Construct the new format
    new_line = f"({timestamp}) {interface} {can_id}#{hex_data}"
    
    return new_line

def convert_file(input_file, output_file):
    """
    Convert the entire input file to the new format and write to output file.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                converted_line = convert_line(line)
                if converted_line:  # Only write non-empty lines
                    outfile.write(converted_line + '\n')
        print(f"Conversion complete. Output saved to {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python can_format_converter.py <input_file> [output_file]")
        print("If output_file is not specified, input_file.converted will be used")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Create default output filename
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}.converted{ext}"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
        
    convert_file(input_file, output_file)

if __name__ == "__main__":
    main()
