#!/usr/bin/env python

import argparse
import datetime 
import os
import time
import subprocess
from subprocess import Popen, PIPE
import configparser
from getpass import getpass
import sys
import tempfile
import pexpect
import re
from pexpect import *
from platform import python_version

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--agentConfig', type=str, required=True)  # agentConfig.txt path

### Recurring variable statements ###
now = datetime.datetime.now()
dateString = now.isoformat()

### Logging
class bcolors:
    PINK = '\033[95m'
    PURPLE = '\033[35m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

### Fetching Current date and time
def get_now():
    now = datetime.datetime.now()
    return now

# validate if logs folder exists in current directory and if not, creates subfolder
cwd = os.getcwd()
remoteLogDir = f"{cwd}/remoteLogs"
isExists = os.path.exists(remoteLogDir)
if isExists != True:
    os.mkdir(remoteLogDir)

### INFO Logging
def info_log(statement):
    print ("\n" + str(get_now()) + f"   | INFO |   " + bcolors.OKBLUE + statement + bcolors.ENDC, flush= True)     

### SUCCESS Logging
def pass_log(statement):
    print ("\n" + str(get_now()) + f"   | SUCCESS |   " + bcolors.OKGREEN + statement + bcolors.ENDC, flush= True)

### WARN Logging
def warn_log(statement):
    print ("\n" + str(get_now()) + f"   | WARN |   " + bcolors.WARNING + statement + bcolors.ENDC, flush= True)

### FAIL Logging
def fail_log(statement):
    print ("\n" + str(get_now()) + f"   | FAIL |   " + bcolors.FAIL + statement + bcolors.ENDC, flush= True)

# argument parsers
args = parser.parse_args()

configFilePath = args.agentConfig
agentConfig = configparser.ConfigParser()
agentConfig.read(configFilePath)

deployFile = agentConfig.get(f'File_Mgmt', 'deployLinuxAgentFile')

ipList=agentConfig.get(f'Server_IPs', 'ipList')
deployIP=agentConfig.get(f'Server_IPs', 'deployIP')
rootUser=agentConfig.get(f'Server_IPs', 'rootUser')

# installers
scriptInstaller=agentConfig.get(f'Linux', 'scriptInstaller')
rpmInstaller=agentConfig.get(f'Linux', 'rpmInstaller')
debianInstaller=agentConfig.get(f'Linux', 'debianInstaller')
suseInstaller=agentConfig.get(f'Linux', 'suseInstaller')
powerpcInstaller=agentConfig.get(f'Linux', 'powerpcInstaller')
aixInstaller=agentConfig.get(f'AIX', 'aixInstaller')
solarisInstaller=agentConfig.get(f'Solaris', 'solarisInstaller')

# validation of installer directories
installers = []
installers.append(scriptInstaller)
installers.append(rpmInstaller)
installers.append(debianInstaller)
installers.append(suseInstaller)
installers.append(powerpcInstaller)
installers.append(aixInstaller)
installers.append(solarisInstaller)

for i in installers:
    if(i != 'null'):
        isExists = os.path.exists(i)
        if isExists != True:
            warn_log(f"Failed to validate Cohesity Agent Installer accessibility to: {i}")
            failure = True
        else:
            pass_log(f"Validated Cohesity Agent Installer accessibility to: {i}")
            
            # is_exec = os.access(i, os.X_OK)
            # if(is_exec != True and i == scriptInstaller):
                # try:
                    # exec_cmd = f"chmod +x {i}"
                    # exec_output = subprocess.getoutput(exec_cmd)
                    # pass_log(f"Successfully updated Cohesity Linux Agent to executable: {exec_output}")
                # except(RuntimeError, TypeError, NameError, ValueError):
                    # fail_log (f"Failed to update Cohesity Linux Agent to executable: {exec_output}")
            # else:
                # info_log(f"Cohesity Agent Installer confirmed executable: {i}")
        
# ask user if they want to exit script to resolve issue
if(failure != False):
    raw_input = input
    warn_log(f"This issue can occur on certain OS, and does not necessarily denote an incorrect pathname.")
    response = input('Do you want to exit the script in order to resolve the Agent Installer accessibility issue? (Y or N): ')
    response = response.lower()
    if(response != "n"):
        info_log("Script now exiting...")
        exit()

# get linux root level user password
if(rootUser):
    password = getpass(f"Please input password for Service User {rootUser}: ")
    user = True
else:
    fail_log(f"No root user has been defined in the {configFilePath}!")
    warn_log(f"Please define a Root/Admin level username present on all boxes and try again.")
    warn_log("Script now exiting...")
    exit()
yes = "yes"

