# process commandline arguments
[CmdletBinding()]
param (
    [Parameter(Mandatory = $True)][string]$apiKey,  # apiKey
    [Parameter(Mandatory = $True)][string]$regionId,  # DMaaS SQL Source Region Id
    [Parameter()][array]$physFQDN,  # physical Source FQDN
    [Parameter()][string]$physList = '',  # optional textfile of Physical Servers to protect
    [Parameter()][string]$priority = 'kMedium',  # protection instance priority (default is kMedium)
    [Parameter()][string]$qosPolicy = 'kBackupSSD',  # QoS policy optimizes throughput performance (default is kBackupSSD)
    [Parameter()][string]$abort = 'false', # abort during blackout periods (default is false)
    [Parameter()][string]$environment = 'kPhysical',  # environment type (kPhysical, kVMware, kAWS, kO365, kNetapp, kSQL, kOracle) (default is kPhysical)
    [Parameter()][string]$volumes = $ALL_LOCAL_DRIVES,  # which volumes to backup
    [Parameter()][bool]$autoProtected = $true,  # whether Physical objects are autoProtected (default is true)
    [Parameter()][bool]$skipNested = $false,  # whether to skip backing up nested volumes (default is false)
    [Parameter()][bool]$usePathLevel = $true,  # whether to use Path Level Skip Nested Volume Setting (default is true)
    [Parameter()][bool]$nasSymlink = $false,  # whether to follow NAS Symlink targets (default is false)
    [Parameter()][bool]$quiesce = $true,  # optional whether to quiesce the backups (Default is true) 
    [Parameter()][bool]$contOnFail = $true,  # optional whether to continue on quiesce failure (Default is true) 
    [Parameter()][bool]$sourceSideDedup = $false,  # optional whether to perform Source Side Deduplication (Default is false) 
    [Parameter()][bool]$index = $false,  # optional whether objects are indexed (default is false)
    [Parameter()][bool]$skipPhysicalRDMDisks = $false,  # optional whether to skip backing up Physical RDM Disks (Default is false)
    [Parameter()][string]$startTime = '20:00',  # e.g. 23:30 for 11:30 PM
    [Parameter()][string]$timeZone = 'America/New_York', # default 'America/New_York'
    [Parameter()][int]$incSLA = 60,  # incremental SLA minutes
    [Parameter()][int]$fullSLA = 120  # full SLA minutes
)

# validate startTime
$hour, $minute = $startTime.split(':')
$tempInt = ''
if(! (($hour -and $minute) -or ([int]::TryParse($hour,[ref]$tempInt) -and [int]::TryParse($minute,[ref]$tempInt)))){
    Write-Host "Please provide a valid start time" -ForegroundColor Yellow
    exit
}

# gather list of SQL Sources to Register
$physServersToAdd = @()
foreach($phys in $physFQDN){
    $physServersToAdd += $phys
}
if ('' -ne $physList){
    if(Test-Path -Path $physList -PathType Leaf){
        $physFQDN = Get-Content $physList
        foreach($phys in $physFQDN){
            $physServersToAdd += [string]$phys
        }
    }else{
        Write-Host "Physical Server list $physList not found!" -ForegroundColor Yellow
        exit
    }
}

$physServersToAdd = @($physServersToAdd | Where-Object {$_ -ne ''})

if($physServersToAdd.Count -eq 0){
    Write-Host "No Physical Servers specified" -ForegroundColor Yellow
    exit
}

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"

# test API Connection
Write-host "Testing API Connection...`n"
$headers.Add("apiKey", "$apiKey")
$apiTest = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/public/mcm/clusters/info' -Method 'GET' -Headers $headers 

if(!$apiTest){
    write-host "Invalid API Key" -ForegroundColor Yellow
    exit
}

# validate DMaaS Tenant ID
Write-host "Validating Tenant ID...`n"
$headers.Add("accept", "application/json, text/plain, */*")
#$headers.Add('content-type: application/json')
$tenant = Invoke-RestMethod 'https://helios.cohesity.com/irisservices/api/v1/mcm/userInfo' -Method 'GET' -Headers $headers

$tenantId = $tenant.user.profiles.tenantId 
Write-host "Tenant ID: " $tenantId


# validate DMaaS Region ID
Write-host "`nValidating Region ID..."
$region = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/dms/tenants/regions?tenantId=$tenantId" -Method 'GET' -Headers $headers

