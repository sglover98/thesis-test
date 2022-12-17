import subprocess
import socket
import random
import time
import ipattk


#limit the number of pings on a host
def icmpC1():
    
    limit_ping= 10
    local_host = socket.gethostname() 
    local_ip = socket.gethostbyname(local_host)
    
    subprocess.run(["sudo","iptables", "-A", "INPUT", "-p", "icmp", "--icmp-type", "echo-request", "-d", local_ip, "-m", "limit", "--limit", str(limit_ping) + "/minute", "-j", "ACCEPT"])
    
    subprocess.run(["sudo","iptables", "-A", "INPUT", "-p", "icmp", "--icmp-type", "echo-request", "-d", local_ip, "-j", "DROP"])
    
    subprocess.run(["sudo","iptables-save"])
    return (local_ip)


def icmpC2():
    ban_IP = ipattk.ipattk
    
    #places ip on ban list using ip and saves the list
    subprocess.run(["sudo","iptables", "-A", "INPUT", "-s", ban_IP, "-j", "DROP"])
    subprocess.run(["sudo","iptables-save"],shell=True)
    
    #creat s object to generate ICMP response
    o = socket.socket(socket.AF_INET,socket.IPPROTO_ICMP)
    
    #send ban message to attacker
    msg = "Activity from your IP has resuleted in a ban."
    
    msg_bytes = bytes(msg, "utf-8")
    
    try:
        o.connect((ban_IP, 0))
    
        o.sendto(msg_bytes, (ban_IP, 0))
    
        time.sleep(1)
    
        o.close()
    except:
        pass



#disconnect all network interfaces and change the ip address of the system
def icmpC3():
    
    ran_num = random.randint(0, 255)
    local_host = socket.gethostname()
    local_ip = socket.gethostbyname(local_host)
    n_ip = "192.16.1." + str(ran_num)
    act_net = subprocess.run(["ip","link"], stdout=subprocess.PIPE).stdout.decode()
    ints= []
    
    "run the namp scan to find the used ip on the network"
    nmap_scan = subprocess.run(["nmap", "-sP",local_ip + "/24"], capture_output=True)
    
    #find the used ip on the network
    nmap_output = str(nmap_scan.stdout)
    taken_ips = []
    for line in nmap_output.split("\n"):
        if "Nmap scan report" in line:
            taken_ips.append(line.split(" ")[-1])
    
    #if new ip is in use, generate a new one
    if n_ip in taken_ips:
        ran_num = random.randint(0, 255)
        n_ip = "192.16.1." + str(ran_num)

    #analyze the output to get the names of the network interfaces
    for line in act_net.splitlines():
        #find the colon and space use as reference to split the line
            if ": " in line:
                #split line 
                int = line.split(": ")[1] 
                # place the interface name in the array
                ints.append(int)

    #manipulates the each avalible interface changing the ip address and shutting it down.
    #Also updates the interfaces with new ip address
    for i in ints:
       subprocess.run(["sudo","ip", "link", "set", "dev", i, "down"])
       subprocess.run(['sudo',"ip", "addr", "add", n_ip, "dev", i])



#Locking down the system from network and also lock 
def icmpC4():
   
    #shut all services 
    #subprocess.run(["systemctl stop --all"])

    active_net = subprocess.run(["ip","link"], stdout=subprocess.PIPE).stdout.decode()

    #analyze the output to get the names of the network interfaces
    networks = []
    for line in active_net.splitlines():
        #find the colon and space use as reference to split the line
        if ": " in line:
            #split line 
            network = line.split(": ")[1] 
            # place the interface name in the array
    networks.append(network)

    #execute subprocess shutdown for all found interfaces
    for i in networks:
        subprocess.run(["sudo","ip", "link", "set", "dev", i, "down"])
        subprocess.run(["sudo","iptables-save"])
    
    time.sleep(30)
    
    #lock system
    subprocess.run(["lock"], shell=True)




        