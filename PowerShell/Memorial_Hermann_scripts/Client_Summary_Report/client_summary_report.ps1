### usage: ./client_summary_report.ps1 -vip 10.10.10.10 -username admin -password pass

### process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$vip,
    [Parameter(Mandatory = $True)][string]$username,
    [Parameter()][string]$domain = 'local',
    [Parameter()][switch]$useApiKey,
    [Parameter(Mandatory = $True)][string]$password = $null
)

# ensure the environment meets the PowerShell Module requirements of 5.1 or above 
$version = $PSVersionTable.PSVersion
if($version.major -lt 5.1){
    write-host "Please upgrade the PowerShell Module to the current revision of 7.2.4 by downloading from the Microsoft site:"
    write-host "https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi"
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

#Get the End Date
$enddate = Get-Date (Get-Date).ToUniversalTime() -UFormat %s
$endtimeusecs = $enddate.PadRight(16,'0')

# Get the Start Date
$startdate = Get-Date (Get-Date).ToUniversalTime().AddDays(-1) -UFormat %s 
$starttimeusecs = $startdate.PadRight(16,'0')

### Get the Object Details
$objectruns = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kProtectionSummaryByObjectTypeReport`&startTimeUsecs=$starttimeusecs

### Capture the needed fields
$name = $clusterdetails.name
$ClusterId = $clusterdetails.id

# Output Config
$dateString = (get-date).ToString('yyyy-MM-dd')
#$dateString = (get-date).ToString().Replace(' ','_').Replace('/','-').Replace(':','-')
$outfileName = "ClientSummaryReport-$dateString.csv" 
"Object Name,Total Runs,Successful Runs,Failed Runs,Success(%)" | Out-File -FilePath $outfileName

for ($index=0; $index -lt $objectruns.protectionSourcesJobsSummary.protectionsource.name.Length; $index++)
    {
    $objectname = $objectruns.protectionSourcesJobsSummary[${index}].protectionSource.name
    $jobname = $objectruns.protectionSourcesJobsSummary[${index}].jobName
    $totalsnapshots = $objectruns.protectionSourcesJobsSummary[${index}].numSnapshots
    $errorsnapshots = $objectruns.protectionSourcesJobsSummary[${index}].numErrors
    $warningsnapshots = $objectruns.protectionSourcesJobsSummary[${index}].numWarnings

    $successfulruns = $totalsnapshots - ($errorsnapshots + $warningsnapshots)
    if($totalsnapshots -gt 0) {
        $successpercent = [math]::round($successfulruns/$totalsnapshots, 3)*100
    }
    else {
        $successpercent = 100
    }
        
    "$objectname,$totalsnapshots,$successfulruns,$errorsnapshots,$successpercent" | Out-File -FilePath $outfileName -Append
}