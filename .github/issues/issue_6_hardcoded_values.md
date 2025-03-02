# Remove Hardcoded Values in gachacon_driver.py

## Issue Description
The gachacon_driver.py script contains many hardcoded values that make the code less flexible and harder to maintain.

## Problems Identified
- Hardcoded file paths for JSON output (`/mnt/ramdisk/outputv1.json`, `/mnt/ramdisk/output.json`)
- Hardcoded CAN IDs with minimal documentation
- Hardcoded relay timing values (`Wait_seconds_Supply_Relay_Precharge = 7`)
- Hardcoded number of devices (`number_of_devices = 0x23`)
- Hardcoded CAN message data values with minimal explanation

## Proposed Improvements
- Move all hardcoded values to constants at the top of the file
- Create a configuration system for values that might change between deployments
- Add clear documentation for what each value represents
- Group related constants together
- Consider creating enums for values with specific meanings

## Technical Details
Example implementation:

```python
# CAN Interface Configuration
CAN_INTERFACE = "vcan0"  # Use "can0" for production

# Device Configuration
NUMBER_OF_DEVICES = 0x23  # 35 devices
NUMBER_OF_ELEMENTS = NUMBER_OF_DEVICES * 4

# File Paths
OUTPUT_JSON_PATH = "/mnt/ramdisk/output.json"
OUTPUT_V1_JSON_PATH = "/mnt/ramdisk/outputv1.json"

# Timing Parameters
SUPPLY_RELAY_PRECHARGE_WAIT_SECONDS = 7
MOTOR_RELAY_PRECHARGE_WAIT_SECONDS = 7

# CAN Message Data Values
CAN_VALUE_OFF = 0x00
CAN_VALUE_PRECHARGE = 0x80
CAN_VALUE_INTERMEDIATE = 0xC0
CAN_VALUE_MAIN_RELAY = 0x40

# CAN Message IDs (with documentation)
CAN_ID_MOTOR_BASE = 0x00001201  # Base ID for motor control messages
CAN_ID_RELAY_1 = 0x00001221     # 500A Relay 1
CAN_ID_RELAY_2 = 0x00001222     # 500A Relay 2
CAN_ID_PATROL_LIGHT = 0x0000120F  # Patrol light control
```

## Priority
Medium

## Impact
Removing hardcoded values will:
- Make the code more maintainable
- Reduce the risk of errors when changing values
- Improve code readability
- Make configuration changes easier without diving into the code
- Aid documentation and knowledge transfer
