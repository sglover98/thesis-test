#!/bin/sh

cd /
#move to snort logs
cd /var/log/snort

#copy all files to pcap directory
cp -p *.log /var/log/snort/log-history/
cp -p *.alert /var/log/snort/log-history/
cp -p *.alert.fast /var/log/snort/log-history/
cp -p *.csv /var/log/snort/log-history/
cp -p *.csv /home/parallels/Desktop/Thesis/main.py

#if files exsist
if [ -f /var/log/snort/snort.log ]
then
    #delete all files
    rm -f snort.csv
    rm -f snort.pcap
    rm -f snort.alert.fast
fi 

#convert to pcap 
u2boat -t pcap snort.alert snort.pcap

#make pcap pub
chmod 777 snort.pcap

exit 0





