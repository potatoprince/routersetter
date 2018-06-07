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

bridges_CCR1036_12G_4S =("/interface bridge\nadd name=e1e2\nadd name=e3e4\nadd name=e5e6\n\
add name=e7e8\nadd name=e9e10\nadd name=e11e12\nadd name=s1s2\nadd name=s3s4\n\n\
/interface bridge port\nadd bridge=e1e2 interface=ether1\nadd bridge=e1e2 interface=ether2\n\
add bridge=e3e4 interface=ether3\nadd bridge=e3e4 interface=ether4\nadd bridge=e5e6 interface=ether5\n\
add bridge=e5e6 interface=ether6\nadd bridge=e7e8 interface=ether7\nadd bridge=e7e8 interface=ether8\n\
add bridge=e9e10 interface=ether9\nadd bridge=e9e10 interface=ether10\nadd bridge=e11e12 interface=ether11\n\
add bridge=e11e12 interface=ether12\nadd bridge=s1s2 interface=sfp1\nadd bridge=s1s2 interface=sfp2\n\
add bridge=s3s4 interface=sfp3\nadd bridge=s3s4 interface=sfp3\nadd bridge=s3s4 interface=sfp4\n\n\n")

n = 0 # Vlan counter
v = 1 # Number of board config cycles
ipaCount = 0 #ethertnet IP address count
sfpCount = 0 # sfp address count
macCount = 0 # mac address count for traffic generator

routerNameORetherCount = raw_input("Use rb name or ethernet count? ( input rb or eth ): ")

f = open("fconfig","w")
f.write(alwaysWrite)

# Code for getting pre-made config
if routerNameORetherCount == "rb":
    infoPrompt = raw_input("Would you like to see the list of available router configurations and numbers?: ")
    if (infoPrompt =="yes" or "y"):
        print("There are router configurations for :\n\
        1) RB3011\n\
        2) CCR1036-12G-4S\n")
    routerboardName = raw_input('Input Routerboard number: ')

    
    if routerboardName == '1':
        f.write(bridges_RB3011)
        boardCount = input("How many boards to test: ")
        stendIP = raw_input("What is the stend IP: ")
        while (boardCount >= v and boardCount <=5):
            ipEnd = stendIP[len(stendIP)-2:len(stendIP)]
            f.write("                                 #Board "+str(v)+"\n\n")
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

    if routerboardName == '2':
        f.write(bridges_CCR1036_12G_4S)
        boardCount = input("how many boards to test: ")
        stendIP = raw_input("What is the stend IP: ")
        if len(stendIP) == 13:
            ipEnd = stendIP[len(stendIP)-2:len(stendIP)]
        elif len(stendIP) == 14:
            ipEnd = stendIP[len(stendIP)-3:len(stendIP)]   
        stendEtherStart = input("Which stend ether is connected to board 1 ether1?: ")
        stendEtherEnd = stendEtherStart
        stendSfpStart =input("Which stend sfp is connected to board 1 sfp1?: ")
        stendSfpEnd = stendSfpStart
        while(boardCount >=v and boardCount <= 2):
            f.write("#Board "+str(v)+"\n\n")
            f.write("/ip address\nadd address=172.2"+str(stendEtherEnd)+"."+ipEnd+".21/26 interface=ether1\n")
            stendEtherEnd+=1
            f.write("add address=172.2"+str(stendEtherEnd)+"."+ipEnd+".21/26 interface=ether12\n")
            stendEtherEnd+=1
            f.write("add address=172.2"+str(stendSfpEnd)+"."+ipEnd+".121/26 interface=sfp1\n")
            stendSfpEnd+=1
            f.write("add address=172.2"+str(stendSfpEnd)+"."+ipEnd+".121/26 interface=sfp4\n\n\n")
            stendSfpEnd+=1
            v+=1

        trafficGenerator = raw_input("Make traffic generator?: ")
        if(trafficGenerator == "yes"):
            while(stendEtherStart < stendEtherEnd ):
                f.write("/tool traffic-generator packet-template\nadd interface=ether"+str(stendEtherStart)+" \
ip-dst=172.2"+str(stendEtherStart+1)+"."+str(ipEnd)+".21 \
mac-dst="+raw_input("Put in the mac-dst for ether"+str(stendEtherStart))+" name=e"+str(stendEtherStart)+"e"+str(stendEtherStart+1)+" \
random-ranges=29:8:1-21,34:16:60000-60001,36:16:50000-50001\n")
                stendEtherStart+=1
                f.write("add interface=ether"+str(stendEtherStart)+" ip-dst 172.2"+str(stendEtherStart-1)+"."+str(ipEnd)+".21 \
mac-dst="+raw_input("put in the mac-dst for ether"+str(stendEtherStart))+" name=e"+str(stendEtherStart)+"e"+str(stendEtherStart-1)+" \
random-ranges=29:8:1-21,34:16:60000-60001,36:16:50000-50001\n")
                stendEtherStart+=1

            while(stendSfpStart < stendSfpEnd):
                f.write("add interface=sfp"+str(stendSfpStart)+" ip-dst=172.2"+str(stendSfpStart+1)+"."+str(ipEnd)+".102 \
mac-dst="+raw_input("put in the mac-dst for sfp"+str(stendSfpStart))+" name=sfp"+str(stendEtherStart)+"sfp"+str(stendSfpStart+1)+" \
random-ranges=29:8:1-21,34:16:60000-60001,36:16:50000-50001\n")
                stendSfpStart+=1
                f.write("add interface=sfp"+str(stendSfpStart)+" ip-dst=172.2"+str(stendSfpStart-1)+"."+str(ipEnd)+".102 \
mac-dst="+raw_input("put in the mac-dst for sfp"+str(stendSfpStart))+ "name=sfp"+str(stendSfpStart)+"sfp"+str(stendSfpStart-1)+" \
random-ranges=29:8:1-21,34:16:60000-60001,36:16:50000-50001\n\n\n")
                stendSfpStart+=1

                f.write("           #Higher CPU Load\n/lcd set backlight-timeout=never\n/ip firewall connection tracking set enabled=yes\n\
/interface bridge settings set use-ip-firewall=yes\n\n\n")
        f.write("           #Remove old logs and start new logging\n\
/file remove log.0.txt\n/file remove log.1.txt\n/tool graphing interface add store-on-disk=no;\n\
/tool graphing resource add store-on-disk=no;\n/system reboot\n\n\n")
        f.write("           #Set fresh logs\n/system logging set [find topics~\"error\"] action=disk\n\
/system logging set [find topics=\"warning\"] action=disk\n/system logging set [find topics=\"critical\"] action=disk\n\
/system logging action set memory memory-lines=1;\n:delay 1s;\n/system logging action set memory memory-lines=1000;\n\
/interface ethernet reset-counters [find];\n/log info message=\"------- LOGS AND ETHERNET COUNTERS CLEARED -------\"\n\
/log print\n\n\n")
        



# Code for making "unique" config #ToDo
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
