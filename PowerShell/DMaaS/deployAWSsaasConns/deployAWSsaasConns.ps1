
# ./deployAWSsaasConns.ps1 -apiKey #### -DMaaSregionId us-east-1 -AWSregionId us-east-1 -AWSid #### -subnetId subnet-#### -securityGroupId sg-#### -vpcId vpc-#### -saasNo 2 -AWStags label=value, label=value

# install PowerShell, if on macOS: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos?view=powershell-7.2
# upgrade PowerShell Module to current revision of 7.2.4: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi


# process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$apiKey,  # apiKey generated in DMaaS UI
    [Parameter(Mandatory = $True)][string]$DMaaSregionId,  # DMaaS region where AWS is Registered
    [Parameter(Mandatory = $True)][string]$AWSid,  # AWS Account ID
    [Parameter(Mandatory = $True)][string]$AWSregionId,  # AWS region where SaaS Connector EC2 Instance will be deployed 
    [Parameter(Mandatory = $True)][string]$subnetId,  # AWS Subnet Identifier
    [Parameter(Mandatory = $True)][string]$securityGroupId,  # AWS Network Security Group
    [Parameter(Mandatory = $True)][string]$vpcId,  # AWS VPC Id
    [Parameter()][int]$saasNo = 1,  # (optional) Number of AWS SaaS Connector EC2 Instances to create
    [Parameter()][string]$AWStags  # (optional) AWS SaaS Connector EC2 Instance Tags (comma separated)

)

# set static variables
$dateString = (get-date).ToString('yyyy-MM-dd')
$dateTime = Get-Date -Format "dddd MM/dd/yyyy HH:mm"
$outfileName = "$PSScriptRoot\log-deployAWSsaasConns-$dateString.txt"

# ensure the environment meets the PowerShell Module requirements of 5.1 or above 

write-host "`nValidating PowerShell Version...`n"
Write-Output "`n$dateTime    INFO    Validating PowerShell Version...`n" | Out-File -FilePath $outfileName -Append
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    write-host "`nPlease upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site: `nhttps://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi" 
    Write-Output "`n$dateTime    WARN    Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site: `nhttps://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi" | Out-File -FilePath $outfileName -Append
}
else {
    write-host "PowerShell Module is up to date." 
    Write-Output "$dateTime    INFO    PowerShell Module is up to date." | Out-File -FilePath $outfileName -Append
}


# test API Connection
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"

Write-host "`nTesting API Connection...`n" 
Write-Output "`n$dateTime    INFO    Testing API Connection...`n" | Out-File -FilePath $outfileName -Append 
$headers.Add("apiKey", "$apiKey")
$apiTest = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/public/mcm/clusters/info' -Method 'GET' -Headers $headers 

if(!$apiTest){
    write-host "`nInvalid API Key" -ForegroundColor Yellow 
    write-output "`n$dateTime    WARN    Invalid API Key" | Out-File -FilePath $outfileName -Append 
    exit
}else{
    Write-Host "`nConnection with apiKey SUCCESSFUL!`n" -ForegroundColor Green 
    write-output "`n$dateTime    INFO    Connection with apiKey SUCCESSFUL!`n" | Out-File -FilePath $outfileName -Append 
    write-output $apiTest | Out-File -FilePath $outfileName -Append 
}

# validate DMaaS Tenant ID
Write-host "`nValidating Tenant ID...`n"  
write-output "`n$dateTime    INFO    Validating Tenant ID...`n" | Out-File -FilePath $outfileName -Append 
$headers.Add("accept", "application/json, text/plain, */*")
#$headers.Add('content-type: application/json')
$tenant = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/mcm/userInfo' -Method 'GET' -Headers $headers

$tenantId = $tenant.user.profiles.tenantId 

if(!$tenantId){
    write-host "`nNo DMaaS Tenant ID found!" -ForegroundColor Yellow
    write-output "`n$dateTime    WARN    No DMaaS Tenant ID found!" | out-file -filepath $outfileName -Append
}
else{
    Write-host "`nTenant ID: $tenantId" -ForegroundColor Green 
    write-output "`n$dateTime    INFO    Tenant ID: $tenantId" | Out-File -FilePath $outfileName -Append 
}



# validate DMaaS Region ID
Write-host "`nValidating DMaaS Region ID...`n" 
write-output "`n$dateTime    INFO    Validating DMaaS Region ID...`n" | Out-File -FilePath $outfileName -Append 
$region = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/dms/tenants/regions?tenantId=$tenantId" -Method 'GET' -Headers $headers

