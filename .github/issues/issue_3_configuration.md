# Add Configuration Management to gachacon_driver.py

## Issue Description
The gachacon_driver.py script currently uses hardcoded settings with no flexible configuration mechanism, making it difficult to deploy in different environments.

## Problems Identified
- Commented-out line for real CAN interface: `#can_bus = can.interface.Bus(channel="can0", interface='socketcan')`
- Currently using virtual CAN: `can_bus = can.interface.Bus(channel="vcan0", interface='socketcan')`
- No configuration mechanism to easily switch between production and development environments
- Hardcoded file paths for JSON output (`/mnt/ramdisk/outputv1.json`, `/mnt/ramdisk/output.json`)
- Hardcoded timing values for relay operations

## Proposed Improvements
- Create a configuration file or command-line argument parsing to control:
  - CAN interface selection (virtual vs. real)
  - Output file paths
  - Logging verbosity
  - Timing parameters for relay operations
- Implement a configuration loader that can adapt to different deployment environments
- Add environment-specific defaults (development, testing, production)

## Technical Details
A simple implementation could use Python's argparse module for command-line configuration along with a YAML or JSON config file for more complex settings:

```python
import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description='Gachacon CAN driver')
    parser.add_argument('--config', type=str, default='config.yaml', 
                      help='Path to configuration file')
    parser.add_argument('--can-interface', type=str, 
                      help='CAN interface to use (overrides config file)')
    return parser.parse_args()

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Usage
args = parse_args()
config = load_config(args.config)
can_interface = args.can_interface or config.get('can_interface', 'vcan0')
```

## Priority
Medium

## Impact
Adding proper configuration management will:
- Simplify deployment across different environments
- Reduce the need for code modifications when changing environments
- Make the system more flexible for different hardware setups
- Improve overall maintainability
