import csv 

#####Do to unknow circular import area the IP address must be imported from a seperate file#########
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
    return protocol, priority
    
csvparse()


print(ipattk)
