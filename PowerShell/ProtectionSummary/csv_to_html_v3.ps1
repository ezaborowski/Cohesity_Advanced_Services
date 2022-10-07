Add-Type -AssemblyName System.Web

#---------------------------------------------------------------------------------------------------------------#

# UPDATE THE FOLLOWING PARAMETERS TO SUIT YOUR ENVIRONMENT
#$source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"
#$html_source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts/Reports"

$orig_email = "ezaborowski@cohesity.com"
$dest_email = "ezaborowski@cohesity.com"
$subject = "Cohesity Reports"
$smtpServer = smtp.gmail.com
$port = 425

#---------------------------------------------------------------------------------------------------------------#

$source = $PSScriptRoot
$html_source = $PSScriptRoot + "\Reports"

$dateString = (get-date).ToString('yyyy-MM-dd')
$clientSummary = "Client_Summary_Report-$dateString.htm"
$fullClientSummary = "Full_Client_Summary_Report-$dateString.htm"
$strikeSummary = "Strike_Summary_Report-$dateString.htm"
$unsuccessfulSummary = "Unsuccesssful_Summary_Report-$dateString.htm"

$client_html = $html_source + "/" + $clientSummary
$fullClient_html = $html_source + "/" + $fullClientSummary
$strike_html = $html_source + "/" + $strikeSummary
$unsuccessful_html = $html_source + "/" + $unsuccessfulSummary

# Create folder for current .html files

$currentFolder = "Reports"

if (Test-Path $source\$currentFolder) {

    Write-Host "Current Reports Folder Exists"
}
else {

    #PowerShell Create directory if not exists
    New-Item $currentFolder -ItemType Directory
    Write-Host "Report Folder Created successfully"
}


# Create folder and move old .htm files from previous runs
$htm = Get-ChildItem $html_source\*.htm -Name
write-host($htm)
if($htm){
    foreach($i in $htm){
        $folder = $i.split("-")
        $folder = $folder.split(".")
    }

    write-host($folder[1])
    $folderName = $html_source + "\" + $folder[1]
    if (Test-Path $folderName) {

        Write-Host "Archive Report Folder Exists"
    }
    else {

        #PowerShell Create directory if not exists
        New-Item $folderName -ItemType Directory
        Write-Host "Archive Report Folder Created successfully"
    }

    foreach($i in $htm){
        $path = $html_source + "\" + $i
        $destination = $folderName + "\" + $i
        Move-Item -Path $path -Destination $destination -Force
    }
}

# load Full Client Summary csv files
$fullClient = Get-ChildItem $source\FullClientSummary-*.csv -Name
write-host($fullClient)


foreach($i in $fullClient){
    $csv_source = $source + "\" + $i
    $full_csv_table = Import-Csv $csv_source
    $convertParams = @{
        PreContent = "<H1>$("Cohesity Full Client Summary Report")</H1>"
        PostContent = "<p class='footer'>$(get-date)</p>"
     }

    
    function ConvertTo-HTMLTable ($Table) {
       
        # add type needed to replace HTML special characters into entities
        Add-Type -AssemblyName System.Web
    

        if ($Table -is [System.Data.DataTable]) {
            # convert to array of PSCustomObjects
            $Table = $Table | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
        }
    
        # manually build the HTML table
        $tdFirst = '<td style="background: black; color: white; font-weight: bold;">'
        $tdOdd   = '<td style="background: #97FAAA;">'
        $tdEven  = '<td style="background: #24FA4E;">'
        $alert  = '<td style="background: red;">'

        # add the headers row
        $headers = @($Table[0].PSObject.Properties | Select -ExpandProperty Name)
        $tbl = New-Object -TypeName System.Text.StringBuilder
        [void]$tbl.Append('<table><thead><tr>')
        foreach ($col in $headers) {
            [void]$tbl.Append("<th>$col</th>")
        }
        [void]$tbl.Append('</tr></thead><tbody>')
        # next add the data rows
        $row = 0
        $Table | ForEach-Object {
            [void]$tbl.AppendLine('<tr>')
            for ($col = 0; $col -lt $headers.Count; $col++) {
                [string]$val =$_.$($headers[$col])
                #$td = if ($col -eq 0) { $tdFirst } elseif ($row -band 1) { $tdOdd } else { $tdEven }
                $td = if($val -eq "Error") 
                        {$alert} 
                    elseif($row -band 1) 
                        {$tdOdd} 
                    else 
                        {$tdEven}
                
                [void]$tbl.Append($td)
                $data = if ([string]::IsNullOrWhiteSpace($val)) { '&nbsp;' } else { [System.Web.HttpUtility]::HtmlEncode($val) }
                [void]$tbl.AppendLine("$data</td>")
            }
            [void]$tbl.AppendLine('</tr>')
            $row++
        }
        [void]$tbl.Append('</tbody></table>')
    
        return $tbl.ToString()
    }

    #write-host($table)
    $html | Out-File "$fullClient_html" -Force

}



