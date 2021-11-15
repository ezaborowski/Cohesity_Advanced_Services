#---------------------------------------------------------------------------------------------------------------#

This PowerShell script can set the password of a Windows Service across one or multiple servers.

#---------------------------------------------------------------------------------------------------------------#

## Download the script

Run these commands from PowerShell to download the script(s) directly into your current directory:

## Download Commands
```powershell
$scriptName = 'update_service_pw'

$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/tree/main/Update_Windows_Service_PW'

(Invoke-WebRequest -Uri "$repoUrl/Update_Pre-Script_Quiescance/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
```
#---------------------------------------------------------------------------------------------------------------#

### Components
./update_service_pw.ps1

#---------------------------------------------------------------------------------------------------------------#

To use a text file containing the Server Hostnames names (one per line):
```powershell
./update_service_pw.ps1 -hostnameFile "text_file_of_server_hostnames.txt" -serviceName CohesityAgent -serviceUser "service_username"
```

To use one Server Hostname:
```powershell
./update_service_pw.ps1 -hostname "hostname_of_server" -serviceName CohesityAgent -serviceUser "service_username"
```
#---------------------------------------------------------------------------------------------------------------#

## Parameters
* -serviceName: Windows Service name (if using for Cohesity Agent Service, input: CohesityAgent)
* -serviceUser: the Windows Service Logon Username (if using a domain user, ex: domain.com\username)
* -hostnameFile: (optional) path and filename of the Server Hostnames text file (ex: "C:\Documents\JobNames.txt")
* -hostname: one Server Hostname which the Service resides on (ex: servername.domain.com or 172.20.1.55)
