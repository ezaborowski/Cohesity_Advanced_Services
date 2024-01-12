#!/usr/bin/env python

import argparse
import platform
import datetime 
import os
import subprocess
import configparser
from platform import python_version
import sys
import pexpect
from pexpect import *
import tempfile
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-rc', '--agentConfig', type=str, default=None)  # (for internal use only)
parser.add_argument('-p', '--password', type=str, default=None)  # (for internal use only)
parser.add_argument('-rl', '--remoteLogDir', type=str, default=None)  # (for internal use only)
parser.add_argument('-ip', '--ipAddy', type=str, default=None)  # (for internal use only)
parser.add_argument('-in', '--installer', type=str, default=None)  # (for internal use only)
parser.add_argument('-l', '--local', type=bool, default=False)  # (for local use - required) if running this script locally on a Linux box, update to True (default is False)
parser.add_argument('-o', '--systemOS', type=str, default=None)  # (for local use - required) OS Type; ubuntu, debian, suse, powerpc, redhat, linux, aix, solaris
parser.add_argument('-i', '--agentInstaller', type=str, default=None)  # (for local use - required) local path and filename of installer package that correlates with OS specified
parser.add_argument('-u', '--oracleUser', type=str, default=None)  # (for local use - optional) Linux Oracle User (if not installing as root)
parser.add_argument('-g', '--oracleUserGroup', type=str, default=None)  # (for local use - optional) Linux Oracle User Group (if not installing as root)

### Recurring variable statements ###
now = datetime.datetime.now()

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

# argument parsers
args = parser.parse_args()

local = args.local

if(local != True):
    configFilePath = args.agentConfig
    agentConfig = configparser.ConfigParser()
    agentConfig.read(configFilePath)
    
    os = args.systemOS
    ipAddy = args.ipAddy
    installer = args.installer
    remoteLogDir = args.remoteLogDir
    password = args.password
    deployIP=agentConfig.get(f'Server_IPs', 'deployIP')
    rootUser=agentConfig.get(f'Server_IPs', 'rootUser')

    # linux
    scriptInstaller=agentConfig.get(f'Linux', 'scriptInstaller')
    rpmInstaller=agentConfig.get(f'Linux', 'rpmInstaller')
    debianInstaller=agentConfig.get(f'Linux', 'debianInstaller')
    suseInstaller=agentConfig.get(f'Linux', 'suseInstaller')
    powerpcInstaller=agentConfig.get(f'Linux', 'powerpcInstaller')

    lnxCohesityCert=agentConfig.get(f'Linux', 'lnxCohesityCert')
    lnxAgentCertFile=agentConfig.get(f'Linux', 'agentCertFile')
    lnxUserCert=agentConfig.get(f'Linux', 'lnxUserCert')
    lnxRootCAfile=agentConfig.get(f'Linux', 'rootCAfile')
    lnxPrivateKeyFile=agentConfig.get(f'Linux', 'privateKeyFile')
    lnxCertChainFile=agentConfig.get(f'Linux', 'certChainFile')

    linuxOracleUser=agentConfig.get(f'Linux', 'linuxOracleUser')
    linuxOracleGroup=agentConfig.get(f'Linux', 'linuxOracleGroup')

    # aix
    aixInstaller=agentConfig.get(f'AIX', 'aixInstaller')

    aixCohesityCert=agentConfig.get(f'AIX', 'aixCohesityCert')
    aixAgentCertFile=agentConfig.get(f'AIX', 'agentCertFile')
    aixUserCert=agentConfig.get(f'AIX', 'aixUserCert')
    aixRootCAfile=agentConfig.get(f'AIX', 'rootCAfile')
    aixPrivateKeyFile=agentConfig.get(f'AIX', 'privateKeyFile')
    aixCertChainFile=agentConfig.get(f'AIX', 'certChainFile')

    aixOracleUser=agentConfig.get(f'AIX', 'aixOracleUser')
    aixOracleGroup=agentConfig.get(f'AIX', 'aixOracleGroup')

    # solaris
    solarisInstaller=agentConfig.get(f'Solaris', 'solarisInstaller')

    solCohesityCert=agentConfig.get(f'Solaris', 'solarisCohesityCert')
    solAgentCertFile=agentConfig.get(f'Solaris', 'agentCertFile')
    solUserCert=agentConfig.get(f'Solaris', 'solarisUserCert')
    solRootCAfile=agentConfig.get(f'Solaris', 'rootCAfile')
    solPrivateKeyFile=agentConfig.get(f'Solaris', 'privateKeyFile')
    solCertChainFile=agentConfig.get(f'Solaris', 'certChainFile')


    ### INFO Logging
    def info_log(statement):
        print ("\n" + str(get_now()) + f"   | INFO for {ipAddy} |   " + bcolors.OKBLUE + statement + bcolors.ENDC, flush= True)     

    ### SUCCESS Logging
    def pass_log(statement):
        print ("\n" + str(get_now()) + f"   | SUCCESS for {ipAddy} |   " + bcolors.OKGREEN + statement + bcolors.ENDC, flush= True)

    ### WARN Logging
    def warn_log(statement):
        print ("\n" + str(get_now()) + f"   | WARN for {ipAddy} |   " + bcolors.WARNING + statement + bcolors.ENDC, flush= True)

    ### FAIL Logging
    def fail_log(statement):
        print ("\n" + str(get_now()) + f"   | FAIL for {ipAddy} |   " + bcolors.FAIL + statement + bcolors.ENDC, flush= True)
        
