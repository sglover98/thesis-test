#!bin/bash
 
sudo apt install snort3 -y
sudo apt-get upgrade snort
ifconfig
IP=$(ifconfig | awk '/inet /{print $2}' | head -1 )
 
# configure snort.conf file
sudo echo "var RULE_PATH /etc/snort/rules" >> /etc/snort/snort.conf
 
sudo echo "var SO_RULE_PATH /etc/snort/so_rules" >> /etc/snort/snort.conf
 
sudo echo "var PREPROC_RULE_PATH /etc/snort/preproc_rules" >> /etc/snort/snort.conf
 
sudo echo "output log_tcpdump: tcpdump.log" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/attack-responses.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/backdoor.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/bad-traffic.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/icmp.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/ftp.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/scan.rules" >> /etc/snort/snort.conf
 
sudo echo "include $RULE_PATH/local.rules" >> /etc/snort/snort.conf
 
 
# configure local.rules file
sudo echo "alert tcp any any -> $IP 22 (msg: "NMAP TCP Scan";sid:10000005; rev:2 ;Priority: 3;)" >> /etc/snort/rules/local.rules
sudo echo "alert tcp any any -> $IP any (msg: "TCP ping sweep Scan";Priority: 1;dsize:0;)" >> /etc/snort/rules/local.rules
sudo echo "alert icmp any any -> $IP any (msg:"PING detected";Priority: 1;)" >> /etc/snort/rules/local.rules
sudo echo "alert ip any any -> $IP any (msg:"Trace route packet detected"; Priority: 2;)" >> /etc/snort/rules/local.rules
sudo echo "alert ip any any -> $IP any (msg:"Tear drop attack detected"; Priority: 3; content:"teardrop";)" >> /etc/snort/rules/local.rules
sudo echo "alert tcp $EXTERNAL_NET any -> $IP any (msg:"hping3 attack detected"; flow:to_server,established; content:"hping3"; nocase; pcre:"/hping3\s+[-c\s+300]\s+[-s\s+1515]\s+[-a\s+192\.168\.193]\s+192\.168\.193/i"; reference:url,www.example.com/hping3-attacks; classtype:attempted-dos; sid:1000001; rev:1;Priority 2;)" >> /etc/snort/rules/local.rules
sudo echo “alert icmp $EXTERNAL_NET any -> $IP any (msg:"PING OF DEATH"; itype:8; icode:0; classtype:attempted-dos; threshold: type limit, track by_src, count 30000, seconds 60; sid:10000001; rev:1; Priority 4;)“ >> /etc/snort/rules/local.rules
sudo echo “alert icmp any any -> any any (msg: "ICMP Scan detected"; itype: 8; reference: arachnids,251; classtype:attempted-recon; sid:10000001; rev:001;Priority 4;)” >> /etc/snort/rules/local.rules
Sudo echo "alert udp any any -> 192.168.193.0/24 any (msg: "Netcat Scan detected"; content: "|00 00 00 00 00 00 00 00 00 00|"; reference: arachnids,251; classtype:attempted-recon; sid:10000002; rev:001; Priority 1;)” >> /etc/snort/rules/local.rules
sudo echo “alert icmp any any -> $IP any (msg: "ICMP Scan detected"; itype: 8; reference: arachnids,251; classtype:attempted-recon; sid:10000001; rev:001;Priority 4;)” >> /etc/snort/rules/local.rules
sudo echo "alert udp any any -> $IP any (msg: "UDP hping detected"; content: "hping"; metadata: service udp;Priority 3;)" >> /etc/snort/rules/local.rules
sudo echo "alert udp any any -> $IP any (msg: "UDP Scan detected"; content: "|00 00 00 00 00 00 00 00 00 00|"; reference: arachnids,251; classtype:attempted-recon; sid:10000003; rev:001;Priority 2)" >>  /etc/snort/rules/local.rules
sudo echo "alert udp any any -> $IP any (msg:"Large UDP Payload"; dsize:>1024; classtype:attempted-recon; Priority: 4;)" >> /etc/snort/rules/local.rules

#start snort
#Network interface name is enp0s5, may not be the same for you
snort -T -i enp0s5 -c etc/snort/snort.conf


