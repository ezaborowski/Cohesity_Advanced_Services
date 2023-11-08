### usage to export: ./ADexport_UI.ps1 
### usage to import: ./ADexport_UI.ps1 -restore $True -export $False

# wrapper.bat script: "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -ExecutionPolicy Bypass -Command "start-process "powershell" -Verb "RunAs" -argumentlist '-File C:\Erins_work\AD_UI\ADexport_UI.ps1'" 1>C:\Erins_work\AD_UI\ADexport_UI-logs.log 2>&1


# Prepare Entra ID data to be Exported:
# - Login to Microsoft Azure Portal
# - Open App Registrations and Register a new App for the 'EntraExport' script
# - Choose the 'Certificates' tab and click 'Upload certificate' (you will need to prepare a self-signed certificate to upload, and also install locally on the server you are running the script from) 
# - Select 'API permissions' from the left-hand pane and click 'Add a permission'
# - Select the 'APIs my organization uses' tab, then choose 'Microsoft Graph'
# - Select 'Application permissions' and checkmark the following permissions:
# 	Directory.Read.All
#     Policy.Read.All
#     IdentityProvider.Read.All
#     Organization.Read.All
#     User.Read.All
#     EntitlementManagement.Read.All
#     UserAuthenticationMethod.Read.All
#     IdentityUserFlow.Read.All
#     APIConnectors.Read.All
#     AccessReview.Read.All
#     AccessReview.ReadWrite.All
#     AccessReview.ReadWrite.Membership
#     Agreement.Read.All
#     Policy.Read.PermissionGrant
#     PrivilegedAccess.Read.AzureResources
#     PrivilegedAccess.Read.AzureAD
#     Application.Read.All
#     AuthenticationContext.Read.All
#     UserAuthenticationMethod.Read.All
#     OrgSettings-AppsAndServices.Read.All
#     IdentityProvider.Read.All
#     AgreementAcceptance.Read.All
#     PrivilegedAccess.Read.AzureADGroup
#     IdentityUserFlow.Read.All
#     IdentityRiskyUser.Read.All
#     User.ReadWrite.All
#     User.Export.All
#     DeviceManagementConfiguration.Read.All
#     RoleManagementPolicy.Read.AzureADGroup
#     Group.Read.All
#     GroupMember.Read.All

# - Click 'Add permissions'
# - Click 'Grant admin consent for Default Directory'
# - Input Mandatory Values below in Parameters section

### Example of how to hard-code Parameters into script:
# [CmdletBinding()]
# param (
#     [Parameter()][string]$clientId = "777bc20a-32c9-456d-b1d1-37f6d10f8056", # comma-delimited list of Client ID(s) from Registration of ADExport App
#     [Parameter()][string]$tenantId = "cec582a6-6d0d-4a38-ae8c-82ef2bed9gf2", # comma-delimited list of Tenant ID(s) from Registration of ADExport App
#     [Parameter()][string]$certThumbprint = "6029DDB9E5559B528FAD529D945B128F3AC70T23", # comma-delimited list of Certificate Thumbprint(s) created for access to ADExport App (used for Backup)
#     [Parameter()][string]$clientSecret = "4ua8Q~BKTR48zL7akvZqNKwuGzrD_EhgayfoWrPO", # comma-delimited list of Client Secret Value(s) created for access to ADExport App (used for Recovery)
#     [Parameter()][string]$cohView = "C:\EntraID\BACKUPS", # SMB address to access the Cohesity View
#     [Parameter()][bool]$export = $True, # switch for utilizing script to Export Azure AD contents (default is True)
#     [Parameter()][bool]$restore = $False,   # switch for utilizing script to Restore to Azure AD (default is False)
#     [Parameter()][int]$days = 30   # amount of Days to keep backed up data on Cohesity View (default is 30 days)
#     # [Parameter()][int]$days = 1   # Days of data to pull (defaults to 1)
#     # [Parameter()][bool]$skipVersionChk = $false   # Skips the Version Check at the beginning of script (defaults to False)
# )

