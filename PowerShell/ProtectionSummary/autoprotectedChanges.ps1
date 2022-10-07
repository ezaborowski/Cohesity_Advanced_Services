
### process commandline arguments
[CmdletBinding()]
# param (
#     [Parameter()][string]$vips, # vips or FQDNs of Cohesity Clusters 
#     [Parameter()][string]$usernames, # Cohesity UI Admin usernames
#     [Parameter()][string]$domains, # Cohesity UI domains of usernames
#     [Parameter()][string]$passwords # Cohesity UI Admin passwords
# )

# example of hardcoding credentails:
param (
    [Parameter()][string]$vips = "10.26.1.9, 10.26.0.198",
    [Parameter()][string]$usernames = "ezabor, ezabor",
    [Parameter()][string]$domains = "sre.cohesity.com, sre.cohesity.com",
    [Parameter()][string]$passwords = "Cohesity#321, Cohesity#321"
)

$source = $PSScriptRoot

# Create folder for current .csv files

$currentFolder = "autoProtection"

if (Test-Path $source\$currentFolder) {

    Write-Host "Current Auto Protection Changes Folder Exists"
}
else {

    #PowerShell Create directory if not exists
    New-Item $currentFolder -ItemType Directory
    Write-Host "Auto Protection Changes Folder Created successfully"
}

$autoProtect_source = "$source\$currentFolder"

# Output Config
$dateString = (get-date).ToString('yyyy-MM-dd')
$autoProtectChanges = "$autoProtect_source\autoProtectChanges-$dateString.csv" 

function write-log {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory=$False)]
        [ValidateSet("INFO","WARN","ERROR","FATAL","DEBUG")]
        [String]
        $Level = "INFO",

        [Parameter(Mandatory=$True)]
        [string]
        $Message,

        [Parameter(Mandatory=$False)]
        [string]
        $logfile
    )

    $Stamp = (Get-Date).toString("yyyy/MM/dd HH:mm:ss")
    $Line = "$Stamp $Level $Message"

    If($logfile) {
        Add-Content $logfile -Value $Line
    }
    Else {
        Write-Output $Line
    }
}

# ensure the environment meets the PowerShell Module requirements of 5.1 or above 
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    write-host "Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site:"
    write-host "https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi"
}
else {
    write-host "PowerShell Module is up to date."

    ### source the cohesity-api helper code
    . $(Join-Path -Path $PSScriptRoot -ChildPath cohesity-api.ps1)

    $credentials = @()

    if(!$usernames){
        while($stopQuery -ne "no") {
            $username = Read-Host -Prompt 'Please input the Cohesity UI admin username'

            $domain = Read-Host -Prompt 'Please input the Cohesity UI domain'

            $vip = Read-Host -Prompt 'Please input the full Cohesity Cluster hostname or IP address (ex: servername.domain.com or 172.20.1.55)'

            $credentials += [pscustomobject] @{
                username = "$username" 
                domain = "$domain"
                vip = "$vip"
            }
            
            $stopQuery = Read-Host -Prompt 'Are there any more Cohesity Clusters to run this script against? (yes/no)'
        }
    }
    else{
        $vip = $vips -split ","
            $vip = $vip.replace(' ', '')
        $username = $usernames -split(",")
            $username = $username.replace(' ', '')
        $domain = $domains -split(",")
            $domain = $domain.replace(' ', '')
        $password = $passwords -split(",")
            $password = $password.replace(' ', '')
        
        For($i=0; $i -lt $username.count; $i++){
            $credentials += [pscustomobject] @{
                username = $username[$i]
                vip = $vip[$i]
                domain = $domain[$i]
                password = $password[$i]
                }
            }
        }


    foreach($credential in $credentials){
        if(!$usernames){
            write-host "Please input password for:" $credential.vip
            $password = Read-Host -AsSecureString
            $password = ConvertFrom-SecureString $password -AsPlainText

            # authenticate to Cohesity Cluster
            apiauth -vip $credential.vip -username $credential.username -domain $credential.domain -password $password
        }
        else {
            # authenticate to Cohesity Cluster
            ForEach-Object{
                apiauth -vip $credential.vip -username $credential.username -domain $credential.domain -password $credential.password    
            }
                     
        }
        if(!$credential){
            Write-host "A complete set of credentials was not input."
            }

        
        # Output headers in csv report
        "" | Out-File -FilePath $autoProtect_source

        # get the Cluster Information
        $clusterdetails = api get /public/cluster

        # get the Protection Source Details
        $protectionSources = api get ​/public​/protectionSources?allUnderHierarchy=true
        
        #???     get /public/protectionSources/protectedObjects?environment=kVMware, kHyperV, kSQL, kView, kPuppeteer, kPhysical, kPure, kNimble, kAzure, kNetapp, kAgent, kGenericNas, kAcropolis, kPhysicalFiles, kIsilon, kGPFS, kKVM, kAWS, kExchange, kHyperVVSS, kOracle, kGCP, kFlashBlade, kAWSNative, kO365, kO365Outlook, kHyperFlex, kGCPNative, kAzureNative, kKubernetes, kElastifile, kAD, kRDSSnapshotManager, kCassandra, kMongoDB, kCouchbase, kHdfs, kHive, kHBase, kUDA&id=$sourceId 3236 3235
        
        # capture the needed fields
        $clusterName = $clusterdetails.name

        foreach($protectionSource in $protectionSources){

            $protectedInfo = $protectionSource.nodes.protectedSourcesSummary
            $unprotectedInfo = $protectionSource.nodes.unprotectedSourcesSummary
            
            $sourceId = $protectionSource.nodes.protectionSource.id 

            foreach($object in $objectrun){

                }
            }
        }

        "" | Out-File -FilePath $autoProtect_source -Append
    }

# comparing csv reports for changes
Write-host "`nComparing Protection Source Objects over the last 24 hours..."

$reports = @("autoProtectChanges-*.csv") 
foreach($report in $reports) {

    $compareReports = Compare-Object -IncludeEqual -ReferenceObject $regionIds -DifferenceObject $regionId -IncludeDifferent

    if(!$compareReports){
        write-host "There was an error comparing the Protection Source Object Reports." -ForegroundColor Yellow
        exit
    }

}

# Create folder and move archived AutoProtection Report files from previous runs
$results = @("autoProtectChanges-*.csv") 
foreach($result in $results) {
    $csv = Get-ChildItem $csv_source\$result -Name
    foreach($i in $csv){
        $folder = $i.split("-")
        #$folder = $folder.split(".")
    }

    write-host($folder[0])
    $folderName = $csv_source + "\" + $folder[0]
    if (Test-Path $folderName) {
    
        Write-Host "Folder Exists"
    }
    else {
    
        #PowerShell Create directory if not exists
        New-Item $folderName -ItemType Directory
        Write-Host "Folder Created successfully"
    }

    foreach($i in $csv){
        $path = $csv_source + "\" + $i
        $destination = $folderName + "\" + $i
        Move-Item -Path $path -Destination $destination -Force
    }
    if(!$csv){

    }
}