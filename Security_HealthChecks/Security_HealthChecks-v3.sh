#!/bin/bash

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski and Christopher Peyton - August 12 2021                                           #"
echo "#Last Updated 9/29/2021                                                                                         #"
echo "#  -updated parameter choice section                                                                            #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

printf '\n'
echo "Please enter Cluster address (ex: https://localhost:8053 or https://mycluster): "
read url
echo "Please enter a prefix to append to output files: "
read filename
echo "Please enter Cluster UI username: "
read username
echo "Please enter Cluster UI password: "
read -s password
​
#---------------------------------------------------------------------------------------------------------------#
#Configuration for multiple choice selection section.

# from SO: https://stackoverflow.com/a/54261882/317605 (by https://stackoverflow.com/users/8207842/dols3m)

function prompt_for_multiselect {

    # little helpers for terminal print control and key input
    ESC=$( printf "\033")
    cursor_blink_on()   { printf "$ESC[?25h"; }
    cursor_blink_off()  { printf "$ESC[?25l"; }
    cursor_to()         { printf "$ESC[$1;${2:-1}H"; }
    print_inactive()    { printf "$2   $1 "; }
    print_active()      { printf "$2  $ESC[7m $1 $ESC[27m"; }
    get_cursor_row()    { IFS=';' read -sdR -p $'\E[6n' ROW COL; echo ${ROW#*[}; }
    key_input()         {
      local key
      IFS= read -rsn1 key 2>/dev/null >&2
      if [[ $key = ""      ]]; then echo enter; fi;
      if [[ $key = $'\x20' ]]; then echo space; fi;
      if [[ $key = $'\x1b' ]]; then
        read -rsn2 key
        if [[ $key = [A ]]; then echo up;    fi;
        if [[ $key = [B ]]; then echo down;  fi;
      fi 
    }
    toggle_option()    {
      local arr_name=$1
      eval "local arr=(\"\${${arr_name}[@]}\")"
      local option=$2
      if [[ ${arr[option]} == true ]]; then
        arr[option]=
      else
        arr[option]=true
      fi
      eval $arr_name='("${arr[@]}")'
    }

    local retval=$1
    local options
    local defaults

    IFS=';' read -r -a options <<< "$2"
    if [[ -z $3 ]]; then
      defaults=()
    else
      IFS=';' read -r -a defaults <<< "$3"
    fi
    local selected=()

    for ((i=0; i<${#options[@]}; i++)); do
      selected+=("${defaults[i]}")
      printf "\n"
    done

    # determine current screen position for overwriting the options
    local lastrow=`get_cursor_row`
    local startrow=$(($lastrow - ${#options[@]}))

    # ensure cursor and input echoing back on upon a ctrl+c during read -s
    trap "cursor_blink_on; stty echo; printf '\n'; exit" 2
    cursor_blink_off

    local active=0
    while true; do
        # print options by overwriting the last lines
        local idx=0
        for option in "${options[@]}"; do
            local prefix="[ ]"
            if [[ ${selected[idx]} == true ]]; then
              prefix="[x]"
            fi

            cursor_to $(($startrow + $idx))
            if [ $idx -eq $active ]; then
                print_active "$option" "$prefix"
            else
                print_inactive "$option" "$prefix"
            fi
            ((idx++))
        done

        # user key control
        case `key_input` in
            space)  toggle_option selected $active;;
            enter)  break;;
            up)     ((active--));
                    if [ $active -lt 0 ]; then active=$((${#options[@]} - 1)); fi;;
            down)   ((active++));
                    if [ $active -ge ${#options[@]} ]; then active=0; fi;;
        esac
    done

    # cursor position back to normal
    cursor_to $lastrow
    printf "\n"
    cursor_blink_on

    eval $retval='("${selected[@]}")'
}

#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster API parameters to output.

echo "-------------------"
echo "API DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

networking=(externalClientSubnets, interfaceGroups, vlans)
informative=(cluster, basicClusterInfo, nodes)
storage=(clusterPartitions, viewBoxes)
remoteTargets=(remoteClusters, vaults)
accessManagement=(activeDirectory, roles, users, groups)
protection=(views, protectionPolicies, protectionSources, protectionJobs)

api_values=("${networking[*]}" "${informative[*]}" "${storage[*]}" "${remoteTargets[*]}" "${accessManagement[*]}" "${protection[*]}" "apps" "idps" "alertNotificationRules")

api_labels=(
    "Networking - Subnets, Interface Groups, and vLANS" 
    "Informative - Cohesity Cluster, Basic Cluster Info, and Cluster Nodes" 
    "Storage - Partitions and Storage Domains" "Remote Targets - Remote Clusters and Archive Targets" 
    "Access Management - Active Directory, Cohesity Roles, Cohesity Users, and Cohesity Groups" 
    "Cohesity Protection - Views, Protection Policies, Sources, Protection Jobs" 
    "Apps" 
    "idps" 
    "Alerts"
    )

for i in "${!api_values[@]}"; do
	api_string+="${api_labels[$i]};"
done

prompt_for_multiselect choice "$api_string"

    for i in "${!api_choice[@]}"; do
        if [ "${api_choice[$i]}" == "true" ]; then
            api_choices+=("${api_labels[$i]}")
            api_choices_values+=("${api_values[$i]}")
        fi
    done

        # Write out each choice
        echo "The following data will be collected: "
        for api_choice in "${api_choices[@]}"
        do
        printf "%s\n" "$api_choice"
        done
        printf '\n'

        echo "API Commands chosen:"
        for api_choice in $(echo ${api_choices_values[@]} | sed "s/,/ /g")
        do
        printf "%s\n" "$api_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#
#Run chosen API data gathering commands.

printf '\n'
printf '\n'
echo "Making subdirectory to save all logs to..."

mkdir API-Logs 

printf '\n'
printf '\n'
echo "Running API Data Collection Commands..."
printf '\n'
echo "Creating output and saving to API-Logs folder..."

#get token
token=`curl -s -k -X POST --url "${url}/irisservices/api/v1/public/accessTokens" -H 'Accept: application/json' -H 'Content-type: application/json' --data-raw '{"password": "'$password'", "username": "'$username'"}' | cut -d : -f 2 | cut -d, -f1 `
​
              echo "The Access Token is" $token
​
#Loop through each api call, optionally pipe to json.tool to beautify.
for f in $(echo ${api_choices_values[@]} | sed "s/,/ /g")
do
         echo -e "\nCalling $f \n"
​
        `curl -s -k -X GET -G --url "$url/irisservices/api/v1/public/$f" -H "Authorization: Bearer $token" -H 'Accept: text/html'` > API-Logs\\$filename-API-$f-`date +%s`.json
 done

# #Create output tgz in local directory.
#  echo "Creating output tgz and saving in local directory..."
#  tar -cvzf $filename-API-`date +%s`.tgz $filename-API*.json

#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster IRIS_CLI parameters to output.

echo "-------------------"
echo "IRIS_CLI DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

networking=(get-bonding-mode, get-dns-server, get-subnets, list-interfaces, get-domain-names, get-ntp-servers)
informative=(get-etc-hosts, get-info)
accessManagement=(get-proxy-servers, get-nfs-whitelist, get-nfs-export-paths)
security=(list-ssl-cert-details, ls-ssh-keys)

iris_values=("${networking[*]}" "${informative[*]}" "${accessManagement[*]}" "${security[*]}" "cluster get-io-pref-tier")

iris_labels=(
    "Networking - To list the bonding mode of the NICs, DNS servers, subnets, interfaces, domain names, and NTP servers for the Cluster." 
    "Informative - To get the hosts info and and general information about the Cluster." 
    "Access Management - To list the proxy servers, client subnets with permissions to access Views, and NFS export paths accessible in the Cluster." 
    "Security - To get the SSL certificate details of the Cluster and list public SSH Keys." 
    "To get the preferred IO tier of the Cluster."
    )   

for i in "${!iris_values[@]}"; do
	iris_string+="${iris_labels[$i]};"
done

prompt_for_multiselect iris_choice "$iris_string"

    for i in "${!iris_choice[@]}"; do
        if [ "${iris_choice[$i]}" == "true" ]; then
            iris_choices+=("${iris_labels[$i]}")
            iris_choices_values+=("${iris_values[$i]}")
        fi
    done

        # Write out each choice
        echo "The following data will be collected: "
        for iris_choice in "${iris_choices[@]}"
        do
        printf "%s\n" "$iris_choice"
        done
        printf '\n'

        for iris_choice in $(echo ${iris_choices_values[@]} | sed "s/,/ /g")
        do
        printf "%s\n" "$iris_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#
#Run chosen IRIS_CLI data gathering commands.

printf '\n'
printf '\n'
echo "Making subdirectory to save all logs to..."

mkdir IRIS_CLI-Logs 

printf '\n'
printf '\n'
echo "Running IRIS_CLI Data Collection Commands..."
printf '\n'
echo "Creating output and saving to IRIS_CLI-Logs folder..."

#Loop through each iris_cli call, optionally pipe to json.tool to beautify.
for x in $(echo ${iris_choices_values[@]} | sed "s/,/ /g")
do
         echo -e "\nCalling $x \n"
​
         iris_cli -username $username -password $password cluster $x > IRIS_CLI-Logs\\$filename-IRIS-$x-`date +%s`.json
 done

# #Create output tgz in local directory.
#  echo "Creating output tgz and saving in local directory..."
#  tar -cvzf $filename-IRIS-`date +%s`.tgz $filename-IRIS*.json


#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster HC_CLI parameters to output.

echo "-------------------"
echo "HC_CLI DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

networking1=(test-ids=10008, test-ids=10025, test-ids=10026, test-ids=10027, test-ids=10030, test-ids=10055, test-ids=10062) 
networking2=(test-ids=10063, test-ids=10064, test-ids=10065, test-ids=10066, test-ids=10067, test-ids=10068, test-ids=10069) 
networking3=(test-ids=10070, test-ids=10071, test-ids=10074, test-ids=10076, test-ids=10077)
informative=(test-ids=10011, test-ids=10035, test-ids=10044)
storage=(test-ids=10004, test-ids=10051, test-ids=10052, )
remoteTargets=(test-ids=10006, test-ids=10017, test-ids=10037, )
accessManagement=(test-ids=10031, )
protection=(test-ids=10049, test-ids=10057, test-ids=10058, test-ids=10075, )
security=(test-ids=10033, test-ids=10045, test-ids=10072, test-ids=10073, )
hardware1=(test-ids=10002, test-ids=10012, test-ids=10023, test-ids=10028, test-ids=10036, test-ids=10040)
hardware2=(test-ids=10032, test-ids=10053, test-ids=10060, test-ids=10081, test-ids=10082, test-ids=10083)
hardware3=(test-ids=10084, test-ids=10085, test-ids=10086, test-ids=10088, test-ids=10090)
clusterIntegrity=(test-ids=10003, test-ids=10007, )
services=(test-ids=10015, test-ids=10020, test-ids=10039, test-ids=10047, test-ids=10050, test-ids=10054, test-ids=10059, )
alerts=(test-ids=10009, test-ids=10018, )
performance=(test-ids=10021, test-ids=10046, test-ids=10087, test-ids=10089, test-ids=10101, test-ids=10102)
fileLevel=(test-ids=10048, test-ids=10038, test-ids=10043, test-ids=10061, )

hc_values=("${networking1[*]}" "${networking2[*]}" "${networking3[*]}" "${informative[*]}" "${storage[*]}" "${remoteTargets[*]}" "${accessManagement[*]}" "${protection[*]}" "${security[*]}" "${hardware1[*]}" "${hardware2[*]}" "${hardware3[*]}" "${clusterIntegrity[*]}" "${services[*]}" "${alerts[*]}" "${performance[*]}" "${fileLevel[*]}" "all")

hc_labels=(
    "Networking - NTP Sync Check | NTPD Reachability Check | Bond Mode Check | Node Connectivity | Default Gateway Status | Duplicate Node IP Configuration Check | Physical Interface Check"
    "Networking (contd) - Primary Interface Check | Network Validation Check | Default Gateway Config Check | DNS Config Check | DNS Reachability Check | NTP Config Check | NTP Reachability Check" 
    "Networking (contd) - VLAN Config Check | VLAN Reachability Check | Route Status Check | Routing Config Check | Routing Status Check"
    "Informative - Agent Health Check | Dedup Status Check | Node Uptime"
    "Storage - Parition Size Check | SMB Exclude Snapshot Check | Cluster Disk Usage Check"
    "Remote Targets - Cloud Connectivity | AWS Reachability Check | Vault Connectivity"
    "Access Management - Check LDAP Connectivity"
    "Protection - VSS Snapshots CNT Check | Protection Sources Connectivity Check | Backup Job SLA Violation | Archive No Tasks"
    "Security - Firewalld Status Check | IPMI Permissions | Firewall Config Check | Firewall Status Check"
    "Hardware - Hardware HDD Utility | CPU Throttled Check | Hardware PCIe Link Check | Uncorrectable ECC MCE | HDD Disk Availability Check | SSD Lifetime Write Limit Check"
    "Hardware (contd) - Cisco UCS Server NIC Port Check | Multiple RAIDS Configuration Check | Disk Latency Check | Validate Product Model | Check DIMMS | Check System Firmware" 
    "Hardware (contd) - Check NVME System Disk | Check Missing Disk | Check NVME Data Disk | Check NIC Slot Port | Disk Serial Number Check"
    "Cluster Integrity - Binary Files Release Version Check | Constituent Uptime Check"
    "Services - Winbind Availability Check | Syslog Server Check | Bridge Proxy Exec Check | Librarian Status Check | Storage Proxy Memory Check | Yoda XFS Check | Apollo Healer Deadline Check"
    "Alerts - Alert Mail Config Check | Alert Service Check"
    "Performance - Disk Commands Check | OOM Check | Indexing Backlog Details | Queue Length Check | SMB Latency Check"
    "File Level - Read Only Disk Check | Stale File Handle Error Check | D State Check | File Count Limit Check"
    "All hc_cli Tests")


for i in "${!hc_values[@]}"; do
	hc_string+="${hc_labels[$i]};"
done

prompt_for_multiselect hc_choice "$hc_string"

    for i in "${!hc_choice[@]}"; do
        if [ "${hc_choice[$i]}" == "true" ]; then
            hc_choices+=("${hc_labels[$i]}")
            hc_choices_values+=("${hc_values[$i]}")
        fi
    done

        # Write out each choice
        echo "The following data will be collected: "
        for hc_choice in "${hc_choices[@]}"
        do
        printf "%s\n" "$hc_choice"
        done
        printf '\n'

        for hc_choice in $(echo ${hc_choices_values[@]} | sed "s/,/ /g")
        do
        printf "%s\n" "$hc_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#

#Run chosen HC_CLI data gathering commands.
printf '\n'
printf '\n'
echo "Making subdirectory to save all logs to..."

mkdir HC_CLI-Logs 

printf '\n'
printf '\n'
echo "Running HC_CLI Data Collection Commands..."
printf '\n'
echo "Creating output and saving to HC_CLI-Logs folder..."
​
#Loop through each hc_cli call, optionally pipe to json.tool to beautify.
for y in $(echo ${hc_choices_values[@]} | sed "s/,/ /g")
do
         echo -e "\nCalling $y \n"
​
         hc_cli run -u $username -p $password hc_cli run --$y -v > HC_CLI-Logs\\$filename-HC-$y-`date +%s`.json

 done

#Create output tgz in local directory.
# printf '\n'
# printf '\n'
#  echo "Creating output tgz and saving in local directory..."
#  tar -cvzf $filename-HC-`date +%s`.tgz $filename-HC*.json


 #---------------------------------------------------------------------------------------------------------------#