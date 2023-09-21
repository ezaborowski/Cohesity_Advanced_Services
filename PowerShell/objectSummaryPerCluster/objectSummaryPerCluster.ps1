### usage: ./clientSummaryPerCluster.ps1 

### process commandline arguments
[CmdletBinding()]
param (
    [Parameter()][string]$vips = "", # vips or FQDNs of Cohesity Clusters 
    [Parameter()][string]$usernames = "", # Cohesity UI Admin usernames
    [Parameter()][string]$domains = "", # Cohesity UI domains of usernames
    [Parameter()][string]$passwords = "", # Cohesity UI Admin passwords
    [Parameter()][string]$apiKeys = ""   # Cohesity UI APIkeys
)

# example:
# param (
#     [Parameter()][string]$vips = "10.26.0.160, 10.26.0.167",
#     [Parameter()][string]$usernames = "ezabor, ezabor",
#     [Parameter()][string]$domains = "cohesity.com, cohesity.com",
#     [Parameter()][string]$passwords = "Cohesity, Cohesity",
#     [Parameter()][string]$apiKeys = ""
# )

$source = $PSScriptRoot

### Logging
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

function runTimes{
    param ([int64]$timeUsecs)
    
    $timeEpoch = $timeUsecs -replace ".{6}$"
    [datetime]$timeHR = Get-Date -UnixTimeSeconds $timeEpoch | Get-Date -Format G

    return $timeHR    
}


# Size: Number of Logical Bytes Protected (Gb) for Object
$size = $object.numLogicalBytesProtected
$sizeGb = [math]::round([int64]$size/1073741824, 2)


# set static variables
$source = $PSScriptRoot
$dateString = (get-date).ToString('yyyy-MM-dd')
$dateTime = Get-Date -Format "dddd MM/dd/yyyy HH:mm"
$outfileName = "$PSScriptRoot\log-BackupSummary-$dateString.txt"