### Parameters 
[CmdletBinding()]
param (
    [Parameter()][string]$clientId, # comma-delimited list of Client ID(s) from Registration of ADExport App
    [Parameter()][string]$tenantId, # comma-delimited list of Tenant ID(s) from Registration of ADExport App
    [Parameter()][string]$certThumbprint, # comma-delimited list of Certificate Thumbprint(s) created for access to ADExport App (used for Backup)
    [Parameter()][string]$clientSecret, # comma-delimited list of Client Secret Value(s) created for access to ADExport App (used for Recovery)
    [Parameter()][string]$cohView, # SMB address to access the Cohesity View
    [Parameter()][bool]$export = $True, # switch for utilizing script to Export Azure AD contents (default is True)
    [Parameter()][bool]$restore = $False,   # switch for utilizing script to Restore to Azure AD (default is False)
    [Parameter()][int]$days = 30   # amount of Days to keep backed up data on Cohesity View (default is 30 days)
    # [Parameter()][int]$days = 1   # Days of data to pull (defaults to 1)
    # [Parameter()][bool]$skipVersionChk = $false   # Skips the Version Check at the beginning of script (defaults to False)
)

$dateString = (get-date).ToString('yyyy-MM-dd')
$dateTime = Get-Date -Format "dddd MM/dd/yyy HH:mm"

# logging
function info_log{
    param ($statement)
    
    Write-Host "`nINFO    $statement`n" -ForegroundColor Blue
    Write-Output "`n$dateTime    INFO    $statement`n" | Out-File -FilePath $outfileName -Append
}

function warn_log{
    param ($statement)
    
    Write-Host "`nWARN    $statement`n" -ForegroundColor Yellow
    Write-Output "`n$dateTime    WARN    $statement`n" | Out-File -FilePath $outfileName -Append
}

function fail_log{
    param ($statement)
    
    Write-Host "`nFAIL    $statement`n" -ForegroundColor Red
    Write-Output "`n$dateTime    FAIL    $statement`n" | Out-File -FilePath $outfileName -Append
}

function pass_log{
    param ($statement)
    
    Write-Host "`nPASS    $statement`n" -ForegroundColor Green
    Write-Output "`n$dateTime    PASS    $statement`n" | Out-File -FilePath $outfileName -Append
}

# validating that necessary PowerShell Modules are installed
$modules = Get-InstalledModule
if($modules.Name -notcontains "EntraExporter"){
    write-host "EntraExporter NOT installed! Installing now..."
    Install-Module EntraExporter
    # Import-Module EntraExporter
}
else{
    write-host "EntraExporter already installed!"
}

if($modules.Name -notcontains "Microsoft.Graph"){
    write-host "Microsoft.Graph NOT installed! Installing now..."
    Install-Module Microsoft.Graph
    Import-Module Microsoft.Graph
}
else{
    write-host "Microsoft.Graph already installed!"
}

# parse through authentication credentials

$credentials = @()
$client = $clientId -split ","
$tenant = $tenantId -split ","
$thumbprint = $certThumbprint -split ","
$secret = $clientSecret -split ","

if($client.count -eq $tenant.count -and $tenant.count -eq $thumbprint.count){
    for($i=0; $i -lt $client.count; $i++){
        $credentials += [pscustomobject] @{
            clientId = $client[$i]
            tenantId = $tenant[$i]
            certThumbprint = $thumbprint[$i]
            clientSecret = $secret[$i]
        }
    }
}
elseif($client.count -lt $tenant.count){
    if($client.count -eq 1){
        for($i=0; $i -lt $tenant.count; $i++){
            $credentials += [pscustomobject] @{
                clientId = $client[0]
                tenantId = $tenant[$i]
                certThumbprint = $thumbprint[0]
                clientSecret = $secret[0]
            }
        }
    }
}
else{
    write-host "One of the following MUST be true for the script to be successful:`n"
    write-host "1) There must be an equal amount of Client ID's, Tenant ID's, and Certificate Thumbprints"
    write-host "2) There must be 1 Client ID, 1 Tenant ID, and multiple Certificate Thumbprints"
    write-host "The script will now stop. Please try again."
    exit
}


