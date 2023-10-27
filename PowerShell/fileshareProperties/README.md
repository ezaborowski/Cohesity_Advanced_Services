# List View Contents using PowerShell

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This powershell script enumerates the list of files and folders in a FileShare from Helios.

## Components

* fileshareProperties.ps1: the main powershell script
* cohesity-api.ps1: the Cohesity REST API helper module

Place both files in a folder together, then run the script like so:

(if utilizing ApiKey)
```powershell
./fileshareProperties.ps1 -viewName myview -clusterName mycluster -useApiKey
```

## Authentication Parameters

* -vip: (optional) name or IP of Cohesity cluster (defaults to helios.cohesity.com)
* -username: (optional) name of user to connect to Cohesity (defaults to helios)
* -domain: (optional) your AD domain (defaults to local)
* -useApiKey: (optional) use API key for authentication
* -password: (optional) will use cached password or will be prompted
* -mcm: (optional) connect through MCM
* -mfaCode: (optional) TOTP MFA code
* -clusterName: (optional) cluster to connect to when connecting through Helios or MCM

## Other Parameters

* -viewName: name of view to inspect
* -noIndex: (optional) don't use index
* -depth: (optional) stop after X levels deep
* -showFiles: (optional) only show directories if omitted
* -unit: (optional) show sizes in MiB or GiB (default is MiB)


## Authenticating to Helios

Helios uses an API key for authentication. To acquire an API key:

* log onto Helios
* click settings -> access management -> API Keys
* click Add API Key
* enter a name for your key
* click Save

Immediately copy the API key (you only have one chance to copy the key. Once you leave the screen, you can not access it again). When running a Helios compatible script for the first time, you will be prompted for a password. Enter the API key as the password.

If you enter the wrong ApiKey, you can re-enter the password like so:

```powershell
> . .\cohesity-api.ps1
> apiauth -helios -username myusername@mydomain.net -updateApiKey
Enter your password: *********************
```