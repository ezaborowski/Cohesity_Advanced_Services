
# ./registerDMaaSAWSsources.ps1 -apiKey #### -regionId us-east-1 -AWSid ####

# install PowerShell on macOS: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos?view=powershell-7.2
# install AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions
# install AWS CLI for Powershell: https://matthewdavis111.com/aws/deploy-cloudformation-powershell/


# process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$apiKey,  # apiKey
    [Parameter(Mandatory = $True)][string]$regionId,  # DMaaS SQL Source Region Id
    #[Parameter(Mandatory = $True)][string]$saasConn,  # name of SaaS Connection to associate with Physical Source
    [Parameter()][array]$AWSid,  # AWS Account ID
    [Parameter()][string]$AWSlist = ''  # optional textfile of AWS Account Id's to protect

)

# set static variables
$dateString = (get-date).ToString('yyyy-MM-dd')
$outfileName = "$PSScriptRoot\log-registerDMaasAWS-$dateString.txt"
$dest = $PSScriptRoot

# ensure the environment meets the PowerShell Module requirements of 5.1 or above 

write-host "`nValidating PowerShell Version...`n"
Write-Output "`nValidating PowerShell Version...`n" | Out-File -FilePath $outfileName -Append
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    write-host "Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site:" 
    Write-Output "Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site:" | Out-File -FilePath $outfileName -Append
    write-host "https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi" 
    write-output "https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi" | Out-File -FilePath $outfileName -Append
}
else {
    write-host "PowerShell Module is up to date." 
    Write-Output "PowerShell Module is up to date." | Out-File -FilePath $outfileName -Append
}

# gather list of AWS ID's to Register
$AWStoAdd = @()
foreach($AWS in $AWSid){
    $AWStoAdd += $AWS
}
if ('' -ne $AWSlist){
    if(Test-Path -Path $AWSlist -PathType Leaf){
        $AWSid = Get-Content $AWSlist
        foreach($AWS in $AWSid){
            $AWStoAdd += [string]$AWS
        }
    }else{
        Write-Host "`nAWS ID list $AWSlist not found!" -ForegroundColor Yellow 
        Write-Output "`nAWS ID list $AWSlist not found!" | Out-File -FilePath $outfileName -Append 
        exit
    }
}

$AWStoAdd = @($AWStoAdd | Where-Object {$_ -ne ''})

if($AWStoAdd.Count -eq 0){
    Write-Host "`nNo AWS ID's specified!" -ForegroundColor Yellow  
    Write-Output "`nNo AWS ID's specified!" | Out-File -FilePath $outfileName -Append 
    exit
}else{
    Write-Host "`nAWS ID's parsed SUCCESSFULLY!`n" -ForegroundColor Green 
    Write-Output "`nAWS ID's parsed SUCCESSFULLY!`n" | Out-File -FilePath $outfileName -Append 
    write-output $AWStoAdd | Out-File -FilePath $outfileName -Append 
}

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"

# test API Connection
Write-host "`nTesting API Connection...`n" 
Write-Output "`nTesting API Connection...`n" | Out-File -FilePath $outfileName -Append 
$headers.Add("apiKey", "$apiKey")
$apiTest = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/public/mcm/clusters/info' -Method 'GET' -Headers $headers 

if(!$apiTest){
    write-host "`nInvalid API Key" -ForegroundColor Yellow 
    write-output "`nInvalid API Key" | Out-File -FilePath $outfileName -Append 
    exit
}else{
    Write-Host "`nConnection with API Key SUCCESSFUL!`n" -ForegroundColor Green 
    write-output "`nConnection with API Key SUCCESSFUL!`n" | Out-File -FilePath $outfileName -Append 
    write-output $apiTest | Out-File -FilePath $outfileName -Append 
}

# validate DMaaS Tenant ID
Write-host "`nValidating Tenant ID...`n"  
write-output "`nValidating Tenant ID...`n" | Out-File -FilePath $outfileName -Append 
$headers.Add("accept", "application/json, text/plain, */*")
#$headers.Add('content-type: application/json')
$tenant = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/mcm/userInfo' -Method 'GET' -Headers $headers

$tenantId = $tenant.user.profiles.tenantId 
Write-host "`nTenant ID: $tenantId" -ForegroundColor Green 
write-output "`nTenant ID: $tenantId" | Out-File -FilePath $outfileName -Append 


# validate DMaaS Region ID
Write-host "`nValidating Region ID...`n" 
write-output "`nValidating Region ID...`n" | Out-File -FilePath $outfileName -Append 
$region = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/dms/tenants/regions?tenantId=$tenantId" -Method 'GET' -Headers $headers

foreach($regionIds in $region){

    $regionIds = $region.tenantRegionInfoList.regionId

    $compareRegion = Compare-Object -IncludeEqual -ReferenceObject $regionIds -DifferenceObject $regionId -ExcludeDifferent

    if(!$compareRegion){
        write-host "`nThere are no matching Region Ids asssociated with the confirmed Tenant ID." -ForegroundColor Yellow 
        write-output "`nThere are no matching Region Ids asssociated with the confirmed Tenant ID." | Out-File -FilePath $outfileName -Append 
        exit
    }else{
        Write-Host "`nRegion ID: $regionId" -ForegroundColor Green
        write-output "`nRegion ID: $regionId" | Out-File -FilePath $outfileName -Append 
    }

}


