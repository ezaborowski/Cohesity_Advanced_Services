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

api_values=("cluster" "externalClientSubnets" "basicClusterInfo" "clusterPartitions" "apps" "nodes" "interfaceGroups" "vlans" "viewBoxes" "remoteClusters" "vaults" "activeDirectory" "roles" "users" "idps" "groups" "alertNotificationRules" "views" "protectionPolicies" "protectionSources" "protectionJobs")
api_labels=("Cohesity Cluster" "Subnets" "Basic Cluster Info" "Partitions" "Apps" "Cluster Nodes" "Interface Groups" "vLANS" "Storage Domains" "Remote Clusters" "Archive Targets" "Active Directory" "Cohesity Roles" "Cohesity Users" "idps" "Cohesity Groups" "Alerts" "Views" "Protection Policies" "Sources" "Protection Jobs")

for i in "${!api_values[@]}"; do
	api_string+="${api_labels[$i]} (${api_values[$i]});"
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
        printf "%s\n " "$api_choice"
        done
        printf '\n'

        echo "API Commands chosen:"
        for api_choice in "${api_choices_values[@]}"
        do
        printf "%s\n " "$api_choice"
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
for f in ${api_choices_values[@]}
do
         echo -e "\nCalling $f \n"
​
         curl -s -k -X GET -G --url "$url/irisservices/api/v1/public/$f" -H "Authorization: Bearer $token" -H 'Accept: text/html' > API-Logs\\$filename-API-$f-`date +%s`.json
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

iris_values=("cluster get-bonding-mode" "cluster get-dns-server" "cluster get-domain-names" "cluster get-etc-hosts" "cluster get-info" "cluster get-io-pref-tier" "cluster get-nfs-export-paths" "cluster get-nfs-whitelist" "cluster get-ntp-servers" "cluster get-proxy-servers" "cluster get-subnets" "cluster get-upgrade-status" "cluster list-interfaces" "cluster list-packages" "cluster list-ssl-cert-details" "cluster ls-ssh-keys")
iris_labels=("To get the bonding mode of the NICs" "To get the IP addresses of the DNS servers for the Cluster." "To get the domain names of the cluster" "To get the hosts info of the Cluster." "To get information about the Cluster." "To get the preferred IO tier of the Cluster." "To list NFS export paths accessible in the Cluster." "To list client subnets with permissions to access Views." "To get the list of the NTP servers for the Cluster." "To get the proxy servers for the Cluster." "To get the subnets of the Cluster." "To get the Cluster software upgrade status." "To list the interfaces in the cluster." "To list the available Cohesity software packages on a Cluster." "To get the SSL certificate details of the Cluster." "List public SSH Keys.")   

for i in "${!iris_values[@]}"; do
	iris_string+="${iris_labels[$i]} (${iris_values[$i]});"
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
        printf "%s\n " "$iris_choice"
        done
        printf '\n'

        echo "IRIS_CLI Commands chosen:"
        for iris_choice in "${iris_choices_values[@]}"
        do
        printf "%s\n " "$iris_choice"
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
for x in ${iris_choices_values[@]}
do
         echo -e "\nCalling $x \n"
​
         iris_cli -username $username -password $password $x > IRIS_CLI-Logs\\$filename-IRIS-$x-`date +%s`.json
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

