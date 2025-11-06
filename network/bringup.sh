#!/bin/bash

sudo ip addr add $1/24 dev enp59s0np$2
sudo ip link set enp59s0np$2 up
sudo ip link set dev enp59s0np$2 mtu 9000
