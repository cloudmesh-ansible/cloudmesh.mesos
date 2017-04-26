#!/bin/sh
#ANSIBLE_HOST_KEY_CHECKING=False
~/github/cloudmesh.mesos/scripts/create-cluster.sh
ansible-playbook create-inventory.yml
ansible-playbook mesos-playbook.yml -i inventory.txt