# shell syntax
def catch(cmd):
    failure = False
    try:
        command = cmd
        cmd_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        result = cmd_output.stdout.decode()
        pass_log(f"Success: {cmd_output.stdout.decode()}")

    except subprocess.CalledProcessError as e:
        print(f"Failure: Command {e.cmd} failed with error {e.returncode}")
        result = e.returncode
        failure = True
    
    return failure

# validating IPs using regular expression
def validateIp(address):
    match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", address)
    if bool(match) is False:
        return False
    for part in address.split("."):
        if int(part) < 0 or int(part) > 255:
            return False
    if address == 0:
        return False
    return True  

# scp function
def scp(ip, direction, origin, dest):
    # package = origin.split('/')
    # installer = package[-1]
    failure = False
    scpTemp = tempfile.mktemp()
    scpLog = open(scpTemp, 'w')
    
    
    if(direction == "toMe"):
        try:
            scp_cmd = 'scp %s@%s:%s %s' % (rootUser, ip, origin, dest)
            child = pexpect.spawnu(scp_cmd, timeout=30)
            child.expect('(?i)(yes/no)?')
            child.sendline(yes)
            child.expect('(?i)password:')
            #time.sleep(4)
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
            result = result.replace(password, '')
            fin.close()
            
            if(0 != child.exitstatus):
                #raise Exception(stdout) 
                if("100%" in result):
                    failure = False
                    pass_log(result)
                else:
                    failure = True
                    fail_log(result)
            else:
                failure = False
                pass_log(result)
                
        except TIMEOUT:    
            scp_cmd = 'scp %s@%s:%s %s' % (rootUser, ip, origin, dest)
            child = pexpect.spawnu(scp_cmd, timeout=60)
            #child.expect('(?i)(yes/no)?')
            #child.sendline(yes)
            child.expect('(?i)password:')
            #time.sleep(4)
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
            result = result.replace(password, '')
            fin.close()
            
            if(0 != child.exitstatus):
                #raise Exception(stdout) 
                if("100%" in result):
                    failure = False
                    pass_log(result)
                else:
                    failure = True
                    fail_log(result)
            else:
                failure = False
                pass_log(result)
         
    elif(direction == "fromMe"):
        try:
            scp_cmd = 'scp %s %s@%s:%s' % (origin, rootUser, ip, dest)
            child = pexpect.spawnu(scp_cmd, timeout=30)
            child.expect('(?i)(yes/no)?')
            child.sendline(yes)
            child.expect('(?i)password:')
            #time.sleep(4)
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
            result = result.replace(password, '')
            fin.close()
            
            if(0 != child.exitstatus):
                #raise Exception(stdout) 
                if("100%" in result):
                    failure = False
                    pass_log(result)
                else:
                    failure = True
                    fail_log(result)
            else:
                failure = False
                pass_log(result)
                
        except TIMEOUT:
            scp_cmd = 'scp %s %s@%s:%s' % (origin, rootUser, ip, dest)
            child = pexpect.spawnu(scp_cmd, timeout=120)
            #child.expect('(?i)(yes/no)?')
            #child.sendline(yes)
            child.expect('(?i)password:')
            #time.sleep(4)
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
            result = result.replace(password, '')
            fin.close()
            
            if(0 != child.exitstatus):
                #raise Exception(stdout) 
                if("100%" in result):
                    failure = False
                    pass_log(result)
                else:
                    failure = True
                    fail_log(result)
            else:
                failure = False
                pass_log(result)
     
    return failure, result

# sshdeploy function
def sshdeploy(ip, cmd):
    failure = False
    if(rootUser):
        sshTemp = tempfile.mktemp()
        sshLog = open(sshTemp, 'w') 
        
        options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
        ssh_cmd = 'ssh %s@%s %s "%s"' % (rootUser, ip, options, cmd)
        child = pexpect.spawnu(ssh_cmd, timeout=240)
        child.expect('(?i)password:')
        child.sendline(password)
        child.expect('SCP Password:')
        child.sendline(password)
        child.logfile = sshLog
        child.expect(pexpect.EOF)
        child.close()
        sshLog.close()
        
        fin = open(sshTemp, 'r')
        result = fin.read()
        result = result.replace(password, '')
        fin.close()
        
        if(0 != child.exitstatus or 'error' in result):
            #raise Exception(stdout) 
            if("File exists" in result):
                failure = False
                warn_log(result)
            else:
                failure = True
                fail_log(result)
        else:
            failure = False
            pass_log(result)
            
    return failure, result
    
