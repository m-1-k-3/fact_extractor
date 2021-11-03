#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

echo "------------------------------------"
echo "           install kpartx           "
echo "------------------------------------"

sudo apt-get install -y kpartx f2fs-tools

exit 0
