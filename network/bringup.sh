#!/bin/bash

IP=${1:-192.168.50.10}
IF=${2:0}

sudo ip addr add $IP/24 dev enp59s0np$IF
sudo ip link set enp59s0np$IF up
sudo ip link set dev enp59s0np$IF mtu 9000
