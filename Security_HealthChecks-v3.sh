#!/bin/bash

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski and Christopher Peyton - August 12 2021                                           #"
echo "#Last Updated 10/04/2021                                                                                        #"
echo "#  -updated parameter choice section: ALL                                                                       #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

printf '\n'
echo "Please enter Cluster address (ex: https://localhost:8053 or https://mycluster): "
read -e url
printf '\n'
echo "Please enter a prefix to append to output files: "
read -e filename
printf '\n'
echo "Please enter a Local Cohesity Cluster UI username: "
read -e username
printf '\n'
echo "Please enter a Local Cohesity Cluster UI password: "
read -es password
printf '\n'

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
#Asks user if they want to pull the cluster_config.

printf '\n'
printf '\n'
echo "-------------------"
echo "CONFIG DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

config_values=("cluster_config.sh fetch" "cat /home/cohesity/data/nexus/software_version_history.json" "allssh.sh ls -ls /home/cohesity/data/hotfix*" "allssh.sh 'iostat | grep -A 1 avg-cpu'")

config_labels=("Cluster_Config" "Software_Version_History" "Hoftixes_Potentially_Applied" "Disk_IO_Check")

for i in "${!config_values[@]}"; do
	config_string+="${config_labels[$i]};"
done

prompt_for_multiselect config_choice "$config_string"

    for i in "${!config_choice[@]}"; do
        if [ "${config_choice[$i]}" == "true" ]; then
            config_choices+=("${config_labels[$i]}")
            config_choices_values+=("${config_values[$i]}")
        fi
    done

        # Write out each choice
        echo "The following data will be collected: "
        for config_choice in "${config_choices[@]}"
        do
        printf "%s\n" "$config_choice"
        done
        printf '\n'

        echo "CLUSTER_CONFIG Commands chosen:"
        for config_choice in "${config_choices_values[@]}"
        do
        printf "%s\n" "$config_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#
#Run CONFIG data gathering commands.

#config_array=(["cluster_config.sh fetch"]=Cluster_Config ["cat data/nexus/software_version_history.json"]=Software_Version_History ["allssh.sh ls -ls /home/cohesity/data/hotfix*"]=Hotfixes_Potentially_Applied ["allssh.sh 'iostat | grep -A 1 avg-cpu'"]=Disk_IO_Check)

printf '\n'
printf '\n'
echo "Making secLogs/CONFIG-Logs subdirectory to save all logs to..."
  mkdir secLogs 2> /dev/null
  mkdir secLogs/CONFIG-Logs 2> /dev/null
    sleep 5

printf '\n'
printf '\n'
echo "Running CONFIG Data Collection Commands and saving output to CONFIG-Logs folder..."
  sleep 5
printf '\n'

#Run config call which writes the output to the /tmp folder.
for c in "${config_choices_values[@]}"
do
#      d=${config_array[$c]}
      d=${config_choices[$c]}

         echo -e "\nCalling $c \n" | python -m json.tool > secLogs/CONFIG-Logs/$filename-CONFIG-$d-`date +%s`.json

        $c
 done

#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster API parameters to output.

printf '\n'
printf '\n'
echo "-------------------"
echo "API DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

networking=(externalClientSubnets, interfaceGroups, vlans,ldapProvider, routes)
#, network/bonds, network/hosts network/interfaces
informative=(cluster, basicClusterInfo, nodes)
storage=(clusterPartitions, viewBoxes)
remoteTargets=(remoteClusters, vaults)
accessManagement=(activeDirectory, roles, users, groups)
protection=(views, protectionPolicies, protectionSources, protectionJobs)
security=(antivirusGroups, icapConnectionStatus, infectedFiles)
alerts=(alertNotificationRules, alerts)

api_values=("${networking[*]}" "${informative[*]}" "${storage[*]}" "${remoteTargets[*]}" "${accessManagement[*]}" "${protection[*]}" "${security[*]}" "${alerts[*]}" "certificates/webServer" "kmsConfig" "apps" "IdPs")

