#!/usr/bin/env python3

with open("GACHACON_log/candump-2025-04-03_142614.log", "r") as f:
    lines = f.readlines()

with open("GACHACON_log/candump-2025-04-03_142614.log", "w") as f:
    for line in lines:
        # Check if line starts with a timestamp without parentheses
        if line[0].isdigit() and not line.startswith("("):
            # Find the position of the closing parenthesis
            pos = line.find(")")
            if pos > 0:
                # Extract timestamp
                timestamp = line[:pos]
                # Extract rest of the line
                rest = line[pos+1:]
                # Write the fixed line
                f.write(f"({timestamp}){rest}")
        else:
            # Line is already formatted correctly or has a different format
            f.write(line)
