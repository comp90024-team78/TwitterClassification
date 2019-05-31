#!/usr/bin/env bash
cat ~/.ssh/team.pem
. ./unimelb-comp90024-group-78-openrc.sh; ansible-playbook -i ./inventory/inventory.ini -u ubuntu --key-file=~/.ssh/team.pem system-setting.yaml