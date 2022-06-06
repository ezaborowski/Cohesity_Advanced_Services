# Client Summary Report

Custom Cohesity Report that includes the following Protection Job parameters: Server, Object Name, Environment, Job Name, JobRun Type, Status, StartTime, and Error.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'failed_objects_last_day'
$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/upload/main/PowerShell/Memorial_Hermann'
(Invoke-WebRequest -Uri "$repoUrl/Failed_Object_LastDay/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/Failed_Object_LastDay/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* failed_objects_last_day.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./failed_objects_last_day.ps1 -username myUsername `
                             -vip myCohesityCluster `
                             -password 'myPassword' `

```

## Parameters

* -username: Admin UI username
* -vip: Cohesity Cluster VIP / FQDN
* -password: Admin UI password
