### usage: ./failed_objects_last_day.ps1 -vip 10.10.10.10 -username admin -password pass

### process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$vip,
    [Parameter(Mandatory = $True)][string]$username,
    [Parameter()][string]$domain = 'local',
    [Parameter()][switch]$useApiKey,
    [Parameter(Mandatory = $True)][string]$password = $null
)

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

### Get the Failed Object Details
$failedobjects = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kFailedObjectsReport`&startTimeUsecs=$starttimeusecs`&statuses=kError

### Capture the needed fields
$name = $clusterdetails.name
$ClusterId = $clusterdetails.id

$dateString = (get-date).ToString().Replace(' ','_').Replace('/','-').Replace(':','-')
$outfileName = "FailedObjectsLastDay-$dateString.csv" 
"Server,Object Name,Environment,Job Name,JobRun Type,Status,StartTime,Error" | Out-File -FilePath $outfileName

for ($index=0; $index -lt $failedobjects.protectionSourcesJobsSummary.protectionsource.name.Length; $index++)
{
$server = $failedobjects.protectionSourcesJobsSummary[${index}].protectionsource.registeredSource
$objectname = $failedobjects.protectionSourcesJobsSummary[${index}].protectionsource.name
$environment = $failedobjects.protectionSourcesJobsSummary[${index}].protectionsource.environment
$jobname = $failedobjects.protectionSourcesJobsSummary[${index}].jobName
$jobruntype = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunType
$status = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunStatus
$runstarttimeepoch = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunStartTimeUsecs -replace ".{6}$"
$failure = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunErrorMsg

$runstarttime = Get-Date -UnixTimeSeconds $runstarttimeepoch | Get-Date -Format G

"$server,$objectname,$environment,$jobname,$jobruntype,$status,$runstarttime,$failure" | Out-File -FilePath $outfileName -Append
}