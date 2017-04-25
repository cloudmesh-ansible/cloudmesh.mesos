#!/bin/sh
cm cluster avail > avail.txt
grep '>' avail.txt > avail1.txt
sed 's/^.\{2\}//g' avail1.txt

cat avail1.txt|cm cluster nodes|awk '{print $2 }'> ip_list	# get ips of all cluster nodes in ip_list 
rm ~/.ssh/known_hosts
touch ~/.ssh/known_hosts
while read line; do
    ssh-keyscan $line >> ~/.ssh/known_hosts			# add ips to known_hosts
done <ip_list
sed -i 's/$/ ansible_ssh_user=cc/' ip_list
#sed -i 's/$/ ansible_ssh_private_key="\/home\/ronak\/.ssh\/rsa_id.pem"/' ip_list
echo [mesos-master]|cat > inventory
head -n2 -q ip_list | tail -n1 >> inventory 
echo [mesos-agents]|cat >> inventory
head -n1 -q ip_list >> inventory 
tail -n1 -q ip_list >> inventory 
rm ip_list
rm avail.txt
rm avail1.txt

