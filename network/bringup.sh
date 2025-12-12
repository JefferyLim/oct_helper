#!/bin/bash

IP=${1:-192.168.50.10}
IF=${2:enp59s0np0}

sudo ip addr add $IP/24 dev $IF
sudo ip link set dev $IF mtu 9000
sudo ip link set $IF up
