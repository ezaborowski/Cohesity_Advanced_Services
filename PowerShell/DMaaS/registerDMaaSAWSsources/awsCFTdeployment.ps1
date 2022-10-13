
# ./awsCFTdeployment.ps1 -roleARN #### -session Test_Session -regionId us-east-1

# install PowerShell on macOS: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-macos?view=powershell-7.2
# install AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions
# install AWS CLI for Powershell: https://matthewdavis111.com/aws/deploy-cloudformation-powershell/


# process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$roleARN,  # AWS ARN associated with CFT Deployment IAM Role
    [Parameter(Mandatory = $True)][string]$session,  # Name identifier of AWS Session
    [Parameter(Mandatory = $True)][string]$regionId,  # DMaaS SQL Source Region Id
    [Parameter(Mandatory = $True)][string]$cftTemplate  # Filename of CFT Template located in CFT folder in root folder of script
    # [Parameter(Mandatory = $True)][string]$saasConn,  # name of SaaS Connection to associate with Physical Source
    # [Parameter()][array]$AWSid,  # AWS Account ID
    # [Parameter()][string]$AWSlist = ''  # optional textfile of AWS Account Id's to protect

)

$cftFolder = "CFT"

    if (Test-Path $PSScriptRoot\$cftFolder) {
    
        Write-Host "`nCFT Folder Exists`n"
        write-output "`nCFT Folder Exists`n" | Out-File -FilePath $outfileName -Append 
    }
    else {
    
        #PowerShell Create directory if not exists
        New-Item $cftFolder -ItemType Directory
        Write-Host "`nCFT Folder Created SUCCESSFULLY!`n" -ForegroundColor Green 
        write-output "`nCFT Folder Created SUCCESSFULLY!`n" | Out-File -FilePath $outfileName -Append 
    }

$cftLocation = "$PSScriptRoot\$cftFolder\$cftTemplate"
$dateString = (get-date).ToString('yyyy-MM-dd')
$outfileName = "$PSScriptRoot\log-deployDMaaScft-$dateString.txt"
$template = Get-Content -Path $cftLocation -Raw

# https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html
# https://docs.aws.amazon.com/powershell/latest/reference/items/Use-STSRole.html

# Set-AWSCredentials -AccessKey AKIAIOSFODNN7EXAMPLE -SecretKey wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY -StoreAs MyMainUserProfile
# Initialize-AWSDefaults -ProfileName MyMainUserProfile -Region us-west-2

$Creds = (Use-STSRole -RoleArn "$roleARN" -RoleSessionName "$session").Credentials
    # need to provide credentials from an IAM User to call that function

    # $Creds.AccessKeyId
    # AKIAIOSFODNN7EXAMPLE

    # $Creds.SecretAccessKey
    # wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    # $Creds.SessionToken
    # AQoDYXdzEGcaEXAMPLE2gsYULo+Im5ZEXAMPLEeYjs1M2FUIgIJx9tQqNMBEXAMPLECvSRyh0FW7jEXAMPLEW+vE/7s1HRp
    # XviG7b+qYf4nD00EXAMPLEmj4wxS04L/uZEXAMPLECihzFB5lTYLto9dyBgSDyEXAMPLE9/g7QRUhZp4bqbEXAMPLENwGPy
    # Oj59pFA4lNKCIkVgkREXAMPLEjlzxQ7y52gekeVEXAMPLEDiB9ST3UuysgsKdEXAMPLE1TVastU1A0SKFEXAMPLEiywCC/C
    # s8EXAMPLEpZgOs+6hz4AP4KEXAMPLERbASP+4eZScEXAMPLEsnf87eNhyDHq6ikBQ==

    # $Creds.Expiration
    # Thursday, June 18, 2018 2:28:31 PM

# https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
# https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html#examples

Set-DefaultAWSRegion -Region $regionId -Credential $Creds



# # New-CFNStack - https://docs.aws.amazon.com/powershell/latest/reference/items/New-CFNStack.html
# #aws cloudformation deploy --template-file template.yaml --stack-name static-website
# New-CFNStack -StackName s3-demo-stack -TemplateBody $template -Parameter $bucketname, $project

# # validate CloudFormation Stack Output
# (Get-CFNStack -StackName s3-demo-stack).Outputs
# DescribeStacksoperation

