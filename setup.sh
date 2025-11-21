#!/bin/bash
#

MCS="${1:-fpga.mcs}"
TARGET="${2:-pc159}"

echo $TARGET

rsync -avz private_key.pem "$MCS" ubuntu22.04.qcow2 $TARGET:~/.
