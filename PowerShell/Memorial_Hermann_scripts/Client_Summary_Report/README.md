# Client Summary Report

Custom Cohesity Report that includes the following Protection Job parameters: Object Name, Total Runs, Successful Runs, Failed Runs, and Success(%).

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'client_summary_report'
$repoURL = 'https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main/PowerShell/Memorial_Hermann_scripts'
(Invoke-WebRequest -Uri "$repoUrl/Client_Summary_Report/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/Client_Summary_Report/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* client_summary_report.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./client_summary_report.ps1 -username myUsername `
                             -vip myCohesityCluster `
                             -password 'myPassword' `

```

## Parameters

* -username: Admin UI username
* -vip: Cohesity Cluster VIP / FQDN
* -password: Admin UI password
