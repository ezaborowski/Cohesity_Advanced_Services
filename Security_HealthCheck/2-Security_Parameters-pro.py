
import json
import glob
import os
import sys 
from datetime import datetime 
import collections
import re 
import subprocess
#from types import NoneType 
import shutil
import csv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# while True:
#     raw_input = input
#     source = input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')
#     if source.isalnum() == True:
#
#     else:
#         print("secLogs directory cannot be blank or contain special characters")
#         raw_input = input
#         source = input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')

# ask user to input secLogs filepath
raw_input = input
source = input('Please input the directory of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ')
apiSource = source + "/" + "API"

# check if file path is correct
while os.path.isdir(apiSource) == False:
    print(bcolors.FAIL + "Did not find the appropriate subfolders listed under: "+str(source)+'. Please check the directory path, spelling, and try again.' + bcolors.ENDC)

    source = None  
    apiSource = None
    raw_input = input
    source = input(bcolors.WARNING + 'Please input a valid file path of the uncompressed secLogs folder (ex: /Users/john.doe/secLogs): ' + bcolors.ENDC)
    apiSource = source + "/" + "API"

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
        #print(' Not Listed')
    except AttributeError:
        print(str1, ' Not Listed')
        #print(' Not Listed')
    except TypeError:
        print(str1, ' Not Listed')
        #print(' Not Listed')

# definition for either printing to log a json object or outputing 'Not Listed' if error occurs
def try_write(str1, str2, ind):
    try:
        pfile.write(str1)
        pfile.write(json.dumps(ind[str2]))
        pfile.write("\n")
    except KeyError:
        #pfile.write(str1)
        pfile.write(' Not Listed')
        pfile.write("\n")
    except AttributeError:
        #pfile.write(str1)
        pfile.write(' Not Listed')
        pfile.write("\n")
    except TypeError:
        #pfile.write(str1)
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

print('Developed by Erin Zaborowski - August 12 2021')
print('Last Updated 6/16/2022')

print("\n")

