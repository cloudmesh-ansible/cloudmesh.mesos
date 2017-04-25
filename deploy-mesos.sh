#!/bin/sh
#ANSIBLE_HOST_KEY_CHECKING=False
sh create-cluster.sh
ansible-playbook create-inventory.yml
ansible-playbook mesos-playbook.yml -i inventory
