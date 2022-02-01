
import json
import glob
import os 
import sys 
from datetime import datetime 
import collections
import re 
import subprocess
from types import NoneType 
import shutil


source = raw_input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')

#---------------------------------------------------------------------------------------------------------------#

#source = "/home/cohesity/secLogs"
#source = "/Users/erin.zaborowski/secLogs"
pdir = "parameters"
param = source + "/" + pdir + "/" + "Security_HealthCheck_parameters.json"
# bash_script = "/home/cohesity/Security_HealthChecks-pro.sh"

# alter permissions and run Security_HealthChecks-pro.sh
# os.chmod(bash_script, 0o0777)

# p = subprocess.Popen(bash_script, stdout=subprocess.PIPE)
# for line in p.stdout:
#     print(line)
# p.wait()
# print(p.returncode)

# create subfolder
path = os.path.join(source, pdir)
isExists = os.path.exists(path)
if isExists == False:
    os.mkdir(path)

#---------------------------------------------------------------------------------------------------------------#

# definition for either printing to screen a json object or outputing 'Not Listed' if error occurs
def try_print(str1, str2, ind):
    try:
        print(str1, json.dumps(ind[str2]))
    except KeyError:
        print(str1 + ' Not Listed')
    except AttributeError:
        print(str1 + ' Not Listed')
    except TypeError:
        print(str1 + ' Not Listed')

# definition for either printing to log a json object or outputing 'Not Listed' if error occurs
def try_write(str1, str2, ind):
    try:
        pfile.write(str1)
        pfile.write(json.dumps(ind[str2]))
    except KeyError:
        pfile.write(str1 + ' Not Listed')
    except AttributeError:
        pfile.write(str1 + ' Not Listed')
    except TypeError:
        pfile.write(str1 + ' Not Listed')

# validate file exists and is not null
def valid_file(file_path):
    os.stat(file_path).st_size > 5

#---------------------------------------------------------------------------------------------------------------#

print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('DOMAIN, ROLES, USER')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
users = glob.glob(source + '/API/*users*.json')