# load Client Summary csv files
$client = Get-ChildItem $source\ClientSummaryReport-*.csv -Name
write-host($client)


foreach($i in $client){
    $csv_source = $source + "\" + $i
    $client_csv_table = Import-Csv $csv_source
    $convertParams = @{
        PreContent = "<H1>$("Cohesity Client Summary Report")</H1>"
        PostContent = "<p class='footer'>$(get-date)</p>"
     }

    
    function ConvertTo-HTMLTable ($Table) {
       
        # add type needed to replace HTML special characters into entities
        Add-Type -AssemblyName System.Web
    

        if ($Table -is [System.Data.DataTable]) {
            # convert to array of PSCustomObjects
            $Table = $Table | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
        }
    
        # manually build the HTML table
        $tdFirst = '<td style="background: black; color: white; font-weight: bold;">'
        $tdOdd   = '<td style="background: #97FAAA;">'
        $tdEven  = '<td style="background: #24FA4E;">'
        $alert  = '<td style="background: red;">'

        # add the headers row
        $headers = @($Table[0].PSObject.Properties | Select -ExpandProperty Name)
        $tbl = New-Object -TypeName System.Text.StringBuilder
        [void]$tbl.Append('<table><thead><tr>')
        foreach ($col in $headers) {
            [void]$tbl.Append("<th>$col</th>")
        }
        [void]$tbl.Append('</tr></thead><tbody>')
        # next add the data rows
        $row = 0
        $Table | ForEach-Object {
            [void]$tbl.AppendLine('<tr>')
            for ($col = 0; $col -lt $headers.Count; $col++) {
                [string]$val =$_.$($headers[$col])
                #$td = if ($col -eq 0) { $tdFirst } elseif ($row -band 1) { $tdOdd } else { $tdEven }
                $td = if($val -eq "Error") 
                        {$alert} 
                    elseif($row -band 1) 
                        {$tdOdd} 
                    else 
                        {$tdEven}
                
                [void]$tbl.Append($td)
                $data = if ([string]::IsNullOrWhiteSpace($val)) { '&nbsp;' } else { [System.Web.HttpUtility]::HtmlEncode($val) }
                [void]$tbl.AppendLine("$data</td>")
            }
            [void]$tbl.AppendLine('</tr>')
            $row++
        }
        [void]$tbl.Append('</tbody></table>')
    
        return $tbl.ToString()
    }

    #write-host($table)
    $html | Out-File "$client_html" -Force

}


# load Strike Summary csv files
$strike = Get-ChildItem $source\StrikeSummary_source-*.csv -Name
write-host($strike)

foreach($i in $strike){
    $csv_source = $source + "\" + $i
    $strike_csv_table = Import-Csv $csv_source
    $convertParams = @{
        PreContent = "<H2>$("Cohesity Strike Summary Report")</H2>"
        PostContent = "<p class='footer'>$(get-date)</p>"
    }

    
    function ConvertTo-HTMLTable ($Table) {
    
        # add type needed to replace HTML special characters into entities
        Add-Type -AssemblyName System.Web
    

        if ($Table -is [System.Data.DataTable]) {
            # convert to array of PSCustomObjects
            $Table = $Table | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
        }
    
        # manually build the HTML table
        $tdFirst = '<td style="background: black; color: white; font-weight: bold;">'
        $tdOdd   = '<td style="background: #97FAAA;">'
        $tdEven  = '<td style="background: #24FA4E;">'
        $alert  = '<td style="background: red;">'

        # add the headers row
        $headers = @($Table[0].PSObject.Properties | Select -ExpandProperty Name)
        $tbl = New-Object -TypeName System.Text.StringBuilder
        [void]$tbl.Append('<table><thead><tr>')
        foreach ($col in $headers) {
            [void]$tbl.Append("<th>$col</th>")
        }
        [void]$tbl.Append('</tr></thead><tbody>')
        # next add the data rows
        $row = 0
        $Table | ForEach-Object {
            [void]$tbl.AppendLine('<tr>')
            for ($col = 0; $col -lt $headers.Count; $col++) {
                [string]$val =$_.$($headers[$col])
                #$td = if ($col -eq 0) { $tdFirst } elseif ($row -band 1) { $tdOdd } else { $tdEven }
                $td = if($val -eq "Error") 
                        {$alert} 
                    elseif($row -band 1) 
                        {$tdOdd} 
                    else 
                        {$tdEven}
                
                [void]$tbl.Append($td)
                $data = if ([string]::IsNullOrWhiteSpace($val)) { '&nbsp;' } else { [System.Web.HttpUtility]::HtmlEncode($val) }
                [void]$tbl.AppendLine("$data</td>")
            }
            [void]$tbl.AppendLine('</tr>')
            $row++
        }
        [void]$tbl.Append('</tbody></table>')
    
        return $tbl.ToString()
    }

    #write-host($table)
    $html | Out-File "$strike_html" -Force
    
}


