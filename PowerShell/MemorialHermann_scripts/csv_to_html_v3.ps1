Add-Type -AssemblyName System.Web

$source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts"
$html_source = "/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Memorial_Hermann/Memorial_Hermann_scripts/Reports"

$dateString = (get-date).ToString('yyyy-MM-dd')
$clientSummary = "Client_Summary_Report-$dateString.htm"
$strikeSummary = "Strike_Summary_Report-$dateString.htm"

$client_html = $html_source + "/" + $clientSummary
$strike_html = $html_source + "/" + $strikeSummary

$orig_email = "ezaborowski@cohesity.com"
$dest_email = "ezaborowski@cohesity.com"
$subject = "Cohesity Reports"
$smtpServer = smtp.gmail.com
$port = 425

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

        Write-Host "Folder Exists"
    }
    else {

        #PowerShell Create directory if not exists
        New-Item $folderName -ItemType Directory
        Write-Host "Folder Created successfully"
    }

    foreach($i in $htm){
        $path = $html_source + "\" + $i
        $destination = $folderName + "\" + $i
        Move-Item -Path $path -Destination $destination -Force
    }
}

# load Client Summary csv files
$client = Get-ChildItem $source\ClientSummary_source-*.csv -Name
write-host($client)


foreach($i in $client){
    #$i | ConvertFrom-Csv | ConvertTo-Html | Set-Content -Path $client_html
    $csv_source = $source + "\" + $i
    $csv_table = Import-Csv $csv_source
    $convertParams = @{
        PreContent = "<H1>$("Client Summary Report")</H1>"
        PostContent = "<p class='footer'>$(get-date)</p>"
     }
    #Import-Csv .\$i | ConvertTo-Html @convertParams | Out-File $client_html 

    
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

    #     $sb = New-Object -TypeName System.Text.StringBuilder
    #     [void]$sb.AppendLine('<table>')
    #     if ($null -ne $obj) {
    #         if (([object]$obj).GetType().FullName -eq 'System.Data.DataTable'){
    #             # it is a DataTable; convert to array of PSObjects
    #             $obj = $obj | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
    #         }
            
    #         $headers = $obj[0].PSObject.Properties | Select-String Name #-ExpandProperty Name
    #         [void]$sb.AppendLine('<thead><tr>')
    #         foreach ($column in $headers) {
    #             [void]$sb.AppendLine(('<th>{0}</th>' -f [System.Web.HttpUtility]::HtmlEncode($column)))
    #         }
    #         write-host("COLUMN: " + $headers)
    #         [void]$sb.AppendLine('</tr></thead><tbody>')
    #         $row = 0
    #         $obj | ForEach-Object {
    #             # add inline style for zebra color rows
    #             if ($row++ -band 1) {
    #                 $tr = '<tr style="background-color: {0};">' -f $oddRowBackColor
    #             } 
    #             else {
    #                 $tr = '<tr>'
    #             }
    #             [void]$sb.AppendLine($tr)
    #             foreach ($column in $headers) {
    #                 [string]$val = $($_.$column)
    #                 if ([string]::IsNullOrWhiteSpace($val)) { 
    #                     $td = '<td>&nbsp;</td>' 
    #                 } 
    #                 else { 
    #                     $td = '<td>{0}</td>' -f [System.Web.HttpUtility]::HtmlEncode($val)
    #                 }
    #                 [void]$sb.Append($td)
    #             }
    #             [void]$sb.AppendLine('</tr>')
    #         }
            
    #         [void]$sb.AppendLine('</tbody>')
    #     }
    #     [void]$sb.AppendLine('</table>')
    
    #     return $sb.ToString()
    # }
    
    
    # $headerBackColor = '#4F81BD'  # backgroundcolor for column headers
    # $oddRowBackColor = '#DCE6F1'  # background color for odd rows
    
    # $style = @"
    # <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # <html xmlns="http://www.w3.org/1999/xhtml">
    #     <head>
    #     <title>Report</title>
    #     <meta name="generator" content="PowerShell" />
    #     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    #     <style type="text/css">
    #     body {
    #         font-family: Verdana, Arial, Geneva, Helvetica, sans-serif;
    #         font-size: 12px;
    #         color: black;
    #     }
    #     table, td, th {
    #         border-color: black;
    #         border-style: solid;
    #         font-family: Verdana, Arial, Geneva, Helvetica, sans-serif;
    #         font-size: 11px;
    #     }
    #     table {
    #         border-width: 0 0 1px 1px;
    #         border-spacing: 0;
    #         border-collapse: collapse;
    #     }
    
    #     td, th {
    #         margin: 0;
    #         padding: 4px;
    #         border-width: 1px 1px 0 0;
    #         text-align: left;
    #     }
    #     th {
    #         color: white;
    #         background-color: $headerBackColor;
    #         font-weight: bold;
    #     }
    #     </style>
    # "@
    
    # $body = '{0}</head><body>{1}</body></html>' -f $style, (ConvertTo-HTMLTable $exportObject)
    
    # Send-MailMessage -From $FromEm -Subject $Subject -To "user@domain.com" -Body $body -BodyAsHtml -SmtpServer $SmtpServer -Port $Port -Credential $Creds -UseSsl
    

#     function ConvertTo-HTMLTable ($obj) {
#     # add type needed to replace HTML special characters into entities
#     Add-Type -AssemblyName System.Web

#     $sb = New-Object -TypeName System.Text.StringBuilder
#     [void]$sb.AppendLine('<table>')
#     if ($null -ne $obj) {
#         $headers = $obj[0].PSObject.Properties | Select-String Name #-ExpandProperty Name
#         [void]$sb.AppendLine('<thead><tr>')
#         foreach ($column in $headers) {
#             [void]$sb.Append(('<th>{0}</th>' -f [System.Web.HttpUtility]::HtmlEncode($column)))
#         }
#         [void]$sb.AppendLine('</tr></thead><tbody>')
#         #[string]$status = ''
#         $obj | ForEach-Object {
#             foreach ($column in $headers) {
#                 [string]$val = $_.$column
#                 # test if $val contains a string, and if so check if it equals "Error"
#                 if ([string]) {
#                     # it's a string value, see it we need to change color
#                     $td = if ($val -eq "Error") {"<td style=color:red;>$val</td>"} else {"<td>$val</td>"}
#                 }
#                 elseif ([string]::IsNullOrWhiteSpace($val)) { 
#                     $td = '<td>&nbsp;</td>' 
#                 } 
#                 else { 
#                     $td = '<td>{0}</td>' -f [System.Web.HttpUtility]::HtmlEncode($val)
#                 }
#                 [void]$sb.Append($td)
#             }
#             [void]$sb.AppendLine('</tr>')
#         }
#         [void]$sb.AppendLine('</tbody>')
#     }
#     [void]$sb.AppendLine('</table>')

#     return $sb.ToString()
# }



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

$body  = "<h1>Client Summary Report</h1>`r`n<h5>Generated on $(Get-Date)</h5>"
$table = ConvertTo-HTMLTable ($csv_table)
#$table = Import-Csv .\$i | ConvertTo-Html 
$html  = @"
<!DOCTYPE html>
<html>
<head>
<title>Report</title>
<meta name="generator" content="PowerShell" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
$css
</head>
<body>
$body
$table
</body></html>
"@

#write-host($table)
$html | Out-File "$client_html" -Force

# Send-MailMessage -From $FromEm -Subject $Subject -To "user@domain.com" -Body $body -BodyAsHtml -SmtpServer $SmtpServer -Port $Port -Credential $Creds -UseSsl
    

    #Import-Csv .\$i | ConvertTo-Html @convertParams | Out-File $client_html 
    #ConvertTo-HTMLTable ($csv_source)

}