hc_values=("test-ids=10002" "test-ids=10003" "test-ids=10004" "test-ids=10006" "test-ids=10007" "test-ids=10008" "test-ids=10009" "test-ids=10011" "test-ids=10012" "test-ids=10015" "test-ids=10017" "test-ids=10018" "test-ids=10020" "test-ids=10021" "test-ids=10023" "test-ids=10025" "test-ids=10026" "test-ids=10027" "test-ids=10028" "test-ids=10030" "test-ids=10031" "test-ids=10032" "test-ids=10033" "test-ids=10035" "test-ids=10036" "test-ids=10037" "test-ids=10038" "test-ids=10039" "test-ids=10040" "test-ids=10043" "test-ids=10044" "test-ids=10045" "test-ids=10046" "test-ids=10047" "test-ids=10048" "test-ids=10049" "test-ids=10050" "test-ids=10051" "test-ids=10052" "test-ids=10053" "test-ids=10054" "test-ids=10055" "test-ids=10057" "test-ids=10058" "test-ids=10059" "test-ids=10060" "test-ids=10061" "test-ids=10062" "test-ids=10063" "test-ids=10064" "test-ids=10065" "test-ids=10066" "test-ids=10067" "test-ids=10068" "test-ids=10069" "test-ids=10070" "test-ids=10071" "test-ids=10072" "test-ids=10073" "test-ids=10074" "test-ids=10075" "test-ids=10076" "test-ids=10077" "test-ids=10081" "test-ids=10082" "test-ids=10083" "test-ids=10084" "test-ids=10085" "test-ids=10086" "test-ids=10087" "test-ids=10088" "test-ids=10089" "test-ids=10090" "test-ids=10101" "test-ids=10102" "all")
hc_labels=(
    "Hardware HDD Utility - Reports the load per disk via iostat and outputest the usage percentage of I/O." 
    "Binary Files Release Version Check - Compares release version of Cluster against all binary files." 
    "Parition Size Check - Checks the used space for each partition and reports the usage percentage." 
    "Cloud Connectivity - Checks connectivity to Helios with proxy enabled or disabled." 
    "Constituent Uptime Check - Checks for uptime of services and counts the number of recent service restarts. Services which aren't up for 5 minutes are marked as FAIL." 
    "NTP Sync Check - Checks if node's time is in sync with NTP server by running ntpq -pn." 
    "Alert Mail Config Check - Checks whether email address is configured to receive alerts." 
    "Agent Health Check - Retrieves agent health from REST API and reports unhealthy agents." 
    "CPU Throttled Check - Checks for CPU throttle event using 'lscpu' command. Checks for CPU speed less than 1000mhz." 
    "Winbind Availability Check - Checks winbind service status with the 'wbinfo -P' command." 
    "AWS Reachability Check - Checks whether Amazon IAM(Identity and Access Management) and services like Amazon Simple Storage Service(S3) and EC2(Elastic and Compute Cloud) are reachable from cluster node by connecting to a public endpoint, such as s3.amazonaws.com." 
    "Alert Service Check - Checks alerts service status. If alerts service is up collect the uptime." 
    "Syslog Server Check - Checks if Syslog server is configured with default port and protocol." 
    "Disk Commands Check - Checks the number of disk commands currently running on a node. When attached disks are invalid or not mounted correctly, running disk commands might become stuck, and a backlog of sudo commands might render the system unusable." 
    "Hardware PCIe Link Check - Checks for PCIe bus errors in the 'dmesg' log output." 
    "NTPD Reachability Check - Checks ntp source reachability using 'ntpdc' command. The 'ntpdc' command sends a query to the ntpd daemon running on each of the hosts. Ntpd daemon on each responding host sends information about the current calculated offset between its time and the time of each of its NTP servers or peers." 
    "Bond Mode Check - Checks the bond mode for bonded interfaces." 
    "Node Connectivity - Checks whether all nodes are reachable via SSH." 
    "Uncorrectable ECC MCE - Checks for uncorrectable ECC and machine check exception errors in 'ipmi sel list log' command." 
    "Default Gateway Status - Checks that a default gateway exists in the 'route n' command and whether it can be reached." 
    "Check LDAP Connectivity - Checks whether all discovered LDAP servers are reachable over port 389." "Cisco UCS Server NIC Port Check - Checks whether NICs in Cisco UCS server are using the appropriate slots." 
    "Firewalld Status Check - Checks SELinux security context settings for firewalld configuration file /etc/firewalld/direct.xml. Checks whether the firewall rules across the nodes are consistent." 
    "Dedup Status Check - Retrieves the dedupe ratio and compares the values for the last seven days. The latest value should be higher." 
    "HDD Disk Availability Check - Checks the list of available HDD disks and reports whether only one disk (sda) is available." 
    "Vault Connectivity - Checks whether the current node can reach all vault targets and list objects in all targets." 
    "Stale File Handle Error Check - Checks for stale file handle errors." 
    "Bridge Proxy Exec Check - Checks whether Bridge Proxy service is bound to port 11116." 
    "SSD Lifetime Write Limit Check - Checks whether 'Lifetime Write Limit' of one or more SSDs is greater than 90%." 
    "D State Check - Finds the number of processes of each type in D-state/Z-state. Processes in a 'D' or uninterruptible sleep state are usually waiting on I/O. Processes in 'Z' or defunct ('zombie') processes." 
    "Node Uptime - Checks uptime for all nodes in a cluster. If any node has been rebooted within 24 hours and others are up for more than two days, the check fails." 
    "IPMI Permissions - Checks if permissions, owner and group for /usr/bin/ipmitool are uniform across all the nodes of a cluster." 
    "OOM Check - Checks for out of memory errors on a node." 
    "Librarian Status Check - Checking the status of Cohesity Indexing service (librarian) service on the cluster." 
    "Read Only Disk Check - Checks whether all the disks are available for read and write operations." 
    "VSS Snapshots CNT Check - Checking whether the number of VSS snapshots is significantly less than the maximum configured on the cluster with the advanced configuration option magneto_vss_max_snapshots." 
    "Storage Proxy Memory Check - This will check whether the service storage_proxy has run out of memory." 
    "SMB Exclude Snapshot Check - Checks for the generic NAS protection jobs and with protocol 'CIFS'. Ensures './Snapshot' directory is excluded for SMB shares." 
    "Cluster Disk Usage Check - Checks for the partition size on all nodes, fails if percentage consumed is over 95%." 
    "Multiple RAIDS Configuration Check - Checks whether any disk is configured with multiple RAIDs." 
    "Yoda XFS Check - Checks whether XFS(file system) for Indexing service is enabled or disabled." 
    "Duplicate Node IP Configuration Check - Checks for duplicate IP configuration in all the available network configuration files." 
    "Protection Sources Connectivity Check - Checks for connectivity to protection sources from the current node." 
    "Backup Job SLA Violation - Check jobs missing SLAs" 
    "Apollo Healer Deadlin Check - Checks for Apollo service healer jobs and fails if any job is failed with deadline exceeded error or any other errors. Error type should be eithe kNoError or kCanceled." "Disk Latency Check - Check disks with high latency" 
    "File Count Limit Check - Checking whether number of files in mounted file share, in each view is less than the limit." 
    "Physical Interface Check - Checks physical interface status." 
    "Primary Interface Check - Checks primary interface status." 
    "Network Validation Check - Checks network status by running a group of network tests." 
    "Default Gateway Config Check - Checks the GW config is programmed in the stack." 
    "DNS Config Check - Checks the DNS config is programmed in the stack." "DNS Reachability Check - Checks the reachability to DNS servers." 
    "NTP Config Check - Checks the NTP config is programmed in the stack." 
    "NTP Reachability Check - Checks the reachability to NTP servers." 
    "VLAN Config Check - Checks the VLAN config is programmed in the stack." 
    "VLAN Reachability Check - Checks the VIPs are reachable." 
    "Firewall Config Check - Checks the Firewall configuration is programmed in the stack." 
    "Firewall Status Check - Checks the Firewall status in the stack." 
    "Route Status Check - Checks the reachability to nexthops in routes." 
    "Archive No Tasks - Check cloud archive jobs that are not getting assigned tasks" 
    "Routing Config Check - Checks the Routing config is programmed in the stack." 
    "Routing Status Check - Checks the Routing status in the stack." 
    "Validate Product Model - Checks product model is valid one with all known hardware configuration. If a node has all known good hardware components, product model name will be displayed in hardware.json file as expected. However, if there is any unknown hardware components, product model name will be 'Unknown Platform'." 
    "Check DIMMS - Four different kinds of DIMM related error will be detectd by this script. Missing DIMM, Correctable errors, Uncorrectable errors,  and meory read error in dmesg" 
    "Check System Firmware - Check system firmwares are up to date. Currently installed versions will be compared with the firmware versions that are bundled in Cohesity O/S. This script will run only on Cohesity hardware platforms." 
    "Check NVME System Disk - nvme system disk health status monitor. script will fail if percentage of life remaining is below threshold(30%), or projected months to 30% life left is less than 3 months. Also, either fail of warning will be flaged based on percentage of remaining spare blocks" 
    "Check Missing Disk - Particular number of disks are expected for each platform. hc_cli will compare expected number of disks and number of currently installed disks. This test will fail if any disks are missing." 
    "Check NVME Data Disk - hc_cli to check healthy status of nvme data disk. remaining life and spare block will be checked, also medium error in drive SMART data will be checked." 
    "Indexing Backlog Details - Checks whether indexing backlog are occuring in cluster. If yes, then shows the corresponding VM's with details." 
    "Check NIC Slot Port - Check NIC port link mode, and NICs are correctly installed on the available PIC slots" 
    "Queue Length Check - Checks for qos queues with high number of requests queued. Unusual queue lengths indicate slowness in processing of the requests. This test will fail if one or more qos queues has high number of requests queued over the last one week." 
    "Disk Serial Number Check - Checks if there are any duplicate disk serial numbers in cluster config." 
    "SMB Latency Check - Checks the latency of all smb2 ops to insure none are running longer than one second." "SMB Setup Latency Check - Checks the latency of all smb2 setupops to insure none are running longer than 5-10 seconds." 
    "All hc_cli Tests")


for i in "${!hc_values[@]}"; do
	hc_string+="${hc_labels[$i]} (${hc_values[$i]});"
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
        printf "%s\n " "$hc_choice"
        done
        printf '\n'

        echo "HC_CLI Commands chosen:"
        for hc_choice in "${hc_choices_values[@]}"
        do
        printf "%s\n " "$hc_choice"
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
for y in ${hc_choices_values[@]}
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