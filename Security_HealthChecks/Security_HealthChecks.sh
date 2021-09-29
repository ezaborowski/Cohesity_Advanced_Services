#!/bin/bash

echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski and Christopher Peyton - August 12 2021                                           #"
echo "#Last Updated 9/29/2021                                                                                         #"
echo "#  -updated parameter choice section                                                                            #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

echo "Please enter Cluster address, e.g https://localhost:8053 or https://mycluster"
read url
echo "Please enter a prefix for output json and tgz"
read filename
echo "Please enter Cluster username"
read username
echo "Please enter Cluster password"
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
#Asks user to choose what Cohesity Cluster parameters to output.

options_values=("cluster" "externalClientSubnets" "basicClusterInfo" "clusterPartitions" "apps" "nodes" "interfaceGroups" "vlans" "viewBoxes" "remoteClusters" "vaults" "activeDirectory" "roles" "users" "idps" "groups" "alertNotificationRules" "views" "protectionPolicies" "protectionSources" "protectionJobs")
options_labels=("Cohesity Cluster" "Subnets" "Basic Cluster Info" "Partitions" "Apps" "Cluster Nodes" "Interface Groups" "vLANS" "Storage Domains" "Remote Clusters" "Archive Targets" "Active Directory" "Cohesity Roles" "Cohesity Users" "idps" "Cohesity Groups" "Alerts" "Views" "Protection Policies" "Sources" "Protection Jobs")

#---------------------------------------------------------------------------------------------------------------#
#NOTES:
#hc_cli
#options_values=("10002" "10003" "10004" "10006" "10007" "10008" "10009" "10011" "10012" "10015" )
#options_labels=("Hardware HDD Utility - Checks for load per disk via iostat and reports the usage percentage of I/O." "Binary Files Release Version Check - Checks for release version of Cluster and version of all binary files and ensures both versions are the same." "Parition Size Check - Checks the used space for each partition and reports the usage percentage." "Cloud Connectivity - Checks connectivity to Helios with proxy enabled or disabled." "Constituent Uptime Check - Checks for uptime of services and counts the number of recent service restarts. Services which aren't up for 5 minutes are marked as FAIL." "NTP Sync Check - Checks if node's time is in sync with NTP server by running ntpq -pn." "Alert Mail Config Check - Checks whether email address is configured to receive alerts." "Agent Health Check - Retrieves agent health from REST API and reports unhealthy agents." "CPU Throttled Check - Checks for CPU throttle event using 'lscpu' command. Checks for CPU speed less than 1000mhz." "Winbind Availability Check - Checks winbind service status with the 'wbinfo -P' command." )

#iris_cli
#---------------------------------------------------------------------------------------------------------------#

for i in "${!options_values[@]}"; do
	options_string+="${options_labels[$i]} (${options_values[$i]});"
done

echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

prompt_for_multiselect choice "$options_string"

    for i in "${!choice[@]}"; do
        if [ "${choice[$i]}" == "true" ]; then
            choices+=("${options_labels[$i]}")
            choices_values+=("${options_values[$i]}")
        fi
    done

        # Write out each choice
        echo "You selected the following: "
        for choice in "${choices[@]}"
        do
        printf "%s\n " "$choice"
        done
        printf '\n'

        echo "API Commands chosen:"
        for choice in "${choices_values[@]}"
        do
        printf "%s\n " "$choice"
        done
        printf '\n'

#---------------------------------------------------------------------------------------------------------------#
#Run chosen API data gathering commands.

#get token
token=$(curl -s -k -X POST --url "${url}/irisservices/api/v1/public/accessTokens" -H 'Accept: application/json' -H 'Content-type: application/json' --data-raw '{"password": "'$password'", "username": "'$username'"}' | cut -d : -f 2 | cut -d, -f1 )
​
              echo "Token is" $token
​
#Add or remove the desired api calls as needed
urlcalls="cluster externalClientSubnets basicClusterInfo clusterPartitions apps nodes interfaceGroups vlans viewBoxes remoteClusters vaults activeDirectory roles users idps groups alertNotificationRules views protectionPolicies protectionSources protectionJobs"
​
#Loop through each api call, optionally pipe to json.tool to beautify.
for f in ${choices_values[@]}
do
         echo -e "\nCalling $f \n"
​
         curl -s -k -X GET -G --url "$url/irisservices/api/v1/public/$f" -H "Authorization: Bearer $token" -H 'Accept: text/html' | python -m json.tool > $filename-$f-`date +%s`.json
 done

#Create output tgz in local directory.
 echo "Creating output tgz"
 tar -cvzf $filename-`date +%s`.tgz $filename*.json

 #---------------------------------------------------------------------------------------------------------------#

sudo su cohesity

hc_cli run -u $username -p $password -v | python -m json.tool > $filename-healthcheck_all-`date +%s`.json
    hc_cli run --test-ids=10006


iris_cli -username $username -password $password cluster info 