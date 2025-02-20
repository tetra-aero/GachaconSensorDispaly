#!/bin/sh

# setup can0, can1, can2
sudo ip link set dev can0 down
sudo ip link set dev can1 down
sudo ip link set dev can2 down

sudo ip link set dev can0 type can bitrate 500000
sudo ip link set dev can1 type can bitrate 500000
sudo ip link set dev can2 type can bitrate 500000

sudo ifconfig can0 txqueuelen 1000
sudo ifconfig can1 txqueuelen 1000
sudo ifconfig can2 txqueuelen 1000

sudo ip link set dev can0 up
sudo ip link set dev can1 up
sudo ip link set dev can2 up

# setup vcan0
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set dev vcan0 down
#sudo ip link set dev vcan0 type can bitrate 500000
sudo ifconfig vcan0 txqueuelen 1000
sudo ip link set dev vcan0 up

# setup can gateway, vcan0 -> can0/can1/can2, can0/can1/can2 -> vcan0
sudo cangw -A -s can0 -d vcan0 -e
sudo cangw -A -s can1 -d vcan0 -e
sudo cangw -A -s can2 -d vcan0 -e

sudo cangw -A -s vcan0 -d can0 -e
sudo cangw -A -s vcan0 -d can1 -e
sudo cangw -A -s vcan0 -d can2 -e

