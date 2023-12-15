# User Verification for Cohesity Agent Service and SQL Instances

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This script validates that the Cohesity Agent Service Logon User is also a member of the Local Administrators Group and has sysadmin Role privileges in select SQL Instances. 

## Warning

This script can update Windows Server Local Administrators Group members, as well as SQL sysadmin Role members.


## Components

* SqlAgentUserSaCheck.ps1: the main powershell script


To validate Users directly from command line:

```powershell
./SqlAgentUserSaCheck.ps1 -ipList SQLServer\SQLinstance, SQLServer\SQLinstance2
```

To validate Users from .txt file:

```powershell
./SqlAgentUserSaCheck.ps1 -ipFile C:\SQLinstances.txt
```

## Authentication Parameters

* This script must be run by a Windows User that has Administrative Access to each Local SQL Server and the SQL Instances in order to update any erroneous configurations.
* All SQL Instances must be accessible from the Windows Server where the script is being executed.
* At least one of the following variables must be utilized to provide script with IP Addresses/Hostnames and SQL Instances: ipList or ipFile 


## Target Parameters

* -ipList  # (optional) IP Addresses (comma separated - ie: SQLServer\SQLinstance, SQLServer\SQLinstance2)
* -ipFile  # (optional) text file of IP Addresses and corresponding SQL Instances (one per line - in the following format: SQLServer\SQLinstance)

