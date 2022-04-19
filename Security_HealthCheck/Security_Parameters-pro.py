
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
        print(str1, ' Not Listed')
    except AttributeError:
        print(str1, ' Not Listed')
    except TypeError:
        print(str1, ' Not Listed')

# definition for either printing to log a json object or outputing 'Not Listed' if error occurs
def try_write(str1, str2, ind):
    try:
        pfile.write(str1)
        pfile.write(json.dumps(ind[str2]))
        pfile.write("\n")
    except KeyError:
        pfile.write(str1)
        pfile.write(' Not Listed')
        pfile.write("\n")
    except AttributeError:
        pfile.write(str1)
        pfile.write(' Not Listed')
        pfile.write("\n")
    except TypeError:
        pfile.write(str1)
        pfile.write(' Not Listed')
        pfile.write("\n")

# validate file exists and is not null
def valid_file(file_path):
    os.stat(file_path).st_size > 5

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER ACCESS MANAGEMENT

# CERTIFICATE BASED AUTHENTICATION CONFIGURED
# KERBEROS PROVIDER CONFIGURED
# LDAP PROVIDER CONFIGURED
# LDAP PROVIDER USING SSL FOR COMMUNICATION
# NIS PROVIDER CONFIGURED
# NIS PROVIDER CONFIGURED
# KEYSTONE SERVER CONFIGURED
# SSO CONFIGURED