foreach($DMaasregionIds in $region){

    $DMaasregionIds = $region.tenantRegionInfoList.regionId

    $compareRegion = Compare-Object -IncludeEqual -ReferenceObject $DMaasregionIds -DifferenceObject $DMaasregionId -ExcludeDifferent

    if(!$compareRegion){
        write-host "`nThere are no matching DMaaS Region Ids asssociated with the specified Tenant ID!" -ForegroundColor Yellow 
        write-output "`n$dateTime    WARN    There are no matching DMaaS Region Ids asssociated with the specified Tenant ID!" | Out-File -FilePath $outfileName -Append 
        exit
    }else{
        Write-Host "`nDMaaS Region ID: $DMaasregionId" -ForegroundColor Green
        write-output "`n$dateTime    INFO    DMaaS Region ID: $DMaasregionId" | Out-File -FilePath $outfileName -Append 
    }

}


# create Payload for DMaaS API call
$headers.Add("regionId", "$DMaasregionId")


if($AWSid){
    Write-Host "`nPreparing DMaaS AWS SaaS Connection data for AWS ID: " $AWSid
    write-output "`n$dateTime    INFO    Preparing DMaaS AWS SaaS Connection data for AWS ID: " $AWSid | Out-File -FilePath $outfileName -Append
    
    $body = @{
        "tenantId" = " $tenantId";
        "connectorType" = " AWS";
        "useCase" = " Ec2Backup";
        "name" = " $AWSid-$AWSregionId-$DMaaSregionId";
        "numberOfRigels" = $saasNo;
        "regionId" = "$DMaasregionId";
        "rigelCloudInfraInfo" = @{
            "awsRigelInfraInfo" = @{
                "accountNumber" = " $AWSid";
                "regionId" = " $AWSregionId";
                "subnetId" = " $subnetId";
                "securityGroupId" = " $securityGroupId";
                "vpcId" = " $vpcId";
                "tags" = @(
                    {
                    "$AWStags"
                    }
                )
            }
        }
    }

    #$body = "{`n    `"tenantId`": `"{{tenantId}}`",`n    `"connectorType`": `"AWS`",`n    `"useCase`": `"Ec2Backup`",`n    `"name`": `"{{accountId}}-{{rigelRegionId}}-{{regionId}}`",`n    `"numberOfRigels`": 1,`n    `"regionId`": `"{{regionId}}`",`n    `"rigelCloudInfraInfo`": {`n        `"awsRigelInfraInfo`": {`n            `"accountNumber`": `"{{accountNumber}}`",`n            `"regionId`": `"{{rigelRegionId}}`",`n            `"subnetId`": `"{{subnetId}}`",`n            `"securityGroupId`": `"{{sgId}}`",`n            `"vpcId`": `"{{vpcId}}`",`n            `"tags`": []`n        }`n    }`n}"


    Write-Host "`nDeploying DMaaS SaaS Connection for AWS Account ID $AWSaccount...`n" 
    write-output "`n$dateTime    INFO    Deploying DMaaS SaaS Connection for AWS Account ID $AWSaccount...`n" | Out-File -FilePath $outfileName -Append     

    # prepare body of REST API Call
    $bodyJson = $body | ConvertTo-Json 
    write-host "`nDeployment of DMaaS SaaS Connection for AWS API Payload: `n$bodyJson"  
    write-output "`n$dateTime    INFO    Deployment of DMaaS SaaS Connection for AWS API Payload: `n$bodyJson" | Out-File -FilePath $outfileName -Append  

    Write-Host "`n*****Launching SaaS Connection in your selected subnets. This could take a few minutes.*****`n" 
    write-output "`n$dateTime    INFO    *****Launching SaaS Connection in your selected subnets. This could take a few minutes.*****`n" | Out-File -FilePath $outfileName -Append 

    $bodyJson = ConvertTo-Json -Compress -Depth 99 $body 

    # deploy AWS SaaS Connection
    $response = Invoke-RestMethod 'https://helios.cohesity.com/v2/mcm/rigelmgmt/rigel-groups' -Method 'POST' -Headers $headers -Body $bodyJson -ContentType 'application/json' 
    $response | ConvertTo-Json
    # Write-host "$response" -ForegroundColor Green 
    write-output "$dateTime    INFO    Response from Deployment of DMaaS SaaS Connection for AWS API Payload:  API: `n$response" | Out-File -FilePath $outfileName -Append

        if($response){
            Write-host "`nDeployment of SaaS Connection in AWS Accouut ID $AWSaccount SUCCESSFUL!`n" -ForegroundColor Green
            write-output "`n$dateTime    INFO    Deployment of SaaS Connection in AWS Accouut ID $AWSaccount SUCCESSFUL!`n"  | Out-File -FilePath $outfileName -Append
        }

        else{
            Write-host "`nDeployment of SaaS Connection in AWS Accouut ID $AWSaccount UNSUCCESSFUL!`n" -ForegroundColor Red 
            write-output "`n$dateTime    WARN    Deployment of SaaS Connection in AWS Accouut ID $AWSaccount UNSUCCESSFUL!`n"  | Out-File -FilePath $outfileName -Append
        }

    }
    else {
        write-host "`nNo valid AWS Account ID' provided!`n" -ForegroundColor Yellow
        write-output "`n$dateTime    WARN    No valid AWS Account ID' provided!`n" | Out-File -FilePath $outfileName -Append 
    }
