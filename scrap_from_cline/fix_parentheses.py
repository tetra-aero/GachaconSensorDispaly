#!/usr/bin/env python3

# This is a simple script to fix the parentheses in the CAN log file
# Specifically targeting the first two lines of the file

with open("GACHACON_log/candump-2025-04-03_142614.log", "r") as f:
    lines = f.readlines()

# Fix the first two lines by adding parentheses around the timestamp
for i in range(min(2, len(lines))):
    line = lines[i]
    if not line.startswith("("):
        # Find the position of the closing parenthesis
        paren_pos = line.find(")")
        if paren_pos > 0:
            # Extract timestamp
            timestamp = line[:paren_pos]
            # Extract rest of line
            rest = line[paren_pos+1:]
            # Reconstruct with proper parentheses
            lines[i] = f"({timestamp}){rest}"

# Write all lines back to the file
with open("GACHACON_log/candump-2025-04-03_142614.log", "w") as f:
    f.writelines(lines)

print("File updated with proper parentheses formatting.")
