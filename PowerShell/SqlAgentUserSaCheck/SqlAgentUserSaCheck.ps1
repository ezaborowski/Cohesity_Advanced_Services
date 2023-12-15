
### Parameters 
[CmdletBinding()]
param (
    [Parameter()][array]$ipList,  # (optional) IP Addresses and corresponding SQL Instances (comma separated - ie: SQLServer\SQLinstance, SQLServer\SQLinstance2)
    [Parameter()][string]$ipFile = ''  # (optional) text file of IP Addresses and corresponding SQL Instances (one per line - in the following format: SQLServer\SQLinstance)
)

$dateString = (get-date).ToString('yyyy-MM-dd')
$dateTime = Get-Date -Format "dddd MM/dd/yyy HH:mm"
$outfileName = "$PSScriptRoot\LOG-SqlAgentUserSaCheck-$dateString.txt"


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


# ensure the environment meets the PowerShell Module requirements of 5.1 or above 
info_log "Validating PowerShell Version..."
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.0){
    warn_log "PowerShell version is currently: $version. To properly run this script, it is recommended that you upgrade PowerShell."
    fail_log "Please upgrade the PowerShell Module to the current revision of 7.4 by downloading from the Microsoft site: `nhttps://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4#installing-the-msi-package"
    fail_log "Script now exiting..."
    exit 
}
else {
    pass_log "PowerShell Module is up to date."
}


# validating that necessary PowerShell Modules are installed
$modules = Get-InstalledModule
if($modules.Name -notcontains "LocalAccount"){
    warn_log "LocalAccount PowerShell Module NOT installed! Installing now..."
    Set-PSRepository PSGallery -InstallationPolicy Trusted
    Install-Module -Name LocalAccount -Confirm:$False -Force -AllowClobber
    Import-Module -Name LocalAccount
}
else {
    pass_log "Verfied that Microsoft.PowerShell.LocalAccounts PowerShell Module already installed."
}


