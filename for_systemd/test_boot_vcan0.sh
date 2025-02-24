#!/bin/sh

# setup vcan0
modprobe vcan
ip link add dev vcan0 type vcan
ip link set dev vcan0 down
ip link set dev vcan0 type can bitrate 500000
ifconfig vcan0 txqueuelen 1000
ip link set dev vcan0 up
