#!/bin/bash
#

TARGET="${1:-pc159}"

echo $TARGET

rsync -avz ~/projects/latest_working_OS4C $TARGET:~/.
rsync -avz private_key.pem corundum.mcs ubuntu22.04.qcow2 $TARGET:~/.
