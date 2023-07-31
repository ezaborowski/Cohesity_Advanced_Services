

from contextlib import contextmanager
from pyhesity import *
from time import sleep



### Gets the Protection Job ID from the corresponding Job Name
def get_fw_profile(firewall):
    firewall_profile = f"iris_cli -username=admin firewall-profile ls-active"
    profileName = firewall_profile[0]['PROFILE NAME']
    ipset = firewall_profile[0]['IPSET ENTRIES']
    #job = [j for j in job if j['name'].lower() == jobname.lower()]
    if len(firewall_profile) != 0:
        
        if(profileName == "Replication"):
            replication_ips = ipset
            print(f"IPset Entries: {replication_ips}")
            
    else:
        print(f"Isolated Cluster Replication Firewall did not populate proplery!")
        
