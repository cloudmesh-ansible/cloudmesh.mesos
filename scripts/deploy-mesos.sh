#!/bin/sh
~/github/cloudmesh.mesos/scripts/create-cluster.sh
ansible-playbook create-inventory.yml
time ansible-playbook mesos-playbook.yml -i inventory.txt
