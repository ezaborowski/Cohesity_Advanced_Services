#---------------------------------------------------------------------------------------------------------------#

This PowerShell script is configured to be a post-script that will trigger an Incremental SQL backup after any currently failed Log backup.

#---------------------------------------------------------------------------------------------------------------#

## Download the script

Run these commands from PowerShell to download the script(s) directly into your current directory:

## Download Commands
```powershell
$scriptName = 'postScript_logchain-break'

$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/tree/main/PowerShell/postScript_logchain-break'

(Invoke-WebRequest -Uri "$repoUrl/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/postScript_wrapper.bat").content | Out-File cohesity-api.ps1; (Get-Content postScript_wrapper.bat) | Set-Content postScript_wrapper.bat
```
#---------------------------------------------------------------------------------------------------------------#

### Components
./postScript_logchain-break.ps1

#---------------------------------------------------------------------------------------------------------------#

To use a this Post-Script:
* -Place the postScript_logchain-break.ps1 and the postScript_wrapper.bat into the C:\Program Files\Cohesity\user_scripts folder on the SQL Server(s) that are contained in a Protection Job
* -Edit the postScript_logchain-break.ps1 variables at the beginning of the script to reflect the Cohesity UI Admin Username and Password, the FQDN of the Cluster, and the SQL Protection Job name
* -Update the Protection Job Settings to include a Post-Script and point it to the Wrapper script at C:\Program Files\Cohesity\user_scripts\postScript_wrapper.bat
* -Run the Protection Job

#---------------------------------------------------------------------------------------------------------------#

## Parameters
* -username: Cohesity local UI admin username
* -password: Cohesity local UI admin password
* -server: Cohesity Cluster hostname or IP address (ex: servername.domain.com or 172.20.1.55)
* -pJob: Cohesity Protection Job Name
