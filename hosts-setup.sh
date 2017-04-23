#!/bin/sh
cm cluster nodes cluster-001|awk '{print $2 }'> ip_list
sed -i 's/$/ ansible_ssh_user=cc/' ip_list
sed -i 's/$/ ansible_ssh_private_key="\/home\/ronak\/.ssh\/rsa_id.pem"/' ip_list
echo [mesos-master]|cat > inventory
head -n2 -q ip_list | tail -n1 >> inventory 
echo [mesos-agents]|cat >> inventory
head -n1 -q ip_list >> inventory 
tail -n1 -q ip_list >> inventory 
rm ip_list
