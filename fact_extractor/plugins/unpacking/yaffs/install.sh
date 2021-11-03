#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

echo "------------------------------------"
echo "          install unyaffs           "
echo "------------------------------------"

sudo apt-get install -y unyaffs || exit 1

exit 0
