import subprocess
import socket
from scapy.all import IP , UDP, send,ICMP
import ipattk
global interface
global interface1
global output
tar_ip = ipattk.ipattk
 


def udpC1():
    
    subprocess.call(["sudo","iptables -D INPUT","-s",tar_ip,"-j","DROP"], shell=True)
    subprocess.run(["sudo","iptables","-A","INPUT", "-p udp","-s", tar_ip, "-j", "DROP"], shell=True)
    subprocess.run(["sudo iptables-save"], shell=True)
    print(tar_ip)
    

def udpC2():
    
    #create a sock object
    o = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)    
    #host bind and time out
    o.bind(("127.0.0.1", 0))
    o.settimeout(1)
    
    while True:
        try:
            packet = o.recvfrom(65565)#receive message from socket
            packet = IP(packet[0])
            if packet.haslayer(UDP):
                print("UDP Scan Detected from: " + packet.src)
                send(IP(dst=packet.src, ttl=64)/ICMP(type=""))
        except socket.timeout:
            break
    subprocess.call(["sudo","iptables -D INPUT","-s",tar_ip,"-j","DROP"], shell=True)
    subprocess.run(["sudo","iptables","-A","INPUT", "-p udp","-s", tar_ip, "-j", "DROP"], shell=True)

def udpC3():
    # Block all incoming and outgoing UDP traffic
    subprocess.run(["sudo","iptables", "-A", "INPUT", "-p", "udp", "-j", "DROP"])
    subprocess.run(["sudo","iptables", "-A", "OUTPUT", "-p", "udp", "-j", "DROP"])

    # Save the iptables rules
    subprocess.run(["service", "iptables", "save"])

    # Sleep for 24 hours
    subprocess.run(["sleep", "86400"])

    # Flush the iptables rules to allow UDP traffic again
    subprocess.run(["service", "iptables", "save"])

    
def udpC4():
    # Get the name of the first network interface
    output = subprocess.run(['sudo','ip', 'link', 'show'], stdout=subprocess.PIPE)
    interface = output.stdout.split()[20].decode('utf-8').strip(':')
    interface1 = output.stdout.split()[1].decode('utf-8').strip(':')


    print(f"The network interface is: {interface} and {interface1}")

    # Disconnect the host from the internet and all networks
    subprocess.run(['sudo','ip', 'link', 'set', 'dev', interface, 'down'])

   
    
    