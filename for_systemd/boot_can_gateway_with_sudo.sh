#!/bin/sh

# setup can0, can1, can2
sudo ip link set dev canL down
sudo ip link set dev canR down
sudo ip link set dev canP down

sudo ip link set dev canL type can bitrate 500000
sudo ip link set dev canR type can bitrate 500000
sudo ip link set dev canP type can bitrate 500000

sudo ifconfig canL txqueuelen 1000
sudo ifconfig canR txqueuelen 1000
sudo ifconfig canP txqueuelen 1000

sudo ip link set dev canL up
sudo ip link set dev canR up
sudo ip link set dev canP up

# setup vcan0
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set dev vcan0 down
#sudo ip link set dev vcan0 type can bitrate 500000
sudo ifconfig vcan0 txqueuelen 1000
sudo ip link set dev vcan0 up

# setup can gateway, vcan0 -> can0/can1/can2, can0/can1/can2 -> vcan0
sudo cangw -A -s canL -d vcan0 -e
sudo cangw -A -s canR -d vcan0 -e
sudo cangw -A -s canP -d vcan0 -e

sudo cangw -A -s vcan0 -d canL -e
sudo cangw -A -s vcan0 -d canR -e
sudo cangw -A -s vcan0 -d canP -e

