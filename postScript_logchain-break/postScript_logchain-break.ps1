
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski - 10/12/2021                                                                      #"
echo "#Last Updated                                                                                                   #"
echo "#  -updated section:                                                                                            #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

#ensure the environment meets the prerequisites listed here: https://cohesity.github.io/cohesity-powershell-module/#/pre-requisites 

#checks if Cohesity.PowerShell is installed and if not, installs module
if (Get-Module -ListAvailable -Name Cohesity.PowerShell) {
    Write-Host "Cohesity PowerShell Module already exists"
} 
else {
    Write-Host "Cohesity PowerShell Module does not exist. `nInstalling now..."
    Install-Module -Name Cohesity.PowerShell -Confirm:$false
}

#---------------------------------------------------------------------------------------------------------------#

#Please input the Cohesity UI admin username after the equals sign
$username = "admin"

#Please input the Cohesity UI admin password after the equals sign
$password = "admin"

#Please input the full Cohesity Cluster hostname or IP address (ex: servername.domain.com or 172.20.1.55) after the equals sign
$server = "localhost"

#Please input the name of the Protection Job
$pJob = "erin_sql_1"

$secureStringPwd = $password | ConvertTo-SecureString -AsPlainText -Force 
#$creds = New-Object System.Management.Automation.PSCredential -ArgumentList $user, $secureStringPwd

$Credentials = New-Object System.Management.Automation.PSCredential -ArgumentList ($username, $secureStringPwd)

#---------------------------------------------------------------------------------------------------------------#

#connect to Cohesity PowerShell API
Connect-CohesityCluster -Credential $Credentials -Server $server -Port 46258

$backupObj = Get-CohesityProtectionJobRun -JobName $pJob -NumRuns 1 | ConvertTo-Json | ConvertFrom-Json 
$runType = $backupObj.backupRun.runType
$status = $backupObj.backupRun.status
    if ($runType -eq "kLog" -AND $status -eq "kFailure") {
            Start-CohesityProtectionJob -Name $pJob -RunType KRegular 
}
else {
    break
}

#---------------------------------------------------------------------------------------------------------------#

#pulls the failed Source Ids from Protection Job error 

#pulls the configuration of the Protection Job and converts to .json format
# $backupObj = Get-CohesityProtectionJobRun -JobName $pJob -RunTypes kLog -NumRuns 1 | ConvertTo-Json | ConvertFrom-Json 
# if ($backupObj.backupRun.status == "kFailure") {
#     if ($backupObj.backupRun.error -Like "*logchain*") {
#         Start-CohesityProtectionJob -Name $pJob -RunType KRegular -SourceIds $backupObj.backupRun.error.Split(',')[1].split(',')
#     }

# }

# $backupObj.backupRun.status

#---------------------------------------------------------------------------------------------------------------#


<#
NAME
    Start-CohesityProtectionJob
    
SYNOPSIS
    Immediately starts a protection job run.
    
    
SYNTAX
    Start-CohesityProtectionJob -Id <long> [-CopyRunTargets <RunJobSnapshotTarget[]>] [-RunType {KRegular | KFull | KLog | KSystem}] [-SourceIds <long[]>] [<CommonParameters>]
    
    Start-CohesityProtectionJob -Name <string> [-CopyRunTargets <RunJobSnapshotTarget[]>] [-RunType {KRegular | KFull | KLog | KSystem}] [-SourceIds <long[]>] [<CommonParameters>]
    
    
DESCRIPTION
    Immediately starts a protection job run. A protection policy associated with the job may define various backup run types: Regular (Incremental, CBT utilized), Full (CBT not utilized), Log, System. 
    The passed in run type defines what type of backup is performed by the job run. The schedule defined in the policy for the backup run type is ignored but other settings such as the snapshot 
    retention and retry settings are used. Returns success if the job run starts.
    

PARAMETERS
    -Id <long>
        Specifies a unique id of the protection job.
        
        Required?                    true
        Position?                    named
        Default value                0
        Accept pipeline input?       true (ByPropertyName)
        Accept wildcard characters?  false
        
    -Name <string>
        Specifies the name of the protection job.
        
        Required?                    true
        Position?                    named
        Default value                
        Accept pipeline input?       false
        Accept wildcard characters?  false
        
    -RunType <RunTypeEnum>
        Specifies the type of backup. If not specified, "KRegular" is assumed.
        
        Possible values: KRegular, KFull, KLog, KSystem
        
        Required?                    false
        Position?                    named
        Default value                KRegular
        Accept pipeline input?       false
        Accept wildcard characters?  false
        
    -SourceIds <long[]>
        If you want to back up only a subset of sources that are protected by the job in this run.
        
        Required?                    false
        Position?                    named
        Default value                
        Accept pipeline input?       false
        Accept wildcard characters?  false
        
    -CopyRunTargets <RunJobSnapshotTarget[]>
        Set if you want specific replication or archival associated with the policy to run.
        
        Required?                    false
        Position?                    named
        Default value                
        Accept pipeline input?       false
        Accept wildcard characters?  false
        
    <CommonParameters>
        This cmdlet supports the common parameters: Verbose, Debug,
        ErrorAction, ErrorVariable, WarningAction, WarningVariable,
        OutBuffer, PipelineVariable, and OutVariable. For more information, see
        about_CommonParameters (https://go.microsoft.com/fwlink/?LinkID=113216). 
    
INPUTS
    System.Int64
        Specifies a unique id of the protection job.
    
    
OUTPUTS
    
    ----------  EXAMPLE 1  ----------
    
    PS>Start-CohesityProtectionJob -Id 1234
    
    Immediately starts a job run for the given protection job.
    
RELATED LINKS
#>