api_labels=(
    "Networking - External Subnets, Interface Groups, vLANS, LDAP Provider, and Routes" 
    #, Bonds, Hosts, and Interfaces
    "Informative - Cohesity Cluster, Basic Cluster Info, and Cluster Nodes" 
    "Storage - Partitions and Storage Domains" "Remote Targets - Remote Clusters and Archive Targets" 
    "Access Management - Active Directory, Cohesity Roles, Cohesity Users, and Cohesity Groups" 
    "Cohesity Protection - Views, Protection Policies, Sources, Protection Jobs" 
    "Security - AntiVirus Groups, ICAP Connection Status, and Infected Files"
    "Alerts - Alert Notification Rules and Current Cluster Alerts"
    "Cluster Certificate"
    "KMS Configuration"
    "Apps" 
    "idps" 
    )

for i in "${!api_values[@]}"; do
	api_string+="${api_labels[$i]};"
done

prompt_for_multiselect api_choice "$api_string"

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
echo "Making secLogs/API-Logs subdirectory to save all logs to..."
  mkdir secLogs 2> /dev/null
  mkdir secLogs/API-Logs 2> /dev/null
#  mkdir secLogs/API-Logs/network 2> /dev/null
    sleep 5

printf '\n'
printf '\n'
echo "Running API Data Collection Commands and saving output to API-Logs folder..."
  sleep 5
printf '\n'

#get token
token=`curl -X POST -k "$url/irisservices/api/v1/public/accessTokens" -H "accept: application/json" -H "content-type: application/json" -d "{ \"domain\": \"LOCAL\", \"password\": \"$password\", \"username\": \"$username\"}" | cut -d : -f 2 | cut -d, -f1 `

              echo "The Access Token is" $token

#Loop through each api call and write the output of each call to secLogs/API-Logs folder. Piping to json.tool to beautify.
for f in $(echo ${api_choices_values[@]} | sed "s/,/ /g")
do
         echo -e "\nCalling $f \n"

        curl -X GET -k "$url/irisservices/api/v1/public/$f" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API-Logs/$filename-API-$f-`date +%s`.json
 done

#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster IRIS_CLI parameters to output.

printf '\n'
printf '\n'
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

        echo "IRIS_CLI Commands chosen:"
        for iris_choice in $(echo ${iris_choices_values[@]} | sed "s/,/ /g")
        do
        printf "%s\n" "$iris_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#
#Run chosen IRIS_CLI data gathering commands.

printf '\n'
printf '\n'
echo "Making secLogs/IRIS_CLI-Logs subdirectory to save all logs to..."
  mkdir secLogs/IRIS_CLI-Logs 2> /dev/null
    sleep 5

printf '\n'
printf '\n'
echo "Running IRIS_CLI Data Collection Commands and saving output to IRIS_CLI-Logs folder..."
  sleep 5
printf '\n'

#Loop through each iris_cli call and write the output of each call to secLogs/IRIS_CLI-Logs folder
for x in $(echo ${iris_choices_values[@]} | sed "s/,/ /g")
do
         echo -e "\nCalling $x \n"

         iris_cli -username $username -password "$password" cluster $x > secLogs/IRIS_CLI-Logs/$filename-IRIS-$x-`date +%s`.json
 done

#---------------------------------------------------------------------------------------------------------------#
#Asks user to choose what Cohesity Cluster HC_CLI parameters to output.

printf '\n'
printf '\n'
echo "-------------------"
echo "HC_CLI DATA CHECKS"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