print('All Index Reference referenced below are in relation to the Security Assessment Scope List, which can be found here: https://docs.google.com/spreadsheets/d/1i9CdB32Qs90yRHMiNLXBYolGNC1JDg7yV1w3aWzG6bI/edit?usp=sharing')
print("\n")
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER ACCESS MANAGEMENT')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('USERS    Index Reference 3')
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
            try:
                try_print('User Exempt from MFA:', 'isUserExemptFromMfa', i['mfaInfo'])
            except KeyError:
                print("mfaInfo Section Not Listed.")
            print("\n")

        # print data to file
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write('Developed by Erin Zaborowski - August 12 2021')
        pfile.write("\n")
        pfile.write('Last Updated 6/16/2022')
        pfile.write("\n")
        pfile.write("\n")
        # pfile.write('All Index References referenced below are in relation to the Security Assessment Scope List, which can be found here: https://docs.google.com/spreadsheets/d/1i9CdB32Qs90yRHMiNLXBYolGNC1JDg7yV1w3aWzG6bI/edit?usp=sharing')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER ACCESS MANAGEMENT')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('USERS    Index Reference 3')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        for i in data:
            pfile.write("\n")
            try_write('Domain:', 'domain', i)
            try_write('Roles:', 'roles', i)
            try_write('Username:', 'username', i)
            try:
                try_write('User Exempt from MFA:', 'isUserExemptFromMfa', i['mfaInfo'])
            except KeyError:
                pfile.write("mfaInfo Section Not Listed.")
            pfile.write("\n")
        
        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write('Look for glaring issues. For example, generic accounts with the Admin Role or Data Security Role.')

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
        pfile.write('USERS    Index Reference 3')
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
print('ROLES    Index Reference 4')
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
                try_print('Role Privileges:', 'privileges', i)
                print("\n")
                print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ROLES    Index Reference 4')
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
                try_write('Role Privileges:', 'privileges', i)
                pfile.write("\n")
                pfile.write("\n")
        
        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write("Look for glaring issues. For example, Roles that were created that give elevated permissions that could impact cluster operations.")

    else:
        print('Roles are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ROLES    Index Reference 4')
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
print('AD GROUPS    Index Reference 3')
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
        pfile.write('AD GROUPS    Index Reference 3')
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

        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write("Look for glaring issues. For example, generic accounts with the Admin Role or Data Security Role.")

    else:
        print('Active Directory Groups are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('AD GROUPS    Index Reference 3')
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
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        domDiscovery = "(trusted_domain_discovery_disabled\: (.*?) )"

        # print data to screen
        print('Trusted Domain Discovery Disabled: ')
        try:
            domDiscovery_search = re.search(domDiscovery, content)
            domDiscovery_group = domDiscovery_search.group()
            domDiscovery_group = domDiscovery_group.split(":")
            print(domDiscovery_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('ACTIVE DIRECTORY CONFIG')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile = open(param, "a")
        pfile.write('Trusted Domain Discovery Disabled: ')
        try:
            domDiscovery_search = re.search(domDiscovery, content)
            domDiscovery_group = domDiscovery_search.group()
            domDiscovery_group = domDiscovery_group.split(":")
            pfile.write(domDiscovery_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        #pfile.write(mfa_search.group())
        pfile.write("\n")

    else:
        print('Trusted Domain Discovery for this Cohesity Cluster is not configured.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")

        pfile.write('Trusted Domain Discoveryfor this Cohesity Cluster is not configured.')
        pfile.write("\n")

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#



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
            try_print('Machine Accounts:', 'machineAccounts', i)
            print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        
        for i in data:
            pfile.write("\n")
            try_write('Domain Name:', 'domainName', i)
            try_write('Blacklisted Domains:', 'ignoredTrustedDomains', i)
            try_write('Trusted Domains:', 'trustedDomains', i)
            try_write('Preferred Domain Controllers:', 'preferredDomainControllers', i)
            try_write('Machine Accounts:', 'machineAccounts', i)
            pfile.write("\n")

        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write("Cohesity Cluster should be a member of AD Domains that are required. Sometimes a production cluster could be added to a QA/Test Domain which could be a security vulnerablity.")

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
print('NTLM AUTHENTICATION DISABLED    Index Reference 12')
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
        pfile.write('NTLM AUTHENTICATION DISABLED    Index Reference 12')
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
        pfile.write('NTLM AUTHENTICATION DISABLED    Index Reference 12')
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
print('SSO AUDIT    Index Reference 19')
print('COHESITY CLUSTER AUTHENTICATION    Index Reference 13')
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
        pfile.write('SSO AUDIT    Index Reference 19')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER AUTHENTICATION    Index Reference 13')
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
        pfile.write('SSO AUDIT    Index Reference 19')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER AUTHENTICATION    Index Reference 13')
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
print('2FA CLUSTER AUDIT    ')
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
        pfile.write('2FA CLUSTER AUDIT    ')
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
        pfile.write('2FA CLUSTER AUDIT    ')
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
print('2FA AUDIT LOCAL    Index Reference 20')
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
        pfile.write('2FA AUDIT LOCAL    Index Reference 20')
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
        pfile.write('2FA AUDIT LOCAL    Index Reference 20')
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
print('2FA SUPPORT AUDIT    Index Reference 24')
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
        pfile.write('2FA SUPPORT AUDIT    Index Reference 24')
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

        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write("The Support Account should have 2FA/MFA configured.")

    else:
        print('Two Factor Authentication for Support User is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('2FA SUPPORT AUDIT    Index Reference 24')
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
print('SUPPORT ACCOUNT PASSWORD AUDIT    Index Reference 25')
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
        pfile.write('SUPPORT ACCOUNT PASSWORD AUDIT    Index Reference 25')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Is Support User Password set:')
        try:
            pwSet_search = re.search(pwSet, content)
            pwSet_group = pwSet_search.group()
            pwSet_group = pwSet_group.split(":")
            pfile.write(pwSet_group[1])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")

        pfile.write('Last Time Support Password Updated:')
        try:
            time_search = re.search(epoch_time, content)
            pfile.write(time_search.group())
            time = (time_search.group())
            time_split = time.split()
            # print(time_split[1])
            # print("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")
        
        pfile.write('Is Support User Password Converted:')
        try:
            pwConv_search = re.search(pwConv, content)
            pwConv_group = pwConv_search.group()
            pwConv_group = pwConv_group.split(":")
            pfile.write(pwConv_group[1])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")
        pfile.write("\n")

        pfile.write("Expected Output:")
        pfile.write("\n")
        pfile.write("Password is unique, 8-character or more & complex, secured, and auditing is in place.")

    else:
        print('Support Account Password is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SUPPORT ACCOUNT PASSWORD AUDIT    Index Reference 25')
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
print('SUDO AUDIT    Index Reference 27')
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
        pfile.write('SUDO AUDIT    Index Reference 27')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Is SUDO Access Enabled:')
        try:
            sudo_search = re.search(sudo, content)
            sudo_group = sudo_search.group()
            sudo_group = sudo_group.split(":")
            pfile.write(sudo_group[1])
            pfile.write("\n")
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
        pfile.write('SUDO AUDIT    Index Reference 27')
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
print('SUPPORT CHANNEL AUDIT    Index Reference 28')
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
        pfile.write('SUPPORT CHANNEL AUDIT    Index Reference 28')
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
        pfile.write('SUPPORT CHANNEL AUDIT    Index Reference 28')
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
print('SMTP SERVER    Index Reference 33')
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
            print(smtp_group)
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
        pfile.write('SMTP SERVER    Index Reference 33')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('SMTP Server: ')
        try:
            smtp_search = re.search(smtp, content)
            smtp_group = smtp_search.group()
            pfile.write(smtp_group)
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
        pfile.write('SMTP SERVER    Index Reference 33')
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
print('NTP AUTHENTICATION KEY    Index Reference 34')
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
        pfile.write('NTP AUTHENTICATION KEY    Index Reference 34')
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
        pfile.write('NTP AUTHENTICATION KEY    Index Reference 34')
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
print('SELF-SIGNED SSL CERTIFICATE VALIDATION    Index Reference 35')
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
        pfile.write('SELF-SIGNED SSL CERTIFICATE VALIDATION    Index Reference 35')
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
        pfile.write('SELF-SIGNED SSL CERTIFICATE VALIDATION    Index Reference 35')
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
print('LOGIN BANNER ENABLED    Index Reference 36')
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
        pfile.write('LOGIN BANNER ENABLED    Index Reference 36')
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
        pfile.write('LOGIN BANNER ENABLED    Index Reference 36')
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
print('LOCAL GROUPS    Index Reference 37')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        groups = "(local_groups_enabled\: (.*?) )"

        # print data to screen
        print('Local Groups Enabled: ')
        try:
            groups_search = re.search(groups, content)
            groups_group = groups_search.group()
            print(groups_group)
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('LOCAL GROUPS    Index Reference 37')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write('Local Groups Enabled: ')
        try:
            groups_search = re.search(groups, content)
            groups_group = groups_search.group()
            pfile.write(groups_group)
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")


    else:
        print('Local Groups not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Local Groups not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")  
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#


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
        pfile.write('LOCAL GROUPS    Index Reference 37')
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
print('STORAGE DOMAIN ENCRYPTION    Index Reference 38')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
vBoxes = glob.glob(source + '/API/*-viewBoxes-*.json')

for x in vBoxes:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Storage Domain Name:', 'name', i)
            try:
                print('Encryption Policy:')

                storagePolicy = (json.dumps(i['storagePolicy']))
                encryption = "(\"encryptionPolicy\"\: (.*?)\, )"
            
                encryption_search = re.search(encryption, storagePolicy)
                encryption_group = encryption_search.group()
                encryption_split = encryption_group.split(':')
                print(encryption_split[1])
            except KeyError:
                print('View Antivirus Not Configured')
            print('\n')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('STORAGE DOMAIN ENCRYPTION    Index Reference 38')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        # print data to screen
        for i in data:
            try_write('Storage Domain Name:', 'name', i)
            try:
                pfile.write('Encryption Policy:')

                storagePolicy = (json.dumps(i['storagePolicy']))
                encryption = "(\"encryptionPolicy\"\: (.*?)\, )"
           
                encryption_search = re.search(encryption, storagePolicy)
                encryption_group = encryption_search.group()
                encryption_split = encryption_group.split(':')
                pfile.write(encryption_split[1])
            except KeyError:
                pfile.write('View Antivirus Not Configured')
            print('\n')

            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Storage Domain Encryption is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('STORAGE DOMAIN ENCRYPTION    Index Reference 38')
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
print('COHESITY CLUSTER ENCRYPTION    Index Reference 39')
print('COHESITY NODE TO NODE ENCRYPTION    Index Reference 40')
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
        pfile.write('COHESITY CLUSTER ENCRYPTION    Index Reference 39')
        pfile.write("\n")
        pfile.write('COHESITY NODE TO NODE ENCRYPTION    Index Reference 40')
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
        pfile.write('COHESITY CLUSTER ENCRYPTION    Index Reference 39')
        pfile.write("\n")
        pfile.write('COHESITY NODE TO NODE ENCRYPTION    Index Reference 40')
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
print('ENCRYPTION KEY ROTATION AUDIT    Index Reference 42')
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
            if rotation_search is None:
                print('Encryption Key set to default - 90 days.')
            else:
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
        pfile.write('ENCRYPTION KEY ROTATION AUDIT    Index Reference 42')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Encryption Key Rotation Period (Days): ')
        try:
            rotation_search = re.search(rotation, content)
            if rotation_search is None:
                print('Encryption Key set to default - 90 days.')
            else:
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
        pfile.write('ENCRYPTION KEY ROTATION AUDIT    Index Reference 42')
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
print('ALERTING CONFIGURATION    Index Reference 43')
print('EMAIL CONFIGURATION AUDIT    Index Reference 43')
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
        pfile.write('ALERTING CONFIGURATION    Index Reference 43')
        pfile.write("\n")
        pfile.write('EMAIL CONFIGURATION AUDIT    Index Reference 43')
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
        pfile.write('ALERTING CONFIGURATION    Index Reference 43')
        pfile.write("\n")
        pfile.write('EMAIL CONFIGURATION AUDIT    Index Reference 43')
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
print('COHESITY PROACTIVE MONITORING ENABLED    Index Reference 44')
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
        pfile.write('COHESITY PROACTIVE MONITORING ENABLED    Index Reference 44')
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
        pfile.write('COHESITY PROACTIVE MONITORING ENABLED    Index Reference 44')
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
print('LOCAL ADMIN EMAIL    Index Reference 46')
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
        pfile.write('LOCAL ADMIN EMAIL    Index Reference 46')
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
        pfile.write('LOCAL ADMIN EMAIL    Index Reference 46')
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
print('BACKUP SUMMARY REPORTING    Index Reference 47')
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
            # print(scheduler_search)
            print("\n")

            # cull out duplicates
            emailList = []
            dupList = []

            for i in scheduler_search:
                if i not in emailList:
                    emailList.append(i)
                else:
                    dupList.append(i)

            for i in emailList:
                print('Report Email Configuration:', i)
        except AttributeError:
            print('Not Listed')
            print("\n")

        # print data to file
        pfile = open(param, "a+")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('BACKUP SUMMARY REPORTING    Index Reference 47')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            scheduler_search = re.findall("(\"receiverEmails\"\: \[ \"(.*?)\" \])|(\"type\"\: \"(.*?)\" \})", content)
            # pfile.write(str(scheduler_search))
            pfile.write("\n")

            # cull out duplicates
            emailList = []
            dupList = []

            for i in scheduler_search:
                if i not in emailList:
                    emailList.append(i)
                else:
                    dupList.append(i)

            for i in emailList:
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
        pfile.write('BACKUP SUMMARY REPORTING    Index Reference 47')
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
print('CLUSTER FIREWALL CONFIGURATION    Index Reference 49')
print('#---------------------------------------------------------------------------------------------------------------#')

print('***To review the Cluster Firewall Configuration, please reference file: ' + source + '/API/*-API-firewall-*.json***')

# print data to file
pfile = open(param, "a")
pfile.write("\n")
pfile.write("\n")
pfile.write('CLUSTER FIREWALL CONFIGURATION    Index Reference 49')
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

        snmp = "(snmp_config \{(.*?) read_user)"
        read = "(read_user \{(.*?) encrypted_auth_password)"
        read_2 = "(read_user \{(.*?) auth_protocol)"
        write = "(write_user \{(.*?) encrypted_auth_password)"
        write_2 = "(write_user \{(.*?) auth_protocol)"
        trap = "(trap_user \{(.*?) encrypted_auth_password)"
        trap_2 = "(trap_user \{(.*?) auth_protocol)"
        op = "(operation\: (.*?) sys_info)"

        # print data to screen
        print('SNMP Configuration: ')
        try:
            search_snmp = re.search(snmp, content)
            search_snmp_group = (search_snmp.group())
            search_snmp_group = search_snmp_group.split('read_user')
            print(search_snmp_group[0])
            print("\n")
        except AttributeError:
            print('Not Listed')
        if search_snmp is None:
            print('SNMP not configured on this Cohesity Cluster.')
        else:
            print('SNMP Read User Configuration: ')
            try:
                search_read = re.search(read, content)
                search_read_group = (search_read.group())
                search_read_group = search_read_group.split('encrypted_auth_password')
                print(search_read_group[0])
                print("\n")
            except AttributeError:
                search_read = re.search(read_2, content)
                search_read_group = (search_read.group())
                search_read_group = search_read_group.split('auth_protocol')
                print(search_read_group[0])
                print("\n")
            except AttributeError:
                print('Not Listed')
            print('SNMP Write User Configuration: ')
            try:
                search_write = re.search(write, content)
                search_write_group = (search_write.group())
                search_write_group = search_write_group.split('encrypted_auth_password')
                print(search_write_group[0])
                print("\n")
            except AttributeError:
                search_write = re.search(write_2, content)
                search_write_group = (search_write.group())
                search_write_group = search_write_group.split('auth_protocol')
                print(search_write_group[0])
                print("\n")
            except AttributeError:
                print('Not Listed')
            print('SNMP Trap User Configuration: ')
            try:
                search_trap = re.search(trap, content)
                search_trap_group = (search_trap.group())
                search_trap_group = search_trap_group.split('encrypted_auth_password')
                print(search_trap_group[0])
                print("\n")
            except AttributeError:
                search_trap = re.search(trap_2, content)
                search_trap_group = (search_trap.group())
                search_trap_group = search_trap_group.split('auth_protocol')
                print(search_trap_group[0])
                print("\n")
            except AttributeError:
                print('Not Listed')
            print('SNMP Operation Configuration: ')
            try:
                search_op = re.search(op, content)
                search_op_group = (search_op.group())
                search_op_group = search_op_group.split('sys_info')
                print(search_op_group[0])
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
        pfile.write('SNMP Configuration: ')
        try:
            search_snmp = re.search(snmp, content)
            search_snmp_group = (search_snmp.group())
            search_snmp_group = search_snmp_group.split('read_user')
            pfile.write(search_snmp_group[0])
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            pfile.write("\n")
        if search_snmp is None:
            pfile.write('SNMP not configured on this Cohesity Cluster.')
            pfile.write("\n")
        else:
            pfile.write('SNMP Read User Configuration: ')
            try:
                search_read = re.search(read, content)
                search_read_group = (search_read.group())
                search_read_group = search_read_group.split('encrypted_auth_password')
                pfile.write(search_read_group[0])
                pfile.write("\n")
            except AttributeError:
                search_read = re.search(read_2, content)
                search_read_group = (search_read.group())
                search_read_group = search_read_group.split('auth_protocol')
                pfile.write(search_read_group[0])
                pfile.write("\n")
            except AttributeError:
                pfile.write('Not Listed')
                pfile.write("\n")
            pfile.write('SNMP Write User Configuration: ')
            try:
                search_write = re.search(write, content)
                search_write_group = (search_write.group())
                search_write_group = search_write_group.split('encrypted_auth_password')
                pfile.write(search_write_group[0])
                pfile.write("\n")
            except AttributeError:
                search_write = re.search(write_2, content)
                search_write_group = (search_write.group())
                search_write_group = search_write_group.split('auth_protocol')
                pfile.write(search_write_group[0])
                pfile.write("\n")
            except AttributeError:
                pfile.write('Not Listed')
                pfile.write("\n")
            pfile.write('SNMP Trap User Configuration: ')
            try:
                search_trap = re.search(trap, content)
                search_trap_group = (search_trap.group())
                search_trap_group = search_trap_group.split('encrypted_auth_password')
                pfile.write(search_trap_group[0])
                pfile.write("\n")
            except AttributeError:
                search_trap = re.search(trap_2, content)
                search_trap_group = (search_trap.group())
                search_trap_group = search_trap_group.split('auth_protocol')
                pfile.write(search_trap_group[0])
                pfile.write("\n")
            except AttributeError:
                pfile.write('Not Listed')
                pfile.write("\n")
            pfile.write('SNMP Operation Configuration: ')
            try:
                search_op = re.search(op, content)
                search_op_group = (search_op.group())
                search_op_group = search_op_group.split('sys_info')
                pfile.write(search_op_group[0])
                pfile.write("\n")
            except AttributeError:
                pfile.write('Not Listed')
                pfile.write("\n")
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
print('GLOBAL WHITELIST    Index Reference 54')
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
        try:
            search_group = whitelist_search.group()
            search_group = search_group.split("   ")

            for x in search_group:
                print(x)
                print("\n")

        except AttributeError:
            print('Not Listed')

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
        pfile.write('GLOBAL WHITELIST    Index Reference 54')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        pfile.write('Global Whitelist:')
        pfile.write("\n")
        

        whitelist_search = re.search(gWhitelist, content)
        try:
            search_group = whitelist_search.group()
            search_group = search_group.split("   ")

            for x in search_group:
                pfile.write(x)
                pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
            

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
        pfile.write('GLOBAL WHITELIST    Index Reference 54')
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
config = glob.glob(source + '/CONFIG/*CONFIG-CLUSTER*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        smbAuth = "(disable_smb_auth\: (.*?) )"
        smbMulti = "(smb_multichannel_enabled\: (.*?) )"

        # print data to screen
        print('Disable SMB Authentication: ')
        try:
            smbAuth_search = re.search(smbAuth, content)
            smbAuth_group = smbAuth_search.group()
            smbAuth_group = smbAuth_group.split(":")
            print(smbAuth_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')
        print('SMB Multichannel Enabled: ')
        try:
            smbMulti_search = re.search(smbMulti, content)
            smbMulti_group = smbMulti_search.group()
            smbMulti_group = smbMulti_group.split(":")
            print(smbMulti_group[1])
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('VIEW/SHARE CONFIGURATIONS')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile = open(param, "a")
        pfile.write('Disable SMB Authentication: ')
        try:
            smbAuth_search = re.search(smbAuth, content)
            smbAuth_group = smbAuth_search.group()
            smbAuth_group = smbAuth_group.split(":")
            pfile.write(smbAuth_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('SMB Multichannel Enabled: ')
        try:
            smbMulti_search = re.search(smbMulti, content)
            smbMultiy_group = smbMulti_search.group()
            smbMulti_group = smbMulti_group.split(":")
            pfile.write(smbMulti_group[1])
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")

    else:
        print('SMB Authentication is not configured for this Cohesity Cluster.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")

        pfile.write('SMB Authentication is not configured for this Cohesity Cluster.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

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
                print('--------------------------------------')
                try_print('View Name:', 'name', i)
                try_print('NFS View Discovery:', 'enableNfsViewDiscovery', i)
                #try_print('Use Global Whitelist:', 'overrideGlobalWhitelist', i)
                try_print('Override Global Whitelist:', 'overrideGlobalWhitelist', i)
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
        
        try:
            for i in data['views']:
                pfile.write("\n")
                pfile.write("\n")
                pfile.write('--------------------------------------')
                pfile.write("\n")
                try_write('View Name:', 'name', i)
                try_write('NFS View Discovery:', 'enableNfsViewDiscovery', i)
                #try_write('Use Global Whitelist:', 'overrideGlobalWhitelist', i)
                try_write('Override Global Whitelist:', 'overrideGlobalWhitelist', i)
                try_write('SMB View Discovery:', 'enableSmbViewDiscovery', i)
                try_write('SMB Encryption:', 'enableSmbEncryption', i)
                try_write('SMB Encryption Enforced:', 'enforceSmbEncryption', i)
                try_write('SMB Access Based Enumeration:', 'enableSmbAccessBasedEnumeration', i)
                try_write('Protocol Access:', 'protocolAccess', i)
                try_write('View Security Mode:', 'securityMode', i)

                # try_write('View Data Protection Configured:', 'enableSmbAccessBasedEnumeration', i)
                
                try:
                    antivirus = (json.dumps(i['antivirusScanConfig']))

                    av = "(\"isEnabled\"\: (.*?)\, )"

                    av_search = re.search(av, antivirus)
                    av_group = av_search.group()
                    av_group = av_group.split(",")
                    pfile.write('Antivirus enabled on Views:')
                    pfile.write(av_group[0])
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

                    jobName_search = re.search(jobName, viewProtection)
                    jobName_group = jobName_search.group()
                    pfile.write('View Protection Job Name:')
                    pfile.write(jobName_group)
                    pfile.write("\n")
                except KeyError:
                    pfile.write('View Protection Not Configured')
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
                
                pfile.write('~~~~~ NFS Root Squash ~~~~~')
                pfile.write("\n")
                try:
                    nfsRootSquash = (json.dumps(i['nfsRootSquash']))
                    pfile.write(nfsRootSquash)
                    pfile.write("\n")
                    pfile.write("\n")
                    pfile.write("\n")
                    
                except KeyError:
                    pfile.write('NFS Root Squash Share Permissions Not Listed') 
                    pfile.write("\n")
                    pfile.write("\n")
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
#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('POLICY DATALOCK CONFIGURATION')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
views = glob.glob(source + '/API/*protectionPolicies*.json')

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
            for i in data:
                print("\n")
                print('--------------------------------------')
                try_print('Policy Name:', 'name', i)
                
                print("\n")
                print('~~~~~ Policy Lock Configuration ~~~~~')

                try:           
                    policyLockConfig = (json.dumps(i['datalockConfig']))
                    policyLockConfig = policyLockConfig.replace(',', ', \n')
                    print(policyLockConfig)
                    print("\n")

                except KeyError:
                    print('Not Listed')
                    print("\n")
        except KeyError:
            print('There are no Policies configured on this Cohesity Cluster.')
            print("\n")   


        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('POLICY DATALOCK CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            for i in data:
                pfile.write('--------------------------------------')
                pfile.write("\n")
                try_write('Policy Name:', 'name', i)

                pfile.write("\n")
                pfile.write('~~~~~ Policy Lock Configuration ~~~~~')
                pfile.write("\n")

                try:           
                    policyLockConfig = (json.dumps(i['datalockConfig']))
                    policyLockConfig = policyLockConfig.replace(',', ', \n')
                    pfile.write(policyLockConfig)
                    pfile.write("\n")
                    pfile.write("\n")
                    pfile.write("\n")

                except KeyError:
                    pfile.write('Not Listed')
                    pfile.write("\n")
                    pfile.write("\n")
                    pfile.write("\n")
        except KeyError:
            pfile.write('There are no Policies configured on this Cohesity Cluster.')
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('Policies are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('POLICY DATALOCK CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
 
        pfile.write('Policies are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")
    
pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('FILE DATALOCK CONFIGURATION')
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
                print('--------------------------------------')
                try_print('View Name:', 'name', i)
                try_print('View Datalock Retention Period:', 'dataLockExpiryUsecs', i)

                print("\n")
                print('~~~~~ File Lock Configuration ~~~~~')

                try:           
                    fileLockConfig = (json.dumps(i['fileLockConfig']))
                    fileLockConfig = fileLockConfig.replace(',', ', \n')
                    print(fileLockConfig)
                    print("\n")

                except KeyError:
                    print('Not Listed')
                    print("\n")
        except KeyError:
            print('There are no Views configured on this Cohesity Cluster.')
            print("\n")   


        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('FILE DATALOCK CONFIGURATION')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        try:
            for i in data['views']:
                pfile.write('--------------------------------------')
                pfile.write("\n")
                try_write('View Name:', 'name', i)
                try_write('View Datalock Retention Period:', 'dataLockExpiryUsecs', i)

                pfile.write("\n")
                pfile.write('~~~~~ File Lock Configuration ~~~~~')
                pfile.write("\n")

                try:           
                    fileLockConfig = (json.dumps(i['fileLockConfig']))
                    fileLockConfig = fileLockConfig.replace(',', ', \n')
                    pfile.write(fileLockConfig)
                    pfile.write("\n")
                    pfile.write("\n")
                    pfile.write("\n")

                except KeyError:
                    pfile.write('Not Listed')
                    pfile.write("\n")
                    pfile.write("\n")
                    pfile.write("\n")
        except KeyError:
            pfile.write('There are no Views configured on this Cohesity Cluster.')
            pfile.write("\n")
            pfile.write("\n")

    else:
        print('View/Share Permissions are not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('FILE DATALOCK CONFIGURATION')
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
print('PROTECTION JOB SLA ALERT    Index Reference 48')
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
        pfile.write('PROTECTION JOB SLA ALERT    Index Reference 48')
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
        pfile.write('PROTECTION JOB SLA ALERT    Index Reference 48')
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

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        f = open(x)
        data = json.load(f)

        # print data to screen
        for i in data:
            try_print('Cloud Archive Name:', 'name', i)
            try_print('Cloud Archive Type:', 'externalTargetType', i)
            try_print('Cloud Archive Encryption:', 'encryptionPolicy', i)
            try_print('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            try_print('Encryption Key File was Downloaded:', 'encryptionKeyFileDownloaded', i)
            try_print('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            try_print('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            try_print('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            try:
                print('AWS Cloud Archive Secure Connection Enabled:', json.dumps(i['config']['amazon']['useHttps']))   
            except KeyError:
                print('AWS Cloud Archive Secure Connection Not Listed')
                print("\n")
            try:
                print('Azure Cloud Archive Secure Connection Enabled:', json.dumps(i['config']['azure']['useHttps']))   
            except KeyError:
                print('Azure Cloud Archive Secure Connection Not Listed')
                print("\n")
            try:
                print('S3 Compatible Cloud Archive Secure Connection Enabled:', json.dumps(i['config']['kS3Compatible']['useHttps']))   
                print("\n")
            except KeyError:
                print('S3 Compatible Cloud Archive Secure Connection Not Listed')
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
            try_write('Cloud Archive Type:', 'externalTargetType', i)
            try_write('Cloud Archive Encryption:', 'encryptionPolicy', i)
            try_write('Customer Managed Encryption Keys:', 'customerManagingEncryptionKeys', i)
            try_write('Encryption Key File was Downloaded:', 'encryptionKeyFileDownloaded', i)
            try_write('Cloud Archive Compression Policy:', 'compressionPolicy', i)
            try_write('Cloud Archive Source Side Deduplication:', 'dedupEnabled', i)
            try_write('Cloud Archive Incremental Archive Enabled:', 'incrementalArchivesEnabled', i)
            try:
                pfile.write('Cloud Archive Secure Connection Enabled:')
                pfile.write(json.dumps(i['config']['amazon']['useHttps'])) 
            except KeyError:
                pfile.write('Cloud Cloud Archive Secure Connection Not Listed')
                pfile.write("\n")
            try:
                pfile.write('Azure Cloud Archive Secure Connection Enabled:')
                pfile.write(json.dumps(i['config']['azure']['useHttps']))
            except KeyError:
                pfile.write('Azure Cloud Archive Secure Connection Not Listed')
                pfile.write("\n")
            try:
                pfile.write('S3 Compatible Cloud Archive Secure Connection Enabled:')
                pfile.write(json.dumps(i['config']['kS3Compatible']['useHttps']))   
                pfile.write("\n")
            except KeyError:
                pfile.write('S3 Compatible Cloud Archive Secure Connection Not Listed')
                pfile.write("\n")
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
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY CLUSTER HEALTH')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('NUMBER OF UNRESOLVED ALERTS    Index Reference 84')
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
        pfile.write('NUMBER OF UNRESOLVED ALERTS    Index Reference 84')
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
        pfile.write('NUMBER OF UNRESOLVED ALERTS    Index Reference 84')
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
print('NTP SYNC    Index Reference 85')
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
        pfile.write('NTP SYNC    Index Reference 85')
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
        pfile.write('NTP SYNC    Index Reference 85')
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
print('OVERALL CLUSTER HEALTH AUDIT    Index Reference 86')
print('#---------------------------------------------------------------------------------------------------------------#')

print('***To review the Overall Cluster Health Audit, please reference file: ' + source + '/HC/*-HC_CLI-ALL-*.json***')

# print data to file
pfile = open(param, "a")
pfile.write("\n")
pfile.write("\n")
pfile.write('OVERALL CLUSTER HEALTH AUDIT    Index Reference 86')
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
print('PLATFORM VERSION    Index Reference 30')
print('COHESITY CLUSTER DOMAIN NAMES    Index Reference 8')
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
        try_print('Cohesity Cluster Domain Names:', 'domainNames', data)
        print("\n")

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PLATFORM VERSION    Index Reference 30')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER DOMAIN NAMES    Index Reference 8')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        try_write('Cohesity Cluster Software Version:', 'clusterSoftwareVersion', data)
        try_write('Cohesity Cluster Patch Version:', 'patchVersion', data)
        try_write('Cohesity Cluster Domain Names:', 'domainNames', data)
        pfile.write("\n")

    else:
        print('Cohesity Cluster Software Versioning is not configured for this environment.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('PLATFORM VERSION    Index Reference 30')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER DOMAIN NAMES    Index Reference 8')
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
print('COHESITY CLUSTER CREATION DATE    ')
print('COHESITY CLUSTER HARDWARE    ')
print('COHESITY NODE COUNT    ')
print('#---------------------------------------------------------------------------------------------------------------#')

# load json file
config = glob.glob(source + '/IRIS/*info*.json')

for x in config:

    if os.stat(x).st_size > 5:

        with open(x, "r") as f:
            content = f.read()
            content = content.replace('\n', ' ')
            content = content.replace('}', '} \n')

        creation = "(CLUSTER CREATION TIME         \: (.*?)\, (.*?)\-(.*?)\-(.*?) (.*?)\:(.*?)\:(.*?) (.*?) )"
        model = "(PRODUCT MODEL                 \: (.*?) (.*?) )"
        nodes = "(NODE COUNT                    \: (.*?) )"

        # print data to screen
        print('Cohesity Cluster Creation Date/Time: ')
        try:
            creation_search = re.search(creation, content)
            creation_group = creation_search.group()
            print(creation_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
        print('Cohesity Cluster Hardware: ')
        try:
            model_search = re.search(model, content)
            model_group = model_search.group()
            print(model_group)
            print("\n")
        except AttributeError:
            print('Not Listed')
        print('Cohesity Node Count: ')
        try:
            nodes_search = re.search(nodes, content)
            nodes_group = nodes_search.group()
            print(nodes_group)
            print("\n")
        except AttributeError:
            print('Not Listed')

        # print data to file
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER CREATION DATE    ')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER HARDWARE    ')
        pfile.write("\n")
        pfile.write('COHESITY NODE COUNT    ')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('Cohesity Cluster Creation Date/Time: ')
        try:
            creation_search = re.search(creation, content)
            creation_group = creation_search.group()
            pfile.write(creation_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Cohesity Cluster Hardware: ')
        try:
            model_search = re.search(model, content)
            model_group = model_search.group()
            pfile.write(model_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write('Cohesity Node Count: ')
        try:
            nodes_search = re.search(nodes, content)
            nodes_group = nodes_search.group()
            pfile.write(nodes_group)
            pfile.write("\n")
        except AttributeError:
            pfile.write('Not Listed')
        pfile.write("\n")
        pfile.write("\n")

    else:
        print('Cohesity Creation Date not recorded for this Cohesity Cluster.')
        print("\n")
        
        pfile = open(param, "a")
        pfile.write("\n")
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER CREATION DATE    ')
        pfile.write("\n")
        pfile.write('COHESITY CLUSTER HARDWARE    ')
        pfile.write("\n")
        pfile.write('COHESITY NODE COUNT    ')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")
        pfile.write("\n")

        print('Cohesity Creation Date not recorded for this Cohesity Cluster.')
        pfile.write("\n")
        pfile.write("\n") 

pfile.close()

f.close()


#---------------------------------------------------------------------------------------------------------------#

print("\n")
print("\n")
print('CUSTOM BINARIES    Index Reference 90')
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
        pfile.write('CUSTOM BINARIES    Index Reference 90')
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
        pfile.write('CUSTOM BINARIES    Index Reference 90')
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
print('#---------------------------------------------------------------------------------------------------------------#')
print('COHESITY LOG SETTINGS')
print('#---------------------------------------------------------------------------------------------------------------#')
print("\n")
print("\n")
print('AUDIT LOG RETENTION    Index Reference 89')
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
        pfile.write('AUDIT LOG RETENTION    Index Reference 89')
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
        pfile.write('AUDIT LOG RETENTION    Index Reference 89')
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
print('SMB/NFS AUDIT LOG RETENTION    Index Reference 90')
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
        pfile.write('SMB/NFS AUDIT LOG RETENTION    Index Reference 90')
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
        pfile.write('SMB/NFS AUDIT LOG RETENTION    Index Reference 90')
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
print('SMB/NFS AUDIT LOGGING FOR VIEWS    Index Reference 91')
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
        pfile.write('SMB/NFS AUDIT LOGGING FOR VIEWS    Index Reference 91')
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
        pfile.write('SMB/NFS AUDIT LOGGING FOR VIEWS    Index Reference 91')
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
print('SYSLOG SERVER CONFIGURATION    Index Reference 92')
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
        pfile.write('SYSLOG SERVER CONFIGURATION    Index Reference 92')
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
        pfile.write('SYSLOG SERVER CONFIGURATION    Index Reference 92')
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
print('HELIOS CONNECTIVITY AUDIT    Index Reference 31')
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
        pfile.write('HELIOS CONNECTIVITY AUDIT    Index Reference 31')
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
        pfile.write('HELIOS CONNECTIVITY AUDIT    Index Reference 31')
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
print('MARKETPLACE APPS    ')
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
        pfile.write('MARKETPLACE APPS    ')
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
        pfile.write('MARKETPLACE APPS    ')
        pfile.write("\n")
        pfile.write('#---------------------------------------------------------------------------------------------------------------#')
        pfile.write("\n")

        pfile.write('MarketPlace Apps are not configured for this environment.')
        pfile.write("\n")
        pfile.write("\n")       

pfile.close()

f.close()

#---------------------------------------------------------------------------------------------------------------#
