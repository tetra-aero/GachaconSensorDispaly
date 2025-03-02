# Implement Proper Error Handling in gachacon_driver.py

## Issue Description
The gachacon_driver.py script lacks robust error handling, which could lead to unexpected crashes or undefined behavior in error conditions.

## Problems Identified
- No error handling for CAN bus initialization failures
- No handling for CAN message reception errors
- No graceful shutdown mechanism or signal handling
- Limited exception handling in data processing sections
- No logging of errors for later diagnosis

## Proposed Improvements
- Add try/except blocks for CAN operations
- Implement graceful shutdown with signal handlers
- Add proper logging instead of print statements
- Handle potential exceptions in data parsing
- Implement recovery mechanisms for common failure modes
- Add detailed error messages to aid in troubleshooting

## Technical Details
Python's standard libraries provide tools that would greatly improve error handling:

```python
import logging
import signal
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('gachacon_driver')

# Signal handling for graceful shutdown
def signal_handler(sig, frame):
    logger.info("Shutdown signal received, cleaning up...")
    # Clean up code (close CAN bus, etc)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# CAN bus initialization with error handling
try:
    can_bus = can.interface.Bus(channel="vcan0", interface='socketcan')
    logger.info("CAN bus initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize CAN bus: {e}")
    sys.exit(1)

# Message reception with error handling
try:
    msg = can_bus.recv(2.0)
    # Process message
except Exception as e:
    logger.error(f"Error receiving CAN message: {e}")
    # Recovery or fallback behavior
```

## Priority
High

## Impact
Proper error handling will:
- Prevent unexpected crashes
- Provide meaningful error messages for debugging
- Allow for graceful recovery from common failure modes
- Improve overall system reliability
- Make diagnosis of issues much easier through proper logging