elif(local != False):
    os = args.systemOS
    os = os.lower()
    agentInstaller = args.agentInstaller
    oracleUser = args.oracleUser
    oracleUserGroup = args.oracleUserGroup
    
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

yes = "yes"

# functions
def pyVer():
    info_log("Validating Python version...")
    try:
        version = (python_version())
        ver = version.split('.')
        ver = ver[0]
        if(int(ver) < 3):
            warn_log(f"Current Python version: {version}")
            fail_log(f"Python version outdated and requires update from: https://www.python.org/downloads/")
            warn_log("Script now exiting...")
            exit()

        elif(int(ver) >= 3):
            pass_log(f"Current Python version: {version}")
            pass_log(f"Python version is current, but it is always best practice to validate that it is up to date from: https://www.python.org/downloads/")
    except (RuntimeError, TypeError, NameError, ValueError):
        warn_log (f"Failed to verify Python version, please ensure is up to date from: https://www.python.org/downloads/")
        
    return version

# validates installer package exists and is executable
# def checkInstaller(i):
    # failure = False
    # if(i != 'null'):
        # isExists = os.path.exists(i)
        # if isExists != True:
            # fail_log(f"Failed to validate Cohesity Agent Installer accessibility to: {i}")
            # failure = True
        # else:
            # pass_log(f"Validated Cohesity Agent Installer accessibility to: {i}")
            
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
        response = input('Do you want to exit the script in order to resolve the Agent Installer accessibility issue? (Y or N): ')
        response = response.lower()
        if(response != "n"):
            info_log("Script now exiting...")
            exit()
    
    return failure

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
    
    return failure, result

    
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
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
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
            #child.expect('(?i)(yes/no)? ')
            #child.sendline(yes)
            child.expect('(?i)password:')
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
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
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
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
            child.sendline(password)
            child.logfile = scpLog
            child.expect(pexpect.EOF)
            child.close()
            scpLog.close()
            
            fin = open(scpTemp, 'r')
            result = fin.read()
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

