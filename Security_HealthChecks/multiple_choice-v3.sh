#/bin/bash
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

echo "-------------------"
echo "HC_CLI DATA COLLECTION"
echo "-------------------"
echo " "
echo "Use the space bar to select, and the ENTER key to complete your selection. Please choose Cohesity Cluster parameters: "

hc_values=("test-ids=10002" "test-ids=10003" "test-ids=10004" "test-ids=10006" "test-ids=10007" "test-ids=10008" "test-ids=10009" "test-ids=10011" "test-ids=10012" "test-ids=10015" "test-ids=10017" "test-ids=10018" "test-ids=10020" "test-ids=10021" "test-ids=10023" "test-ids=10025" "test-ids=10026" "test-ids=10027" "test-ids=10028" "test-ids=10030" "test-ids=10031" "test-ids=10032" "test-ids=10033" "test-ids=10035" "test-ids=10036" "test-ids=10037" "test-ids=10038" "test-ids=10039" "test-ids=10040" "test-ids=10043" "test-ids=10044" "test-ids=10045" "test-ids=10046" "test-ids=10047" "test-ids=10048" "test-ids=10049" "test-ids=10050" "test-ids=10051" "test-ids=10052" "test-ids=10053" "test-ids=10054" "test-ids=10055" "test-ids=10057" "test-ids=10058" "test-ids=10059" "test-ids=10060" "test-ids=10061" "test-ids=10062" "test-ids=10063" "test-ids=10064" "test-ids=10065" "test-ids=10066" "test-ids=10067" "test-ids=10068" "test-ids=10069" "test-ids=10070" "test-ids=10071" "test-ids=10072" "test-ids=10073" "test-ids=10074" "test-ids=10075" "test-ids=10076" "test-ids=10077" "test-ids=10081" "test-ids=10082" "test-ids=10083" "test-ids=10084" "test-ids=10085" "test-ids=10086" "test-ids=10087" "test-ids=10088" "test-ids=10089" "test-ids=10090" "test-ids=10101" "test-ids=10102" "all")
hc_labels=(
    "Hardware HDD Utility" 
    "Binary Files Release Version Check" 
    "Parition Size Check" 
    "Cloud Connectivity" 
    "Constituent Uptime Check" 
    "NTP Sync Check" 
    "Alert Mail Config Check" 
    "Agent Health Check" 
    "CPU Throttled Check" 
    "Winbind Availability Check" 
    "AWS Reachability Check" 
    "Alert Service Check" 
    "Syslog Server Check" 
    "Disk Commands Check" 
    "Hardware PCIe Link Check" 
    "NTPD Reachability Check" 
    "Bond Mode Check" 
    "Node Connectivity" 
    "Uncorrectable ECC MCE" 
    "Default Gateway Status" 
    "Check LDAP Connectivity" 
    "Firewalld Status Check" 
    "Dedup Status Check" 
    "HDD Disk Availability Check" 
    "Vault Connectivity" 
    "Stale File Handle Error Check" 
    "Bridge Proxy Exec Check" 
    "SSD Lifetime Write Limit Check" 
    "D State Check" 
    "Node Uptime" 
    "IPMI Permissions" 
    "OOM Check" 
    "Librarian Status Check" 
    "Read Only Disk Check" 
    "VSS Snapshots CNT Check" 
    "Storage Proxy Memory Check" 
    "SMB Exclude Snapshot Check" 
    "Cluster Disk Usage Check" 
    "Multiple RAIDS Configuration Check" 
    "Yoda XFS Check" 
    "Duplicate Node IP Configuration Check" 
    "Protection Sources Connectivity Check" 
    "Backup Job SLA Violation" 
    "Apollo Healer Deadlin Check" 
    "Disk Latency Check" 
    "File Count Limit Check" 
    "Physical Interface Check" 
    "Primary Interface Check" 
    "Network Validation Check" 
    "Default Gateway Config Check" 
    "DNS Config Check" 
    "NTP Config Check" 
    "NTP Reachability Check" 
    "VLAN Config Check" 
    "VLAN Reachability Check" 
    "Firewall Config Check" 
    "Firewall Status Check" 
    "Route Status Check" 
    "Archive No Tasks" 
    "Routing Config Check" 
    "Routing Status Check" 
    "Validate Product Model" 
    "Check DIMMS" 
    "Check System Firmware" 
    "Check NVME System Disk" 
    "Check Missing Disk" 
    "Check NVME Data Disk" 
    "Indexing Backlog Details" 
    "Check NIC Slot Port" 
    "Queue Length Check" 
    "Disk Serial Number Check" 
    "SMB Latency Check" 
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
 