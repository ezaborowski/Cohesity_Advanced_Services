### usage: ./clientSummaryPerCluster.ps1 

### process commandline arguments
[CmdletBinding()]
# param (
#     [Parameter()][string]$vips,
#     [Parameter()][string]$usernames,
#     [Parameter()][string]$domains,
#     [Parameter()][string]$passwords
# )

# example of hardcoding credentails:
param (
    [Parameter()][string]$vips = "10.26.1.15, 10.26.0.230",
    [Parameter()][string]$usernames = "ezabor, ezabor",
    [Parameter()][string]$domains = "sre.cohesity.com, sre.cohesity.com",
    [Parameter()][string]$passwords = "Cohesity#321, Cohesity#321"
)

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
 
    # Output Config
    $dateString = (get-date).ToString('yyyy-MM-dd')
    $clientSummary = "ClientSummaryReport-$dateString.csv"
    $outfileName_source = "ClientSummary_source-$dateString.csv" 
    $allClients = "AllClientsBackedUp-$dateString.csv" 
    $unsuccessfulClients = "UnsuccessfulClients-$dateString.csv" 
    $strikeSummary_source = "StrikeSummary_source-$dateString.csv" 
    $strikeSummary = "StrikeSummary-$dateString.csv" 
    "Object,Source,Job Name,Cluster,Status,Level,Size (Gb),Started,Ended,Duration,Expires,Total,Successful,Warning,Failed,Success(%)" | Out-File -FilePath $outfileName_source
    "Cluster,One Strike,Two Strikes,Three Strikes" | Out-File -FilePath $strikeSummary_source
  
    $source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"

    # Create folder and move old .csv files from previous runs
    $csv = Get-ChildItem $source\*.csv -Name
    if($csv){
        foreach($i in $csv){
            $folder = $i.split("-")
            $folder = $folder.split(".")
        }

        write-host($folder[1])
        $folderName = $source + "\" + $folder[1]
        if (Test-Path $folderName) {
        
            Write-Host "Folder Exists"
        }
        else {
        
            #PowerShell Create directory if not exists
            New-Item $folderName -ItemType Directory
            Write-Host "Folder Created successfully"
        }

        foreach($i in $csv){
            $path = $source + "\" + $i
            $destination = $folderName + "\" + $i
            Move-Item -Path $path -Destination $destination
        }
}

    # Get the End Date
    [long]$endtimeusecs = (([datetime]::Now)-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000

    # Get the Start Date (1 day ago)
    [long]$starttimeusecs = ((([datetime]::Now).AddDays(-1))-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000

    # Get the Start Date (3 days ago)
    [long]$failedstarttime = ((([datetime]::Now).AddDays(-3))-(Get-Date -Date '1/1/1970')).TotalMilliseconds * 1000
  
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

        # get the Cluster Information
        $clusterdetails = api get /public/cluster

        # get the Object Details
        $objectruns = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kProtectionSummaryByObjectTypeReport`&startTimeUsecs=$starttimeusecs

        ### Get the Failed Object Details
        $failedobjects = api get /public/reports/protectionSourcesJobsSummary?allUnderHierarchy=true`&endTimeUsecs=$endtimeusecs`&reportType=kFailedObjectsReport`&startTimeUsecs=$failedstarttime`&statuses=kError
        
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
                
                #pulling Cohesity Pollicy data to extrapolate Retention Period of backups
                $runs = api get /public/protectionJobs?names=$jobName
                foreach($run in $runs){
                    $policyId =$run.policyId
                    $policy= api get /public/protectionPolicies/$policyId 
                    if($policy){ 
                        [double]$policyRetention = $policy.daysToKeep
                    }
                }
                
                # Expires: Expiration date of Protection Job Run Object Snapshot
                $expires = @()
                if($policyRetention){
                    $expires = $runend.AddDays(+$policyRetention)
                }
                    
                "$objectName,$sourceName,$jobName,$clusterName,$status,$level,$sizeGb,$started,$runend,$duration,$expires,$totalsnapshots,$successfulruns,$warningsnapshots,$errorsnapshots,$successpercent" | Out-File -FilePath $outfileName_source -Append
            }
        }

        # Strike Summary
        foreach($failedobject in $failedobjects){
            
            # checking if the numErrors in last 3 days is less than or equal to 3
            $failedobject = $failedobject.protectionSourcesJobsSummary
            $numerrors = $failedobject.numErrors

            if ($numerrors -eq 3)
                {
                $objectname = $failedobject.protectionsource.name
                $environment = $failedobject.protectionsource.environment
                $jobname = $failedobject.jobName
                $jobruntype = $failedobject.lastRunType
                $failure = $failedobject.lastRunErrorMsg
                $errorCount3 = $numerrors.count


                "$clusterName,,,$errorCount3" | Out-File -FilePath $strikeSummary_source -Append
                }

            if ($numerrors -eq 2)
                {
                $objectname = $failedobject.protectionsource.name
                $environment = $failedobject.protectionsource.environment
                $jobname = $failedobject.jobName
                $jobruntype = $failedobject.lastRunType
                $failure = $failedobject.lastRunErrorMsg
                $errorCount2 = $numerrors.count
                $errorCount = $errorCount2 - $errorCount3

                "$clusterName,,$errorCount," | Out-File -FilePath $strikeSummary_source -Append
                }

            if ($numerrors -eq 1)
                {
                $objectname = $failedobject.protectionsource.name
                $environment = $failedobject.protectionsource.environment
                $jobname = $failedobject.jobName
                $jobruntype = $failedobject.lastRunType
                $failure = $failedobject.lastRunErrorMsg
                $errorCount1 = $numerrors.count
                $errorCount = $errorCount1 - $errorCount3

                "$clusterName,$errorCount,," | Out-File -FilePath $strikeSummary_source -Append
                }

        }

    }

}
$stopQuery = $null
