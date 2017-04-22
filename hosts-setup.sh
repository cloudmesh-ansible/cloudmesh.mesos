#!/bin/sh
if grep -Fxq "[mesos]" inventory1.txt
then
   echo [mesos]|cat > inventory1.txt
else
   echo [mesos]|cat > inventory1.txt
fi
cm cluster nodes cluster-001|awk '{print $2 }'> ip_list
sed -i 's/$/ ansible_ssh_user=cc/' ip_list
sed -i '/\[mesos\]/ r ip_list' inventory1.txt



if grep -Fxq "[mesos-master]" inventory.txt 
then
   rm inventory.txt
   echo [mesos-master]|cat > inventory.txt
else
   echo [mesos-master]|cat > inventory.txt
fi

head -n2 -q ip_list >> inventory.txt
rm ip_list