networking1=(test-ids=10008, test-ids=10025, test-ids=10026, test-ids=10027, test-ids=10030, test-ids=10055, test-ids=10062) 
networking2=(test-ids=10063, test-ids=10064, test-ids=10065, test-ids=10066, test-ids=10067, test-ids=10068, test-ids=10069) 
networking3=(test-ids=10070, test-ids=10071, test-ids=10074, test-ids=10076, test-ids=10077)
informative=(test-ids=10011, test-ids=10035, test-ids=10044)
storage=(test-ids=10004, test-ids=10051, test-ids=10052)
remoteTargets=(test-ids=10006, test-ids=10017, test-ids=10037)
accessManagement=(test-ids=10031)
protection=(test-ids=10049, test-ids=10057, test-ids=10058, test-ids=10075)
security=(test-ids=10033, test-ids=10045, test-ids=10072, test-ids=10073)
hardware1=(test-ids=10002, test-ids=10012, test-ids=10023, test-ids=10028, test-ids=10036, test-ids=10040)
hardware2=(test-ids=10032, test-ids=10053, test-ids=10060, test-ids=10081, test-ids=10082, test-ids=10083)
hardware3=(test-ids=10084, test-ids=10085, test-ids=10086, test-ids=10088, test-ids=10090)
clusterIntegrity=(test-ids=10003, test-ids=10007)
services=(test-ids=10015, test-ids=10020, test-ids=10039, test-ids=10047, test-ids=10050, test-ids=10054, test-ids=10059)
alerts=(test-ids=10009, test-ids=10018)
performance=(test-ids=10021, test-ids=10046, test-ids=10087, test-ids=10089, test-ids=10101, test-ids=10102)
fileLevel=(test-ids=10048, test-ids=10038, test-ids=10043, test-ids=10061)

hc_values=("${networking1[*]}" "${networking2[*]}" "${networking3[*]}" "${informative[*]}" "${storage[*]}" "${remoteTargets[*]}" "${accessManagement[*]}" "${protection[*]}" "${security[*]}" "${hardware1[*]}" "${hardware2[*]}" "${hardware3[*]}" "${clusterIntegrity[*]}" "${services[*]}" "${alerts[*]}" "${performance[*]}" "${fileLevel[*]}" "all")

