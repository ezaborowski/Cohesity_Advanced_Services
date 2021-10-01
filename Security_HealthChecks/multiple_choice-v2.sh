#/bin/bash
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

iris_labels=("Networking - To list the bonding mode of the NICs, DNS servers, subnets, interfaces, domain names, and NTP servers for the Cluster." "Informative - To get the hosts info and and general information about the Cluster." "Access Management - To list the proxy servers, client subnets with permissions to access Views, and NFS export paths accessible in the Cluster." "Security - To get the SSL certificate details of the Cluster and list public SSH Keys." "To get the preferred IO tier of the Cluster.")   

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