# first portion of AWS Registration
$headers.Add("regionId", "$regionId")

foreach($AWSaccount in $AWStoAdd){

    Write-Host "`nPreparing Registration of AWS ID: " $AWSaccount
    write-output "`nPreparing Registration of AWS ID: " $AWSaccount | Out-File -FilePath $outfileName -Append

    # $body = "{
    # `n    `"useCases`": [
    # `n        `"EC2`", 
    # `n        `"RDS`"
    # `n    ],
    # `n    `"tenantId`": `"$tenantId`",
    # `n    `"destinationRegionId`": `"$regionId`",
    # `n    `"awsAccountNumber`": `"$AWSid`"
    # `n}"

    $body = @{
        "useCases" = @(
            "EC2";
            "RDS"
        );        
        "tenantId" = "$tenantId";
        "destinationRegionId" = "$regionId";
        "awsAccountNumber" = "$AWSaccount"
    }


    if($AWSaccount){

        Write-Host "`nSTEP 1 - Registering AWS Account ID $AWSaccount in DMaaS...`n" 
        write-output "`nSTEP 1 - Registering AWS Account ID $AWSaccount in DMaaS...`n" | Out-File -FilePath $outfileName -Append 

        # prepare body of REST API Call
        $bodyJson = $body | ConvertTo-Json 
        write-host "$bodyJson"  
        write-output "$bodyJson" | Out-File -FilePath $outfileName -Append  
        $bodyJson = ConvertTo-Json -Compress -Depth 99 $body 

        # register DMaaS AWS Account - STEP 1
        $response = Invoke-RestMethod 'https://helios.cohesity.com/v2/mcm/dms/tenants/regions/aws-cloud-source' -Method 'POST' -Headers $headers -Body $bodyJson -ContentType 'application/json' 
        $response | ConvertTo-Json
        Write-host "$response" -ForegroundColor Green 
        write-output "$response" | Out-File -FilePath $outfileName -Append

        #---------------------------------------------------------------------------------------------------------------#

        # PULL CFT FROM $response OUTPUT
        # SAVE AS .cft

        #---------------------------------------------------------------------------------------------------------------#

        Write-Host "`nValidating Registration of AWS Account ID $AWSaccount in DMaaS...`n" 
        write-output "`nValidating Registration of AWS Account ID $AWSaccount in DMaaS...`n" | Out-File -FilePath $outfileName -Append 

        # validate STEP 1
        $validation = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/dms/tenants/regions/aws-cloud-source-verify?tenantId=$tenantId&destinationRegionId=$regionId&awsAccountNumber=$AWSaccount" -Method 'GET' -Headers $headers
        $validation | ConvertTo-Json 
        Write-host "$validation" -ForegroundColor Green
        write-output "$validation" | Out-File -FilePath $outfileName -Append
    }

    else{
    Write-Host "`nNo AWS Account ID available to Register!`n" -ForegroundColor Yellow 
    write-output "`nNo AWS Account ID available to Register!`n" | Out-File -FilePath $outfileName -Append 
    }
  }

# #---------------------------------------------------------------------------------------------------------------#

# # final portion of AWS Registration

# $body = @{
#     "environment" = "kAWS";
#     "awsParams" = @(
#         "subscriptionType" = "kAWSCommercial";
#         "standardParams" = @(
#             "authMethodType" = "kUseIAMRole";
#             "iamRoleAwsCredentials" = @(
#                 "iamRoleArn" = "{{iam_role_arn}}";
#                 "cpIamRoleArn" = "{{cp_role_arn}}"
#             )
#         )
#     )
# }

# $response = Invoke-RestMethod 'https://helios.cohesity.com/v2/mcm/data-protect/sources/registrations' -Method 'POST' -Headers $headers -Body $body
# $response | ConvertTo-Json


# $body = @{
#     "useCases" = @(
#         "EC2";
#         "RDS"
#     )
    
#     "tenantId" = "$tenantId";
#     "destinationRegionId" = "$regionId";
#     "awsAccountNumber" = "$AWSid"
# }


# if($AWSaccount){

#     Write-Host "Registering AWS Account ID $AWSid..."

#     $bodyJson = $body | ConvertTo-Json 
#     write-host "$bodyJson"   
#     $bodyJson = ConvertTo-Json -Compress -Depth 99 $body 

#     $response = Invoke-RestMethod 'https://helios.cohesity.com/v2/mcm/dms/tenants/regions/aws-cloud-source' -Method 'POST' -Headers $headers -Body $bodyJson -ContentType 'application/json' 
    
#     $response | ConvertTo-Json

#     $response  
   
#     Write-host "$response"
# }

# else{
# Write-Host "AWS Account ID $AWSid not registered" -ForegroundColor Yellow
# }
# }


