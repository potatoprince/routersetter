import glob, os, fileinput, sys

os.chdir("/home/martin/Documents/Info/TestExport/Templates")

bridges_2_ethernets = ("/interface bridge\nadd name=e1e2\n""/interface bridge port\nadd bridge=e1e2\
interface=ether1\nadd bridge=e1e2 interface=ether2")

bridges_4_ethernets = ("/interface bridge\nadd name=e1e2\nadd name=e3e4\n/interface bridge port\nadd bridge=e1e2\
interface=ether1\nadd bridge=e1e2 interface=ether2\nadd bridge=e3e4 interface=ether3\nadd bridge=e3e4 interface=ether4")

bridges_6_ethernets = ("/interface bridge\nadd name=e1e2\nadd name=e3e4\nadd name=e5e6\n\
/interface bridge port\nadd bridge=e1e2 interface=ether1\nadd bridge=e1e2 interface=ether2\nadd \
bridge=e3e4 interface=ether3\nadd bridge=e3e4 interface=ether4\nadd bridge=e5e6 interface=ether5\
\nadd bridge=e5e6 interface=ether6")

bridges_8_ethernets = ("/interface bridge\nadd name=e1e2\nadd name=e3e4\nadd name=e5e6\nadd name=e7e8\n\
/interface bridge port\nadd bridge=e1e2 interface=ether1\nadd bridge=e1e2 interface=ether2\nadd\
bridge=e3e4 interface=ether3\nadd bridge=e3e4 interface=ether4\nadd bridge=e5e6 interface=ether5\
\nadd bridge=e5e6 interface=ether6\nadd bridge=e7e8 interface=ether7\nadd bridge=e7e8 interface=ether8\n")

alwaysWrite = ("/system clock\nset time-zone-name=Europe/Riga\n/system ntp client\n\
set enabled=yes primary-ntp=10.155.0.1\n/ip dns\nset servers=10.155.0.1\n\n\n")

bridges_RB3011 =("/interface bridge\nadd name=e1e2\nadd name=e3e4\nadd name=e6e7\nadd name=e8e10\n\n\
/interface bridge port\nadd bridge=e1e2 interface=ether1\nadd bridge=e1e2 interface=ether2\n\
add bridge=e3e4 interface=ether3\nadd bridge=e3e4 interface=ether4\nadd bridge=e6e7 interface=ether6\n\
add bridge=e6e7 interface=ether7\nadd bridge=e8e10 interface=ether8\nadd bridge=e8e10 interface=ether10\n\n\n")

n = 0 # Vlan counter
v = 1 # Number of board config cycles
ipaCount = 0 #ethertnet IP address count
sfpCount = 0 # sfp address count
routerNameORetherCount = raw_input("Use rb name or ethernet count? ( input rb or eth ): ")

f = open("fconfig","w")
f.write(alwaysWrite)

# Code for getting pre-made config
if routerNameORetherCount == "rb":
    routerboardName = raw_input('Routerboard name ')
    
    if routerboardName =="RB3011":
        f.write(bridges_RB3011)
        boardCount = input("How many boards to test: ")
        stendIP = raw_input("What is the stend IP: ")
        while (boardCount >= v and boardCount <=5):
            ipEnd = stendIP[len(stendIP)-2:len(stendIP)]
            f.write("#Board "+str(v)+"\n\n")
            sfpCount+=1
            ipaCount+=1
            f.write("/ip address\nadd address=172.2"+str(ipaCount)+"."+ipEnd+".21/26 interface=ether5\n")
            ipaCount+=1
            f.write("add address=172.2"+str(ipaCount)+"."+ipEnd+".21/26 interface=ether9\n")
            f.write("add address=172.2"+str(sfpCount)+"."+ipEnd+".121/26 interface=sfp1\n")
            f.write("/ip route\nadd gateway=172.2"+str(v)+"."+ipEnd+".2\n\n")
            n+=1
            f.write("/interface vlan\nadd interface=ether5 name=vlan"+str(n)+"0 vlan-id="+str(n)+"0\n\
add interface=ether5 name=vlan"+str(n)+"1 vlan-id="+str(n)+"1\n")
            f.write("/ip address\nadd address=192.168."+str(n)+"0.10/24 interface=vlan"+str(n)+"0\n\
add address=192.168."+str(n)+"1.10/24 interface=vlan"+str(n)+"1\n")
            n+=1
            f.write("/interface vlan\nadd interface=ether9 name=vlan"+str(n)+"0 vlan-id="+str(n)+"0\n\
add interface=ether9 name=vlan"+str(n)+"1 vlan-id="+str(n)+"1\n")
            f.write("/ip address\nadd address=192.168."+str(n)+"0.10/24 interface=vlan"+str(n)+"0\n\
add address=192.168."+str(n)+"1.10/24 interface=vlan"+str(n)+"1\n\n\n")
            v+=1



# Code for making "unique" config
elif routerNameORetherCount == "eth":
    etherCount = input("How many ethernet bridges?: ")
    while etherCount > 0:
        if etherCount == 2:
            f.write(bridges_2_ethernets) 
        elif etherCount == 4:
            f.write(bridges_4_ethernets)
        elif etherCount == 6:
            f.write(bridges_6_ethernets)
        elif etherCount == 8:
            f.write(bridges_8_ethernets)
        break

    # stendIP = raw_input("What is the stend IP: ")
    # ipEnd = stendIP[11:13]
    # i = 1

    # while(i <= etherCount):
    #     if i == 1:
    #         f.write("/ip address\n")

    #     f.write("add address=172.2"+str(i)+"."+ipEnd+".21 interface=ether"+str(i)+"\n")
    #     i+=1


            

        


f.close()

#file.write("bridge")

# with open(routerboardName, "r") as f:
#     searchlines = f.readlines()
# for i, line in enumerate(searchlines):
#     if "bridge" in line: 
#         for l in searchlines[i:i+5]: print l,
#         print