hc_labels=(
    "Networking 1 - NTP Sync Check | NTPD Reachability Check | Bond Mode Check | Node Connectivity | Default Gateway Status | Duplicate Node IP Configuration Check | Physical Interface Check"
    "Networking 2 - Primary Interface Check | Network Validation Check | Default Gateway Config Check | DNS Config Check | DNS Reachability Check | NTP Config Check | NTP Reachability Check" 
    "Networking 3 - VLAN Config Check | VLAN Reachability Check | Route Status Check | Routing Config Check | Routing Status Check"
    "Informative - Agent Health Check | Dedup Status Check | Node Uptime"
    "Storage - Parition Size Check | SMB Exclude Snapshot Check | Cluster Disk Usage Check"
    "Remote Targets - Cloud Connectivity | AWS Reachability Check | Vault Connectivity"
    "Access Management - Check LDAP Connectivity"
    "Protection - VSS Snapshots CNT Check | Protection Sources Connectivity Check | Backup Job SLA Violation | Archive No Tasks"
    "Security - Firewalld Status Check | IPMI Permissions | Firewall Config Check | Firewall Status Check"
    "Hardware 1 - Hardware HDD Utility | CPU Throttled Check | Hardware PCIe Link Check | Uncorrectable ECC MCE | HDD Disk Availability Check | SSD Lifetime Write Limit Check"
    "Hardware 2 - Cisco UCS Server NIC Port Check | Multiple RAIDS Configuration Check | Disk Latency Check | Validate Product Model | Check DIMMS | Check System Firmware" 
    "Hardware 3 - Check NVME System Disk | Check Missing Disk | Check NVME Data Disk | Check NIC Slot Port | Disk Serial Number Check"
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

        echo "HC_CLI Commands chosen:"
        for hc_choice in $(echo ${hc_choices_values[@]} | sed "s/,/ /g")
        do
        printf "%s\n" "$hc_choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#

 declare -A hc_array
h c_array=( [test-ids=10002]=Hardware_HDD_Utility [test-ids=10003]=Binary_Files_Release_Version_Check [test-ids=10004]=Parition_Size_Check [test-ids=10006]=Cloud_Connectivity [test-ids=10007]=Constituent_Uptime_Check [test-ids=10008]=NTP_Sync_Check [test-ids=10009]=Alert_Mail_Config_Check [test-ids=10011]=Agent_Health_Check [test-ids=10012]=CPU_Throttled_Check [test-ids=10015]=Winbind_Availability_Check [test-ids=10017]=AWS_Reachability_Check [test-ids=10018]=Alert_Service_Check [test-ids=10020]=Syslog_Server_Check [test-ids=10021]=Disk_Commands_Check [test-ids=10023]=Hardware_PCIe_Link_Check [test-ids=10025]=NTPD_Reachability_Check [test-ids=10026]=Bond_Mode_Check [test-ids=10027]=Node_Connectivity [test-ids=10028]=Uncorrectable_ECC_MCE [test-ids=10030]=Default_Gateway_Status [test-ids=10031]=Check_LDAP_Connectivity [test-ids=10032]=Cisco_UCS_Server_NIC_Port_Check [test-ids=10033]=Firewalld_Status_Check [test-ids=10035]=Dedup_Status_Check [test-ids=10036]=HDD_Disk_Availability_Check [test-ids=10037]=Vault_Connectivity [test-ids=10038]=Stale_File_Handle_Error_Check [test-ids=10039]=Bridge_Proxy_Exec_Check [test-ids=10040]=SSD_Lifetime_Write_Limit Check [test-ids=10043]=D_State_Check [test-ids=10044]=Node_Uptime [test-ids=10045]=IPMI_Permissions [test-ids=10046]=OOM_Check [test-ids=10047]=Librarian_Status_Check [test-ids=10048]=Read_Only_Disk_Check [test-ids=10049]=VSS_Snapshots_CNT_Check [test-ids=10050]=Storage_Proxy_Memory_Check [test-ids=10051]=SMB_Exclude_Snapshot_Check [test-ids=10052]=Cluster_Disk_Usage_Check [test-ids=10054]=Multiple_RAIDS_Configuration_Check [test-ids=10055]=Yoda_XFS_Check [test-ids=10057]=Duplicate_Node_IP_Configuration_Check [test-ids=10058]=Protection_Sources_Connectivity_Check [test-ids=10059]=Backup_Job_SLA_Violation [test-ids=10060]=Apollo_Healer_Deadline_Check [test-ids=10061]=Disk_Latency_Check [test-ids=10062]=File_Count_Limit_Check [test-ids=10063]=Physical_Interface_Check [test-ids=10064]=Primary_Interface_Check [test-ids=10065]=Network_Validation_Check [test-ids=10066]=Default_Gateway_Config_Check [test-ids=10067]=DNS_Config_Check [test-ids=10068]=NTP_Config_Check [test-ids=10069]=NTP_Reachability_Check [test-ids=10070]=VLAN_Config_Check [test-ids=10071]=VLAN_Reachability_Check [test-ids=10072]=Firewall_Config_Check [test-ids=10073]=Firewall_Status_Check [test-ids=10074]=Route_Status_Check [test-ids=10075]=Archive_No_Tasks [test-ids=10076]=Routing_Config_Check [test-ids=10077]=Routing_Status_Check [test-ids=10081]=Validate_Product_Model [test-ids=10082]=Check_DIMMS [test-ids=10083]=Check_System_Firmware [test-ids=10084]=Check_NVME_System_Disk [test-ids=10085]=Check_Missing_Disk [test-ids=10086]=Check_NVME_Data_Disk [test-ids=10087]=Indexing_Backlog_Details [test-ids=10088]=Check_NIC_Slot_Port [test-ids=10089]=Queue_Length_Check [test-ids=10090]=Disk_Serial_Number_Check [test-ids=10101]=SMB_Latency_Check [test-ids=10102]=SMB_Setup_Latency_Check [all]=All_hc_cli_Tests )


#Run chosen HC_CLI data gathering commands.
printf '\n'
printf '\n'
echo "Making secLogs/HC_CLI-Logs subdirectory to save all logs to..."
  mkdir secLogs/HC_CLI-Logs 2> /dev/null
    sleep 5

printf '\n'
printf '\n'
echo "Running HC_CLI Data Check Commands and saving output to HC_CLI-Logs folder."
printf '\n'
echo "This may take a few minutes..."
  sleep 5
printf '\n'

#Loop through each hc_cli calls and write the output of each call to secLogs/HC_CLI-Logs folder
for y in $(echo ${hc_choices_values[@]} | sed "s/,/ /g")
do

    d=${hc_array[$y]}

         echo -e "\nCalling $y \n"

         sudo hc_cli run -v -u $username -p $password --$y > secLogs/HC_CLI-Logs/$filename-HC-$d-`date +%s`.json
done

 #---------------------------------------------------------------------------------------------------------------#