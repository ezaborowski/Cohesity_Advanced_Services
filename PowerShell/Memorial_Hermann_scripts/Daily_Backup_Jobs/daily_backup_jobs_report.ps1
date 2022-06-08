### usage: ./daily_backup_jobs_report.ps1 -vip 10.10.10.10 -username admin -password pass

## process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$vip,
    [Parameter(Mandatory = $True)][string]$username,
    [Parameter()][string]$domain = 'local',
    [Parameter()][switch]$useApiKey,
    [Parameter(Mandatory = $True)][securestring]$password = $null
)

# ensure the environment meets the PowerShell Module requirements of 5.1 or above 
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    write-host "Please upgrade the PowerShell Module to the current revision of 7.2.4 by running the following command from your PowerShell prompt:"
    write-host "msiexec.exe /package PowerShell-7.2.4-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL=1 REGISTER_MANIFEST=1 USE_MU=1 ENABLE_MU=1"
}
else {
    write-host "PowerShell Module is up to date."
}

### source the cohesity-api helper code
. $(Join-Path -Path $PSScriptRoot -ChildPath cohesity-api.ps1)

### authenticate
if($useApiKey){
    apiauth -vip $vip -username $username -domain $domain -useApiKey -password $password
}else{
    apiauth -vip $vip -username $username -domain $domain -password $password
}

### Get the Cluster Information
$clusterdetails = api get /public/cluster

### Get the End Date
$enddate = Get-Date (Get-Date).ToUniversalTime() -UFormat %s
$endtimeusecs = $enddate.PadRight(16,'0')

### Get the Start Date
$startdate = Get-Date (Get-Date).ToUniversalTime().AddDays(-1) -UFormat %s 
$starttimeusecs = $startdate.PadRight(16,'0')

### Get the Object Details
$objectruns = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kProtectionSummaryByObjectTypeReport`&startTimeUsecs=$starttimeusecs

### Capture the needed fields
$name = $clusterdetails.name
$ClusterId = $clusterdetails.id

$dateString = (get-date).ToString().Replace(' ','_').Replace('/','-').Replace(':','-')
$outfileName = "DailyBackupObjectsReport-$dateString.csv" 

"Client,Server,Status,Level,Size (Gb),Started,Duration (min),Expires" | Out-File -FilePath $outfileName

for ($index=0; $index -lt $objectruns.protectionSourcesJobsSummary.protectionsource.name.Length; $index++)
    {
    
    $jobName = $objectruns.protectionSourcesJobsSummary[${index}].jobName

    # Client: Object
    $client = $objectruns.protectionSourcesJobsSummary[${index}].protectionSource.name
    
    # Server: Object Source
    $server = $objectruns.protectionSourcesJobsSummary[${index}].registeredSource

    #$jobname = $objectruns.protectionSourcesJobsSummary[${index}].jobName
    #$environment = $objectruns.protectionSourcesJobsSummary[${index}].protectionSource.environment

    # Status: Last Protection Job Run Status
    $status = $objectruns.protectionSourcesJobsSummary[${index}].lastRunStatus

    # Level: Last Protection Job Run Type
    $level = $objectruns.protectionSourcesJobsSummary[${index}].lastRunType

    # Started: Start Time of Protection Job Run
    $runstarttimeepoch = $objectruns.protectionSourcesJobsSummary[${index}].lastRunStartTimeUsecs -replace ".{6}$"

    # Ended: End Time of Protection Job Run
    $runendtimeepoch = $objectruns.protectionSourcesJobsSummary[${index}].lastRunEndTimeUsecs -replace ".{6}$"
    
    #$dataread = $objectruns.protectionSourcesJobsSummary[${index}].numDataReadBytes
    #$datareadMB = [math]::round($dataread/1048576, 2)

    # Size: Number of Logical Bytes Protected (Gb) for Object
    $size = $objectruns.protectionSourcesJobsSummary[${index}].numLogicalBytesProtected
    $sizeGb = [math]::round($size/1073741824, 2)

    $started = Get-Date -UnixTimeSeconds $runstarttimeepoch | Get-Date -Format G
    [datetime]$runend = Get-Date -UnixTimeSeconds $runendtimeepoch | Get-Date -Format G

    # Duration: Length of Protection Job Run
    $endTime = $runendtimeepoch = $objectruns.protectionSourcesJobsSummary[${index}].lastRunEndTimeUsecs
    $startTime = $objectruns.protectionSourcesJobsSummary[${index}].lastRunStartTimeUsecs
    $timeSpent = $endTime - $startTime
    $timeSpent = ($timeSpent/1000)
    $duration = [TimeSpan]::FromMilliseconds([double]$timeSpent)
    
    #pulling Cohesity Pollicy data to extrapolate Retention Period of backups
    $runs = api get /public/protectionJobs?names=$jobName
    foreach($run in $runs){
        $policyId =$run.policyId
        $policy= api get /public/protectionPolicies/$policyId  
        [double]$policyRetention = $policy.daysToKeep
    }
    
    # Expires: Expiration date of Protection Job Run Object Snapshot
    $expires = @()
    $expires = $runend.AddDays(+$policyRetention)

    "$client,$server,$status,$level,$sizeGb,$started,$duration,$expires" | Out-File -FilePath $outfileName -Append
}