# parsing list of Windows Server IP's
$ipsToAdd = @()
$sqlInstances = @()
if($ipList){
    info_log "Parsing list of IP Addresses to use in the process of validating if the Cohesity Agent Service Logon User has correct permissions to begin Cohesity SQL Backups..."
    foreach($line in $ipList){
        $sqlInstances += $line
        $split = $line.split("\")
        $ip = $split[0]
        $ipsToAdd += $ip
    }
}
if($ipFile){
    info_log "Parsing list of IP Addresses to use in the process of validating if the Cohesity Agent Service Logon User has correct permissions to begin Cohesity SQL Backups..."
    if(Test-Path -Path $ipFile -PathType Leaf){
        $ips = Get-Content $ipFile
        foreach($line in $ips){
            $sqlInstances += $line
            $split = $line.split("\")
            $ip = $split[0]
            $ipsToAdd += [string]$ip
        }
    }
    else {
        fail_log "IP Address file $ipFile not found at specified directory!"
        fail_log "Script now exiting..."
        exit
    }
}

$ipsToAdd = @($ipsToAdd | Where-Object {$_ -ne ''})
$ipsToAdd = $ipsToAdd | Get-Unique
$sqlInstances = @($sqlInstances | Where-Object {$_ -ne ''})

if($ipsToAdd.Count -gt 0){
    info_log "IP Addresses parsed SUCCESSFULLY:"
    info_log "$ipsToAdd"
}

if($sqlInstances.Count -gt 0){
    info_log "SQL Instances parsed SUCCESSFULLY:"
    info_log "$sqlInstances"
}


# functions
function QueryDatabaseScript($databaseServer, $dbScript, $timeout) {
    # Query and return recordset array for passed T-SQL string
    $SQLConnection = New-Object System.Data.SqlClient.SqlConnection
    $SQLConnection.ConnectionString = "server=$($databaseServer);Initial Catalog=master;Integrated Security=True;"

    try {    
        $SQLConnection.Open()
        $SQLCommand = New-Object System.Data.SqlClient.SqlCommand
        $SQLCommand.Connection = $SQLConnection 
        $SQLCommand.CommandTimeout = $timeout
        
        $SQLCommand.CommandText = $dbScript
        $reader = $SQLCommand.ExecuteReader()

        $recordsetArray = @()
        while ($reader.Read()) {
            $recordsetArray += $reader[0]
        }

        $SQLConnection.Close()
        $SQLConnection.Dispose()
    }
    catch {
        fail_log "QueryDatabaseScript failed: $($_.Exception.Message)"
        $SQLConnection.Dispose()
        throw $_
    }

    return $recordsetArray
}


foreach($ip in $ipsToAdd){
    #log into remote server
    # $session = New-PSSession -ComputerName $ip

    # get Cohesity Agent Service logon user
    $agentUser = (get-wmiObject -class win32_service -ComputerName $ip | where-object Name -eq "CohesityAgent").startname
    info_log "Server $ip - Cohesity Agent Service Logon User: $agentUser"
    if($agentUser -like "*\*") {
        $user = $agentUser.split("\")
        $adminUser = $user[1] + "@" + $user[0]
        $domainUser = $user[1]
        $sqlUser = $agentUser
        $domain = $true
    }
    elseif($agentUser -contains "localsystem") {
        $sqlUser = "NT AUTHORITY\SYSTEM"
        $adminUser = "SYSTEM"
    }
    else {
        $sqlUser = $agentUser
    }

    # validate logon user against members of Administrators Group
    try {
        $admins = Get-LocalGroupMember -ComputerName $ip -Name "Administrators" # | Select-Object -ExpandProperty Name
    }
    catch {
        if($_ -like "* compare *") {
            warn_log "Local Administrators Group may have a member that has been deleted and this script cannot output the Group appropriately."
            fail_log "Failed to validate if Windows User '$agentUser' is a member of the Local Administrators Group on Server $ip."
            fail_log "Please add the Windows User '$agentUser' to the Local Administrators Group manually on Server $ip."
        }
        else {
            warn_log "$_"
            fail_log "Failed to validate if Windows User '$agentUser' is a member of the Local Administrators Group on Server $ip."
            fail_log "Please add the Windows User '$agentUser' to the Local Administrators Group manually on Server $ip."
        }
    }

    if($admins) {
        if($admins.Contains("$domainUser") -or $admins.contains("$adminUser")) {
            pass_log "Server $ip - $agentUser User is a member of the Local Administrators Group"
        } 
        else {
            warn_log "Server $ip - $agentUser User is NOT a member of the Local Administrators Group"
            warn_log "Server $ip - Attempting to add Windows User '$adminUser' to Local Administrators Group..."

            # attempt to add Windows User to Administrators Group
            try {
                Add-LocalGroupMember -ComputerName $ip -groupname "Administrators" -Name "$adminUser"
                $admins = Get-LocalGroupMember -ComputerName $ip -Name "Administrators" # | Select-Object -ExpandProperty Name

                if($admins.Contains("$domainUser") -or $admins.contains("$adminUser")) {
                    pass_log "Successfully added Windows User '$adminUser' to Local Administrators Group on Server $ip."
                } 
                else {
                    fail_log "Failed to add Windows User '$adminUser' to Local Administrators Group on Server $ip."
                    fail_log "Please add the Windows User '$agentUser' to the Local Administrators Group manually on Server $ip."
                }
            }
            catch { 
                fail_log "Failed to add Windows User '$adminUser' to Local Administrators Group on Server '$ip': $_"
                fail_log "Please add the Windows User '$agentUser' to the Local Administrators Group manually on Server $ip."
            }  
        }
    }

    # assign SQL Server Instance
    foreach($sqlInstance in $sqlInstances){
        if($sqlInstance -contains $ip){
            $queryResults = QueryDatabaseScript $sqlInstance "select IS_SRVROLEMEMBER ('sysadmin', '$sqlUser'); " 0
            $isSysadmin = $queryResults[0]
            if($isSysadmin -eq 0){
                warn_log "Windows User '$agentUser' is NOT a memeber of the SQL sysadmin Role on SQL Instance '$sqlInstance'."
                warn_log "Attempting to add Windows User '$agentUser' to SQL sysadmin Role  on SQL Instance '$sqlInstance'..."

                # attempt to add Windows User to SQL sysadmin Role
                try {
                    $queryResults = QueryDatabaseScript $sqlInstance "EXEC master..sp_addsrvrolemember @loginame = N'$sqlUser', @rolename = N'sysadmin'; " 0
                    $queryResults = QueryDatabaseScript $sqlInstance "select IS_SRVROLEMEMBER ('sysadmin', '$sqlUser'); " 0
                    $isSysadmin = $queryResults[0]

                    if($isSysadmin -eq 0){
                        fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                        fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                    } 
                    elseif($isSysadmin -eq 1){
                        pass_log "Windows User '$agentUser' is a memeber of the SQL sysadmin Role on SQL Instance '$sqlInstance'."
                    }
                }
                catch { 
                    fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                    fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                }
            }
            elseif($isSysadmin -eq 1){
                pass_log "Windows User '$agentUser' is a memeber of the SQL sysadmin Role on SQL Instance '$sqlInstance'."
            }
            elseif($isSysadmin -eq "NULL"){
                warn_log "sysadmin Role or '$agentUser' login is not valid, or you do not have permission to view the Role Membership on SQL Instance '$sqlInstance'."
                warn_log "Attempting to add Windows User '$agentUser' to SQL sysadmin Role  on SQL Instance '$sqlInstance'..."

                try {
                    if($domain -ne $false){
                        # attempt to add Windows Domain User to SQL Master DB
                        $queryResults = QueryDatabaseScript $sqlInstance "CREATE LOGIN [$sqlUser] from WINDOWS; " 0
                        pass_log "Successfully added the Windows User '$agentUser' to SQL Instance '$sqlInstance'"
                    }
                    else {
                        # attempt to add Windows Local User to SQL Master DB
                        $queryResults = QueryDatabaseScript $sqlInstance "CREATE LOGIN $sqlUser WITH PASSWORD = 'Cohesity#123'; " 0
                        pass_log "Successfully added the Windows User '$agentUser' to SQL Instance '$sqlInstance' with password: Cohesity#123"
                    }

                    # attempt to add Windows User to SQL sysadmin Role
                    try {
                        $queryResults = QueryDatabaseScript $sqlInstance "EXEC master..sp_addsrvrolemember @loginame = N'$sqlUser', @rolename = N'sysadmin'; " 0
                        $queryResults = QueryDatabaseScript $sqlInstance "select IS_SRVROLEMEMBER ('sysadmin', '$sqlUser'); " 0
                        $isSysadmin = $queryResults[0]

                        if($isSysadmin -eq 0){
                            fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                            fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                        } 
                        elseif($isSysadmin -eq 1){
                            pass_log "Windows User '$agentUser' is a memeber of the SQL sysadmin Role on SQL Instance '$sqlInstance'."
                        }
                    }
                    catch { 
                        fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                        fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                    }
                }
                catch { 
                    fail_log "Failed to add Windows User '$sqlUser' to SQL Instance '$sqlInstance': $_"
                    fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                }
            }
            elseif($isSysadmin -eq ''){
                warn_log "sysadmin Role or '$agentUser' login is not valid, or you do not have permission to view the Role Membership on SQL Instance '$sqlInstance'."
                warn_log "Attempting to add Windows User '$agentUser' to SQL sysadmin Role  on SQL Instance '$sqlInstance'..."
                    
                try {
                    if($domain -ne $false){
                        # attempt to add Windows Domain User to SQL Master DB
                        $queryResults = QueryDatabaseScript $sqlInstance "CREATE LOGIN [$sqlUser] from WINDOWS; " 0
                        pass_log "Successfully added the Windows User '$agentUser' to SQL Instance '$sqlInstance'"
                    }
                    else {
                        # attempt to add Windows Local User to SQL Master DB
                        $queryResults = QueryDatabaseScript $sqlInstance "CREATE LOGIN $sqlUser WITH PASSWORD = 'Cohesity#123'; " 0
                        pass_log "Successfully added the Windows User '$agentUser' to SQL Instance '$sqlInstance' with password: Cohesity#123"
                    }

                    # attempt to add Windows User to SQL sysadmin Role
                    try {
                        $queryResults = QueryDatabaseScript $sqlInstance "EXEC master..sp_addsrvrolemember @loginame = N'$sqlUser', @rolename = N'sysadmin'; " 0
                        $queryResults = QueryDatabaseScript $sqlInstance "select IS_SRVROLEMEMBER ('sysadmin', '$sqlUser'); " 0
                        $isSysadmin = $queryResults[0]

                        if($isSysadmin -eq 0){
                            fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                            fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                        } 
                        elseif($isSysadmin -eq 1){
                            pass_log "Windows User '$agentUser' is a memeber of the SQL sysadmin Role on SQL Instance '$sqlInstance'."
                        }
                    }
                    catch { 
                        fail_log "Failed to add Windows User '$sqlUser' to sysadmin Role on SQL Instance '$sqlInstance': $_"
                        fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                    }
                }
                catch { 
                    fail_log "Failed to add Windows User '$sqlUser' to SQL Instance '$sqlInstance': $_"
                    fail_log "Please add the Windows User '$agentUser' to the sysadmin Role manually on SQL Instance '$sqlInstance'."
                }
            }
        }  
    }
}





