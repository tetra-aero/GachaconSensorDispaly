# Optimize Performance in gachacon_driver.py

## Issue Description
The gachacon_driver.py script contains several performance inefficiencies that could impact system responsiveness and resource usage.

## Problems Identified
- `time.sleep()` calls inside state transitions could cause timing issues
- Inefficient string manipulations for parsing CAN data
- Recreating the same CAN messages in each state transition rather than reusing message objects
- Unnecessary object creation and data conversion in the main loop
- Inefficient JSON serialization occurring every second

## Proposed Improvements
- Create reusable CAN message objects instead of recreating them each time
- Optimize data parsing operations to reduce string manipulations
- Review and optimize the timing-sensitive sections
- Consider using more efficient data structures for state tracking
- Implement more efficient JSON serialization

## Technical Details
Several optimization opportunities exist:

1. **Reusable CAN Messages**:
```python
# Pre-create message objects (outside the loop)
relay_messages = {
    0x00001221: {
        "off": can.Message(arbitration_id=0x00001221, data=[0x00], is_extended_id=True),
        "precharge": can.Message(arbitration_id=0x00001221, data=[0x80], is_extended_id=True),
        "intermediate": can.Message(arbitration_id=0x00001221, data=[0xC0], is_extended_id=True),
        "main": can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True)
    }
}

# Then use them in state handlers
def handle_standby_state():
    can_bus.send(relay_messages[0x00001221]["off"])
    # ...
```

2. **More Efficient Data Parsing**:
```python
# Directly parse bytes without string conversions
def parse_voltage(data_bytes):
    # Assuming data_bytes is actual bytes
    value = int.from_bytes(data_bytes[0:2], byteorder='little')
    return round(value / 10.0, 1)
```

3. **Optimized JSON Handling**:
Consider using incremental updates to JSON data rather than rebuilding the entire structure on each iteration.

## Priority
Medium

## Impact
Performance optimizations will:
- Improve system responsiveness
- Reduce CPU and memory usage
- Potentially reduce timing-related issues
- Make the code more maintainable
- Support larger scale deployments with better resource utilization
