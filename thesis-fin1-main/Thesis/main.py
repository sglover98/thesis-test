import pandas as pd
import numpy as np
import csv
import subprocess
from scapy.all import  *
import conTCP
import conUDP
import conICMP
import time
import evidenceCollection

starttime = time.time()

print("Thesis Project-Stanley Glover")


### Comment out StartScript() if snort is already installed and configured to your linux system

def StartScript():
    
    subprocess.run(['sudo sh root.sh'], shell=True)
    print("manipulating sudo permissions")
    
    subprocess.run(['sudo sh snortsetup.sh'], shell=True)
    print("installing snort and configuring rules")
    
    subprocess.run(['sudo sh start.sh'], shell=True)
    print("starting snort")
    
    subprocess.run(['sudo sh snort2pcap.sh'], shell=True)
    print("converting snort to pcap")
StartScript()


loops = 10000
delay = 1

#loop file 100000 times
for i in range(loops):
    #parse snort log csv
    def csvparse():
        with open('alert.csv', 'r') as f:
            s_csv = csv.reader(f , delimiter=',', quotechar='"')
            s_csvarray = []#27 items in each row
            
            for row in s_csv:
                s_csvarray.append(row) #append each row to the array
                
        lastrow= s_csvarray[-1] #access last row
        global protocol
        global priority
        global ipattk
        protocol = lastrow[5]#access protocol in csv row
        ipattk = lastrow[6] #access ip address in csv row
        priority = lastrow[13] #access priority in csv row
        print(protocol)
        return protocol, priority
        
    csvparse()



    #check protocol and set proto 
    def checkprotocol(): 
        global proto
        if protocol == 'UDP':
            proto = 'UDP'
            print("True") 
        elif protocol == 'TCP':
            proto = 'TCP'
            print("True") 
        elif protocol == 'ICMP':
            proto = 'ICMP'
            print("True") 
        else: 
            print("unknown protocol")
            proto = 'unknown' 
    checkprotocol()

    ## check priority and set priorityint
    def checkpriority():
        global priorityint 
        if priority == 'Priority: 0':
            print("No action needed") ## add priority
            priorityint = 0
        elif priority == 'Priority: 1':
            print("Priority: 1") ## check priority function
            priorityint = 1
        elif priority == 'Priority: 2':
            print("Priority: 2") ## check priority 
            priorityint = 2
        elif priority == 'Priority: 3':
            print("Priority: 3") ## check priority 
            priorityint = 3
        elif priority == 'Priority: 4':
            print("Priority:4") ## check priority 
            priorityint = 4
        else: 
            print("unknown priority") ## add unknown priority 
            priorityint = "unknown"
        
        return priorityint
    checkpriority()

    #org alert data
    def orgdata():
        global containmentset
        containmentset = [proto,priorityint]
        print(containmentset)
        return containmentset
    orgdata()

    time.sleep(5)
    print("starting containment")


    def udpfunction():
        if containmentset == ['UDP',0]:
            print("No action needed")
        elif containmentset == ['UDP',1]:
            conUDP.udpC1()
            print("containment set 1")
        elif containmentset == ['UDP',2]:
            conUDP.udpC2()
            print("containment set 2")
        elif containmentset == ['UDP',3]:
            conUDP.udpC3()
            print("containment script 3")
        elif containmentset == ['UDP',4]:
            conUDP.udpC4()
            print("containment script 4")
        else:
            print("safe mode")
        




    def tcpfunction():
        if containmentset == ['TCP',0]:
            print("No action needed(TCP)")
        elif containmentset == ['TCP',1]:
            conTCP.tcpC2() ## TCP containment script 1 function
            print("TCP containment set 1")
        elif containmentset == ['TCP',2]:
            conTCP.tcpC2() ## TCP containment script 2 function
            print("TCP containment set 2")
        elif containmentset == ['TCP',3]:
            conTCP.tcpC3() ## TCP containment script 3 function 
            print("TCP containment script 3 has been run")  
            
        elif containmentset == ['TCP',4]:
            conTCP.tcpC4() ## TCP containment script 4 function
            print("TCP containment script 4")
            print("Complete Isolation of this machine has occured")
        

    def icmpfunction():
        if containmentset == ['ICMP',0]:
            print("No action needed(TCP)")
            
        elif containmentset == ['ICMP',1]:
            conICMP.icmpC1() ## TCP containment script 1 function
            print("ICMP containment set 1")
            print("The number of Pings has be limited for IP: " + ipattk)
        elif containmentset == ['ICMP',2]:
            conICMP.icmpC2() ## TCP containment script 2 function
            print("ICMP containment set 2")
            print(ipattk + " has been removed from the network continue to monitor for further attacks")
        elif containmentset == ['ICMP',3]:
            conICMP.icmpC3() ## TCP containment script 3 function 
            print("ICMP containment script 3 has been run")
            print("Your machine has been removed from the network and ip has been changed, you will need to restart your machine to regain access to the network")  
            
        elif containmentset == ['ICMP',4]:
            conICMP.icmpC4() ## TCP containment script 4 function
            print("iCMP containment script 4")
            print("You have been isolated from the network and your machine has been shut down")
        



    def action():#pick and run containment options based on containment set
        
        if proto == 'UDP':
            udpfunction()
        elif proto == 'TCP':
            tcpfunction()
        elif proto == 'ICMP':
            icmpfunction()
        elif proto == 'ftp':
            print("FTP")
        else:
            subprocess.run(['sudo lock'], shell=True)
            print("safe mode") 
    action()

    evidenceCollection.evidence()
print("Time --- %s seconds ---" % (time.time() - starttime))
time.sleep(delay)

