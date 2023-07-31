

from contextlib import contextmanager
from pyhesity import *
from time import sleep
import os
import json


firewall_profile = "iris_cli -username=admin firewall-profile ls-active"
    
firewallOutput = (os.popen(firewall_profile).read()).strip()

with open(firewall.json, 'w') as json_file:
    json.dump(firewallOutput, json_file)
    

for x in firewall.json:
    if os.stat(x).st_size > 5:
        f = open(x)
        data = json.load(f)
        
        for i in data:
            profileName = i['PROFILE NAME']
            ipset = i['IPSET ENTRIES']

            if(profileName == "Replication"):
                replicationIps = ipset
                print("Current Replication IPset Entries: ")
                print(replicationIps)
        
                    
    else:
        print("Isolated Cluster Replication Firewall did not populate proplery!")
        