# configure linux certs
def lnxCerts():
    if(local != True):
        if(lnxCohesityCert == 'true'):
            info_log("Installing Linux Cohesity Agent Certificate...")
            certOutput, result = catch(f"export ENFORCE_USE_CUSTOM_CERTS=true && export AGENT_CERT_FILE={lnxAgentCertFile}")
            if(certOutput != False):
                fail_log(f"Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()
            else:
                pass_log("Successfully implemented Certificate!")
                return result
        else:
            info_log("Verified no Linux User Certificates specified.")
            result = False
            return result
                    
        if(lnxUserCert == 'true'):
            info_log("Installing Linux Root CA Certificate...")
            rootOutput, result = catch(f"export ENFORCE_USE_CUSTOM_CERTS=true && export USE_THIRD_PARTY_CERTS=true && export ROOT_CA_FILE={lnxRootCAfile}")
            if(rootOutput != False):
                return rootOutput
            
            info_log("Implementing Private Key File...")
            pvtOutput, result = catch(f"export PRIVATE_KEY_FILE={lnxPrivateKeyFile}")
            if(pvtOutput != False):
                return pvtOutput
            
            info_log("Initiating Certificate Chain File...")
            chainOutput, result = catch(f"export CERT_CHAIN_FILE={lnxCertChainFile}")
            if(chainOutput != False):
                return chainOutput
            
            if(rootOutput or pvtOutput or chainOutput != False):
                fail_log("Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()
            else:
                pass_log("Successfully implemented Certificate!")
                return chainOutput
        else:
            info_log("Verified no Linux User Certificates specified.")
            result = False
            return result
        
    else:
        info_log("Verified no Linux User Certificates specified.")
        result = False
        return result

# scp logs back to deployIP
def logs():
    agentLog = glob.glob(f'/tmp/CohesityAgentInstaller/{ipAddy}_deployAgent-*-LOG.txt')
    
    scpOutput, result = scp(deployIP, "fromMe", agentLog, remoteLogDir)

    if(scpOutput != False):
        fail_log(f"Transfer of Local Cohesity Agent Deployment log file to {deployIP} ERROR output: {result}")
        fail_log(f"Local Cohesity Agent Logs for {ipAddy} failed to scp to {deployIP} !")
        warn_log(f"The Cohesity Agent Deployment log file for {ipAddy} can be found locally on {ipAddy} in the following directory: /tmp/CohesityAgentInstaller")
        
        print(f"Transfer of Agent Deployment log file for {ipAddy} ERROR output: {result}")
        print(f"Local Cohesity Agent Logs for {ipAddy} failed to scp to {deployIP} ! The log file for {ipAddy} can be found locally on {ipAddy} in the following directory: /tmp/CohesityAgentInstaller") 
    else:
        pass_log(f"Successful transfer of Local Cohesity Agent Deployment log file to {deployIP} output: {result}")

# start linux agent and scp logs
def startAgent():
    info_log("Attempting to start the Cohesity Agent Service...")
    startOutput, result = catch("sudo /etc/init.d/cohesity-agent start")
    
    info_log("Verifying the status of the Cohesity Agent Service...")
    statusOutput, result = catch("sudo /etc/init.d/cohesity-agent status")
    
    if(local != True):
        logs()
            
    pass_log("Cohesity Linux Agent Deployed!")
    info_log("Script now exiting...")
    exit()

# start aix agent and scp logs
def aixAgent():
    info_log("Attempting to start the Cohesity Agent Service...")
    startOutput, result = catch("/usr/local/cohesity/agent/aix_agent.sh start")
    
    info_log("Verifying the status of the Cohesity Agent Service...")
    statusOutput, result = catch("/usr/local/cohesity/agent/aix_agent.sh status")
    
    if(local != True):
        logs()
    if(statusOutput != True):            
        pass_log("Cohesity Linux Agent Deployed!")
        info_log("Script now exiting...")
        exit() 

# verification if Cohesity Agent Installer exists in path
def exists(path, folder, agent):
    isExists = os.path.exists(path)
    if(isExists != True):
        fail_log(f"Validated Linux Cohesity Agent Installer is not present in {folder} !")
        warn_log(f"Please manually mv or cp {agent} package to {folder} and try again.")
        warn_log(f"Script now exiting...")
        exit()
    else:
        pass_log(f"Verified Linux Cohesity Agent Installer successfully transferred to {path}")

# get Python version and OS flavor
ver = pyVer()



agentDir = '/tmp/CohesityAgentInstall'

if(local != False):
    sysos = platform.system()
    sysos = sysos.lower()
    
    if(f"*{os}*" in sysos):
        pass_log(f"Verified OS: {sysos}")
        os = sysos
    else:
        warn_log(f"User specified OS ({os}) does not match system specified OS: {sysos}")
        warn_log(f"Please specify which OS is correct...")
        
        print("Please select correct OS Cohesity Agent to install: ")
        print(f"1. {os}")
        print(f"2. {sysos}")
        print(f"3. Manually Input OS")
        print(f"4. Exit Script")
        response = input("Please input the number that corresponds with the correct response: ")
        if(response == 1):
            pass_log(f"User Verified OS: {os}")
            os = os
        if(response == 2):
            pass_log(f"User Verified OS: {sysos}")
            os = sysos
        if(response == 3):
            print("Please select correct OS Cohesity Agent to install: ")
            print("1. ubuntu")
            print("2. debian")
            print("3. suse")
            print("4. powerpc")
            print("5. redhat")
            print("6. linux")
            print("7. aix")
            print("8. solaris")
            manual = input("Please input the number that corresponds with the correct OS: ")
            if(manual == 1):
                pass_log(f"User Verified OS: ubuntu")
                os = "ubuntu"
            if(manual == 2):
                pass_log(f"User Verified OS: debian")
                os = "debian"
            if(manual == 3):
                pass_log(f"User Verified OS: suse")
                os = "suse"
            if(manual == 4):
                pass_log(f"User Verified OS: powerpc")
                os = "powerpc"
            if(manual == 5):
                pass_log(f"User Verified OS: redhat")
                os = "redhat"
            if(manual == 6):
                pass_log(f"User Verified OS: linux")
                os = "linux"
            if(manual == 7):
                pass_log(f"User Verified OS: aix")
                os = "aix"
            if(manual == 8):
                pass_log(f"User Verified OS: solaris")
                os = "solaris"
        if(response == 4):
            exitInput = input('Are you sure that you want to exit the script in order to resolve this OS discrepancy? (Y or N): ')
            exitInput = exitInput.lower()
            if(exitInput != "n"):
                warn_log(f"Confirmed Script Exit chosen!")
                info_log("Script now exiting...")
                exit()
    
    # ensuring that Cohesity Agent Installer is in appropriate directory for deployment
    source = agentInstaller.split('/')
    installer = source[-1]
    dirCreate, result = catch("mkdir /tmp")
    dirCreate, result = catch("mkdir /tmp/CohesityAgentInstaller")
    if(dirCreate != True):
        info_log(f"Transferring Linux Cohesity Agent Installer to {agentDir}...")
        mvPackage, result = catch(f"mv {agentInstaller} {agentDir}")
        if(mvPackage != False):
            cpPackage, result = catch(f"cp {agentInstaller} {agentDir}")
        #    exists(agentPath, agentDir, installer)
        #else:
        #    exists(agentPath, agentDir, installer)
                   
else:
    pass_log(f"Verified OS: {os}")
    #os = sysos
    os = str(os)
    rel = platform.release()
    pass_log(f"Verified Release: {rel}")

# platform = platform.platform()

## Linux Agent Deployment (login as root to install)

if('ubuntu' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Ubuntu Cohesity Agent...")
        ubuntuOutput, result = catch(f"sudo ./{installer} -- -i -y")
            
        if(ubuntuOutput != False):
            fail_log(f"Failure during Cohesity Agent Installation: {result}")
            warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
            warn_log("Script now exiting...")
            exit()
        else:
            pass_log(f"Successful Cohesity Agent Installation: {result}")
            startAgent()

elif('debian' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Debian Cohesity Agent...") 
        if(local != True):
            if(linuxOracleUser != 'null'):
                debOutput, result = catch(f"COHESITYUSER={linuxOracleUser} dpkg -i {installer}")
            else:
                debOutput, result = catch(f"dpkg -i {installer}")
        else:
            if(oracleUser):
                debOutput, result = catch(f"COHESITYUSER={oracleUser} dpkg -i {installer}")
            else:
                debOutput, result = catch(f"dpkg -i {installer}")
    
    if(debOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        startAgent()

elif('suse' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Suse Cohesity Agent...")
        if(local != True):
            if(linuxOracleUser != 'null'):
                 suseOutput, result = catch(f"export COHESITYUSER={linuxOracleUser} rpm -i {installer}")
            else:
                suseOutput, result = catch(f"rpm -i {installer}")
        else:
            if(oracleUser):
                suseOutput, result = catch(f"export COHESITYUSER={oracleUser} rpm -i {installer}")
            else:
                suseOutput, result = catch(f"rpm -i {installer}")
        
    if(suseOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        startAgent()

elif('power' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Linux PowerPC Cohesity Agent...")
        if(local != True):
            if(linuxOracleUser != 'null'):
                pwrOutput, result = catch(f"export COHESITYUSER={linuxOracleUser}; rpm -i {installer}")
            else:
                pwrOutput, result = catch(f"rpm -i {installer}")
        else:
            if(oracleUser):
                pwrOutput, result = catch(f"export COHESITYUSER={oracleUser}; rpm -i {installer}")
            else:
                pwrOutput, result = catch(f"rpm -i {installer}")
    
    if(pwrOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        startAgent()

elif('redhat' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing RHEL Cohesity Agent...")
        if(local != True):
            if(linuxOracleUser != 'null'):
                rhelOutput, result = catch(f"export COHESITYUSER={linuxOracleUser}; rpm -i {installer}")
            else:
                rhelOutput, result = catch(f"rpm -i {installer}")
        else:
            if(oracleUser):
                rhelOutput, result = catch(f"export COHESITYUSER={oracleUser}; rpm -i {installer}")
            else:
                rhelOutput, result = catch(f"rpm -i {installer}")
            
    if(rhelOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        startAgent()

elif('linux' in os):
    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    result = lnxCerts()
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Linux Cohesity Agent...")  
        if(local != True):
            if(linuxOracleUser != 'null'):
                if(linuxOracleUser):
                    lnxOutput, result = catch(f"sudo ./{installer} -- --install -S {linuxOracleUser} -G {linuxOracleGroup} -c 1")
                    if(lnxOutput != False):
                        lnxOutput, result = catch(f"sudo ./{installer} -- --install -S {linuxOracleUser} -c 1")
                else:
                    lnxOutput, result = catch(f"sudo ./{installer} -- --install -S root -G root -c 0")
        else:
            if(oracleUser):
                lnxOutput, result = catch(f"sudo ./{installer} -- --install -S {oracleUser} -G {oracleUserGroup} -c 1")
                if(lnxOutput != False):
                    lnxOutput, result = catch(f"sudo ./{installer} -- --install -S {oracleUser} -c 1")
            else:
                lnxOutput, result = catch(f"sudo ./{installer} -- --install -S root -G root -c 0")

    if(lnxOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        startAgent()

## AIX Agent Deployment (login as Oracle root to install)
    # AIX 7.1 TL5, 7.2 TV2+
    # The latest Bash package. For more information, see AIX Toolbox for Linux Applications.
    # Java version, JRE 1.8.0 AIX ppc-64 bit for the agent.
    
elif('aix' in os):   
    if(local != True):
        if(aixCohesityCert == 'true'):
            info_log("Installing AIX Cohesity Agent Certificate...")
            custOutput, result = catch(f"echo ENFORCE_USE_CUSTOM_CERTS=true >> /usr/local/cohesity/set_env.sh")
            certOutput, result = catch(f"echo AGENT_CERT_FILE={aixAgentCertFile} >> /usr/local/cohesity/set_env.sh")
            
            if(custOutput or certOutput != False):
                fail_log("Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()
        else:
            info_log("Verified no AIX Cohesity Certificates specified.")
            
        if(aixUserCert == 'true'):
            info_log("Installing AIX Root CA Certificate...")
            custOutput, result = catch(f"echo ENFORCE_USE_CUSTOM_CERTS=true >> /usr/local/cohesity/set_env.sh")
            thirdOutput, result = catch(f"echo USE_THIRD_PARTY_CERTS=true >> /usr/local/cohesity/set_env.sh")
            rootOutput, result = catch(f"echo ROOT_CA_FILE={aixRootCAfile} >> /usr/local/cohesity/set_env.sh")
            
            info_log("Implementing Private Key File...")
            pvtOutput, result = catch(f"echo PRIVATE_KEY_FILE={aixPrivateKeyFile} >> /usr/local/cohesity/set_env.sh")
            
            info_log("Initiating Certificate Chain File...")
            chainOutput, result = catch(f"echo CERT_CHAIN_FILE={aixCertChainFile} >> /usr/local/cohesity/set_env.sh")
            
            if(custOutput or thirdOutput or rootOutput or pvtOutput or chainOutput != False):
                fail_log("Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()
        else:
            info_log("Verified no AIX User Certificates specified.")

    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing AIX Cohesity Agent...")
        if(local != True):
            if(aixOracleUser != 'null'):
                aixOutput, result = catch(f"sudo install_with_oracle_adapter_support=true install_oracle_adapter_user_name={aixOracleUser}install_oracle_adapter_dba_group_name={aixOracleGroup} installp -ad {installer} all")
            else:
                aixOutput, result = catch(f"sudo install_with_oracle_adapter_support=true installp -ad {installer} all")
        else:
            if(oracleUser):
                aixOutput, result = catch(f"sudo install_with_oracle_adapter_support=true install_oracle_adapter_user_name={oracleUser}install_oracle_adapter_dba_group_name={aixOracleGroup} installp -ad {installer} all")
            else:
                aixOutput, result = catch(f"sudo install_with_oracle_adapter_support=true installp -ad {installer} all")
        
    if(aixOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        aixAgent()

    
## Solaris Agent Deployment (login as root to install)
    # Oracle's latest bash package running on Oracle Solaris 11 or greater on SPARC v9 (64-bit).
    # Java version, JRE 8 for Oracle Solaris SPARC (64 bit) for the agent.

elif('solaris' in os):
    if(local != True):
        if(solCohesityCert == 'true'):
            info_log("Installing Solaris Agent Certificate...")
            custOutput, result = catch(f"echo ENFORCE_USE_CUSTOM_CERTS=true >> /usr/local/cohesity/set_env.sh")
            certOutput, result = catch(f"echo AGENT_CERT_FILE={solAgentCertFile} >> /usr/local/cohesity/set_env.sh")
            
            if(custOutput or certOutput != False):
                fail_log("Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()
                    
        else:
            info_log("Verified no Solaris Cohesity Certificates specified.")
            
        if(solUserCert == 'true'):
            info_log("Installing AIX Root CA Certificate...")
            custOutput, result = catch(f"echo ENFORCE_USE_CUSTOM_CERTS=true >> /usr/local/cohesity/set_env.sh")
            thirdOutput, result = catch(f"echo USE_THIRD_PARTY_CERTS=true >> /usr/local/cohesity/set_env.sh")
            rootOutput, result = catch(f"echo ROOT_CA_FILE={solRootCAfile} >> /usr/local/cohesity/set_env.sh")
            
            info_log("Implementing Private Key File...")
            pvtOutput, result = catch(f"echo PRIVATE_KEY_FILE={solPrivateKeyFile} >> /usr/local/cohesity/set_env.sh")
            
            info_log("Initiating Certificate Chain File...")
            chainOutput, result = catch(f"echo CERT_CHAIN_FILE={solCertChainFile} >> /usr/local/cohesity/set_env.sh")
            
            if(custOutput or thirdOutput or rootOutput or pvtOutput or chainOutput != False):
                fail_log("Failed to implement Certificate! Please resolve issue and try again.")
                warn_log("If manually implementing Certificate, please skip automated Certificate Implementation by updating the agentConfig.txt CohesityCert and UserCert values to: false ")
                warn_log("Script now exiting...")
                exit()                    
        else:
            info_log("Verified no Solaris User Certificates specified.")

    chmodOutput = catch(f"chmod +x {agentDir}/{installer}")
    chDir, result = catch(f"cd {agentDir}")
    if(chDir != True):
        info_log("Installing Solaris Cohesity Agent...")
        solOutput, result = catch(f"sudo /usr/sbin/pkgadd -d {installer}")
        
    if(solOutput != False):
        fail_log(f"Failure during Cohesity Agent Installation: {result}")
        warn_log("Cohesity Agent Installation Error. Please review logs, resolve issue, and try again.")
        warn_log("Script now exiting...")
        exit()
    else:
        pass_log(f"Successful Cohesity Agent Installation: {result}")
        info_log("Attempting to start the Cohesity Agent Service...")
        startOutput, result = catch("/usr/sbin/svcadm enable svc:/application/cohesity-agent:default")
        
        info_log("Verifying the status of the Cohesity Agent Service...")
        statusOutput, result = catch("/usr/bin/svcs -x svc:/application/cohesity-agent:default")
        
        if(local != True):
            logs()
                
        pass_log("Cohesity Linux Agent Deployed!")
        info_log("Script now exiting...")
        exit()
else:
    fail_log("deployLinuxAgent.py script could not determine the correct Cohesity Agent Installer to use!")
    warn_log(f"Please SCP the '{installer}' manually and run the '/tmp/CohesityAgentInstaller/deployLinuxAgent.py' script locally.")
    exit()
    
if(local != True):
    logs()
        
pass_log("Cohesity Linux Agent Deployed!")
info_log("Script now exiting...")
exit()