# ensure the environment meets the PowerShell Module requirements of 5.1 or above 
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    fail_log "Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site:"
    warn_log "https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi"
}
else {
    info_log "PowerShell Module is up to date."

    # source the cohesity-api helper code
    . $(Join-Path -Path $PSScriptRoot -ChildPath cohesity-api.ps1)

    # compiling credentials per Cohesity Cluster
    $credentials = @()
    $vip = $vips -split ","
        $vip = $vip.replace(' ', '')
    $username = $usernames -split(",")
        $username = $username.replace(' ', '')
    $domain = $domains -split(",")
        $domain = $domain.replace(' ', '')
    
    if(!$apiKeys){
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
    if(!$passwords){
        $apiKey = $apiKeys -split(",")
            $apiKey = $apiKey.replace(' ', '')
        For($i=0; $i -lt $username.count; $i++){
            $credentials += [pscustomobject] @{
                username = $username[$i]
                vip = $vip[$i]
                domain = $domain[$i]
                apiKey = $apiKey[$i]
                }
            }
        }
    

    # create folder for current datestring directories
    $opFolder = "Output"

    if (Test-Path $source\$opFolder) {
        info_log "Output Folder Exists"
    }
    else {
        # PowerShell Create directory if not exists
        New-Item $opFolder -ItemType Directory
        pass_log "Output Folder Created successfully"
    }

    $op_source = "$source\$opFolder"

    # create folder for current .csv files
    $csvFolder = "$dateString"
    $csv_source = "$op_source\$csvFolder"

    if (Test-Path $csv_source) {
        info_log "Output Folder Exists"
    }
    else {
        #PowerShell Create directory if not exists
        New-Item $csv_source -ItemType Directory
        pass_log "Current Run Folder Created successfully"
    }


    # Output Config
    #$clientSummary = "$csv_source\ClientSummaryReport.csv"
    $fullClientSummary = "$csv_source\FullClientSummary.csv" 
    #$allClients = "$csv_source\AllClientsBackedUp.csv" 
    $unsuccessfulClients = "$csv_source\UnsuccessfulClients.csv" 
    
    # Output headers in csv files
    "Cluster,Job Name,Source,Object,Status,Level,Size (Gb),Started,Ended,Duration,Expires,Total,Successful,Warning,Failed,Success(%)" | Out-File -FilePath $fullClientSummary

    #"Cluster,Total,Successful,Warning,Failed,Success(%)" | Out-File -FilePath $clientSummary

    "Object,Source,Job Name,Cluster,Status,Level,Size (Gb),Started,Ended,Duration,Expires" | Out-File -FilePath $unsuccessfulClients
    
    # Validate that files were created
    $results = @("FullClientSummary.csv", "UnsuccessfulClients.csv") 
    foreach($result in $results) {
        if(Test-Path $csv_source\$result) {
            pass_log "Initial $result file created successfully!"
        }
        else{
            fail_log "Initial $result file not created successfully!"
            break
        }
    }

    # Get the End Date
    [long]$endtimeusecs = (([datetime]::Now)-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000

    # Get the Start Date (1 day ago)
    [long]$starttimeusecs = ((([datetime]::Now).AddDays(-1))-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000

    # Get the Start Date (3 days ago)
    #[long]$failedstarttime = ((([datetime]::Now).AddDays(-3))-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000
  
    foreach($credential in $credentials){
        # authenticate to Cohesity Cluster
        ForEach-Object{
            if(!$credential.apiKey){
                apiauth -vip $credential.vip -username $credential.username -domain $credential.domain -password $credential.password    
                }
            if(!$credential.password){
                apiauth -vip $credential.vip -username $credential.username -domain $credential.domain -apiKey $credential.apiKey    
            }
        }
        if(!$credential){
            Write-host "A complete set of credentials was not input."
            }


        # get the Cluster Information
        $clusterdetails = api get /public/cluster

        # get the Object Details
        $objectruns = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kProtectionSummaryByObjectTypeReport`&startTimeUsecs=$starttimeusecs

        ### Get the Failed Object Details
        #$failedobjects = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kFailedObjectsReport`&startTimeUsecs=$failedstarttime`&statuses=kError

        
        # capture the needed fields
        $clusterName = $clusterdetails.name

        foreach($objectrun in $objectruns){

            $objectrun = $objectrun.protectionSourcesJobsSummary
            foreach($object in $objectrun){
            
                $objectName = $object.protectionSource.name
                $sourceName = $object.registeredSource
                $jobName = $object.jobName
                $totalsnapshots = $object.numSnapshots
                $errorsnapshots = $object.numErrors
                $warningsnapshots = $object.numWarnings
                $cohesityStatus = $object.lastRunStatus
                    if($cohesityStatus -eq "kSuccess"){
                        $status = "Success"
                    }
                    elseif($cohesityStatus -eq "kError"){
                        $status = "Error"
                    }
                    elseif($cohesityStatus -eq "kWarning"){
                        $status = "Warning"
                    }
                    elseif($cohesityStatus -eq "kWarn"){
                        $status = "Warning"
                    }
                    elseif($cohesityStatus -eq "kFail"){
                        $status = "Failure"
                    }
                    else{
                        $status = $cohesityStatus
                    }

                $cohesityLevel = $object.lastRunType
                    if($cohesityLevel -eq "kRegular"){
                        $level = "Regular"
                    }
                    elseif($cohesityLevel -eq "kLog"){
                        $level = "Log"
                    }
                    elseif($cohesityLevel -eq "kFull"){
                        $level = "Full"
                    }
                    else{
                        $level = $cohesityLevel
                    }

                $runstarttimeepoch = $object.lastRunStartTimeUsecs -replace ".{6}$"
                $runendtimeepoch = $object.lastRunEndTimeUsecs -replace ".{6}$"

                [int64]$successfulruns = [int64]$totalsnapshots - ([int64]$errorsnapshots + [int64]$warningsnapshots)
                if($totalsnapshots -gt 0) {
                    $successpercent = [math]::round($successfulruns/$totalsnapshots, 3)*100
                }
                else {
                    $successpercent = 100
                }

                # Size: Number of Logical Bytes Protected (Gb) for Object
                $size = $object.numLogicalBytesProtected
                $sizeGb = [math]::round([int64]$size/1073741824, 2)
            
                [datetime]$started = Get-Date -UnixTimeSeconds $runstarttimeepoch | Get-Date -Format G
                [datetime]$runend = Get-Date -UnixTimeSeconds $runendtimeepoch | Get-Date -Format G
            
                # Duration: Length of Protection Job Run
                $endTime = $object.lastRunEndTimeUsecs
                $startTime = $object.lastRunStartTimeUsecs
                $timeSpent = $endTime - $startTime
                $timeSpent = ($timeSpent/1000)
                $duration = [TimeSpan]::FromMilliseconds([double]$timeSpent)
                
                # Pulling Cohesity Pollicy data to extrapolate Retention Period of backups
                $runs = api get /public/protectionJobs?names=$jobName
                foreach($run in $runs){
                    $policyId = $run.policyId
                    $policy = api get /public/protectionPolicies/$policyId 
                    if($policy){ 
                        [double]$policyRetention = $policy.daysToKeep
                    }
                }
                
                # Expires: Expiration date of Protection Job Run Object Snapshot
                $expires = @()
                if($policyRetention){
                    $expires = $runend.AddDays(+$policyRetention)
                }
                    
                # Output data to csv files
                "$clusterName,$jobName,$sourceName,$objectName,$status,$level,$sizeGb,$started,$runend,$duration,$expires,$totalsnapshots,$successfulruns,$warningsnapshots,$errorsnapshots,$successpercent" | Out-File -FilePath $fullClientSummary -Append

                if($status -eq "Error"){
                    "$clusterName,$jobName,$sourceName,$objectName,$status,$level,$sizeGb,$started,$runend,$duration,$expires" | Out-File -FilePath $unsuccessfulClients -Append 
                }
            }
        }
    }
}