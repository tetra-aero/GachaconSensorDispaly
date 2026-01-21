#!/bin/sh

# setup can0, can1, can2
ip link set dev canL down
ip link set dev canR down
ip link set dev canP down

ip link set dev canL type can bitrate 500000
ip link set dev canR type can bitrate 500000
ip link set dev canP type can bitrate 500000

ifconfig canL txqueuelen 1000
ifconfig canR txqueuelen 1000
ifconfig canP txqueuelen 1000

ip link set dev canL up
ip link set dev canR up
ip link set dev canP up

# setup vcan0
modprobe vcan
ip link add dev vcan0 type vcan
ip link set dev vcan0 down
ip link set dev vcan0 type can bitrate 500000
ifconfig vcan0 txqueuelen 1000
ip link set dev vcan0 up

# setup can gateway, vcan0 -> can0/can1/can2, can0/can1/can2 -> vcan0
modprobe can-gw
cangw -A -s canL -d vcan0 -e
cangw -A -s canR -d vcan0 -e
cangw -A -s canP -d vcan0 -e

cangw -A -s vcan0 -d canL -e
cangw -A -s vcan0 -d canR -e
cangw -A -s vcan0 -d canP -e