# load Unsuccessful Clients csv files
$unsuccessful = Get-ChildItem $source\UnsuccessfulClients-*.csv -Name
write-host($unsuccessful)

foreach($i in $unsuccessful){
    $csv_source = $source + "\" + $i
    $unsuccessful_csv_table = Import-Csv $csv_source
    $convertParams = @{
        PreContent = "<H2>$("Cohesity Unsuccessful Client Summary Report")</H2>"
        PostContent = "<p class='footer'>$(get-date)</p>"
    }

    
    function ConvertTo-HTMLTable ($Table) {
    
        # add type needed to replace HTML special characters into entities
        Add-Type -AssemblyName System.Web
    

        if ($Table -is [System.Data.DataTable]) {
            # convert to array of PSCustomObjects
            $Table = $Table | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
        }
    
        # manually build the HTML table
        $tdFirst = '<td style="background: black; color: white; font-weight: bold;">'
        $tdOdd   = '<td style="background: #97FAAA;">'
        $tdEven  = '<td style="background: #24FA4E;">'
        $alert  = '<td style="background: red;">'

        # add the headers row
        $headers = @($Table[0].PSObject.Properties | Select -ExpandProperty Name)
        $tbl = New-Object -TypeName System.Text.StringBuilder
        [void]$tbl.Append('<table><thead><tr>')
        foreach ($col in $headers) {
            [void]$tbl.Append("<th>$col</th>")
        }
        [void]$tbl.Append('</tr></thead><tbody>')
        # next add the data rows
        $row = 0
        $Table | ForEach-Object {
            [void]$tbl.AppendLine('<tr>')
            for ($col = 0; $col -lt $headers.Count; $col++) {
                [string]$val =$_.$($headers[$col])
                #$td = if ($col -eq 0) { $tdFirst } elseif ($row -band 1) { $tdOdd } else { $tdEven }
                $td = if($val -eq "Error") 
                        {$alert} 
                    elseif($row -band 1) 
                        {$tdOdd} 
                    else 
                        {$tdEven}
                
                [void]$tbl.Append($td)
                $data = if ([string]::IsNullOrWhiteSpace($val)) { '&nbsp;' } else { [System.Web.HttpUtility]::HtmlEncode($val) }
                [void]$tbl.AppendLine("$data</td>")
            }
            [void]$tbl.AppendLine('</tr>')
            $row++
        }
        [void]$tbl.Append('</tbody></table>')
    
        return $tbl.ToString()
    }

    #write-host($table)
    $html | Out-File "$unsuccessful_html" -Force
    
    $css = @"
    <style>
    h1, h5, th, td { text-align: center; font-family: Segoe UI; }
    table { margin: auto; font-family: Segoe UI; box-shadow: 10px 10px 5px #888; border: thin ridge grey; }
    th { background: #04B727; color: #fff; max-width: 400px; padding: 5px 10px; }
    td { font-size: 11px; padding: 5px 20px; color: #000; }
    tr { background: #b8d1f3; }
    tr:nth-child(even){ background: #dae5f4; }
    </style>
"@
    
    # Create the body of the message (a plain-text and an HTML version)
    $body  = "<h1>Cohesity Summary Reports</h1>`r`n<h5>Generated on $(Get-Date)</h5>  \nBelow is the link to the Cohesity Full Protection Summary HTML:`r`n" + $fullClient_html 
    
    "`r`nBelow are the links to the Cohesity Protection Summary HTML, Cohesity Strike Summary HTML, and Cohesity Unsuccessful Clients Summary HTML:`r`n" + $client_html + "`r`n" + $strike_html + "`r`n" + $unsuccessful_html

    "r`n<h5>Cohesity Client Summary Report</h5>"
    $client_csv_table = ConvertTo-HTMLTable ($client_csv_table)

    "r`n<h5>Cohesity Strike Summary Report</h5>"
    $strike_csv_table = ConvertTo-HTMLTable ($strike_csv_table)

    "r`n<h5>Cohesity Unsuccessful Clients Summary Report</h5>"
    $unsuccessful_csv_table = ConvertTo-HTMLTable ($unsuccessful_csv_table)

    $html  = @"
    <!DOCTYPE html>
    <html>
    <head>
    <title>Cohesity Summary Reports</title>
    <meta name="generator" content="PowerShell" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    $css
    </head>
    <body>
    $body
    $client_csv_table
    $strike_csv_table
    $unsuccessful_csv_table
    </body></html>
"@
    
#---------------------------------------------------------------------------------------------------------------#

# UNCOMMENT THIS LINE TO PRODUCE ACTIVE EMAILS
    # Send-MailMessage -From "$orig_email" -Subject "$subject" -To "dest_email" -Body $body -BodyAsHtml -SmtpServer $smtpServer -Port $port -Credential $creds -UseSsl

#---------------------------------------------------------------------------------------------------------------#
    
}


