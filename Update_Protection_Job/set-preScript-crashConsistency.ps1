param(
    [Parameter(Mandatory = $True)][string]$username,
    [Parameter(Mandatory = $True)][string]$cluster,
    [Parameter()][string]$jobnamefile = '',
    [Parameter()][array]$jobname,
    [Parameter()][string]$quiesce,
    [Parameter()][string]$prescript
)
#process commmand line args ^


echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski - 10/12/2021                                                                      #"
echo "#Last Updated                                                                                                   #"
echo "#  -updated section:                                                                                            #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

#ensure the environment meets the prerequisites listed here: https://cohesity.github.io/cohesity-powershell-module/#/pre-requisites 

#tests if Cohesity.PowerShell is installed and if not, it installs it
if (Get-Module -ListAvailable -Name Cohesity.PowerShell) {
    Write-Host "Cohesity PowerShell Module already exists"
} 
else {
    Write-Host "Cohesity PowerShell Module does not exist. `nInstalling now..."
    Install-Module -Name Cohesity.PowerShell -Confirm:$false
}


#connect to Cohesity PowerShell API
Connect-CohesityCluster -Credential (Get-Credential -User $username) -Server $cluster -Port 46258

#---------------------------------------------------------------------------------------------------------------#

#iterates through Protection Job names
$jobnames = @()
if($jobnamefile -ne '' -and (Test-Path $jobnamefile -PathType Leaf)){
    $jobnames += Get-Content -Path $jobnamefile}

if($jobname){
    $jobnames += $jobname
}

#iterates through each Cohesity Protection Job Name
foreach ($job in $jobnames)
{
    #pulls the configuration of the Protection Job and converts to .json format
    $backupObj = Get-CohesityProtectionJob -Name "$job" | ConvertTo-Json | ConvertFrom-Json 

    #updates the Protection Job prescript name to 'CoBMR.bat'
    $backupObj.preBackupScript.incrementalBackupScript.scriptPath = "$prescript"

    #updates the Protection Job Crash Consistency
    $backupObj.quiesce = "$quiesce"

    #updates Cohesity Protection Job with new configuration parameters
    Set-CohesityProtectionJob -ProtectionJob $backupObj -Confirm:$false

    Write-Output "`n*************** UPDATE OF $job IS COMPLETE. ***************"

        }




<#
NAME     
    Set-CohesityProtectionJob                                                                                                                                                                                                                                                                                                                                                                                       
SYNOPSIS
    Updates a protection job.
    
    
SYNTAX
    Set-CohesityProtectionJob [-ProtectionJob] <Object> [-WhatIf] [-Confirm] [<CommonParameters>]
    
    
DESCRIPTION
    Returns the updated protection job.
    

RELATED LINKS
    https://cohesity.github.io/cohesity-powershell-module/#/README

REMARKS
    To see the examples, type: "Get-Help Set-CohesityProtectionJob -Examples"
    For more information, type: "Get-Help Set-CohesityProtectionJob -Detailed"
    For technical information, type: "Get-Help Set-CohesityProtectionJob -Full"
    For online help, type: "Get-Help Set-CohesityProtectionJob -Online"

PS /Users/erin.zaborowski> get-help Set-CohesityProtectionJob -full

NAME
    Set-CohesityProtectionJob
    
SYNOPSIS
    Updates a protection job.
    
    
SYNTAX
    Set-CohesityProtectionJob [-ProtectionJob] <Object> [-WhatIf] [-Confirm] [<CommonParameters>]
    
    
DESCRIPTION
    Returns the updated protection job.
    

PARAMETERS
    -ProtectionJob <Object>
        The updated protection job.
        
        Required?                    true
        Position?                    1
        Default value                
        Accept pipeline input?       true (ByValue)
        Accept wildcard characters?  false
        
    -WhatIf [<SwitchParameter>]
        
        Required?                    false
        Position?                    named
        Default value                
        Accept pipeline input?       false
        Accept wildcard characters?  false
        
    -Confirm [<SwitchParameter>]
        
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
    
OUTPUTS
    System.Object
    
    
NOTES
    
    
        Published by Cohesity
    
    -------------------------- EXAMPLE 1 --------------------------
    
    PS > $job = Get-CohesityProtectionJob -Names "jobnas"
    $job.name = "jobnas1"
    Set-CohesityProtectionJob -ProtectionJob $job
    Updates a protection job with the specified parameters, the object $job can also be piped.
    
    
    
    
    
    
    
RELATED LINKS
    https://cohesity.github.io/cohesity-powershell-module/#/README
#>