for x in users:
    
    if os.stat(x).st_size > 5:
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Domain:', 'domain', i)
            try_print('Roles:', 'roles', i)
            try_print('Username:', 'username', i)
            print("\n")

        # print data to file
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('DOMAIN, ROLES, USER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Domain:', 'domain', i)
            pfile.write("\n")
            try_write('Roles:', 'roles', i)
            pfile.write("\n")
            try_write('Username:', 'username', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Users are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('DOMAIN, ROLES, USER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Users are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('ROLES')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
roles = glob.glob(source + '/API/*roles*.json')

for x in roles:
    
    if os.stat(x).st_size > 5:
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Description:', 'description', i)
            try_print('Label:', 'label', i)
            try_print('Role Name:', 'name', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ROLES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Description:', 'description', i)
            pfile.write("\n")
            try_write('Label:', 'label', i)
            pfile.write("\n")
            try_write('Role Name:', 'name', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Roles are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ROLES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Roles are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('GROUPS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
groups = glob.glob(source + '/API/*groups*.json')

for x in groups:

    if os.stat(x).st_size > 5:
    
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Domain:', 'domain', i)
            try_print('Group Name:', 'name', i)
            try_print('Roles:', 'roles', i)
            try_print('SID:', 'sid', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Domain:', 'domain', i)
            pfile.write("\n")
            try_write('Group Name:', 'name', i)
            pfile.write("\n")
            try_write('Roles:', 'roles', i)
            pfile.write("\n")
            try_write('SID:', 'sid', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Groups are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Groups are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('ACTIVE DIRECTORY CONFIG')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
ad = glob.glob(source + '/API/*activeDirectory*.json')

for x in ad:
    
    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Domain Name:', 'domainName', i)
            try_print('Blacklisted Domains:', 'ignoredTrustedDomains', i)
            try_print('Preferred Domain Controllers:', 'preferredDomainControllers', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ACTIVE DIRECTORY CONFIG')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Domain Name:', 'domainName', i)
            pfile.write("\n")
            try_write('Blacklisted Domains:', 'ignoredTrustedDomains', i)
            pfile.write("\n")
            try_write('Preferred Domain Controllers:', 'preferredDomainControllers', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Active Directory is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ACTIVE DIRECTORY CONFIG')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Active Directory is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('NTLM AUTHENTICATION DISABLED')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
gflags = glob.glob(source + '/IRIS/*gflags*.json')

for x in gflags:

    if os.stat(x).st_size > 5:
    #     f = open(x)   
# data = json.load(f)
        file = open(x, "r")

        ntlmDisabled = "(bridge_smb_portal_auth_use_ntlm_and_kerberos_with_ad (.*?)\n)"

        # print data to screen
        print('NTLM Authentication Enabled: ')
        for i in file:
            if re.search(ntlmDisabled, i):
                print(i)

        # search = re.search(ntlmDisabled, file)
        # print(search.group())

        print("\n")
        print('***If the flag is set false, NTLM Authentication is disabled. If there is no flag set, NTLM is enabled.***')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTLM AUTHENTICATION DISABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTLM Authentication Enabled: ')

        for i in file:
            if re.search(ntlmDisabled, i):
                pfile.write(i)

        # search = re.search(ntlmDisabled, file)
        # pfile.write(search.group())

        pfile.write("\n")
        pfile.write('***If the flag is set false, NTLM Authentication is disabled. If there is no flag set, NTLM is enabled.***')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('NTLM Authentication is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTLM AUTHENTICATION DISABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('NTLM Authentication is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

file.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('GLOBAL WHITELIST')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        gWhitelist_init = "(client_subnet_whitelist(.*?)\n storage_tier_vec)"
        gWhitelist = gWhitelist_init.replace('storage_tier_vec', '')

        # print data to screen
        print('Global Whitelist: ')
        search = re.search(gWhitelist, content)
        search_group = search.group()
        search_group = search_group.split("   ")
        for x in search_group:
            print(x)

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GLOBAL WHITELIST')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Global Whitelist:')
        for x in search_group:
            pfile.write(x)
        pfile.write("\n")

    else:
        print('Global Whitelist is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GLOBAL WHITELIST')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Global Whitelist is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()
f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('NFS VIEW DISCOVERY')
print('VIEW IP WHITELIST')
print('SMB ACL (NTFS) PERMISSIONS')
print('SHARE PERMISSIONS')
print('SMB AUTHENTICATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
views = glob.glob(source + '/API/*views*.json')

for x in views:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data['views']:
            try_print('View Name:', 'name', i)
            try_print('NFS View Discovery:', 'enableNfsViewDiscovery', i)
            try_print('Override Global Whitelist:', 'overrideGlobalWhitelist', i)
            try_print('SMB ACL (NTFS) Permissions Enabled:', 'enableSmbAccessBasedEnumeration', i)
            try_print('SMB Authentication:', 'enableSmbViewDiscovery', i)
            print("\n")
            print('~~~~~ Cohesity View IP Whitelist ~~~~~')
            print("\n")
            try:
                for x in i['subnetWhitelist']:
                    try_print('Description:', 'description', x)
                    try_print('IP:', 'ip', x)
                    try_print('Subnet Mask:', 'netmaskBits', x)
                    try_print('NFS Access:', 'nfsAccess', x)
                    try_print('S3 Access:', 's3Access', x)
                    try_print('SMB Access:', 'smbAccess', x)
                    print("\n")
            except KeyError:
                print('Cohesity View IP Whitelist Not Listed')
                print("\n")

            print('~~~~~ Share Permissions ~~~~~')
            print("\n")

            try:
                for y in i['sharePermissions']:
                    try_print('Access:', 'access', y)
                    try_print('SID:', 'sid', y)
                    try_print('Type:', 'type', y)
                    print("\n")
            except KeyError:
                print('Share Permissions Not Listed')
            print("\n")
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NFS VIEW DISCOVERY')
        pfile.write("\n")
        pfile.write('VIEW IP WHITELIST')
        pfile.write("\n")
        pfile.write('SMB ACL (NTFS) PERMISSIONS')
        pfile.write("\n")
        pfile.write('SHARE PERMISSIONS')
        pfile.write("\n")
        pfile.write('SMB AUTHENTICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data['views']:
            pfile.write("\n")
            try_write('View Name:', 'name', i)
            pfile.write("\n")
            try_write('NFS View Discovery:', 'enableNfsViewDiscovery', i)
            pfile.write("\n")
            try_write('Override Global Whitelist:', 'overrideGlobalWhitelist', i)
            pfile.write("\n")
            try_write('SMB ACL (NTFS) Permissions Enabled:', 'enableSmbAccessBasedEnumeration', i)
            pfile.write("\n")
            try_write('SMB Authentication:', 'enableSmbViewDiscovery', i)
            pfile.write("\n")
            pfile.write("\n")
            pfile.write('~~~~~ Cohesity View IP Whitelist ~~~~~')
            pfile.write("\n")
            try:
                for x in i['subnetWhitelist']:
                    try_write('Description:', 'description', x)
                    try_write('IP:', 'ip', x)
                    try_write('Subnet Mask:', 'netmaskBits', x)
                    try_write('NFS Access:', 'nfsAccess', x)
                    try_write('S3 Access:', 's3Access', x)
                    try_write('SMB Access:', 'smbAccess', x)
                    pfile.write("\n")
            except KeyError:
                pfile.write('Cohesity View IP Whitelist Not Listed')
                pfile.write("\n")
            pfile.write("\n")
            pfile.write('~~~~~ Share Permissions ~~~~~')
            pfile.write("\n")
            try:    
                for y in i['sharePermissions']:
                    try_write('Access:', 'access', y)
                    try_write('SID:', 'sid', y)
                    try_write('Type:', 'type', y)
                    pfile.write("\n")
            except KeyError:
                pfile.write('Share Permissions Not Listed')
                pfile.write("\n")
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('View/Share Permissions are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NFS VIEW DISCOVERY')
        pfile.write("\n")
        pfile.write('VIEW IP WHITELIST')
        pfile.write("\n")
        pfile.write('SMB ACL (NTFS) PERMISSIONS')
        pfile.write("\n")
        pfile.write('SHARE PERMISSIONS')
        pfile.write("\n")
        pfile.write('SMB AUTHENTICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('View/Share Permissions are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CLOUD ARCHIVE AUDIT')
print('CLOUD ARCHIVE ENCRYPTION')
print('CLOUD ARCHIVE COMPRESSION')
print('CLOUD ARCHIVE SOURCE SIDE DEDUPLICATION')
print('CLOUD ARCHIVE INCREMENTAL ARCHIVAL')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
vaults = glob.glob(source + '/API/*-vaults-*.json')

for x in vaults:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Cloud Archive Name:', 'name', i)
            try_print('Cloud Archive Encryption:', 'encryptionPolicy', i)
            try_print('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            try_print('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            try_print('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE AUDIT')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE ENCRYPTION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE COMPRESSION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE SOURCE SIDE DEDUPLICATION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE INCREMENTAL ARCHIVAL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Cloud Archive Name:', 'name', i)
            pfile.write("\n")
            try_write('Cloud Archive Encryption:', 'encryptionPolicy', i)
            pfile.write("\n")
            try_write('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            pfile.write("\n")
            try_write('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            pfile.write("\n")
            try_write('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Cloud Archives are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE AUDIT')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE ENCRYPTION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE COMPRESSION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE SOURCE SIDE DEDUPLICATION')
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE INCREMENTAL ARCHIVAL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Cloud Archives are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('REMOTE CLUSTER REPLICATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
remote = glob.glob(source + '/API/*remoteClusters*.json')

for x in remote:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Remote Cluster Name:', 'name', i)
            try_print('Remote Cluster ID:', 'clusterId', i)
            try_print('Remote Cluster Replication Enabled:', 'purposeReplication', i)
            try_print('Replicated Data Compression Enabled:', 'compressionEnabled', i)
            try:
                for x in i['viewBoxPairInfo']:
                    try_print('Local Cohesity View Name:', 'localViewBoxName', x)
                    try_print('Remote Cohesity View Name:', 'remoteViewBoxName', x)
                    print("\n")
            except KeyError:
                print('View Pair Info Not Listed')
                print("\n")
            except TypeError:
                print('View Pair Info Not Listed')
                print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('REMOTE CLUSTER REPLICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Remote Cluster Name:', 'name', i)
            pfile.write("\n")
            try_write('Remote Cluster ID:', 'clusterId', i)
            pfile.write("\n")
            try_write('Remote Cluster Replication Enabled:', 'purposeReplication', i)
            pfile.write("\n")
            try_write('Replicated Data Compression Enabled:', 'compressionEnabled', i)
            pfile.write("\n")

            try:
                for x in i['viewBoxPairInfo']:
                    try_write('Local Cohesity View Name:', 'localViewBoxName', x)
                    pfile.write("\n")
                    try_write('Remote Cohesity View Name:', 'remoteViewBoxName', x)
                    pfile.write("\n")
            except KeyError:
                pfile.write('View Pair Info Not Listed')
                pfile.write("\n")
            except TypeError:
                pfile.write('View Pair Info Not Listed')
                pfile.write("\n")

            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Remote Cluster Replication is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('REMOTE CLUSTER REPLICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Remote Cluster Replication is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('ALERTING CONFIGURATION')
print('EMAIL CONFIGURATION AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
alerts = glob.glob(source + '/API/*alertNotificationRules*.json')

for x in alerts:
    
    if os.stat(x).st_size > 5:
        f = open(x)
        data = json.load(f)

    # print data to screen

        for i in data:
            try_print('Email Alert Rule Name:', 'ruleName', i)
            try_print('Alert Categories:', 'categories', i)
            try_print('Alert Severities:', 'severities', i)
            try_print('sysLog Enabled:', 'syslogEnabled', i)
            try_print('Email Delivery Targets:', 'emailDeliveryTargets', i)
            print("\n")

    # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ALERTING CONFIGURATION')
        pfile.write("\n")
        pfile.write('EMAIL CONFIGURATION AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Email Alert Rule Name:', 'ruleName', i)
            pfile.write("\n")
            try_write('Alert Categories:', 'categories', i)
            pfile.write("\n")
            try_write('Alert Severities:', 'severities', i)
            pfile.write("\n")
            try_write('sysLog Enabled:', 'syslogEnabled', i)
            pfile.write("\n")
            try_write('Email Delivery Targets:', 'emailDeliveryTargets', i)
            pfile.write("\n")
            pfile.write("\n")
    else:
        print('Alerting is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ALERTING CONFIGURATION')
        pfile.write("\n")
        pfile.write('EMAIL CONFIGURATION AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Alerting is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")       
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('PROTECTION JOB SLA ALERT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
pJobs = glob.glob(source + '/API/*-protectionJobs-*.json')

for x in pJobs:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Protection Job Name:', 'name', i)
            try_print('Full Protection Job SLA (mins):', 'fullProtectionSlaTimeMins', i)
            try_print('Incremental Protection Job SLA (mins):', 'incrementalProtectionSlaTimeMins', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PROTECTION JOB SLA ALERT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Protection Job Name:', 'name', i)
            pfile.write("\n")
            try_write('Full Protection Job SLA (mins):', 'fullProtectionSlaTimeMins', i)
            pfile.write("\n")
            try_write('Incremental Protection Job SLA (mins):', 'incrementalProtectionSlaTimeMins', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Alerting is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PROTECTION JOB SLA ALERT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Alerting is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")    
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('STORAGE DOMAIN ENCRYPTION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
vBoxes = glob.glob(source + '/API/*-viewBoxes-*.json')

for x in vBoxes:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Storage Domain Name:', 'name', i)
            # try:
            
            sPolicy = json.dumps(i['storagePolicy'])
            sPolicy_split = sPolicy.split()
            print('Encryption Policy:', sPolicy_split[1])
            print('\n')
            
            # except KeyError:
            #     print('Encryption Policy:' + ' Not Listed')
            #     print('\n')
            # except AttributeError:
            #     print('Encryption Policy:' + ' Not Listed')
            #     print('\n')
            # except TypeError:
            #     print('Encryption Policy:' + ' Not Listed')
            #     print('\n')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('STORAGE DOMAIN ENCRYPTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Storage Domain Name:', 'name', i)
            pfile.write("\n")

            # try:
            sPolicy = json.dumps(i['storagePolicy'])
            sPolicy_split = sPolicy.split()
            pfile.write('Encryption Policy: ')
            pfile.write(sPolicy_split[1])
            pfile.write('\n')
            # except KeyError:
            #     pfile.write('Encryption Policy:' + ' Not Listed')
            #     pfile.write('\n')
            # except AttributeError:
            #     pfile.write('Encryption Policy:' + ' Not Listed')
            #     pfile.write('\n')
            # except TypeError:
            #     pfile.write('Encryption Policy:' + ' Not Listed')
            #     pfile.write('\n')

            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Storage Domain Encryption is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('STORAGE DOMAIN ENCRYPTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Storage Domain Encryption is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SNMP, SNMPv3')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        snmp = "(snmp_config \{(.*?)\})"

        # print data to screen
        print('SNMP Configuration: ')
        try:
            search = re.search(snmp, content)
            print(search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SNMP, SNMPv3')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SNMP Configuration:')
        try:
            pfile.write(search.group())
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SNMP Configuration is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SNMP, SNMPv3')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SNMP Configuration is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER HEALTH

print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER HEALTH')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('PLATFORM VERSION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
cluster = glob.glob(source + '/API/*-cluster-*.json')

for x in cluster:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        try_print('Cohesity Cluster Software Version:', 'clusterSoftwareVersion', data)
        try_print('Cohesity Cluster Patch Version:', 'patchVersion', data)
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER HEALTH')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PLATFORM VERSION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        try_write('Cohesity Cluster Software Version:', 'clusterSoftwareVersion', data)
        pfile.write("\n")
        try_write('Cohesity Cluster Patch Version:', 'patchVersion', data)
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Cohesity Cluster Software Versioning is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER HEALTH')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PLATFORM VERSION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Cohesity Cluster Software Versioning is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CUSTOM BINARIES')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
binary = glob.glob(source + '/HC/*Binary_Files*.json')

# print data to screen
for x in binary:
    if os.stat(x).st_size > 5:

        with open (x, 'r') as f:
            for line in f.readlines():
                if '10003' in line:
                    print(line)

        print("\n")
        print('***If result is anything other than "Pass", please reference file: ' + source + '/HC/*-HC-Binary_Files_Release_Version_Check-*.json***')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CUSTOM BINARIES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        for x in binary:
            with open (x, 'r') as f:
                for line in f.readlines():
                    if '10003' in line:
                        pfile.write(line)

        pfile.write("\n")
        pfile.write('***If result is anything other than "Pass", please reference file: ' + source + '/HC/*-HC-Binary_Files_Release_Version_Check-*.json***')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Custom Binaries are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CUSTOM BINARIES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Custom Binaries are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('LDAP ERRORS IN BRIDGE LOGS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
ldap = glob.glob(source + '/HC/*LDAP*.json')

# print data to screen
for x in ldap:
    if os.stat(x).st_size > 5:

        with open (x, 'r') as f:
            print(f.read())

        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LDAP ERRORS IN BRIDGE LOGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        for x in ldap:
            with open (x, 'r') as f:
                pfile.write(f.read())
                    
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('LDAP Errors are not present on this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LDAP ERRORS IN BRIDGE LOGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('LDAP Errors are not present on this environment.')
        pfile.write("\n")
        pfile.write("\n") 
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER SECURITY SETTINGS

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER SECURITY SETTINGS')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('SSO AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
basic = glob.glob(source + '/API/*basicCluster*.json')

for x in basic:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Identity Provider Configured:', json.dumps(data['idpConfigured']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER SECURITY SETTINGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SSO AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Identity Provider Configured:')
        pfile.write(json.dumps(data['idpConfigured']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Single Sign-on is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER SECURITY SETTINGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SSO AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Single Sign-on is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('2FA AUDIT LOCAL')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
basic = glob.glob(source + '/API/*basicCluster*.json')

for x in basic:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Authentication Type:', json.dumps(data['authenticationType']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA AUDIT LOCAL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Authentication Type:')
        pfile.write(json.dumps(data['authenticationType']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Two Factor Authentication is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA AUDIT LOCAL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Two Factor Authentication is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('2FA SUPPORT AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        fa = "(two_fa_mode\: (.*?) )"
        faEmail = "(two_fa_email_id\: (.*?) )"

        # print data to screen
        print('2FA Mode: ')
        try:
            fa_search = re.search(fa, content)
            print(fa_search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')

        print('2FA Email Address: ')
        try:
            faE_search = re.search(faEmail, content)
            print(faE_search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA SUPPORT AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA Mode:')
        try:
            pfile.write(fa_search.group())
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(fa_search.group())
        pfile.write("\n")
        pfile.write('2FA Email Address:')
        try:
            pfile.write(faE_search.group())
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(faE_search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Two Factor Authentication for Support User is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA SUPPORT AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Two Factor Authentication for Support User is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SUPPORT ACCOUNT PASSWORD AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        # set variables
        pwSet = "(is_password_set\: (.*?) )"
        epoch_time = "(last_password_updated_timestamp_sec\: (.*?) )"
        pwConv = "(is_password_converted\: (.*?) )"

        # print data to screen
        print('Has Support User Password been set: ')
        try:
            pwSet_search = re.search(pwSet, content)
            print(pwSet_search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        print('Last Time Support Password Updated: ')
        try:
            time_search = re.search(epoch_time, content)
            print(time_search.group())
            time = (time_search.group())
            time_split = time.split()
            # print(time_split[1])
            # print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        # convert epoch time
        try:
            datetime_time = datetime.fromtimestamp(float(time_split[1])) 
            print(datetime_time)
            print("\n")
        except NameError:
            print("\n")

        print('Has Support User Password been Converted: ')
        try:
            pwConv_search = re.search(pwConv, content)
            print(pwConv_search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUPPORT ACCOUNT PASSWORD AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Has Support User Password been set:')
        try:
            pfile.write(pwSet_search.group())
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Last Time Support Password Updated:')
        try:
            pfile.write(str(datetime_time))
        except NameError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Has Support User Password been Converted:')
        try:
            pfile.write(pwConv_search.group())
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Support Account Password is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUPPORT ACCOUNT PASSWORD AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Support Account Password is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SUDO AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        sudo = "(is_sudo_access_enabled\: (.*?) )"

        # print data to screen
        print('Is SUDO Access Enabled: ')
        try:
            sudo_search = re.search(sudo, content)
            print(sudo_search.group())
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUDO AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Is SUDO Access Enabled:')
        try:
            pfile.write(sudo_search.group())
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SUDO Access is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUDO AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SUDO Access is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SUPPORT CHANNEL AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
cluster = glob.glob(source + '/API/*-cluster-*.json')

for x in cluster:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Is Remote Tunnel Enabled:', json.dumps(data['reverseTunnelEnabled']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUPPORT CHANNEL AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Is Remote Tunnel Enabled:')
        pfile.write(json.dumps(data['reverseTunnelEnabled']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Remote Tunnel is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUPPORT CHANNEL AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Remote Tunnel is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SELF-SIGNED SSL CERTIFICATE')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
cert = glob.glob(source + '/API/*certificate*.json')

for x in cert:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # convert epoch time 
        epoch_time = json.dumps(data['lastUpdateTimeMsecs'])
        print(epoch_time)
        datetime_time = datetime.fromtimestamp(float(epoch_time)/1000) 

        # print data to screen
        print('Last Time Certificate was Updated: ')
        print(datetime_time)
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SELF-SIGNED SSL CERTIFICATE')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Last Time Certificate was Updated:')
        pfile.write(str(datetime_time))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SSL Certificate is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SELF-SIGNED SSL CERTIFICATE')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SSL Certificate is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY LOG SETTINGS

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY LOG SETTINGS')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('AUDIT LOG RETENTION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
cluster = glob.glob(source + '/API/*-cluster-*.json')

for x in cluster:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Audit Log Configuration:', json.dumps(data['clusterAuditLogConfig']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY LOG SETTINGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('AUDIT LOG RETENTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Audit Log Configuration:')
        pfile.write(json.dumps(data['clusterAuditLogConfig']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Cohesity Audit Logs are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY LOG SETTINGS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('AUDIT LOG RETENTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Cohesity Audit Logs are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SMB/NFS AUDIT LOG RETENTION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
cluster = glob.glob(source + '/API/*-cluster-*.json')

for x in cluster:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Filer Audit Log Configuration:', json.dumps(data['filerAuditLogConfig']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMB/NFS AUDIT LOG RETENTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Filer Audit Log Configuration:')
        pfile.write(json.dumps(data['filerAuditLogConfig']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SMB/NFS Audit Logs are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMB/NFS AUDIT LOG RETENTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SMB/NFS Audit Logs are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SMB/NFS AUDIT LOGGING FOR VIEWS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
views = glob.glob(source + '/API/*views*.json')

for x in views:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data['views']:
            try_print('View Name:', 'name', i)
            try_print('Filer Audit Logging Enabled:', 'enableFilerAuditLogging', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMB/NFS AUDIT LOGGING FOR VIEWS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        for i in data['views']:
            pfile.write("\n")
            try_write('View Name:', 'name', i)
            pfile.write("\n")
            try_write('Filer Audit Logging Enabled:', 'enableFilerAuditLogging', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('SMB/NFS Audit Logs are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMB/NFS AUDIT LOGGING FOR VIEWS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SMB/NFS Audit Logs are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 
            
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SYSLOG SERVER CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
syslog = glob.glob(source + '/IRIS/*syslog*.json')

# print data to screen
for i in syslog:

    if os.stat(i).st_size > 5:

        with open(i, 'r') as f:
            print(f.read())

        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SYSLOG SERVER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        for i in syslog:
            with open(i, 'r') as f:
                pfile.write(f.read())
                    
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Syslog Server is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SYSLOG SERVER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Syslog Server is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")       
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# CLOUD CONFIGURATION AUDIT

# print data to file
# pfile = open(param, "a")
# pfile.write("\n")
# pfile.write('#---------------------------------------------------------------------------------------------------------------#')
# pfile.write("\n")
# pfile.write('CLOUD CONFIGURATION AUDIT')
# pfile.write("\n")
# pfile.write('#---------------------------------------------------------------------------------------------------------------#')
# pfile.write("\n")
# pfile.write("\n")

# pfile.close()

#---------------------------------------------------------------------------------------------------------------#
# MARKETPLACE APP AUDIT

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('MARKETPLACE APP AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('MARKETPLACE APPS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
apps = glob.glob(source + '/API/*apps*.json')

for x in apps:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('"', '')
            content = content.replace(',', '} \n')

            name_search = "(name\: (.*?) )"
            desc_search = "(description\: (.*?)\} )"
            dev_search = "(devVersion\: (.*?)\} )"

            names = re.findall(name_search, content)
            descs = re.findall(desc_search, content)
            devs = re.findall(dev_search, content)

        # for x in apps:
            f = open(x)
            data = json.load(f)

        for i, name, desc, dev in zip(data, names, descs, devs):

            print(name)
            print(desc)
            print(dev)

            # convert epoch time 
            try:
                epoch_time_install = json.dumps(i['installTime'])
                datetime_time_install = datetime.fromtimestamp(float(epoch_time_install)) 
            except:
                datetime_time_install = 'Not Listed'

            try:
                epoch_time_uninstall = json.dumps(i['uninstallTime'])
                datetime_time_uninstall = datetime.fromtimestamp(float(epoch_time_uninstall)) 
            except:
                datetime_time_uninstall = 'Not Listed'

            try_print('App ID:', 'appId', i)
            try_print('App Install Status:', 'installState', i)
            print('Install Time: ')
            try:
                print(datetime_time_install)
            except:
                print('Not Listed')

            print('Uninstall Time: ')
            try:
                print(datetime_time_uninstall)
                print("\n") 
            except:
                print('Not Listed')
                print("\n") 

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('MARKETPLACE APP AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('MARKETPLACE APPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i, name, desc, dev in zip(data, names, descs, devs):

            # try:
            pfile.write(str(name))
            pfile.write("\n")
            pfile.write(str(desc))
            pfile.write("\n")
            pfile.write(str(dev))
            pfile.write("\n")
            # except TypeError:
            #     pfile.write('Not Listed')
            #     pfile.write("\n")

            try_write('App ID:', 'appId', i)
            pfile.write("\n")
            try_write('App Install Status:', 'installState', i)
            pfile.write("\n")
            pfile.write('Install Time: ')
            pfile.write("\n")
            # try:
            pfile.write(str(datetime_time_install))
            pfile.write("\n")
            # except:
            #     pfile.write('Not Listed')
            #     pfile.write("\n")

            pfile.write('Uninstall Time: ')
            # try:
            pfile.write(str(datetime_time_uninstall))
            pfile.write("\n") 
            pfile.write("\n")
            # except:
            #     pfile.write('Not Listed')
            #     pfile.write("\n") 
            #     pfile.write("\n")

    else:
        print('MarketPlace Apps are not configured for this environment.')
        print("\n")

        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('MARKETPLACE APP AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('MARKETPLACE APPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('MarketPlace Apps are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")       

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