# ssh function
def ssh(ip, cmd):
    failure = False
    if(rootUser):
        sshTemp = tempfile.mktemp()
        sshLog = open(sshTemp, 'w') 
        
        options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
        ssh_cmd = 'ssh %s@%s %s "%s"' % (rootUser, ip, options, cmd)
        child = pexpect.spawnu(ssh_cmd, timeout=240)
        child.expect('(?i)password:')
        child.sendline(password)
        child.logfile = sshLog
        child.expect(pexpect.EOF)
        child.close()
        sshLog.close()
        
        fin = open(sshTemp, 'r')
        result = fin.read()
        result = result.replace(password, '')
        fin.close()
        
        if(0 != child.exitstatus):
            #raise Exception(stdout) 
            if("File exists" in result):
                failure = False
                warn_log(result)
            else:
                failure = True
                fail_log(result)
        else:
            failure = False
            pass_log(result)
            
    else:
        try:
            ssh_output = subprocess.Popen(["ssh", ip, cmd], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pass_log(f"Success: {ssh_output}")
            
            result = ssh_output.stdout.readlines()
            if result == []:
                error = ssh_output.stderr.readlines()
                #print >>sys.stderr, "ERROR: %s" % error
                fail_log(sys.stderr, "ERROR: %s" % error)
                failure = True
            else:
                #print >>sys.stdout, "STANDARD OUTPUT: %s" % result
                pass_log(sys.stdout, "STANDARD OUTPUT: %s" % result)
                failure = False
        except(RuntimeError, TypeError, NameError, ValueError):
            fail_log(f"Failure: {ssh_output}")
            failure = True
        
    return failure, result

# pull/parse python version
def pyVer(version):
    info_log("Validating Python version...")
    ver = version.split(' ')
    ver = ver[1]
    ver = ver.split('.')
    ver = ver[0]
    if(int(ver) >= 3):
        pyVersion = True
        pass_log(f"Current Python version: {version}")
        pass_log(f"Python version is current, but it is always best practice to validate that it is up to date from: https://www.python.org/downloads/")
    else:
        pyVersion = False
        warn_log(f"Current Python version: {version}")
        fail_log(f"Python version outdated and requires update from: https://www.python.org/downloads/")
        warn_log("Script now exiting...")
        exit()
        
    return pyVersion

# extrapolating Linux flavor and transmitting appropriate Cohesity Agent Installer
def flavor(flav, ip):
    failure = False
    flav = flav.lower()
    if('rhel' in flav):
        sysos = "redhat"
        source = rpmInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is RHEL")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", rpmInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity RHEL Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('ubuntu' in flav):
        sysos = "ubuntu"
        source = scriptInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is Ubuntu")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", scriptInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity Ubuntu Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('linux' in flav):
        sysos = "linux"
        source = scriptInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is Linux")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", scriptInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity Linux Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('sles' in flav):
        sysos = "suse"
        source = suseInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is Suse")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", suseInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity Suse Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('deb' in flav):
        sysos = "debian"
        source = debianInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is Debian")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", debianInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity Debian Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('aix' in flav):
        sysos = "aix"
        source = aixInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is AIX")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", aixInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity AIX Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('solaris' in flav):
        sysos = "solaris"
        source = solarisInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is Solaris")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", solarisInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity Solaris Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
    if('power' in flav):
        sysos = "powerpc"
        source = powerpcInstaller.split('/')
        installer = source[-1]
        info_log(f"Validated Linux flavor on {ip} is PowerPC")
        info_log(f"Transferring {installer} to /tmp/CohesityAgentInstall on remote Linux box {ip}...")
        scpOutput, result = scp(ip, "fromMe", powerpcInstaller, f"/tmp/CohesityAgentInstall/{installer}")
        if(scpOutput != False):
            fail_log(f"SCP of the Cohesity PowerPC Agent Installer to remote Linux box {ip} failed!")
            warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
            failure = True
            
    return failure, sysos, installer    

# parsing IPs
linuxIpList = [e.strip() for e in ipList.split(',')]
validIpList = []
invalidIpList = []
info_log(f"Validating Remote Linux box IP's...")
for x in range(len(linuxIpList)):
    validateIpList = validateIp(linuxIpList[x])
    if not validateIpList:
        fail_log(f"IP Address {(linuxIpList[x])} is invalid and will not be accessed during this run!")
        warn_log(f"Please resolve the aforementioned IP address in the agentConfig.txt and run this script again.")
        invalidIpList.append(linuxIpList[x]) 
    else:
        pass_log(f"Validated IP Address {(linuxIpList[x])} successfully!")
        validIpList.append(linuxIpList[x]) 
errorIps = ()
# iterate through Server IPs and install Cohesity Agent
for ip in validIpList:
    info_log(f"LOGGING INTO LINUX: {ip}")
    info_log(f"Creating '/tmp/CohesityAgentInstall' directory on remote Linux box {ip}...")
    sshOutput, result = ssh(ip, "mkdir /tmp")
    sshOutput, result = ssh(ip, "mkdir /tmp/CohesityAgentInstall")
    if(sshOutput != True):
        #pass_log(f"Remote Linux box {ip} SUCCESSFUL output: {result}")
        info_log(f"Validating Linux flavor and sending appropriate Cohesity Agent Installer to remote Linux box {ip}...")
        sshOutput, result = ssh(ip, "cat /etc/os-release | grep ID= | grep 'rhel\|ubuntu\|linux\|sles\|deb\|power\|aix\|solaris'")
        flavOutput, sysos, installer = flavor(result, ip)
        if(flavOutput != True):
            #pass_log(f"Remote Linux box {ip} SUCCESSFUL output: {result}")
            info_log(f"Transferring {deployFile} and {configFilePath} to remote Linux box {ip}...")
            scpOutput, result = scp(ip, "fromMe", deployFile, "/tmp/CohesityAgentInstall/deployLinuxAgent.py")
            scpOutput1, result = scp(ip, "fromMe", configFilePath, "/tmp/CohesityAgentInstall/agentConfig.txt")
            if(scpOutput !=True and scpOutput1 != True):
                #pass_log(f"Remote Linux box {ip} SUCCESSFUL output: {result}")
                info_log(f"Validating Python version installed on remote Linux box {ip}...")
                sshOutput, result = ssh(ip, "python3 -V")
                if(sshOutput != True):
                    pyVersion = pyVer(result)
                    if(pyVersion):
                        info_log(f"Validating that all necessary Python Modules are installed on remote Linux box {ip}...")
                        sshOutput, result = ssh(ip, "pip install argparse")
                        sshOutput1, result = ssh(ip, "pip install datetime")
                        sshOutput2, result = ssh(ip, "pip install configparser")
                        sshOutput3, result = ssh(ip, "pip install pexpect")
                        
                        if(sshOutput or sshOutput1 or sshOutput2 or sshOutput3 != False):
                            fail_log(f"Could not validate if all necessary Python Modules are implemented on Remote Linux box {ip}!")
                            warn_log(f"Please ensure the following Python Modules are installed on all remote Linux boxes: argparse, datetime, conifgparser, pexpect.")
                            
                        info_log(f"Running deployLinuxAgent Script on Remote Linux box {ip}...")
                        #remotePass = r"{}".format(password)
                        sshOutput, result = sshdeploy(ip, f"python3 /tmp/CohesityAgentInstall/deployLinuxAgent.py -rl {remoteLogDir} -in {installer} -o '{sysos}' -rc '/tmp/CohesityAgentInstall/agentConfig.txt' -ip {ip} > /tmp/CohesityAgentInstall/{ip}_deployAgent-{dateString}-LOG.txt")
                        if(sshOutput != True):
                            #pass_log(f"Remote Linux box {ip} SUCCESSFUL output: {result}")
                            pass_log(f"Cohesity Linux Agent successfully deployed on Linux box {ip}!")
                        else: 
                            #fail_log(f"Remote Linux box {ip} ERROR output: {result}")
                            fail_log(f"Failed to remotely run deployLinuxAgent Script on Remote Linux box {ip}!")
                            warn_log(f"Please log into {ip} directly and use the following command to run the script:\n python3 /tmp/CohesityAgentInstall/deployLinuxAgent.py > /tmp/CohesityAgentInstall/{ip}-deployAgent-LOG.txt")
                else:
                    #fail_log(f"Remote Linux box {ip} ERROR output: {result}")
                    fail_log(f"Failed to remotely retrieve Python version on Remote Linux box {ip}!")
                    warn_log(f"Please ensure Python is up to date from: https://www.python.org/downloads/")
            else:
                #fail_log(f"Remote Linux box {ip} ERROR output: {result}")
                errorIps.append(ip)
                fail_log(f"Failed to transfer files needed to install Cohesity Agent to remote Linux box {ip}!")
                warn_log(f"Please run the deployLinuxAgent.py script manually on remote Linux box {ip}")
                warn_log("Moving on to next remote Linux box...")
                break
        else:
            errorIps.append(ip)
            warn_log("Moving on to next remote Linux box...")
            break
    else:
        #fail_log(f"Remote Linux box {ip} ERROR output: {result}")
        errorIps.append(ip)
        fail_log(f"Failed to create directory '/tmp/CohesityAgentInstall' on remote Linux box {ip}!")
        warn_log(f"Please run the deployLinuxAgent.py script manually on Remote Linux box {ip}")
        warn_log("Moving on to next remote Linux box...")
        break
if(errorIps):     
    warn_log(f"The following are the IP addresses of those remote Linux boxes that encountered errors during the deployment phase and require a manual run of the deployLinuxAgent.py script locally: \n{errorIps}")
    
info_log(f"Cohesity Linux Agent Deploy script has completed iterating through all Remote Linux boxes found in {configFilePath} under the File_Mgmt > ipList section.")