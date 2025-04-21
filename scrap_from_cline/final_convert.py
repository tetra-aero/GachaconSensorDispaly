#!/usr/bin/env python3

# Input and output files
input_file = "GACHACON_log/test_canlog_250403-1-1.log"
output_file = "GACHACON_log/candump-2025-04-03_142614.log"

def convert_file():
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    with open(output_file, 'w') as outfile:
        for line in lines:
            line = line.strip()
            
            # Handle both formats - with or without parentheses
            if line.startswith('('):
                # Format with parentheses
                parts = line.split(')')
                if len(parts) > 1:
                    timestamp = parts[0][1:]  # Remove opening parenthesis
                    rest = ')'.join(parts[1:]).strip()
                    
                    # Extract the CAN ID and data
                    segments = rest.split()
                    if len(segments) >= 4 and segments[0] == "vcan0" and "[" in segments[2]:
                        can_id = segments[1]
                        
                        # Find data section
                        data_start_idx = rest.find(']') + 1
                        if data_start_idx > 0:
                            data = rest[data_start_idx:].strip()
                            # Remove spaces from data
                            data_no_spaces = data.replace(" ", "")
                            
                            # Write the properly formatted line
                            outfile.write(f"({timestamp}) vcan0 {can_id}#{data_no_spaces}\n")
                            continue
            else:
                # Format without parentheses
                parts = line.split(')')
                if len(parts) > 1:
                    timestamp = parts[0]  # Timestamp without parentheses
                    rest = ')'.join(parts[1:]).strip()
                    
                    # Extract the CAN ID and data
                    segments = rest.split()
                    if len(segments) >= 4 and segments[0] == "vcan0" and "[" in segments[2]:
                        can_id = segments[1]
                        
                        # Find data section
                        data_start_idx = rest.find(']') + 1
                        if data_start_idx > 0:
                            data = rest[data_start_idx:].strip()
                            # Remove spaces from data
                            data_no_spaces = data.replace(" ", "")
                            
                            # Write the properly formatted line WITH parentheses
                            outfile.write(f"({timestamp}) vcan0 {can_id}#{data_no_spaces}\n")
                            continue
            
            # If we reached here, the line didn't match our expected format or processing failed
            # Just write the original line
            outfile.write(f"{line}\n")

# Run the conversion
convert_file()
print(f"Conversion completed successfully. Output saved to {output_file}")
