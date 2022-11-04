# Deploy AWS SaaS Connectors using PowerShell

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This powershell script deploys AWS SaaS Connector EC2 Instances to Registered DMaaS AWS Sources.

## Download the script

Run these commands from PowerShell to download the script(s) into your current directory

```powershell
# Download Commands
$scriptName = 'deployAWSsaasConns'
$repoURL = 'https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main/PowerShell/DMaaS/main'
(Invoke-WebRequest -Uri "$repoUrl/PowerShell/DMaaS/$scriptName/$scriptName.ps1").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "$scriptName.ps1"
(Invoke-WebRequest -Uri "$repoUrl/PowerShell/DMaaS/$scriptName/README.md").content | Out-File "$scriptName.ps1"; (Get-Content "$scriptName.ps1") | Set-Content "README.md"
# End Download Commands
```

## Components

* deployAWSsaasConns.ps1: the main powershell script

Run the main script like so:

```powershell
./deployAWSsaasConns.ps1 -apiKey #### -DMaaSregionId us-east-1 -AWSregionId us-east-1 -AWSid #### -subnetId subnet-#### -securityGroupId sg-#### -vpcId vpc-#### -saasNo 2 -AWStags "label=value", "label=value"
```

## Parameters

* -apiKey : apiKey generated in DMaaS UI
* -DMaaSregionId: DMaaS region where AWS is Registered
* -AWSid: AWS Account ID
* -AWSregionId: AWS region where SaaS Connector EC2 Instance will be deployed
* -subnetId: AWS Subnet Identifier
* -securityGroupId: AWS Network Security Group
* -vpcId: AWS VPC Id
* -saasNo: (optional) Number of AWS SaaS Connector EC2 Instances to create
* -AWStags: (optional) AWS SaaS Connector EC2 Instance Tags (comma separated)

## Authenticating to DMaaS

DMaaS uses an API key for authentication. To acquire an API key:

* log onto DMaaS
* click Settings -> access management -> API Keys
* click Add API Key
* enter a name for your key
* click Save

Immediately copy the API key (you only have one chance to copy the key. Once you leave the screen, you can not access it again).
