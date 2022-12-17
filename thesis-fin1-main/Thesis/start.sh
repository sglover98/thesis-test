#!/bin/sh
 sudo sh root.sh
 sudo apt-get update

#set cronjob to run this script every 30 seconds
crontab -e

echo "*/30 * * * * /home/parallels/Desktop/Thesis/start.sh"

#navigate to the directory 
cd /home/parallels/Desktop/Thesis

#install IPtables
sudo apt-get install iptables
sudo apt-get install iptables-persistent

#install Nmap
sudo apt-get install nmap

#Manipulating permissions
sudo sh /home/parallels/Desktop/Thesis/root.sh
sudo chmod -R 777 /usr/bin/md5sum
sudo chmod -R 777 /usr/sbin/iptables
sudo chmod -R 777 /sbin/sysctl
sudo chmod -R 777 /media
sudo chmod u=rwx /var/log/snort/*
sudo chmod -R 777 /etc
sudo chmod u+x /etc/iptables
sudo chmod u+x /etc/iptables/rules.v4
sudo chmod -R 777 /bin/dd
sudo chmod -R 777 /dev/sda1
sudo chmod -R 777 /dev/sda2
sudo setcap cap_net_admin=ep /home/parallels/Desktop/Thesis/conICMP.py
sudo setcap cap_net_admin=ep /home/parallels/Desktop/Thesis/conTCP.py
sudo setcap cap_net_admin=ep /home/parallels/Desktop/Thesis/conUDP.py
sudo setcap cap_net_admin=ep /home/parallels/Desktop/Thesis/.py


#run python script
sudo python /home/parallels/Desktop/Thesis/main.py
#finish script
exit 0