function tokenRequest($tenantID, $clientID, $clientSecret) {

    # prepare token request
    $url = 'https://login.microsoftonline.com/' + $tenantID + '/oauth2/v2.0/token'

    $body = @{
        grant_type = "client_credentials"
        client_id = "$clientID"
        client_secret = "$clientSecret"
        scope = "https://graph.microsoft.com/.default"
    }

    # obtain the token
    Write-Verbose "Authenticating to Microsoft Azure Portal..."
    try { 
        $tokenRequest = Invoke-WebRequest -Method 'POST' -Uri $url -ContentType "application/x-www-form-urlencoded" -Body $body -UseBasicParsing -ErrorAction Stop 
        $token = ($tokenRequest.Content | ConvertFrom-Json).access_token
    }
    catch { 
        fail_log "Unable to obtain access token: $tokenRequest"
        fail_log "Unable to obtain access token, aborting..."
        exit 
    }
    #$token = convertto-securestring $token -asPlainText -Force

    return $token
    
}


function selectList($title, $objects, [array[]]$listObjects, [array[]]$listObjects2) {

    Write-Host "$title..."

    Start-Sleep -Seconds 1       
    Write-Host "`nPlease Select a $objects from the list below...`n"   -ForegroundColor Yellow
    
    for($i = 0 ; $i -lt $listObjects.count ; $i++){
        Write-Host "$($i + 1)).  $($listObjects[$i])"
        if($listObjects2) {
            Write-Host  "     $($listObjects2[$i])"
        }       
    }
    
    Write-Host "`n"
    Write-Host "Enter the number of the $objects to restore to,"
    Write-Host "or type 0 to break from this menu.`n"  
    
    $valid = $False
    while($valid -ne $True) {
        [int]$selection = Read-Host "Please enter your selection number"
        switch ($selection){
            0
                {
                    write-host "A selection from this menu is required for the script to proceed!" -ForegroundColor Red
                    Write-Host "`nAre you sure you want to exit this menu?" -ForegroundColor Yellow
                    $confirm = Read-Host "[Y] or [N]"
                    if($confirm -ne 'y' -and $confirm -ne "Y"){
                        Write-Host "Please try again..." -ForegroundColor Yellow
                        $valid = $False
                    }
                    else {
                    $valid = $True
                    break 
                    }
                }
            {$_ -ge 1 -and $_ -le $listObjects.count }
                {
                    Write-Host "`nYou Selected: '$($listObjects[$selection -1])'" -ForegroundColor Green
                
                    Write-Host "`nIs This Correct?" -ForegroundColor Yellow
                    $confirm = Read-Host "[Y] or [N]"
                    if($confirm -ne 'y' -and $confirm -ne "Y"){
                        Write-Host "Please try again..." -ForegroundColor Yellow
                        $valid = $False
                    }
                    else {
                        $select = $($listObjects[$selection -1])
                        return $select
                        #set-location "$cohView\$select"
                        $valid = $True
                    }
                }
        }
    }
}


$view = $cohView

if($view -contains '\\') {
    $connection = Test-Connection $view
}

