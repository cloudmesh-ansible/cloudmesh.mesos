#!/bin/sh
ansible-playbook output-playbook.yml -i agent1.txt
ansible-playbook output-playbook.yml -i agent2.txt
