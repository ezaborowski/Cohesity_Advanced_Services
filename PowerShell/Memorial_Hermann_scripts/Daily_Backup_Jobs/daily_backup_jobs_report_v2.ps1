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

# source the cohesity-api helper code
. $(Join-Path -Path $PSScriptRoot -ChildPath cohesity-api.ps1)

# authenticate
if($useApiKey){
    apiauth -vip $vip -username $username -domain $domain -useApiKey -password $password
}else{
    apiauth -vip $server -username $username -domain local -password $password
}

# Get the Cluster Information
$clusterdetails = api get /public/cluster
$clusterId = $clusterdetails.Id 
$jobName = $clusterdetails.jobName

# Get the End Date
$enddate = Get-Date (Get-Date).ToUniversalTime() -UFormat %s
$endtimeusecs = $enddate.PadRight(16,'0')

# Get the Start Date
$startdate = Get-Date (Get-Date).ToUniversalTime().AddDays(-1) -UFormat %s 
$starttimeusecs = $startdate.PadRight(16,'0')

# Get Current Date
$dateString = (get-date).ToString().Replace(' ','_').Replace('/','-').Replace(':','-')

# Get the Object Details
$jobs = api get /public/protectionJobs
$jobIds = $jobs.Id

foreach($jobId in $jobIds){
    $objectruns = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kProtectionSummaryByObjectTypeReport`&startTimeUsecs=$starttimeusecs`&jobids=$jobId


# Create Output file

$outfileName = "DailyBackupObjectsReport-$dateString.csv" 

"Client,Server,Status,Level,Size (Gb),Started,Duration,Expires" | Out-File -FilePath $outfileName

    # Iterate through each Protection Job Run
    foreach($objectrun in $objectruns){
        $protectionruns = $objectrun.protectionSourcesJobsSummary
        foreach($protectionrun in $protectionruns){
            $jobName = $protectionrun.jobName

            # Client: Object
            $client = $protectionrun.protectionSource.name
            
            # Server: Object Source
            $server = $protectionrun.registeredSource

            # $parentIds = $protectionrun.protectionSource.parentId
            # foreach($parentId in $parentIds){
            #     $environment = $protectionrun.protectionSource.environment
            #     # if(!$environment){
            #     #     $serverObject = api get /public/protectionSources/objects/$parentId
            #     #     $server = $serverObject.name
            #     #     }
            #     if($environment -eq "kView"){
            #             $server = $client
            #         }
            #     else{
            #         $serverObject = api get /public/protectionSources/objects/$parentId
            #         $server = $serverObject.name
            #     }   
            # }
            
            # Status: Last Protection Job Run Status
            $status = $protectionrun.lastRunStatus

            # Level: Last Protection Job Run Type
            $level = $protectionrun.lastRunType

            # Size: Number of Logical Bytes Protected (Gb) for Object
            $size = $protectionrun.numLogicalBytesProtected
            #$size = [string]$size
            $sizeGb = ($size/1e+9)
            
            # Started: Start Time of Protection Job Run
            $startTime = $protectionrun.lastRunStartTimeUsecs
            $runstarttimeepoch = $protectionrun.lastRunStartTimeUsecs -replace ".{6}$"
            $runstarttimeepoch = [string]$runstarttimeepoch
            $started = Get-Date -UnixTimeSeconds $runstarttimeepoch | Get-Date -Format G

            # Ended: End Time of Protection Job Run
            $endTime = $protectionrun.lastRunEndTimeUsecs
            $runendtimeepoch = $protectionrun.lastRunEndTimeUsecs -replace ".{6}$"
            $runendtimeepoch = $runendtimeepoch
            [datetime]$runend = Get-Date -UnixTimeSeconds $runendtimeepoch | Get-Date -Format G

            # Duration: Length of Protection Job Run
            $timeSpent = $endTime - $startTime
            #$duration = [TimeSpan]::FromMilliseconds([double]$timeSpent)
            $timeSpent = ($timeSpent/1000)
            $duration = [TimeSpan]::FromMilliseconds([double]$timeSpent)
            
            #pulling Cohesity Pollicy data to extrapolate Retention Period of backups
            $runs = api get /public/protectionJobs/$jobId
            $policyId =$runs.policyId
            $policy= api get /public/protectionPolicies/$policyId  
            [double]$policyRetention = $policy.daysToKeep

            # Expires: Expiration date of Protection Job Run Object Snapshot
            $expires = @()
            $expires = $runend.AddDays(+$policyRetention)

            "$client,$server,$status,$level,$sizeGb,$started,$duration,$expires" | Out-File -FilePath $outfileName -Append

        }
    }
}