#!/bin/sh

# RUN+=boot_can_gateway.sh $kernel, $kernel -> can0 or can1 or can2
IFNAME=$1

# setup can0, can1, can2
ip link set dev $IFNAME down

ip link set dev $IFNAME type can bitrate 500000

ip ifconfig $IFNAME txqueuelen 1000

ip link set dev $IFNAME up

