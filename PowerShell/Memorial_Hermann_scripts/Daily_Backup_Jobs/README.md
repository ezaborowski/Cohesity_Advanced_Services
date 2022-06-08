# Daily Backup Jobs Report

Custom Cohesity Report that includes the following Protection Job parameters: Client, Server, Status, Level, Size (Gb), Started, Duration, and Expires.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'daily_backup_jobs_report'
$repoURL = 'https://github.com/ezaborowski/Cohesity_Advanced_Services/upload/main/PowerShell/Memorial_Hermann'
(Invoke-WebRequest -Uri "$repoUrl/Daily_Backup_Jobs/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/Daily_Backup_Jobs/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* daily_backup_jobs_report_v2.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./daily_backup_jobs_report_v2.ps1 -username myUsername `
                             -vip myCohesityCluster `
                             -password 'myPassword' `

```

## Parameters

* -username: Admin UI username
* -vip: Cohesity Cluster VIP / FQDN
* -password: Admin UI password
