# Object Summary Report

Custom Cohesity Report that includes the following Protection Job parameters: Object Name, Total Runs, Successful Runs, Failed Runs, and Success(%).

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'objectSummaryPerCluster'
$repoURL = 'https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main/PowerShell/ProtectionSummary'
(Invoke-WebRequest -Uri "$repoUrl/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/cohesity-api.ps1").content | Out-File cohesity-api.ps1; (Get-Content cohesity-api.ps1) | Set-Content cohesity-api.ps1
# End Download Commands
```

## Components

* objectSummaryPerCluster.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together and run the main script like so:

```powershell
./objectSummaryPerCluster.ps1

```

## Parameters
* To be updated in the "param" section of the PowerShell Script itself:

  * -vips: Cohesity Cluster VIP / FQDN (comma separated)  - Required
  * -usernames: Admin UI username (comma separated)       - Required
  * -domains: Admin UI domain (comma separated)           - Required
  * -passwords: Admin UI password (comma separated)       - Optional
  * -apiKeys: Admin UI apiKey (comma separated)           - Optional
  * -skipVersionChk: If set to True, will skip the PowerShell version check (is False by default)
    Example: ./objectSummaryPerCluster.ps1 -skipVersionChk True
