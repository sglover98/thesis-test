import subprocess
import glob 
import socket
from datetime import datetime, timedelta
from scapy.all import IP , TCP, sniff
import ipattk


### TCP Containment System ####

def tcpC1():
    
    subprocess.call(["sudo", "iptables","-A","INPUT", "-s",ipattk.ipattk, "-j", "DROP"])
    
    subprocess.call(["sudo","iptables","-A","INPUT", "-s",ipattk.ipattk, "-j", "DROP"])
    
    subprocess.call(["sudo","iptables-save"])



#Iterate through all ports and ip addresses. Then disconnects the connection.
#Checks for all established connections and removes them
    
def tcpC2():
    #sock object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #set timeout
    sock.settimeout(1)
    #Iterate through all ip addresses and ports
    for ip in range(1, 256):
        
        address = (f"192.168.1.{ip}", range)
        
        try:
            sock.connect(address)
            
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        except:
            pass 
    
    #check netstat and prep for output info
    netstatout = subprocess.check_output("netstat -an", shell=True)

    lines = str(netstatout.splitlines())
 
#iterate through  and shows  established connections
    for line in lines:
        if "CONNECTED" in line:
         print(line)
    
    
## Containment for Nmap scan
## net.ipv4.tcp_* may not work if not configured on your distro
def tcpC3():
       subprocess.call(["sudo sysctl -w net.ipv4tcp_syncookies=1"], shell=True)
       subprocess.call(["sudo sysctl -w net.ipv4.tcp_max_syn_backlog=50000"], shell=True)
       subprocess.call(["sudo sysctl -w net.ipv4.tcp_synack_retries=2"], shell=True)
       subprocess.call(["sudo sysctl -w net.ipv4.tcp_syn_retries=2"], shell=True)
       
       #ip blacklisting using packet callback
       def packet_callback(packet):
           
           if packet.haslayer(TCP) and packet.getlater(TCP) == 0x12:
               
               # capture the source IP address
               srcip = packet.getlayer(IP).src
               srcport = packet.getlayer(TCP).sport
               
               #Iptables manipulation 
               
               subprocess.call(["iptables -D", "-s",ipattk.ipattk, "-j DROP"], shell=True)
               
               subprocess.call(["sudo","iptables -A INPUT -s " + srcip + " -p tcp --destination-port " + srcport + " -j DROP"], shell=True)
               
               subprocess.call(["sudo","iptables -A OUTPUT -d " + srcip + " -p tcp --source-port " + srcport + " -j DROP"], shell=True)
               
               #Sniff and add callback function
               sniff(filter="tcp", prn=packet_callback)
               subprocess.call(["sudo iptables-save"], shell=True)
               
           return packet_callback(packet)
    
   
   
   
#Conatinment system lockdown complete system lockdown
#DO NOT USE UNLESS ABSOLUTELY NECESSARY MAY CAUSE SYSTEM FAILURE OR DAMAGE 

def tcpC4():

    def connectionLock():
        # remove old rule for specific IP firewall rules
        subprocess.call(["sudo","iptables -D", "-s",ipattk.ipattk, "-j DROP"], shell=True)

        # Block all incoming connections
        subprocess.call(["sudo","iptables -A INPUT -j DROP"], shell=True)

        # Block all outgoing connections
        subprocess.call(["sudo","iptables -A OUTPUT -j DROP"], shell=True)
        
    connectionLock()  
    
    def dirLock():
        base_dir= "/" #set base directory
        
        #get all directories from base directory
        dirs = glob.glob(base_dir + "**/", recursive=True)
        
        #loop through directories and set permissions
        for directory in dirs:
             subprocess.run(["sudo","chmod", "600", directory])
    dirLock()