foreach($regionIds in $region){

    $regionIds = $region.tenantRegionInfoList.regionId

    $compareRegion = Compare-Object -IncludeEqual -ReferenceObject $regionIds -DifferenceObject $regionId -ExcludeDifferent

    if(!$compareRegion){
        write-host "There are no matching Region Ids asssociated with the confirmed Tenant ID." -ForegroundColor Yellow
        exit
    }

}

$headers.Add("regionId", "$regionId")


Write-Host "Finding protection policy"

$policy = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/data-protect/policies?types=DMaaSPolicy" -Method 'GET' -Headers $headers 

foreach($pol in $policy.policies){
    if($pol.policies.name -eq "$policyName"){
    }
}
$policyId = $pol.id

if(!$policyId){
    write-host "Policy $policyName not found" -ForegroundColor Yellow
    exit
}


# find Physical source
Write-host "Finding registered Physical Source"

foreach($physServer in $physServersToAdd){

    Write-Host "Finding Physical Server $physServer"

    $sources = Invoke-RestMethod "https://helios.cohesity.com/v2/mcm/data-protect/sources" -Method 'GET' -Headers $headers
    $source = $sources.sources | where-object {$_.name -eq $physServer}

# configure protection parameters
    $body = "{
        `n    `"policyId`": `"$policyId`",
        `n    `"startTime`": {
        `n        `"hour`": [int64]$hour,
        `n        `"minute`": [int64]$minute,
        `n        `"timeZone`": `"$timeZone`"
        `n    },
        `n    `"priority`": `"$priority`",
        `n    `"sla`": [
        `n        {
        `n            `"backupRunType`": `"kFull`",
        `n            `"slaMinutes`": $fullSLA
        `n        },
        `n        {
        `n            `"backupRunType`": `"kIncremental`",
        `n            `"slaMinutes`": $incSLA
        `n        }
        `n    ],
        `n    `"qosPolicy`": `"$qosPolicy`",
        `n    `"abortInBlackouts`": $abort,
        `n    `"objects`": [
        `n        {
        `n            `"environment`": `"$environment`",
        `n            `"physicalParams`":{
        `n                     `"objectProtectionType`":`"kFile`",
        `n                     `"fileObjectProtectionTypeParams`":{
        `n                              `"indexingPolicy`":{
        `n                                  `"enableIndexing`":$index,
        `n                                  `"includePaths`":[],
        `n                                  `"excludePaths`":[]
        `n                                },
        `n                          `"objects`":[{
        `n                              `"id`":$sourceId,
        `n                              `"filePaths`":[{
        `n                                  `"includedPath`":`"$volumes`",
        `n                                  `"excludedPaths`":[],
        `n                                  `"skipNestedVolumes`": $skipNested
        `n                                  }
        `n                              ],
        `n                              `"usesPathLevelSkipNestedVolumeSetting`": $usePathLevel,
        `n                              `"nestedVolumeTypesToSkip`":[],
        `n                              `"followNasSymlinkTarget`": $nasSymlink
        `n                              }
        `n                          ],
        `n                          `"performSourceSideDeduplication`": $sourceSideDedup,
        `n                          `"quiesce`": $quiesce,
        `n                          `"continueOnQuiesceFailure`": $contOnFail,
        `n                          `"dedupExclusionSourceIds`":[],
        `n                          `"globalExcludePaths`":[]
        `n                      }
        `n                  }
        `n              }
        `n              ]
        `n          }            
        `n        }
        `n    ]
        `n} "


        # indexing includePaths
        # if($indexInclude){
        #     $body.objects.physicalparams.fileObjectProtectionTypeParams.indexingPolicy.indexinclude = @(
        #         @{
        #             "$indexInclude"
        #         }
        #     )
        # indexing excludePaths
        # backup includePaths
        # backup excludePaths
        # nestedVolumeTypesToSkip
        # dedupExclusionSourceIds
        # globalExcludePaths


        


        if($source){
            Write-Host "Protecting $physServer"
            # $response = api post -v2 data-protect/protected-objects $protectionParams
            $response = Invoke-RestMethod 'https://helios.cohesity.com/v2/data-protect/protected-objects' -Method 'POST' -Headers $headers -Body $body -ContentType 'application/json' 
            $response | ConvertTo-Json
            }
        else{
            Write-Host "Server $physServer not found" -ForegroundColor Yellow
        }
    }