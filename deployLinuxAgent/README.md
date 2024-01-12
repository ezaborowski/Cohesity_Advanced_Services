# Deploy the Cohesity Linux Agent

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This script detects OS Platform, updates any custom Certificate configurations, assigns any selected Oracle User and Group designations, and deploys the Cohesity Linux Agent on the following OS's: Linux (Debian, Suse, PowerPC, RHEL, Ubuntu, and all other supported Linux flavors), AIX, and Solaris.


## Prerequisites

On the machine running the deploy.py script (when deploying the Cohesity Agent across multiple remote Linux boxes), ensure the following Python Modules are installed:
* Python3
* pip
* argparse
* datetime 
* configparser
* pexpect


On the machine running the deployLinuxAgent.py script (the Linux box where the Cohesity Agent will be installed), following Python Modules are required:
* Python3
* pip
* argparse
* datetime 
* configparser
* pexpect
*** If deploying the Cohesity Agent remotely, the deploy.py will attempt to install the above modules as long as Python3 and pip are installed on the remote Linux boxes. ***


## Components

* deployLinuxAgent.py: main powershell script that deploys the Cohesity Agent
* deploy.py: powershell script utilized when deploying Cohesity Agent across multiple remote Linux boxes
* agentConfig.txt: Cohesity Agent Configuration settings


Place all files in one folder and run as shown below.

### To Deploy the Cohesity Agent across multiple Remote Linux boxes
Please populate the agentConfig.txt and run the following from a Linux box that has ssh/scp access to all remote Linux boxes:
```bash
python3 deploy.py -c /path/to/agentConfig.txt | tee deployLinuxAgent_LOG.txt
```
### To Deploy the Cohesity Agent Locally on Linux box
```bash
python3 deployLinuxAgent.py -l True -o redhat -i /path/to/agentInstaller | tee deployLinuxAgent_LOG.txt
```

## Parameters (if running deploy.py to update REMOTE Linux)

* -c, --agentConfig: agentConfig.txt path

### Parameters (if running deployLinuxAgent.py LOCALLY)

* -l, --local: (required) if running this script locally on a Linux box, update to True (default is False)
* -o, --os: (required) OS Type; ubuntu, debian, suse, powerpc, redhat, linux, aix, solaris
* -i, --agentInstaller: (required) local path and filename of installer package that correlates with OS specified
* -u, --oracleUser: (optional) Linux Oracle User (if not installing as root)
* -g, --oracleUserGroup: (optional) Linux Oracle User Group (if not installing as root)