# load Strike Summary csv files
$strike = Get-ChildItem $source\StrikeSummary_source-*.csv -Name
write-host($strike)

    foreach($i in $strike){
    #$i | ConvertFrom-Csv | ConvertTo-Html | Set-Content -Path $client_html

    $csv_source = $source + "\" + $i
    $csv_table = Import-Csv $csv_source

    $convertParams = @{
        PreContent = "<H2>$("Strike Summary Report")</H2>"
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
    $body  = "<h1>Strike Summary Report</h1>`r`n<h5>Generated on $(Get-Date)</h5>  \nBelow are the links to the Cohesity Protection Summary HTML and the Cohesity Strike Summary HTML:\n" + $html_source + "/Client_Summary.htm\n" + $html_source + "/Strike_Summary.htm"
    $table = ConvertTo-HTMLTable ($csv_table)
    #$table = Import-Csv .\$i | ConvertTo-Html 
    $html  = @"
    <!DOCTYPE html>
    <html>
    <head>
    <title>Report</title>
    <meta name="generator" content="PowerShell" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    $css
    </head>
    <body>
    $body
    $table
    </body></html>
"@
    
    #write-host($table)
    $html | Out-File "$strike_html" -Force
    
    # Send-MailMessage -From "$orig_email" -Subject "$subject" -To "dest_email" -Body $body -BodyAsHtml -SmtpServer $smtpServer -Port $port -Credential $creds -UseSsl
        
    
    #Import-Csv .\$i | ConvertTo-Html @convertParams | Out-File $client_html 
    #ConvertTo-HTMLTable ($csv_source)
    
}

    #Import-Csv .\$i | ConvertTo-Html | Out-File $strike_html 


