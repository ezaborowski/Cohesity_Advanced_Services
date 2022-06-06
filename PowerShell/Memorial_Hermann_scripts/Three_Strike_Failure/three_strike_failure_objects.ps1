# ### usage: ./three_strike_failed_objects.ps1 -vip 10.10.10.10 -username admin -password pass

### process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$vip,
    [Parameter(Mandatory = $True)][string]$username,
    [Parameter()][string]$domain = 'local',
    [Parameter()][switch]$useApiKey,
    [Parameter(Mandatory = $True)][securestring]$password = $null
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
$startdate = Get-Date (Get-Date).ToUniversalTime().AddDays(-3) -UFormat %s 
$starttimeusecs = $startdate.PadRight(16,'0')

### Get the Failed Object Details
$failedobjects = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kFailedObjectsReport`&startTimeUsecs=$starttimeusecs`&statuses=kError


### Capture the needed fields
$name = $clusterdetails.name
$ClusterId = $clusterdetails.id

$dateString = (get-date).ToString().Replace(' ','_').Replace('/','-').Replace(':','-')
$outfileName = "ThreeStrikeObjectFailures-$dateString.csv" 
"Object Name,Job Name,Error Count" | Out-File -FilePath $outfileName


for ($index=0; $index -lt $failedobjects.protectionSourcesJobsSummary.protectionsource.name.Length; $index++)
    {

    ### Checking if the numErrors in last 3 days is greater or equal to 3
    $numerrors = $failedobjects.protectionSourcesJobsSummary[${index}].numErrors

    if ($numerrors -ge 3)
        {
        $objectname = $failedobjects.protectionSourcesJobsSummary[${index}].protectionsource.name
        $environment = $failedobjects.protectionSourcesJobsSummary[${index}].protectionsource.environment
        $jobname = $failedobjects.protectionSourcesJobsSummary[${index}].jobName
        $jobruntype = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunType
        $failure = $failedobjects.protectionSourcesJobsSummary[${index}].lastRunErrorMsg

        "$objectname,$jobname,$numerrors" | Out-File -FilePath $outfileName -Append
        }
    }