#---------------------------------------------------------------------------------------------------------------#

This PowerShell script prompts the user to set the name of a PreScript for one or multiple Cohesity Protection Jobs, and also enables or disables the Crash Consistency of the backups created.

#---------------------------------------------------------------------------------------------------------------#

## Download the script

Run these commands from PowerShell to download the script(s) directly into your current directory:

## Download Commands
```powershell
$scriptName = 'set-preScript-crashConsistency-prompt'

$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/tree/main/PowerShell/Update_Pre-Script_Quiescance_prompts'

(Invoke-WebRequest -Uri "$repoUrl/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
```
#---------------------------------------------------------------------------------------------------------------#

### Components
./set-preScript-crashConsistency.ps1

#---------------------------------------------------------------------------------------------------------------#

To use a script:
```powershell
./set-preScript-crashConsistency-prompt.ps1
```
