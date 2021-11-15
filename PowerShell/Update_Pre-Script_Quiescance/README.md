#---------------------------------------------------------------------------------------------------------------#

This PowerShell script can set the name of a PreScript for one or multiple Cohesity Protection Jobs, and also enables or disables the Crash Consistency of the backups created.

#---------------------------------------------------------------------------------------------------------------#

## Download the script

Run these commands from PowerShell to download the script(s) directly into your current directory:

## Download Commands
```powershell
$scriptName = 'set-preScript-crashConsistency'

$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/tree/main/PowerShell/Update_Pre-Script_Quiescance'

(Invoke-WebRequest -Uri "$repoUrl/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
```
#---------------------------------------------------------------------------------------------------------------#

### Components
./set-preScript-crashConsistency.ps1

#---------------------------------------------------------------------------------------------------------------#

To use a text file containing the Protection Job names (one per line):
```powershell
./set-preScript-crashConsistency.ps1 -username myusername -password mypassword -cluster mycluster -jobnamefile "C:\Documents\JobNames.txt" -quiesce True -prescript script.bat
```

To use one or more Cohesity Protection Job Names (comma separated):
```powershell
./set-preScript-crashConsistency.ps1 -username myusername -password mypassword -cluster mycluster -jobname jobname1,jobname2 -quiesce True -prescript script.bat
```
#---------------------------------------------------------------------------------------------------------------#

## Parameters
* -username: Cohesity admin username (if using a domain user, ex: domain.com\username)
* -cluster: Cohesity Cluster hostname or IP address (ex: servername.domain.com or 172.20.1.55)
* -quiesce: whether Crash-Consistency should be enabled - True OR False (True=enabled, False=disabled)
* -prescript: PreScript Filename (ex: script.bat, script1.ps1)
* -jobnamefile: (optional) path and filename of the Protection Job Names text file (ex: "C:\Documents\JobNames.txt")
* -jobname: (optional) one or more Cohesity Protection Job Names (comma separated)
