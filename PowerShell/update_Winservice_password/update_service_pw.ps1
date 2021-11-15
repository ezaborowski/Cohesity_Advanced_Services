 
param(
    [Parameter(Mandatory = $True)][string]$serviceName,
    [Parameter(Mandatory = $True)][string]$serviceUser,
    [Parameter()][string]$hostnameFile = '',
    [Parameter()][array]$hostname
)
# process commmand line args ^

echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski - 11/15/2021                                                                      #"
echo "#Last Updated                                                                                                   #"
echo "#  -updated section: ALL                                                                                           #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

# update_service_pw.ps1 -hostnameFile "text_file_of_server_hostnames.txt" -serviceName CohesityAgent -serviceUser "service_username"
# update_service_pw.ps1 -hostname "hostname_of_server" -serviceName CohesityAgent -serviceUser "service_username"

# get the secure string password 
$Password = Read-Host -Prompt "Enter password for $serviceUser" -AsSecureString

# Extracting password from secure string to be passed to Change method
$BSTR = [system.runtime.interopservices.marshal]::SecureStringToBSTR($Password)
  $Password = [system.runtime.interopservices.marshal]::PtrToStringAuto($BSTR)

# extrapolating hostnames
$hostnames = @()
if($hostnameFile -ne '' -and (Test-Path $hostnameFile -PathType Leaf)){
    $hostnames += Get-Content -Path $hostnameFile}

if($hostname){
    $hostnames += $hostname
}

# iterating through each server 
# updating password and restarting service
foreach ($server in $hostnames){

    $filter = 'Name=' + "'" + "$serviceName" + "'" + ''
    if ($service = Get-WmiObject -ComputerName $server -Class Win32_Service -Filter $filter -ErrorAction SilentlyContinue) {

    $service.Change($Null,$Null,$Null,$Null,$Null,$Null,$Null,$Password,$Null,$Null,$Null)

    # pulling Service status
    $agent = Get-Service -ComputerName $server -Name CohesityAgent

    # stop service
    while ($agent.Status -eq 'Running') {
        $service.StopService()
        sleep 2
        $agent.Refresh()
        if ($agent.Status -ne 'Running') {
            Write-Output "`n~~~~~~~~~~~ $serviceName Service on $server has successfully stopped. ~~~~~~~~~~~`n"
            break
            }
        }

    # start service
    while ($agent.Status -ne 'Running') {
        $service.StartService()
        sleep 2
        $agent.Refresh()
        if ($agent.Status -eq 'Running') {
            Write-Output "`n~~~~~~~~~~~ $serviceName Service on $server has successfully started. ~~~~~~~~~~~`n"
            break
            }
        }
    
    Write-Output "`n*************** UPDATE OF $serviceName on $server IS COMPLETE. ***************`n"
    }
    else {
        Write-Output "`n*************** UPDATE OF $serviceName on $server FAILED. ***************`n"
    }
}

# Remove-Variable Password,BSTR

#   [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
   
