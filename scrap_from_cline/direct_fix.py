#!/usr/bin/env python3

# This script directly converts the format of CAN log files
# It converts:
# - From: (timestamp) vcan0 ID [length] data bytes with spaces
# - To:   (timestamp) vcan0 ID#data bytes without spaces
# - Ensures all timestamps are wrapped in parentheses

# Define input and output files
src_file = "GACHACON_log/test_canlog_250403-1-1.log"
dst_file = "GACHACON_log/candump-2025-04-03_142614.log"

# Open files for reading and writing
with open(src_file, 'r') as infile, open(dst_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        
        # Extract parts using string manipulation instead of regex
        # This is more robust for this specific format
        
        # First, determine if the timestamp has parentheses
        if line.startswith("("):
            # Extract timestamp with parentheses
            close_paren = line.find(")")
            if close_paren > 0:
                timestamp = line[1:close_paren]
                rest = line[close_paren+1:].strip()
            else:
                # Malformed line, skip
                continue
        else:
            # Extract timestamp without parentheses
            close_paren = line.find(")")
            if close_paren > 0:
                timestamp = line[:close_paren]
                rest = line[close_paren+1:].strip()
            else:
                # Malformed line, skip
                continue
        
        # Extract CAN ID and data
        parts = rest.split()
        if len(parts) >= 3 and parts[0] == "vcan0" and "[" in parts[2]:
            can_id = parts[1]
            
            # Find data bytes (everything after the [x] marker)
            data_start = rest.find("]") + 1
            if data_start > 0:
                data = rest[data_start:].strip()
                # Remove spaces from data
                data_no_spaces = data.replace(" ", "")
                
                # Format the output line
                new_line = f"({timestamp}) vcan0 {can_id}#{data_no_spaces}"
                outfile.write(new_line + "\n")
            else:
                # Couldn't find data section
                outfile.write(line + "\n")
        else:
            # Line doesn't match expected format
            outfile.write(line + "\n")

print(f"Conversion complete. Output written to {dst_file}")
