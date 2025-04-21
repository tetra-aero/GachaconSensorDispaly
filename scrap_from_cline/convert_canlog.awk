#!/usr/bin/awk -f

# AWK script to convert CAN log format
# From: (timestamp)  vcan0  ID   [length]  bytes
# To:   (timestamp) vcan0 ID#bytes

{
    # Trim leading whitespace
    gsub(/^[ \t]+/, "");
    
    # Extract timestamp
    timestamp_regex = "\\([0-9]+\\.[0-9]+\\)";
    if (match($0, timestamp_regex)) {
        timestamp = substr($0, RSTART, RLENGTH);
    } else {
        # If missing parentheses, use a fallback
        timestamp = "(" $1 ")";
    }
    
    # Extract interface (vcan0)
    interface = $2;
    
    # Extract ID
    id = $3;
    
    # Find the position of [n] to locate the data bytes
    data_start_pos = match($0, "\\[[0-9]+\\][ \t]+");
    if (data_start_pos > 0) {
        # Extract all bytes after [n]
        data_start_pos += RLENGTH;
        data_part = substr($0, data_start_pos);
        
        # Remove all whitespace from the data
        gsub(/[ \t\r\n]+/, "", data_part);
    } else {
        # Fallback if we can't find data
        data_part = "0000";
    }
    
    # Print in the desired format
    printf("%s %s %s#%s\n", timestamp, interface, id, data_part);
}
