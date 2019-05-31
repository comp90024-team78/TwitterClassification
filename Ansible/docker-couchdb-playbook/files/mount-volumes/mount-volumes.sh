#!/usr/bin/env bash
mkdir -p common
cd common
mkdir -p data
sudo mkfs.ext4 -y /dev/vdb
sudo mount -t auto /dev/vdb ./data/
echo /dev/vdb /home/ubuntu/common/data auto defaults 0 0 | sudo tee -a /etc/fstab