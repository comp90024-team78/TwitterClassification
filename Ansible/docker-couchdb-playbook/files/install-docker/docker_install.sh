#!/bin/bash

echo "*************1. Remove old version**************"
sudo apt-get -y remove docker docker-engine docker.io docker-ce docker-ce-cli containerd.io runc
sudo rm -rf /var/lib/docker

echo "**************2. Install dependencies***************"
sudo apt-get -y update
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

echo "***************3. Install Docker**************"
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

