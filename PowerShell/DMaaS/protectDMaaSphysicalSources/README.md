# Protect DMaaS Physical Sources using PowerShell

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This powershell script registers DMaaS Physical Sources.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'protectDMaaSphysicalSources'
$repoURL = 'https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main'
(Invoke-WebRequest -Uri "$repoUrl/PowerShell/DMaaS/$scriptName/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
# End Download Commands
```

## Components

* protectDMaaSphysicalSources.ps1: the main powershell script

Run the main script like so:

```powershell
./registerDMaasSQLsources.ps1 -apiKey API-KEY -regionId us-east-2 -phylist ./physList.txt -quiesce $false
```

## Parameters

* -apiKey: apiKey generated in DMaaS UI
* -regionId: DMaaS region to use
* -physFQDN: (optional) one or more Physical Source FQDNs (comma separated)
* -phylist: (optional) text file of Physical Source FQDNs (one per line)
* -priority: protection instance priority (default is kMedium)
* -qosPolicy: QoS policy optimizes throughput performance (default is kBackupSSD)
* -abort: abort during blackout periods (default is false)
* -environment: environment type (kPhysical, kVMware, kAWS, kO365, kNetapp, kSQL, kOracle) (default is kPhysical)
* -volumes: which volumes to backup (default is all local drives)
* -autoProtected: whether Physical objects are autoProtected (default is true)
* -skipNested: whether to skip backing up nested volumes (default is false)
* -usePathLevel: whether to use Path Level Skip Nested Volume Setting (default is true)
* -nasSymlink: whether to follow NAS Symlink targets (default is false)
* -quiesce: optional whether to quiesce the backups (Default is true)
* -contOnFail: optional whether to continue on quiesce failure (Default is true)
* -sourceSideDedup = $false,  # optional whether to perform Source Side Deduplication (Default is false)
* -index: optional whether objects are indexed (default is false)
* -skipPhysicalRDMDisks: optional whether to skip backing up Physical RDM Disks (Default is false)
* -startTime: e.g. 23:30 for 11:30 PM (default is 20:00)
* -timeZone: (default 'America/New_York')
* -incSLA: incremental SLA minutes (default is 60)
* -fullSLA: full SLA minutes (default is 120)


## Authenticating to DMaaS

DMaaS uses an API key for authentication. To acquire an API key:

* log onto DMaaS
* click Settings -> access management -> API Keys
* click Add API Key
* enter a name for your key
* click Save

Immediately copy the API key (you only have one chance to copy the key. Once you leave the screen, you can not access it again).
