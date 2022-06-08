# Three Strike Failure within last 3 days

Custom Cohesity Report that includes the following Protection Job parameters: Object Name, Job Name, and Error Count for Protection Jobs within the last 3 days.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'three_strike_failure_objects'
$repoURL = 'https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main/PowerShell/Memorial_Hermann_scripts'
(Invoke-WebRequest -Uri "$repoUrl/Three_Strike_Failure/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/Three_Strike_Failure/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* failed_objects_last_day.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./three_strike_failure_objects.ps1 -username myUsername `
                             -vip myCohesityCluster `
                             -password 'myPassword' `

```

## Parameters

* -username: Admin UI username
* -vip: Cohesity Cluster VIP / FQDN
* -password: Admin UI password