print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER ACCESS MANAGEMENT')
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
        pfile.write('COHESITY CLUSTER ACCESS MANAGEMENT')
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
            try_write('Roles:', 'roles', i)
            try_write('Username:', 'username', i)
            pfile.write("\n")

    else:
        print('Users are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER ACCESS MANAGEMENT')
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
            customRole = i['isCustomRole']
            if (customRole == True):
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
            customRole = i['isCustomRole']
            if (customRole == True):
                pfile.write("\n")
                try_write('Description:', 'description', i)
                try_write('Label:', 'label', i)
                try_write('Role Name:', 'name', i)
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
print('AD GROUPS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
groups = glob.glob(source + '/API/*groups*.json')

for x in groups:

    if os.stat(x).st_size > 5:
    
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            domain = i['domain']
            if (domain != 'LOCAL'):
                try_print('Domain:', 'domain', i)
                try_print('Group Name:', 'name', i)
                try_print('Roles:', 'roles', i)
                try_print('SID:', 'sid', i)
                print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('AD GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            domain = i['domain']
            if (domain != 'LOCAL'):
                try_write('Domain:', 'domain', i)
                try_write('Group Name:', 'name', i)
                try_write('Roles:', 'roles', i)
                try_write('SID:', 'sid', i)
                pfile.write("\n")

    else:
        print('Active Directory Groups are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Active Directory Groups are not configured for this environment.')
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
            try_print('Trusted Domains:', 'trustedDomains', i)
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
            try_write('Blacklisted Domains:', 'ignoredTrustedDomains', i)
            try_write('Trusted Domains:', 'trustedDomains', i)
            try_write('Preferred Domain Controllers:', 'preferredDomainControllers', i)
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

#NEED TO TEST

print("\n")
print("\n")
print('NTLM AUTHENTICATION DISABLED')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
gflags = glob.glob(source + '/IRIS/*gflags*.json')

for x in gflags:
    if os.stat(x).st_size > 5:
        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('GFLAG', '\n GFLAG \n')

        ntlmDisabled = "(bridge_smb_portal_auth_use_ntlm_and_kerberos_with_ad\, (.*?) )"

        # print data to screen
        print('NTLM Authentication: ')
        try:
            ntlm_search = re.search(ntlmDisabled, content)
            print(ntlm_search.group())
            print("\n")
            print('***If the flag is set false, NTLM Authentication is disabled. If there is no flag or if it is set to true, NTLM is enabled.***')

        except AttributeError:
            print('***There is no flag set, NTLM is enabled.***')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTLM AUTHENTICATION DISABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('NTLM Authentication: ')
        try:
            ntlm_search = re.search(ntlmDisabled, content)
            pfile.write(ntlm_search.group())
            pfile.write("\n")
            pfile.write('***If the flag is set false, NTLM Authentication is disabled. If there is no flag or if it is set to true, NTLM is enabled.***')
            pfile.write("\n")

        except AttributeError:
            pfile.write('***There is no flag set, NTLM is enabled.***')
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

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SSO AUDIT')
print('COHESITY CLUSTER AUTHENTICATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
basic = glob.glob(source + '/API/*basicCluster*.json')

for x in basic:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Single Sign-on Identity Provider Configured:', json.dumps(data['idpConfigured']))
        print('Cohesity Cluster Authentication Type:', json.dumps(data['authenticationType']))
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SSO AUDIT')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER AUTHENTICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Single Sign-On Identity Provider Configured:')
        pfile.write(json.dumps(data['idpConfigured']))
        pfile.write("\n")
        pfile.write('Cohesity Cluster Authentication Type:') 
        pfile.write(json.dumps(data['authenticationType']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Single Sign-on is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SSO AUDIT')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER AUTHENTICATION')
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
print('2FA CLUSTER AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        mfa = "(is_cluster_mfa_enabled\: (.*?) )"

        # print data to screen
        print('2FA Mode for Cluster: ')
        try:
            mfa_search = re.search(mfa, content)
            mfa_group = mfa_search.group()
            mfa_group = mfa_group.split(":")
            print(mfa_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA CLUSTER AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA Mode for Cluster:')
        try:
            mfa_search = re.search(mfa, content)
            mfa_group = mfa_search.group()
            mfa_group = mfa_group.split(":")
            pfile.write(mfa_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(mfa_search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Two Factor Authentication for the Cohesity Cluster is not configured.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA CLUSTER AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Two Factor Authentication for the Cohesity Cluster is not configured.')
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
        print('Local User Authentication Type:', json.dumps(data['authenticationType']))
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
        pfile.write('Local User Authentication Type:')
        pfile.write(json.dumps(data['authenticationType']))
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Two Factor Authentication is not configured for local users in this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA AUDIT LOCAL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Two Factor Authentication is not configured for local users in this environment.')
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
        print('2FA Mode for Support User: ')
        try:
            fa_search = re.search(fa, content)
            fa_group = fa_search.group()
            fa_group = fa_group.split(":")
            print(fa_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        print('2FA Support User Email Address: ')
        try:
            faE_search = re.search(faEmail, content)
            faE_group = faE_search.group()
            faE_group = faE_group.split(":")
            print(faE_group[1])
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
        pfile.write('2FA Mode for Support User:')
        try:
            fa_search = re.search(fa, content)
            fa_group = fa_search.group()
            fa_group = fa_group.split(":")
            pfile.write(fa_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(fa_search.group())
        pfile.write("\n")
        pfile.write('2FA Support User Email Address:')
        try:
            faE_search = re.search(faEmail, content)
            faE_group = faE_search.group()
            faE_group = faE_group.split(":")
            pfile.write(faE_group[1])
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
        print('Is Support User Password set: ')
        try:
            pwSet_search = re.search(pwSet, content)
            pwSet_group = pwSet_search.group()
            pwSet_group = pwSet_group.split(":")
            print(pwSet_group[1])
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

        print('Is Support User Password Converted: ')
        try:
            pwConv_search = re.search(pwConv, content)
            pwConv_group = pwConv_search.group()
            pwConv_group = pwConv_group.split(":")
            print(pwConv_group[1])
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
        pfile.write('Is Support User Password set:')
        try:
            pfile.write(pwSet_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Last Time Support Password Updated:')
        try:
            pfile.write(str(datetime_time))
        except NameError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Is Support User Password Converted:')
        try:
            pfile.write(pwConv_group[1])
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
            sudo_group = sudo_search.group()
            sudo_group = sudo_group.split(":")
            print(sudo_group[1])
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
            pfile.write(sudo_group[1])
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
# COHESITY CLUSTER CONFIGURATION

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('SMTP SERVER')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        smtp = "(smtp_server \{(.*?)\} )"

        # print data to screen
        print('SMTP Server: ')
        try:
            smtp_search = re.search(smtp, content)
            smtp_group = smtp_search.group()
            smtp_group = smtp_group.split()
            print(smtp_group[3])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMTP SERVER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMTP Server: ')
        try:
            smtp_search = re.search(smtp, content)
            smtp_group = smtp_search.group()
            smtp_group = smtp_group.split()
            pfile.write(smtp_group[3])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')

        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SMTP Server is not configured in this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write('COHESITY CLUSTER CONFIGURATION')
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMTP SERVER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SMTP Server is not configured in this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('NTP AUTHENTICATION KEY')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        ntp = "(ntp_authentication_enabled\: (.*?) )"

        # print data to screen
        print('NTP Authentication Key Enabled: ')
        try:
            ntp_search = re.search(ntp, content)
            ntp_group = ntp_search.group()
            ntp_group = ntp_group.split(":")
            print(ntp_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTP AUTHENTICATION KEY')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTP Authentication Key Enabled: ')
        try:
            ntp_search = re.search(ntp, content)
            ntp_group = ntp_search.group()
            ntp_group = ntp_group.split(":")
            pfile.write(ntp_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('NTP Authentication Configuration is not available for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTP AUTHENTICATION KEY')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('NTP Authentication Configuration is not available for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('SELF-SIGNED SSL CERTIFICATE VALIDATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# print('***To review the Self-Signed SSL Certification Validation Audit, please reference file: ' + source + '/CONFIG/*Cert_val*.json***')

# load json file
cert = glob.glob(source + '/CONFIG/*Cert_val*.json')

for x in cert:

    if os.stat(x).st_size > 5:
        with open(x, 'r') as f:
            print(f.read())
            print("\n")

#         with open(x, "r") as f:
#             content = f.read()
#             content = content.replace('\n', ' ')
            
#         cert = "(Issuer (.*?)\. )"
#         expired = "( (.*?)  expired\.)"

#         # print data to screen
#         print('Certificate Validation: ')
#         try:
#             cert_search = re.search(cert, content)
#             print(cert_search.group())
#             print("\n")
#         except AttributeError:
#             print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SELF-SIGNED SSL CERTIFICATE VALIDATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        with open(x, 'r') as f:
            pfile.write(f.read())
            pfile.write("\n")

        # pfile.write('Certificate Validation:')
        # try:
        #     cert_search = re.search(cert, content)
        #     pfile.write(cert_search.group())
        #     pfile.write("\n")
        # except AttributeError:
        #     pfile.write('Not Listed')

        # pfile.write('***To review the Self-Signed SSL Certification Validation Audit, please reference file: ' + source + '/CONFIG/*Cert_val*.json***')
        pfile.write("\n")

    else:
        print('SSL Certificate is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SELF-SIGNED SSL CERTIFICATE VALIDATION')
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

print("\n")
print("\n")
print('LOGIN BANNER ENABLED')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        banner = "(banner_enabled\: (.*?) )"

        # print data to screen
        print('Cluster Login Banner Enabled: ')
        try:
            banner_search = re.search(banner, content)
            banner_group = banner_search.group()
            banner_group = banner_group.split(":")
            print(banner_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOGIN BANNER ENABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Cluster Login Banner Enabled: ')
        try:
            banner_search = re.search(banner, content)
            banner_group = banner_search.group()
            banner_group = banner_group.split(":")
            pfile.write(banner_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Login Banner is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOGIN BANNER ENABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Login Banner is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('LOCAL GROUPS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
groups = glob.glob(source + '/API/*groups*.json')

for x in groups:

    if os.stat(x).st_size > 5:
    
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            domain = i['domain']
            if (domain == 'LOCAL'):
                try_print('Domain:', 'domain', i)
                try_print('Group Name:', 'name', i)
                try_print('Roles:', 'roles', i)
                try_print('SID:', 'sid', i)
                print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOCAL GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            domain = i['domain']
            if (domain == 'LOCAL'):
                try_write('Domain:', 'domain', i)
                try_write('Group Name:', 'name', i)
                try_write('Roles:', 'roles', i)
                try_write('SID:', 'sid', i)
                pfile.write("\n")

    else:
        print('Local Groups are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOCAL GROUPS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Local Groups are not configured for this environment.')
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
print('COHESITY CLUSTER ENCRYPTION')
print('COHESITY NODE TO NODE ENCRYPTION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        clusterLevel = "(cluster_level_encryption_enabled\: (.*?) )"
        nodeLevel = "(is_internode_protorpc_encryption_enabled\: (.*?) )"

        # print data to screen
        print('Cluster Level Encryption Enabled:')
        try:
            clusterLevel_search = re.search(clusterLevel, content)
            clusterLevel_group = clusterLevel_search.group()
            clusterLevel_group = clusterLevel_group.split(":")
            print(clusterLevel_group[1])
        except AttributeError:
            print('Not Listed')

        print('Node Level Encryption Enabled:')
        try:
            nodeLevel_search = re.search(nodeLevel, content)
            nodeLevel_group = nodeLevel_search.group()
            nodeLevel_group = nodeLevel_group.split(":")
            print(nodeLevel_group[1])
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER ENCRYPTION')
        pfile.write("\n")
        pfile.write('COHESITY NODE TO NODE ENCRYPTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Cluster Level Encryption Enabled:')
        try:
            clusterLevel_search = re.search(clusterLevel, content)
            clusterLevel_group = clusterLevel_search.group()
            clusterLevel_group = clusterLevel_group.split(":")
            pfile.write(clusterLevel_group[1])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Node Level Encryption Enabled:')
        try:
            nodeLevel_search = re.search(nodeLevel, content)
            nodeLevel_group = nodeLevel_search.group()
            nodeLevel_group = nodeLevel_group.split(":")
            pfile.write(nodeLevel_group[1])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

    else:
        print('Cluster Encryption is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER ENCRYPTION')
        pfile.write("\n")
        pfile.write('COHESITY NODE TO NODE ENCRYPTION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Cluster Encryption is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('KMS PROVIDER')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        kms = "(kms_server_vec \{(.*?)\})"

        # print data to screen
        print('KMS Provider Configuration Type: ')
        try:
            kms_search = re.search(kms, content)
            kms_group = kms_search.group()
            kms_group = kms_group.split()
            print(kms_group[3])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('KMS PROVIDER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('KMS Provider Configuration Type:')
        try:
            kms_search = re.search(kms, content)
            kms_group = kms_search.group()
            kms_group = kms_group.split()
            pfile.write(kms_group[3])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('KMS Provider is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('KMS PROVIDER')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('KMS Provider is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('ENCRYPTION KEY ROTATION AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        rotation = "(encryption_key_rotation_period_secs\: (.*?) )"

        # print data to screen
        print('Encryption Key Rotation Period (Days): ')
        try:
            rotation_search = re.search(rotation, content)
            rotation_group = rotation_search.group()
            rotation_group = rotation_group.split(":")
            # print(rotation_search.group())
            # print(rotation_group(1))
            seconds = rotation_group[1]
            days = (int(seconds))/86400
            print(days)
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ENCRYPTION KEY ROTATION AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Encryption Key Rotation Period (Days): ')
        try:
            rotation_search = re.search(rotation, content)
            rotation_group = rotation_search.group()
            rotation_group = rotation_group.split(":")
            # print(rotation_search.group())
            # print(rotation_group(1))
            seconds = rotation_group[1]
            days = (int(seconds))/86400
            # pfile.write(rotation_search.group())
            pfile.write(str(days))
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(mfa_search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Encryption Key Rotation for the Cohesity Cluster is not configured.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ENCRYPTION KEY ROTATION AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Encryption Key Rotation for this Cohesity Cluster is not configured.')
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
            try:
                print('Alert Categories:', json.dumps(i['categories']))
            except KeyError:
                print('Alert Categories:', 'All')
            except AttributeError:
                print('Alert Categories:', 'All')
            except TypeError:
                print('Alert Categories:', 'All')   
            
            try:
                print('Alert Severities:', json.dumps(i['severities']))
            except KeyError:
                print('Alert Severities:', 'All')
            except AttributeError:
                print('Alert Severities:', 'All')
            except TypeError:
                print('Alert Severities:', 'All')   

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
            try:
                pfile.write('Alert Categories:')
                pfile.write(json.dumps(i['categories']))
                pfile.write("\n")
            except KeyError:
                pfile.write('Alert Categories: All')
            except AttributeError:
                pfile.write('Alert Categories: All')
            except TypeError:
                pfile.write('Alert Categories: All')   
            
            try:
                pfile.write('Alert Severities:')
                pfile.write(json.dumps(i['severities']))
                pfile.write("\n")
            except KeyError:
                pfile.write('Alert Severities: All')
            except AttributeError:
                pfile.write('Alert Severities: All')
            except TypeError:
                pfile.write('Alert Severities: All')   
            try_write('sysLog Enabled:', 'syslogEnabled', i)
            try_write('Email Delivery Targets:', 'emailDeliveryTargets', i)
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
print('COHESITY PROACTIVE MONITORING ENABLED')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/IRIS/*info*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        monitoring = "(ACTIVE MONITORING ENABLED     \: (.*?) )"

        # print data to screen
        print('Cohesity Proactive Monitoring Enabled: ')
        try:
            monitoring_search = re.search(monitoring, content)
            monitoring_group = monitoring_search.group()
            print(monitoring_group)
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY PROACTIVE MONITORING ENABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Cohesity Proactive Monitoring Enabled: ')
        try:
            monitoring_search = re.search(monitoring, content)
            monitoring_group = monitoring_search.group()
            pfile.write(monitoring_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Cohesity Proactive Monitoring for the Cohesity Cluster is not configured.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY PROACTIVE MONITORING ENABLED')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Cohesity Proactive Monitoring for this Cohesity Cluster is not configured.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()


#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('LOCAL ADMIN EMAIL')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
users = glob.glob(source + '/API/*users*.json')

for x in users:
    
    if os.stat(x).st_size > 5:
        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            if (i['username'] == 'admin'):
                try_print('Domain:', 'domain', i)
                try_print('Roles:', 'roles', i)
                try_print('Username:', 'username', i)
                try_print('Local Admin Email Address:', 'emailAddress', i)
                print("\n")

        # print data to file
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOCAL ADMIN EMAIL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            if (i['username'] == 'admin'):
                try_write('Domain:', 'domain', i)
                try_write('Roles:', 'roles', i)
                try_write('Username:', 'username', i)
                try_write('Local Admin Email Address:', 'emailAddress', i)
                print("\n")

    else:
        print('Local Admin Email is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOCAL ADMIN EMAIL')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Local Admin Email is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

# FIREWALL CONFIG

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('BACKUP SUMMARY REPORTING')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
scheduler = glob.glob(source + '/API/*scheduler*.json')

for x in scheduler:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')
            content = content.replace('                         ', ' ')
            content = content.replace('                     ', ' ')
            content = content.replace('         ', ' ')
           
        receiver = "(\"receiverEmails\"\: \[ \"(.*?)\" \])"
        type = "(\"type\"\: \"(.*?)\" \})"


        try:
            scheduler_search = re.findall("(\"receiverEmails\"\: \[ \"(.*?)\" \])|(\"type\"\: \"(.*?)\" \})", content)
            print(scheduler_search)
            print("\n")
            for i in scheduler_search:
                print('Report Email Configuration:', i)
        except AttributeError:
            print('Not Listed')
            print("\n")

        # print data to file
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('BACKUP SUMMARY REPORTING')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            scheduler_search = re.findall("(\"receiverEmails\"\: \[ \"(.*?)\" \])|(\"type\"\: \"(.*?)\" \})", content)
            pfile.write(str(scheduler_search))
            pfile.write("\n")
            for i in scheduler_search:
                pfile.write('Report Email Configuration:')
                pfile.write(str(i))
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

    else:
        print('Reporting is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('BACKUP SUMMARY REPORTING')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Reporting is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CLUSTER FIREWALL CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')

print('***To review the Cluster Firewall Configuration, please reference file: ' + source + '/API/*-API-firewall-*.json***')

# print data to file
pfile = open(param, "a")
pfile.write("\n")
pfile.write("\n")
pfile.write('CLUSTER FIREWALL CONFIGURATION')
pfile.write("\n")
pfile.write('#---------------------------------------------------------------------------------------------------------------#')
pfile.write("\n")
pfile.write("\n")
pfile.write('***To review the Cluster Firewall Configuration, please reference file: ' + source + '/API/*-API-firewall-*.json***')
pfile.write("\n")

pfile.close()

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
            search = re.search(snmp, content)
            pfile.write(search.group())
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(search.group())
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('SNMP is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SNMP, SNMPv3')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('SNMP is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER SMARTFILES CONFIGURATION

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER SMARTFILES CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')
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
        whitelist_search = re.search(gWhitelist, content)
        search_group = whitelist_search.group()
        search_group = search_group.split("   ")
        
        for x in search_group:
            print(x)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER SMARTFILES CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('GLOBAL WHITELIST')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Global Whitelist:')
        pfile.write("\n")
        whitelist_search = re.search(gWhitelist, content)
        search_group = whitelist_search.group()
        search_group = search_group.split("   ")
        for x in search_group:
            pfile.write(x)
            pfile.write("\n")

    else:
        print('Global Whitelist is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER SMARTFILES CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
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
print('VIEW/SHARE CONFIGURATIONS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
views = glob.glob(source + '/API/*views*.json')

for x in views:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        f = open(x)
        data = json.load(f)

        

        # print data to screen
        try:
            for i in data['views']:
                try_print('View Name:', 'name', i)
                try_print('NFS View Discovery:', 'enableNfsViewDiscovery', i)
                try_print('Use Global Whitelist:', 'overrideGlobalWhitelist', i)
                try_print('SMB View Discovery:', 'enableSmbViewDiscovery', i)
                try_print('SMB Encryption:', 'enableSmbEncryption', i)
                try_print('SMB Encryption Enforced:', 'enforceSmbEncryption', i)
                try_print('SMB Access Based Enumeration:', 'enableSmbAccessBasedEnumeration', i)
                try_print('Protocol Access:', 'protocolAccess', i)
                try_print('View Security Mode:', 'securityMode', i)

                # try_print('View Data Protection Configured:', 'enableSmbAccessBasedEnumeration', i)
                

                try:
                    # print(json.dumps(i['antivirusScanConfig']))
                    antivirus = (json.dumps(i['antivirusScanConfig']))

                    av = "(\"isEnabled\"\: (.*?)\, )"

                    #print('Antivirus enabled on Views:')
                
                    av_search = re.search(av, antivirus)
                    av_group = av_search.group()
                    av_group = av_group.split(",")
                    print('Antivirus enabled on Views:', av_group[0])
                except KeyError:
                    print('View Antivirus Not Configured')


                # try:
                #     for c in i['antivirusScanConfig']:
                #         try_print('Antivirus enabled on Views:', 'isEnabled', c)
                # except KeyError:
                #     print('Antivirus Not Listed')
                try:
                    viewProtection = (json.dumps(i['viewProtection']))

                    inactivity = "(\"inactive\"\: (.*?)\, )"
                    jobName = "(\"jobName\"\: \"(.*?)\"\, )"

                    #print('View Data Protection Configuration Inactivity:')
                
                    inactivity_search = re.search(inactivity, viewProtection)
                    inactivity_group = inactivity_search.group()
                    print('View Data Protection Configuration Inactivity:', inactivity_group)
                

                    #print('View Protection Job Name:')
                
                    jobName_search = re.search(jobName, viewProtection)
                    jobName_group = jobName_search.group()
                    print('View Protection Job Name:', jobName_group)
                    print("\n")
                except KeyError:
                    print('View Protection Not Configured')
                    print("\n")

                # try:
                #     for a in i['viewProtection']:
                #         try_print('View Data Protection Configuration Inactivity:', 'inactive', a)
                #         for b in a['protectionJobs']:
                #             try_print('View Protection Job Name:', 'jobName', b)
                # except KeyError:
                #     print('View Protection Not Configured')
                #     print("\n")

                print('~~~~~ Cohesity View IP Whitelist ~~~~~')
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

                print('~~~~~ SMB Share Permissions ~~~~~')
                try:
                    for y in i['sharePermissions']:
                        try_print('Access:', 'access', y)
                        try_print('SID:', 'sid', y)
                        try_print('Type:', 'type', y)
                        print("\n")
                except KeyError:
                    print('SMB Share Permissions Not Listed')
                    print("\n")

                print('~~~~~ NFS Root Squash ~~~~~')

                try:
                    nfsRootSquash = (json.dumps(i['nfsRootSquash']))
                    print(nfsRootSquash)
                    print("\n")
                    # gid = "(\"gid\"\: (.*?) )"
                    # uid = "(\"uid\"\: (.*?) )"

                    # #print('GID:')
                
                    # gid_search = re.search(gid, nfsRootSquash)
                    # gid_group = gid_search.group()
                    # print('GID:', gid_group)
                
                    
                    # #print('UID:')
                
                    # uid_search = re.search(uid, nfsRootSquash)
                    # print(uid_search)
                    # uid_group = uid_search.group()
                    # print('UID:', uid_group)
                except KeyError:
                    print('NFS Root Squash Share Permissions Not Listed')

            # try:
            #     for z in i['nfsRootSquash']:
            #         try_print('GID:', 'gid', z)
            #         try_print('UID:', 'uid', z)
            #         print("\n")
            # except KeyError:
            #     print('NFS Root Squash Share Permissions Not Listed')
            #     print("\n")  
        except KeyError:
            print('There are no Views configuration on this Cohesity Cluster.')


        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('VIEW/SHARE CONFIGURATIONS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            for i in data['views']:
                try_write('View Name:', 'name', i)
                try_write('NFS View Discovery:', 'enableNfsViewDiscovery', i)
                try_write('Use Global Whitelist:', 'overrideGlobalWhitelist', i)
                try_write('SMB View Discovery:', 'enableSmbViewDiscovery', i)
                try_write('SMB Encryption:', 'enableSmbEncryption', i)
                try_write('SMB Encryption Enforced:', 'enforceSmbEncryption', i)
                try_write('SMB Access Based Enumeration:', 'enableSmbAccessBasedEnumeration', i)
                try_write('View Data Protection Configured:', 'enableSmbAccessBasedEnumeration', i)
                
                try:
                    antivirus = (json.dumps(i['antivirusScanConfig']))

                    av = "(\"isEnabled\"\: (.*?)\, )"

                    av_search = re.search(av, antivirus)
                    av_group = av_search.group()
                    av_group = av_group.split(",")
                    pfile.write('Antivirus enabled on Views:')
                    pfile.write(av_group[0])
                    pfile.write("\n")
                except KeyError:
                    pfile.write('View Antivirus Not Configured')
                    pfile.write("\n")

                try:
                    viewProtection = (json.dumps(i['viewProtection']))

                    inactivity = "(\"inactive\"\: (.*?)\, )"
                    jobName = "(\"jobName\"\: \"(.*?)\"\, )"

                    #print('View Data Protection Configuration Inactivity:')
                
                    inactivity_search = re.search(inactivity, viewProtection)
                    inactivity_group = inactivity_search.group()
                    pfile.write('View Data Protection Configuration Inactivity:')
                    pfile.write(inactivity_group)
                    pfile.write("\n")

                    jobName_search = re.search(jobName, viewProtection)
                    jobName_group = jobName_search.group()
                    pfile.write('View Protection Job Name:')
                    pfile.write(jobName_group)
                    pfile.write("\n")
                except KeyError:
                    pfile.write('View Protection Not Configured')
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
                pfile.write('~~~~~ SMB Share Permissions ~~~~~')
                pfile.write("\n")
                try:
                    for y in i['sharePermissions']:
                        try_write('Access:', 'access', y)
                        try_write('SID:', 'sid', y)
                        try_write('Type:', 'type', y)
                        pfile.write("\n")
                except KeyError:
                    pfile.write('SMB Share Permissions Not Listed')
                    pfile.write("\n")

                
                pfile.write("\n")
                ('~~~~~ NFS Root Squash ~~~~~')
                pfile.write("\n")
                try:
                    nfsRootSquash = (json.dumps(i['nfsRootSquash']))
                    pfile.write(nfsRootSquash)
                    pfile.write("\n")
                    
                except KeyError:
                    pfile.write('NFS Root Squash Share Permissions Not Listed') 
                    pfile.write("\n")
        except KeyError:
            pfile.write('There are no Views configuration on this Cohesity Cluster.')

    else:
        print('View/Share Permissions are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('VIEW/SHARE CONFIGURATIONS')
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
# DATA PROTECTION POLICY CONFIGURATION

# DATALOCK ENABLED FOR POLICIES
# FILE DATALOCK CONFIGURED WITHIN PROTECTION POLICIES
# FILE DATALOCK RETENTION CONFIGURATION (DATALOCK PERIOD)
# VIEW LEVEL DATALOCK CONFIGURED
# VIEW LEVEL DATALOCK RETENTION CONFIGURATION (COMPLIANCE/ENTERPRISE)
# VIEW LEVEL DATALOCK OVERRIDE CONFIGURED
# GRANULAR DATALOCK CONFIGURED

print("\n")
print("\n")
print('DATALOCK CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
views = glob.glob(source + '/API/*views*.json')

for x in views:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        f = open(x)
        data = json.load(f)

        # print data to screen
        try:
            for i in data['views']:
                print("\n")
                try_print('View Name:', 'name', i)
                try_print('View Datalock Retention Period:', 'dataLockExpiryUsecs', i)

                print("\n")
                print('~~~~~ File Lock Configuration ~~~~~')

                try:
                    fileLockConfig = (json.dumps(i['fileLockConfig']))

                    autoLock = "(\"autoLockAfterDurationIdle\"\: (.*?)\, )"
                    lockingProtocol = "(\"lockingProtocol\"\: \"(.*?)\"\, )"
                    fileRetention = "(\"defaultFileRetentionDurationMsecs\"\: (.*?)\, )"
                    mode = "(\"mode\"\: \"(.*?)\"\, )"
                    expiry = "(\"expiryTimestampMsecs\"\: (.*?)\, )"

                    print('AutoLock After Duration:')
                    print("\n")

                    try:
                        autoLock_search = re.search(autoLock, fileLockConfig)
                        autoLock_group = autoLock_search.group()
                        print(autoLock_group)
                    except AttributeError:
                        print('Not Listed')

                    print('File Data Locking Protocol:')
                    try:
                        lockingProtocol_search = re.search(lockingProtocol, fileLockConfig)
                        lockingProtocol_group = lockingProtocol_search.group()
                        print(lockingProtocol_group)
                    except AttributeError:
                        print('Not Listed')
                
                    print('File Datalock Retention Period:')
                    try:
                        fileRetention_search = re.search(fileRetention, fileLockConfig)
                        fileRetention_group = fileRetention_search.group()
                        print(fileRetention_group)
                    except AttributeError:
                        print('Not Listed')
            

                    print('File Level Datalock Mode:')
                    try:
                        mode_search = re.search(mode, fileLockConfig)
                        mode_group = mode_search.group()
                        print(mode_group)
                    except AttributeError:
                        print('Not Listed')
                

                    print('File Level Datalock Override Expiry:')
                    try:
                        expiry_search = re.search(expiry, fileLockConfig)
                        expiry_group = expiry_search.group()
                        print(expiry_group)
                    except AttributeError:
                        print('Not Listed')

                except KeyError:
                    print('Not Listed')
        except KeyError:
            print('There are no Views configuration on this Cohesity Cluster.')
            print("\n")



            # try:
            #     for d in i['fileLockConfig']:
            #         # print('AutoLock After Duration:', json.dumps(x['autoLockAfterDurationIdle']))
            #         try_print('AutoLock After Duration:', 'autoLockAfterDurationIdle', d)
            #         try_print('File Data Locking Protocol:', 'lockingProtocol', d)
            #         try_print('File Datalock Retention Period:', 'defaultFileRetentionDurationMsecs', d)
            #         try_print('File Level Datalock Mode:', 'mode', d)
            #         print('File Level Datalock Mode:', json.dumps(d['mode']))

            #         # try:
            #         #     print('File Level Datalock Override Expiry:', json.dumps(x['expiryTimestampMsecs']))
            #         #     print("\n")
            #         # except KeyError:
            #         #     print('File Level Datalock Override not configured.')
            #         #     print("\n")
            #         # except AttributeError:
            #         #     print('File Level Datalock Override not configured.')
            #         #     print("\n")
            #         # except TypeError:
            #         #     print('File Level Datalock Override not configured.')
            #         #     print("\n")
            # except KeyError:
            #     print('File DataLock is not configured for this View.')
            #     print("\n")
            # # except AttributeError:
            # #     print('File DataLock is not configured for this View.')
            # #     print("\n")
            # # except TypeError:
            # #     print('File DataLock is not configured for this View.')
            # #     print("\n")
   


        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('DATALOCK CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            for i in data['views']:
                try_write('View Name:', 'name', i)
                try_write('View Datalock Retention Period:', 'dataLockExpiryUsecs', i)

                pfile.write("\n")
                pfile.write('~~~~~ File Lock Configuration ~~~~~')
                pfile.write("\n")

                try:
                    fileLockConfig = (json.dumps(i['fileLockConfig']))

                    autoLock = "(\"autoLockAfterDurationIdle\"\: (.*?)\, )"
                    lockingProtocol = "(\"lockingProtocol\"\: \"(.*?)\"\, )"
                    fileRetention = "(\"defaultFileRetentionDurationMsecs\"\: (.*?)\, )"
                    mode = "(\"mode\"\: \"(.*?)\"\, )"
                    expiry = "(\"expiryTimestampMsecs\"\: (.*?)\, )"

                    pfile.write('AutoLock After Duration:')
                    pfile.write("\n")

                    try:
                        autoLock_search = re.search(autoLock, fileLockConfig)
                        autoLock_group = autoLock_search.group()
                        pfile.write(autoLock_group)
                        pfile.write("\n")
                    except AttributeError:
                        pfile.write('Not Listed')
                        pfile.write("\n")

                    pfile.write("\n")
                    pfile.write('File Data Locking Protocol:')
                    pfile.write("\n")
                    try:
                        lockingProtocol_search = re.search(lockingProtocol, fileLockConfig)
                        lockingProtocol_group = lockingProtocol_search.group()
                        pfile.write(lockingProtocol_group)
                        pfile.write("\n")
                    except AttributeError:
                        pfile.write('Not Listed')
                        pfile.write("\n")
                
                    pfile.write("\n")
                    pfile.write('File Datalock Retention Period:')
                    pfile.write("\n")
                    try:
                        fileRetention_search = re.search(fileRetention, fileLockConfig)
                        fileRetention_group = fileRetention_search.group()
                        pfile.write(fileRetention_group)
                        pfile.write("\n")
                    except AttributeError:
                        pfile.write('Not Listed')
                        pfile.write("\n")
            
                    pfile.write("\n")
                    pfile.write('File Level Datalock Mode:')
                    pfile.write("\n")
                    try:
                        mode_search = re.search(mode, fileLockConfig)
                        mode_group = mode_search.group()
                        pfile.write(mode_group)
                        pfile.write("\n")
                    except AttributeError:
                        pfile.write('Not Listed')
                        pfile.write("\n")
                
                    pfile.write("\n")
                    pfile.write('File Level Datalock Override Expiry:')
                    pfile.write("\n")
                    try:
                        expiry_search = re.search(expiry, fileLockConfig)
                        expiry_group = expiry_search.group()
                        pfile.write(expiry_group)
                        pfile.write("\n")
                    except AttributeError:
                        pfile.write('Not Listed')
                        pfile.write("\n")

                except KeyError:
                    pfile.write('Not Listed')
                    pfile.write("\n")
        except KeyError:
            pfile.write('There are no Views configuration on this Cohesity Cluster.')
            pfile.write("\n")

    else:
        print('View/Share Permissions are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('DATALOCK CONFIGURATION')
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
print('#---------------------------------------------------------------------------------------------------------------#')
print('DATA PROTECTION POLICY CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')
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
            try_print('Alerting Policy Severity:', 'alertingPolicy', i)
            try_print('Alerting Policy Email Addresses:', 'alertingConfig', i)
            print('\n')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('DATA PROTECTION POLICY CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PROTECTION JOB SLA ALERT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Protection Job Name:', 'name', i)
            try_write('Alerting Policy Severity:', 'alertingPolicy', i)
            try_write('Alerting Policy Email Addresses:', 'alertingConfig', i)
            pfile.write("\n")

    else:   
        print('Alerting is not configured for this environment.')
        print("\n")

        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('DATA PROTECTION POLICY CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
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
# INFRASTRUCTURE SERVICES

# CLOUD ARCHIVE ENCRYPTION KEYS DOWNLOADED FROM COHESITY CLUSTER
# CLOUD ARCHIVE SECURE CONNECTION ENABLED

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('INFRASTRUCTURE SERVICES')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('REMOTE CLUSTER CONFIGURATION')
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
            #try_print('All Remote Cluster Endpoints Reachable:', 'allEndpointsReachable', i)
            try_print('Remote Cluster Access Enabled:', 'purposeRemoteAccess', i)
            try_print('Remote Cluster Replication Enabled:', 'purposeReplication', i)
            try_print('Replicated Data Compression Enabled:', 'compressionEnabled', i)

            if 'encryptionKey' in i:
                print('Remote Cluster Encryption: Enabled')
            else:
                print('Remote Cluster Encryption: Disabled')

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
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write('INFRASTRUCTURE SERVICES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('REMOTE CLUSTER CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Remote Cluster Name:', 'name', i)
            try_write('Remote Cluster ID:', 'clusterId', i)
            #try_write('Remote Cluster Endpoints Reachable:', 'allEndpointsReachable', i)
            try_write('Remote Cluster Access Enabled:', 'purposeRemoteAccess', i)
            try_write('Remote Cluster Replication Enabled:', 'purposeReplication', i)
            try_write('Replicated Data Compression Enabled:', 'compressionEnabled', i)

            if 'encryptionKey' in i:
                pfile.write('Remote Cluster Encryption: Enabled')
                pfile.write("\n")
            else:
                pfile.write('Remote Cluster Encryption: Disabled')
                pfile.write("\n")

            try:
                for x in i['viewBoxPairInfo']:
                    try_write('Local Cohesity View Name:', 'localViewBoxName', x)
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
        print('Remote Cluster not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('INFRASTRUCTURE SERVICES')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('REMOTE CLUSTER REPLICATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Remote Cluster not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CLOUD ARCHIVE CONFIGURATION')
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
            try_print('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            try_print('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            try_print('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            try_print('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Cloud Archive Name:', 'name', i)
            try_write('Cloud Archive Encryption:', 'encryptionPolicy', i)
            try_write('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            try_write('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            try_write('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            try_write('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            pfile.write("\n")

    else:
        print('Cloud Archiving is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD ARCHIVE CONFIGURATION')
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Cloud Archiving is not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CLOUD TARGET CUSTOMER MANAGED ENCRYPTION KEYS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
vaults = glob.glob(source + '/API/*-vaults-*.json')

for x in vaults:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            #for x in i['config']:
            try_print('Cloud Target Name:', 'name', i)
            try_print('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD TARGET CUSTOMER MANAGED ENCRYPTION KEYS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            #for x in i['config']:
            try_write('Cloud Target Name:', 'name', i)
            pfile.write("\n")
            try_write('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Customer Managed Encryption Keys are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('CLOUD TARGET CUSTOMER MANAGED ENCRYPTION KEYS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Customer Managed Encryption Keys are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER HEALTH

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER HEALTH')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('NUMBER OF UNRESOLVED ALERTS')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
alerts = glob.glob(source + '/API/*-alerts-*.json')

for x in alerts:

    if os.stat(x).st_size > 5:

        f = open(x)
        data = json.load(f)

        # print data to screen
        print('Number of Current Unresolved Alerts')
        for iteration, item in enumerate(data):
            total_iteration = iteration
        print(total_iteration)
        print('\n')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER HEALTH')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NUMBER OF UNRESOLVED ALERTS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Number of Current Unresolved Alerts: ')
        for iteration, item in enumerate(data):
            total_iteration = iteration
        pfile.write(str(total_iteration))
        pfile.write("\n")

    else:
        print('There are currently no unresolved Alerts on this cluster.')
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
        pfile.write('NUMBER OF UNRESOLVED ALERTS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('There are currently no unresolved Alerts on this cluster.')
        pfile.write("\n")
        pfile.write("\n")  

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('NTP SYNC')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
ntpSync = glob.glob(source + '/HC/*NTP_Sync_Check*.json')


# print data to screen
for x in ntpSync:
    if os.stat(x).st_size > 5:
        with open(x, 'r') as f:
            print(f.read())
            print("\n")

        # with open(x, "r") as f:
        #     content = f.read()
        #     content = content.replace('\n', ' ')
        #     content = content.replace('}', '} \n')

        # output = "(\"10008\"\: (.*?) )"

        # try:
        #     output_search = re.search(output, content)
        #     output_group = output_search.group()
        #     print(output_group)
        # except AttributeError:
        #     print('Not Listed')
        #     print("\n")

        print("\n")
        print('***If result is anything other than "Pass", please reference file: ' + source + '/HC/*-HC-NTP_Sync_Check-*.json***')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTP SYNC')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        with open(x, 'r') as f:
            pfile.write(f.read())
            pfile.write("\n")

        # try:
        #     output_search = re.search(output, content)
        #     output_group = output_search.group()
        #     pfile.write(output_group)
        # except AttributeError:
        #     pfile.write('Not Listed')
        #     pfile.write("\n")

        pfile.write("\n")
        pfile.write('***If result is anything other than "Pass", please reference file: ' + source + '/HC/*-HC-NTP_Sync_Check-*.json***')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('NTP Sync Test not listed for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('NTP SYNC')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('NTP Sync Test not listed for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('OVERALL CLUSTER HEALTH AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

print('***To review the Overall Cluster Health Audit, please reference file: ' + source + '/HC/*-HC_CLI-ALL-*.json***')

# print data to file
pfile = open(param, "a")
pfile.write("\n")
pfile.write("\n")
pfile.write('OVERALL CLUSTER HEALTH AUDIT')
pfile.write("\n")
pfile.write('#---------------------------------------------------------------------------------------------------------------#')
pfile.write("\n")
pfile.write("\n")
pfile.write('***To review the Overall Cluster Health Audit, please reference file: ' + source + '/HC/*-HC_CLI-ALL-*.json***')
pfile.write("\n")

pfile.close()

#---------------------------------------------------------------------------------------------------------------#

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
        pfile.write("\n")
        pfile.write('PLATFORM VERSION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        try_write('Cohesity Cluster Software Version:', 'clusterSoftwareVersion', data)
        try_write('Cohesity Cluster Patch Version:', 'patchVersion', data)
        pfile.write("\n")

    else:
        print('Cohesity Cluster Software Versioning is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
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
        with open(x, 'r') as f:
            print(f.read())
            print("\n")

        # with open(x, "r") as f:
        #     content = f.read()
        #     content = content.replace('\n', ' ')
        #     content = content.replace('}', '} \n')

        # output = "(\"10003\"\: (.*?) )"

        # try:
        #     output_search = re.search(output, content)
        #     output_group = output_search.group()
        #     print(output_group)
        # except AttributeError:
        #     print('Not Listed')
        #     print("\n")

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

        with open(x, 'r') as f:
            pfile.write(f.read())
            pfile.write("\n")

        #for x in binary:
        # try:
        #     output_search = re.search(output, content)
        #     output_group = output_search.group()
        #     pfile.write(output_group)
        # except AttributeError:
        #     pfile.write('Not Listed')
        #     pfile.write("\n")

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

# print("\n")
# print("\n")
# print('LDAP ERRORS IN BRIDGE LOGS')
# print('#---------------------------------------------------------------------------------------------------------------#')

# # load json file
# ldap = glob.glob(source + '/HC/*LDAP*.json')

# # print data to screen
# for x in ldap:
#     if os.stat(x).st_size > 5:

#         with open (x, "r") as f:
#             content = f.read()
#             print(content)

#         print("\n")

#         # print data to file
#         pfile = open(param, "a")
#         pfile.write("\n")
#         pfile.write("\n")
#         pfile.write('LDAP ERRORS IN BRIDGE LOGS')
#         pfile.write("\n")
#         pfile.write('#---------------------------------------------------------------------------------------------------------------#')
#         pfile.write("\n")
#         pfile.write("\n")

#         for x in ldap:
#             with open (x, "r") as f:
#                 content = f.read()
#                 pfile.write(content)
                    
#         pfile.write("\n")
#         pfile.write("\n")

#     else:
#         print('LDAP Errors are not present on this environment.')
#         print("\n")
        
#         pfile = open(param, "a")
#         pfile.write("\n")
#         pfile.write("\n")
#         pfile.write('LDAP ERRORS IN BRIDGE LOGS')
#         pfile.write("\n")
#         pfile.write('#---------------------------------------------------------------------------------------------------------------#')
#         pfile.write("\n")
#         pfile.write("\n")

#         pfile.write('LDAP Errors are not present on this environment.')
#         pfile.write("\n")
#         pfile.write("\n") 
    
# pfile.close()

# f.close()

#---------------------------------------------------------------------------------------------------------------#
# COHESITY CLUSTER SECURITY SETTINGS



#---------------------------------------------------------------------------------------------------------------#
# COHESITY LOG SETTINGS

# PERFORM SYSLOG LOG SHIPPING VALIDATION

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
        try:
            for i in data['views']:
                try_print('View Name:', 'name', i)
                try_print('Filer Audit Logging Enabled:', 'enableFilerAuditLogging', i)
                print("\n")
        except KeyError:
            print('There are no Views configuration on this Cohesity Cluster.')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMB/NFS AUDIT LOGGING FOR VIEWS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        try:
            for i in data['views']:
                pfile.write("\n")
                try_write('View Name:', 'name', i)
                try_write('Filer Audit Logging Enabled:', 'enableFilerAuditLogging', i)
                pfile.write("\n")
        except KeyError:
            pfile.write('There are no Views configuration on this Cohesity Cluster.')

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
#HELIOS CLOUD CONFIGURATION

# HELIOS MANAGEMENT AUDIT 
# HELIOS PERMISSIONS AND ACCESS AUDIT 
# HELIOS ALERTING AUDIT 
# HELIOS CLOUD SSO AUDIT 
# HELIOS CLOUND 2FA AUDIT 

print("\n")
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('HELIOS CLOUD CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('HELIOS CONNECTIVITY AUDIT')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
mcmConfig = glob.glob(source + '/API/*mcmConfig*.json')

for x in mcmConfig:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        connected = "(\"connectedToMcm\"\: (.*?) )"
        enabled = "(\"enableMcm\"\: (.*?) )"
        appMode = "(\"isAppMode\"\: (.*?) )"
        readOnly = "(\"mcmReadOnly\"\: (.*?) )"
        registration = "(\"registrationStatus\"\: (.*?) )"
        error = "(\"registrationError\"\: (.*?) )"

        # print data to screen
        print('Helios Enabled: ')
        try:
            enabled_search = re.search(enabled, content)
            enabled_group = enabled_search.group()
            print(enabled_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")
        
        print('Cluster Connected to Helios: ')
        try:
            connected_search = re.search(connected, content)
            connected_group = connected_search.group()
            print(connected_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        print('Helios App Mode: ')
        try:
            appMode_search = re.search(appMode, content)
            appMode_group = appMode_search.group()
            print(appMode_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        print('Helios Read Only Mode: ')
        try:
            readOnly_search = re.search(readOnly, content)
            readOnly_group = readOnly_search.group()
            print(readOnly_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        print('Helios Registration Status: ')
        try:
            registration_search = re.search(registration, content)
            registration_group = registration_search.group()
            print(registration_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        print('Helios Registration Error: ')
        try:
            error_search = re.search(error, content)
            error_group = error_search.group()
            print(error_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('HELIOS CLOUD CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('HELIOS CONNECTIVITY AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Helios Enabled: ')
        pfile.write("\n")
        try:
            enabled_search = re.search(enabled, content)
            enabled_group = enabled_search.group()
            pfile.write(enabled_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")
        
        pfile.write('Cluster Connected to Helios: ')
        pfile.write("\n")
        try:
            connected_search = re.search(connected, content)
            connected_group = connected_search.group()
            pfile.write(connected_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Helios App Mode: ')
        pfile.write("\n")
        try:
            appMode_search = re.search(appMode, content)
            appMode_group = appMode_search.group()
            pfile.write(appMode_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Helios Read Only Mode: ')
        pfile.write("\n")
        try:
            readOnly_search = re.search(readOnly, content)
            readOnly_group = readOnly_search.group()
            pfile.write(readOnly_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Helios Registration Status: ')
        pfile.write("\n")
        try:
            registration_search = re.search(registration, content)
            registration_group = registration_search.group()
            pfile.write(registration_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Helios Registration Error: ')
        pfile.write("\n")
        try:
            error_search = re.search(error, content)
            error_group = error_search.group()
            pfile.write(error_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

    else:
        print('Helios Connectivity is not configured on this cluster.')
        print("\n")

        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('HELIOS CLOUD CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('HELIOS CONNECTIVITY AUDIT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('Helios Connectivity is not configured on this cluster.')
        pfile.write("\n")
        pfile.write("\n")       

pfile.close()

f.close()

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
            try_write('App Install Status:', 'installState', i)
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
