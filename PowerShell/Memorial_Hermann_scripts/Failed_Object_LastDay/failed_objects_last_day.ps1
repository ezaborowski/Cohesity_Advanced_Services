### usage: ./failed_objects_last_day.ps1 -vip 10.10.10.10 -username admin -password pass

### process commandline arguments
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
    write-host "msiexec.exe /package PowerShell-7.2.4-win-x64.msi ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL=1 REGISTER_MANIFEST=1 USE_MU=1 ENABLE_MU=1"
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

function Get-CurrentUnixTimeStamp {
    [DateTime]$epoch = New-Object System.DateTime 1970, 1, 1, 0, 0, 0, 0, Utc
    [TimeSpan]$diff  = (Get-Date).ToUniversalTime() - $epoch
    return [int64][Math]::Floor($diff.TotalSeconds)
}

[string]$currentTimeEpoch = Get-CurrentUnixTimeStamp
$microDay = 86400000000

### Get the End Date (Updated for legacy PowerShell terminal)
# $enddate = Get-Date (Get-Date).ToUniversalTime() -UFormat %s
# $endtimeusecs = $enddate.PadRight(16,'0')
[string]$currentTimeEpoch = Get-CurrentUnixTimeStamp
$currentDateEpoch = $currentTimeEpoch.PadRight(16,'0')
$currentDateEpoch = $endtimeusecs

### Get the Start Date (Updated for legacy PowerShell terminal)
# $startdate = Get-Date (Get-Date).ToUniversalTime().AddDays(-1) -UFormat %s 
# $starttimeusecs = $startdate.PadRight(16,'0')
$starttimeusecs = ($currentDateEpoch - $microDay)

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