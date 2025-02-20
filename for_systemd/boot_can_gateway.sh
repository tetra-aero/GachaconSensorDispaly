#!/bin/sh

# setup can0, can1, can2
ip link set dev can0 down
ip link set dev can1 down
ip link set dev can2 down

ip link set dev can0 type can bitrate 500000
ip link set dev can1 type can bitrate 500000
ip link set dev can2 type can bitrate 500000

ifconfig can0 txqueuelen 1000
ifconfig can1 txqueuelen 1000
ifconfig can2 txqueuelen 1000

ip link set dev can0 up
ip link set dev can1 up
ip link set dev can2 up

# setup vcan0
modprobe vcan
ip link add dev vcan0 type vcan
ip link set dev vcan0 down
ip link set dev vcan0 type can bitrate 500000
ifconfig vcan0 txqueuelen 1000
ip link set dev vcan0 up

# setup can gateway, vcan0 -> can0/can1/can2, can0/can1/can2 -> vcan0
modprobe can-gw
cangw -A -s can0 -d vcan0 -e
cangw -A -s can1 -d vcan0 -e
cangw -A -s can2 -d vcan0 -e

cangw -A -s vcan0 -d can0 -e
cangw -A -s vcan0 -d can1 -e
cangw -A -s vcan0 -d can2 -e