if($view -notcontains '\\' -or $connection -eq $True) {

    # exporting Entra ID Objects
    if($export -eq $True) {
        foreach($credential in $credentials){
        
            # update Cohesity View Folder Hierarchy per Tenant ID
            $pathTenant = $credential.tenantId
            $tenantView = Test-Path $view\$pathTenant

            # validate if Tenant ID folder exists (if not, create folder)
            if($tenantView -eq $False) {
                new-item $view\$pathTenant -type Directory
            }


            # validate if Dated folder exists (if not, create folder)
            $dateFolder = $dateString

            $i = 2
            while(Test-Path $view\$pathTenant\$dateFolder){
                write-host "Folder $dateFolder already exists in the Cohesity View Entra ID Tenant folder: $view\$pathTenant. Creating Secondary Directory..."
                $dateFolder = "$(get-date -f MM-dd-yyyy)-$i"
                $i++
            }

            new-item "$view\$pathTenant\$dateFolder" -type directory
            write-host "New Directory $view\$pathTenant\$dateFolder successfully created!"

            $dateView = "$view\$pathTenant\$dateFolder"
            set-location $dateView


            # define log file
            $outfileName = "$dateView\$dateString-exportLog.txt"

            #Delete files older than X Days
            info_log "Removing Entra ID Exporting Data older than $days days. This may take a moment..."
            Get-ChildItem $view\$pathTenant -Recurse -Force -ea 0 | Where-Object {!$_.PsIsContainer -and $_.LastWriteTime -lt (Get-Date).AddDays(-[int]$days)} | ForEach-Object {$_ | Remove-Item -Force $_.FullName | Out-File "$dateView\$dateString-deleteLog.txt" -Append}

            #Delete empty folders and subfolders
            Get-ChildItem $Folder -Recurse -Force -ea 0 | Where-Object {$_.PsIsContainer -eq $True} | Where-Object {$_.getfiles().count -eq 0} | ForEach-Object {$_ | Remove-Item -Force $_.FullName | Out-File "$dateView\$dateString-deleteLog.txt" -Append}
            pass_log "Successfully purged Entra ID Data older than $days days. Please find log of items expired here: $dateView\$dateString-deleteLog.txt"

            # retrieve API token 
            $token = tokenRequest $credential.tenantId $credential.clientId $credential.clientSecret
            pass_log "Successfully retrieved Microsoft Azure Token!"

            $secureToken = convertto-securestring $token -asPlainText -Force

            
            # connecting to Azure and Entra ID Instances
            info_log "Connecting to Microsoft Azure Instance via Microsoft Graph..."
            Connect-MgGraph -ClientId $credential.clientId -TenantId $credential.tenantId -CertificateThumbprint $credential.certThumbprint 
            #Connect-MgGraph -AccessToken $secureToken 

            # validaion of appropriate Entra ID Permissions
            $neededScopes = @('Directory.Read.All','Policy.Read.All','IdentityProvider.Read.All','Organization.Read.All','User.Read.All','EntitlementManagement.Read.All','UserAuthenticationMethod.Read.All','IdentityUserFlow.Read.All','APIConnectors.Read.All','AccessReview.Read.All','Agreement.Read.All','Policy.Read.PermissionGrant','PrivilegedAccess.Read.AzureResources','PrivilegedAccess.Read.AzureAD','Application.Read.All')
  
            info_log "Connecting to Microsoft Entra ID Instance via EntraExporter..."
            #Connect-EntraExporter -TenantId $tenantId 
            #Connect-MgGraph -Scopes $neededScopes
         
            # export Entra ID in JSON Format
            info_log "Exporting All Entra ID Objects to Cohesity View in JSON format..."
            Export-Entra -Path "$dateView" -All
            copy-item -path "$dateView\Organization\Organization.json" -destination "$view\$pathTenant\Organization.json"


            # exporting User and Group metadata to CSV File 
            info_log "Exporting Entra ID User and Group metadata to Cohesity View in CSV format..."
            Get-MgUser -All | Export-CSV -Path $dateView\users.csv -NoTypeInformation
            Get-MgGroup -All  | Export-CSV -Path $dateView\Groups.csv -NoTypeInformation


            # exporting Group Membership metadata for use in Entra ID Recovery
            info_log "Exporting Entra ID Group Membership data for use in Recovering User Objects..."
            $grpmember=New-Item -Path $dateView -ItemType Directory -Name "GroupMembership"
            $GrpCSV=Import-Csv $dateView\Groups.csv

            # extrapolating each Entra ID Group's metadata
            foreach($GrpProperties in $GrpCSV){
                $GrpId=$GrpProperties.Id
                $GroupFolder=New-Item -Path $grpmember -ItemType Directory -Name $GrpId
                Set-Location $GroupFolder
                Get-MgGroupMember -GroupId $GrpId | Export-CSV -Path Groupmembers.csv -NoTypeInformation
            }
        }

        pass_log "The Entra ID Export has completed successfully!"
    }

    # restoring Entra ID Objects
    if($restore -eq $True) {
        $tenantsArray = @()
        $datesArray = @()
        $tenantNames = @()
        $tenantDomains = @()
        #$objects = @('Users','Groups')
        set-location $cohView
        
        # prompting for selection of Tenant ID
        $tenants = get-childitem -path $cohView -Name -Directory
        if($tenants.count -gt 1){
            foreach($tenant in $tenants){
                $tenantsArray += $tenant
                $orgDisplayName = @()
                $orgTenantDomain = @()
                $content = get-content "$cohView\$tenant\Organization.json"
                $org = $content | ConvertFrom-Json
                $orgDisplayName += $org.DisplayName
                if(!$orgDisplayName){
                    $orgDisplayName = "N/A"
                }
                $orgTenantDomain += $org.verifiedDomains.name
                if(!$orgTenantDomain){
                    $orgTenantDomain = "N/A"
                }
    
                $tenantNames += , $orgDisplayName
                $tenantDomains += , $orgTenantDomain
            }
        }
        elseif($tenants.count -eq 0){
            write-host "There are non Tenant ID folders found in: $cohView"
        }
        else {
            $tenantsArray = $tenants
            $orgDisplayName = @()
            $orgTenantDomain = @()
            $content = get-content "$cohView\$tenants\Organization.json"
            $org = $content | ConvertFrom-Json
            $orgDisplayName += $org.DisplayName
            if(!$orgDisplayName){
                $orgDisplayName = "N/A"
            }
            $orgTenantDomain += $org.verifiedDomains.name
            if(!$orgTenantDomain){
                $orgTenantDomain = "N/A"
            }

            $tenantNames += , $orgDisplayName
            $tenantDomains += , $orgTenantDomain
        }

        $select = selectList "Retrieving Entra ID Tenant Names..." "Tenant" $tenantsArray $tenantNames

        $tenantPath = "$cohView\$select"
        set-location "$tenantPath"
        
        write-host "User has selected Entra ID Tenant: $select"

        foreach ($credential in $credentails){
            if($select -eq $credential.tenantId){
                $tenantID = $credentail.tenantId
                $clientID = $credentail.clientId
                $clientSecret = $credential.clientSecret
            }
        }
        

        $dateFolders = get-childitem -path (Get-Location) -Name -Directory

        if($dateFolders.count -gt 1){
            foreach($folder in $dateFolders){
                $datesArray += $folder
            }
        }
        elseif($dateFolders.count -eq 0){
            write-host "There are non Backup Date folders found in: $tenantPath"
        }
        else {
            $datesArray = $dateFolders
        }

        # prompting for selection of Backup Date
        $select = selectList "Retrieving Backup Dates..." "Backup Date" $datesArray 

        write-host "User has selected Backup Date: $dateSelect"
        
        $buDate = $select
        $datePath = "$tenantPath\$buDate"
        set-location $datePath

        # define log file
        $outfileName = "$datePath\$dateString-restoreLog.txt"

        $usersCSV = Import-Csv .\users.csv
        $groupsCSV = Import-Csv .\Groups.csv

        # prompting for selection of Entra ID User
        info_log "Please input the UserPrincipalName for the User requesting to be Restored:"
        $upn = read-host "UserPrincipalName"
        
        foreach($user in $usersCSV){
            $upn = $upn.ToLower()
            $UserPrincipalName = $user.UserPrincipalName.ToLower()
            if ($upn -eq $UserPrincipalName) {
                $userName = $user.DisplayName
                $userId = $user.Id
            }
        }
        
        if(!$userId){
            fail_log "UserPrincipalName did not match any records currently on file. Please try again..."
            info_log "Please input the UserPrincipalName for the User requesting to be Restored:"
            $upn = read-host "UserPrincipalName"
            
            foreach($user in $usersCSV){
                if ($upn -eq $user.UserPrincipalName) {
                    $userName = $user.DisplayName
                    $userId = $user.Id
                }
            }
            if(!$userId){
                fail_log "UserPrincipalName did not match any records currently on file. Exiting..."
                exit
            }
        }
       
        pass_log "Successfully associated UserPrincipalName $upn with User '$userName' and UserId '$userId'" 

        $userPath = "$datePath\Users\$userId"
        $userJSON = "$userPath\$userId.json"


        # extrapolating Entra ID User data to Restore
        $jsonContent = Get-Content -Path $userJSON | ConvertFrom-Json | Select-Object accountEnabled,ageGroup,assignedLicenses,assignedPlans,authorizationInfo,businessPhones,city,companyName,consentProvidedForMinor,country,department,displayName,employeeHireDate,employeeId,employeeLeaveDateTime,employeeOrgData,employeeType,faxNumber,givenName,imAddresses,infoCatalogs,isResourceAccount,jobTitle,legalAgeGroupClassification,mail,mailNickname,mobilePhone,officeLocation,onPremisesDistinguishedName,onPremisesDomainName,onPremisesExtensionAttributes,onPremisesImmutableId,onPremisesLastSyncDateTime,onPremisesProvisioningErrors,onPremisesSamAccountName,onPremisesSecurityIdentifier,onPremisesSyncEnabled,onPremisesUserPrincipalName,otherMails,passwordPolicies,passwordProfile,postalCode,preferredDataLocation,preferredLanguage,provisionedPlans,proxyAddresses,showInAddressList,state,streetAddress,surname,usageLocation,userPrincipalName,userType | ConvertTo-Json -Depth 99
        
        # associating Entra ID Group ID's with User
        write-host "Associating Group ID's with User object..."
        if($jsonContent){
            $groupIDs = @()
            $groupIDvalid = @()
            $groupNames = @()
            $groupFolder = "$datePath\GroupMembership\"

            $groups = Get-ChildItem -Path $groupFolder -Name -Directory

            foreach ($group in $groups) {
                $groupMemberCSV = import-csv "$groupFolder\$group\Groupmembers.csv"

                foreach ($groupMember in $groupMemberCSV) {
                    if($userId -eq $groupMember.id){
                        $groupIDs += $group
                    }
                }
            }

            foreach ($groups in $groupsCSV){
                $groupDisplayName = $groups.DisplayName
                $groupId = $groups.Id

                if($groupIDs -contains $groupId){
                    $groupNames += $groupDisplayName
                    info_log "Assocating '$userName' with Group '$groupDisplayName'"
                    $groupIDvalid += $groupId
                }
            }
            if($groupNames.count -eq 0){
                warn_log "$userName is not associated with any Entra ID Groups!"
            }
            else{
                pass_log "Associated '$userName' User with the following Group objects: $groupNames"
            }
            
        }
        else {
            fail_log "Failed to parse User '$userName' json content!"
            info_log "User Content: `n $jsonContent"
        }
        
        start-sleep -s 5

        $json = $jsonContent | ConvertFrom-Json

        $password = 'P@assw0rd123'

        # configuring if User Account is Enabled or Disabled
        info_log "`nShould the $userName User Account be Enabled?'"
        $confirm = Read-Host "[Y] or [N]"
        if($confirm -ne 'n' -and $confirm -ne "N"){
            $acctEnabled = "$true"
            pass_log "$userName User Account has been successfully configured for Enablement!"
        }
        else{
            $acctEnabled = "$false"
            pass_log "$userName User Account has been successfully configured for Disablement!"
        }

        start-sleep -s 3

        info_log "Parsing $userName User Account data..."
        $userData = @{
            "accountEnabled" = $acctEnabled;
            "ageGroup" = $json.ageGroup;
            "assignedLicenses" = $json.assignedLicenses;
            "assignedPlans" = $json.assignedPlans;
            "authorizationInfo"= $json.authorizationInfo;
            "businessPhones" = $json.businessPhones;
            "city" = $json.city;
            "companyName" = $json.companyName;
            "consentProvidedForMinor" = $json.consentProvidedForMinor;
            "country" = $json.country;
            "department" = $json.department;
            "displayName" = $json.displayName;
            "employeeId" = $json.employeeId;
            "employeeLeaveDateTime" = $json.employeeLeaveDateTime;
            "employeeOrgData" = $json.employeeOrgData;
            "employeeType" = $json.employeeType;
            "faxNumber" = $json.faxNumber;
            "givenName" = $json.givenName;
            "imAddresses" = $json.imAddresses;
            "isResourceAccount" = $json.isResourceAccount;
            "jobTitle" = $json.jobTitle;
            "legalAgeGroupClassification" = $json.legalAgeGroupClassification;
            "mail" = $json.mail;
            "mailNickname" = $json.mailNickname;
            "mobilePhone" = $json.mobilePhone;
            "officeLocation" = $json.officeLocation;
            "onPremisesDistinguishedName" = $json.onPremisesDistinguishedName;
            "onPremisesDomainName" = $json.onPremisesDomainName;
            "onPremisesExtensionAttributes" = $json.onPremisesExtensionAttributes;
            "onPremisesImmutableId" = $json.onPremisesImmutableId;
            "onPremisesLastSyncDateTime" = $json.onPremisesLastSyncDateTime;
            "onPremisesProvisioningErrors" = $json.onPremisesProvisioningErrors;
            "onPremisesSamAccountName" = $json.onPremisesSamAccountName;
            "onPremisesSecurityIdentifier" = $json.onPremisesSecurityIdentifier;
            "onPremisesSyncEnabled" = $json.onPremisesSyncEnabled;
            "onPremisesUserPrincipalName" = $json.onPremisesUserPrincipalName;
            "otherMails" = $json.otherMails;
            "passwordPolicies" = $json.passwordPolicies;
            "passwordProfile" = @{
                    "password" = "$password";
                    "forceChangePasswordNextSignIn" = "$true"
                    #"ForceChangePasswordNextSignInWithMfa" = "$true"
                };
            "postalCode" = $json.postalCode;
            "preferredDataLocation" = $json.preferredDataLocation;
            "preferredLanguage" = $json.preferredLanguage;
            "provisionedPlans" = $json.provisionedPlans;
            "proxyAddresses" = $json.proxyAddresses;
            "showInAddressList" = $json.showInAddressList;
             "state" = $json.state;
            "streetAddress" = $json.streetAddress;
            "surname" = $json.surname;
            "usageLocation" = $json.usageLocation;
            "userType" = $json.userType;
            "userPrincipalName" = $json.userPrincipalName
            }

        $userRecover = "$datePath\$dateString-$userName.json"    
        $userSave = $userData | ConvertTo-Json -Depth 99 | Out-File $userRecover
        $body = Get-Content -Path $userRecover | ConvertFrom-Json | ConvertTo-Json -Depth 99

        if($body) {
            pass_log "Successfully extrapolated User Account Data!"
            Start-Sleep -s 3

            info_log "`nBelow are the User Values to be Recovered:"
            info_log "$body"
        }
        else {
            fail_log "Failed to extrapolate Account Data for User: $userName"
            fail_log "Script now exiting..."
            exit
        }
        

        warn_log "The password that will need to be used the next time '$userName' logs in is: '$password'" 
        Write-Host "`nAre you certain you want to proceed with the Recovery of User '$userName' from Date '$buDate'?" -ForegroundColor Green
        $confirm = Read-Host "[Y] or [N]"
        if($confirm -ne 'y' -and $confirm -ne "Y"){
            Write-Host "Aborting Recovery..." -ForegroundColor Red
            exit
        }
        else {

            # retrieve API token 
            $token = tokenRequest $tenantID $clientID $clientSecret
            pass_log "Successfully retrieved Microsoft Azure Token!"
            $secureToken = convertto-securestring $token -asPlainText -Force
            
            # connecting to Azure and Entra ID Instances
            info_log "Connecting to Microsoft Azure Instance via Microsoft Graph..."
             
            Connect-MgGraph -AccessToken $secureToken 
            Connect-MgGraph -scopes "User.ReadWrite.All"

            # create API Headers for WebRequest
            $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
            # $headers.Add("accept", "application/json, text/plain, */*, odata.metadata=minimal, odata.streaming=true, IEEE754Compatible=false, charset=utf-8")
            $headers.Add("Authorization", "Bearer $token")

            # restoration of Entra ID User via MS Graph API
            info_log "Restoring Entra ID Backup from '$buDate' for User: $userName"
            try{
                $response = Invoke-RestMethod 'https://graph.microsoft.com/v1.0/users' -Method 'POST' -Headers $headers -body $body -ContentType 'application/json' 
                # 'application/json,odata.metadata=minimal,odata.streaming=true,IEEE754Compatible=false,charset=utf-8'  
            }
            catch { 
                if($_.ErrorDetails.Message){
                    fail_log "Unable to Recovery Entra ID User: $($_.ErrorDetails.Message)"
                    fail_log "aborting Recovery..."
                    exit 
                }
                else {
                    pass_log "Successfully restored Entra ID User: $userName"
                    pass_log "Azure Portal Response: $_"
                }
            }


            # pulling new User ID
            info_log "Fetching Recovered User New ID..."
            try{
                $recoveredUser = Invoke-RestMethod "https://graph.microsoft.com/v1.0/users/$upn" -Method 'GET' -Headers $headers 
                #-ContentType 'application/json' # 'application/json,odata.metadata=minimal,odata.streaming=true,IEEE754Compatible=false,charset=utf-8' 
                
            }
            catch { 
                if($_.ErrorDetails.Message){
                    fail_log "Unable to fetch New User ID:  $($_.ErrorDetails.Message)"
                    fail_log "Please manually associate New Entra ID User to the following Groups: $groupNames"
                    fail_log "Script now exiting..."
                    exit 
                }
                else {
                    $newUserId = $recoveredUser.id
                    pass_log "Successfully validated New User ID: $newUserId"
                    pass_log "New Entra ID User Profile: $_"
                }
            }            

            # creating User Group association Payload for use with MS Graph Recovery API
            $groupPayload = @{
                "@odata.id"= "https://graph.microsoft.com/v1.0/directoryObjects/$newUserId"
            }

            $groupSave = $groupPayload | ConvertTo-Json -Depth 99 | Out-File $datePath\$dateString-userGroups.json
            $groupRecover = "$datePath\$dateString-userGroups.json"
            $groupBody = Get-Content -Path $groupRecover | ConvertFrom-Json | ConvertTo-Json -Depth 99

            # restoration of Entra ID User Group associations via MS Graph API
            info_log "Writing Group Membership associations to Entra ID User: $groupNames"
            info_log "Group Payload: `n $groupPayload"

            $ref = '$ref'

            for($i=0; $i -lt $groupIDvalid.count; $i++) {
                $groupID = $groupIDvalid[$i]
                try {
                    $grouping = Invoke-RestMethod "https://graph.microsoft.com/v1.0/groups/$groupID/members/$ref" -Method 'POST' -Headers $headers -body $groupBody -ContentType 'application/json' 
                }
                catch { 
                    if($_.ErrorDetails.Message){
                        $groupName = $groupNames[$i]
                        fail_log "Unable to Associate New User ID with Group: $($_.ErrorDetails.Message)"
                        fail_log "Please manually associate New Entra ID User to the following Group: $groupName"
                        fail_log "Script now exiting..."
                        exit 
                    }
                    else {
                        $groupName = $groupNames[$i]
                        pass_log "Successfully restored Entra ID User Group Membership association: $groupName"
                        pass_log "Azure Portal Response: $_" 
                    }
                }    
            }

            pass_log "Entra ID User Recovery and Group Association Successful!"
        }          
    }
}

exit 
