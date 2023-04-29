#!/bin/bash


function checkSum {
    checkSum_valid="false"
    printf '\n'
    printf '\n'
    echo "Verifying Checksum on download..."
    printf '\n'
    sumCheck=`sudo sha256sum "/home/cohesity/bin/installers/$agent" | head -n1 | awk '{print $1;}' | sed 's/ //g'`
    if [[ "$sumCheck" == "$valid_checkSum" ]]; then 
        checkSum_valid="true"
        echo "Checksum for v$y $x Agent verified successfully"
        printf '\n'

        echo "Disseminating Updated $x Agent across Cohesity Cluster..."
        printf '\n'
        allscp.sh /home/cohesity/bin/installers/$agent /home/cohesity/bin/installers/

    else
        checkSum_valid="false"
        echo "Checksum for v$y $x Agent NOT verified!"
        printf '\n'
    fi

}

function write_log {

    log_file="$SCRIPT_DIR/manualUpdatesNEEDED-`date +%s`.txt"

    printf '\n' | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "!!! ATTENTION for New Cohesity v$y Agent Implementation: The agent_installer_files.json file could not be updated automatically, please reference the $SCRIPT_DIR/manualUpdatesNEEDED log for further instructions prior to attempting to update agents via Cohesity UI !!!" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "It is IMPERATIVE that you read these instructions to completion prior to attempting any of the below tasks - thank you." | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "You will need to update the /home/cohesity/bin/installers/agent_installer_files.json file manually by using the below instructions..." | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Rename the file by running the following command: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "cp -p /home/cohesity/bin/installers/agent_installer_files.json /home/cohesity/bin/installers/agent_installer_files.json.new" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Open the /home/cohesity/bin/installers/agent_installer_files.json.new file in edit mode by running the following command: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "vi /home/cohesity/bin/installers/agent_installer_files.json file" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Find each "Hostenv" section that refers to the following updated Agents: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"

    if [[ -n "${updated_6_5_1_agents[@]}" ]]; then
        for key in "${!updated_6_5_1_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v6.5.1f: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_6_5_1_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi
    if [[ -n "${updated_6_6_agents[@]}" ]]; then
        for key in "${!updated_6_6_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v6.6: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_6_6_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi
    if [[ -n "${updated_6_6_0d_Go_agents[@]}" ]]; then
        for key in "${!updated_6_6_0d_Go_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v6.6.0d_GoAgent: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_6_6_0d_Go_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi
    if [[ -n "${updated_6_6_0d_ent_agents[@]}" ]]; then
        for key in "${!updated_6_6_0d_ent_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v6.6.0d_ent: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_6_6_0d_ent_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi
    if [[ -n "${updated_6_8_1_agents[@]}" ]]; then
        for key in "${!updated_6_8_1_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v6.8.1: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_6_8_1_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi
    if [[ -n "${updated_7_0_agents[@]}" ]]; then
        for key in "${!updated_7_0_agents[@]}"; do
            echo "Updated Cohesity Agents Downloaded for v7.0: "
            echo "HostEnv: ${key}"      -       "Filename: ${updated_7_0_agents[${key}]}" | tee -a "$log_file"
            printf '\n' | tee -a "$log_file"
        done
    fi

    printf '\n' | tee -a "$log_file"
    echo "* Hit the 'i' key to enable INSERT mode" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Replace the Filename in each section with it's respective new Agent filename " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* If there is no "Hostenv" parameter that references the updated Agent, please create a section by copying a section with similar parameters and updating the Hostenv, AgentType, and Filename fields " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Please call support if you need assistance with this: 1-855-926-4374" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Once correct changes have been made, please save the file by hitting the Escape key, then typing ':wq' (without the quotes), and then hit the Enter key" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Disseminate the updated /home/cohesity/bin/installers/agent_installer_files.json.new across Cohesity Cluster by running the following command: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "allscp.sh /home/cohesity/bin/installers/agent_installer_files.json.new /home/cohesity/bin/installers/agent_installer_files.json.new" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "* Lastly, we rename the /home/cohesity/bin/installers/agent_installer_files.json.new back to /home/cohesity/bin/installers/agent_installer_files.json by running the following command: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "allssh.sh 'sudo cp -p /home/cohesity/bin/installers/agent_installer_files.json.new /home/cohesity/bin/installers/agent_installer_files.json'" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "!!! If there was a "Permission Denied" error during the dissemination of any of the updated Cohesity Agents, please run the following command manually: " | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"
    echo "allscp.sh /home/cohesity/bin/installers/REPLACE_WITH_AGENT_FILENAME /home/cohesity/bin/installers/" | tee -a "$log_file"
    printf '\n' | tee -a "$log_file"

}

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
      selected+=("${defaults[i]:-false}")
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

SCRIPT_DIR=`pwd`
declare -A updated_6_5_1_agents
declare -A updated_6_6_agents
declare -A updated_6_6_0d_Go_agents
declare -A updated_6_6_0d_ent_agents
declare -A updated_6_8_1_agents
declare -A updated_7_0_agents
declare -A updated_agents


version_values=("6.5.1f" "6.6" "6.6.0d_GoAgent" "6.6.0d_ent" "6.8.1" "7.0")
#opt_labels=("cloud" "on-prem" "virtual")

for i in "${!version_values[@]}"; do
	opt_string+="${version_values[$i]};" # (${opt_labels[$i]});"
done

printf '\n'
printf '\n'
echo "Which Version Cohesity is installed on this Cluster?"
echo "(please choose ONE)"
printf '\n'
prompt_for_multiselect selection "$opt_string"

for i in "${!selection[@]}"; do
	if [ "${selection[$i]}" == "true" ]; then
		selected+=("${version_values[$i]}")
	fi
done

echo "Cohesity Cluster Version(s) selected: ${selected[@]}"
printf '\n'

if [[ -n "${selected[@]}" ]]; then
#if [${selected[@]} != None ]; then
    # echo "Backing up /home/cohesity/bin/installers directory on all Cohesity Cluster Nodes..."
    # allssh.sh sudo cp -r /home/cohesity/bin/installers /home/cohesity/bin/installers_old

    echo "Backing up /home/cohesity/bin/installers/agent_installer_files.json on all Cohesity Cluster Nodes..."
    printf '\n'
    cp -p /home/cohesity/bin/installers/agent_installer_files.json /home/cohesity/bin/installers/agent_installer_files.json.bak
    allscp.sh /home/cohesity/bin/installers/agent_installer_files.json.bak /home/cohesity/bin/installers/

    # changing directory in order to download agents to appropriate directory
    cd /home/cohesity/bin/installers

    for y in "${selected[@]}"; do 
        if [ $y == "6.5.1f" ]; then 
            v6_5_agents=("AIX")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v6_5_agents[@]}"; do
                v6_5_string+="${v6_5_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v6_5_selection "$v6_5_string"

            for b in "${!v6_5_selection[@]}"; do
                if [ "${v6_5_selection[$b]}" == "true" ]; then
                    v6_5_selected+=("${v6_5_agents[$b]}")
                fi
            done
            echo "${v6_5_selected[@]}"
    
            for x in "${v6_5_selected[@]}"; do 
                if [ $x == "AIX" ]; then 

                    # printf '\n'
                    # echo "Please enter Cohesity UI Admin Username to allow gflag application: "
                    # read -e username

                    # printf '\n'
                    # echo "Please enter the Cohesity Cluster UI Username password: "
                    # read -es password

                    agent="cohesity_agent_6.5.1f_cpd_aix_java.bff"
                    valid_checkSum="64b151166c0ad1ab365179bbb0cfcfabd218e2ade98b7b11feca934b386c4020"

                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    printf '\n'
                    download=`curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/$agent" -o "/home/cohesity/bin/installers/$agent"`
                    echo "Download Results: $download"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum" "$x"

                    if [ $checkSum_valid == "true" ]; then
                        updated_6_5_1_agents[$x]+=" $agent"

                    echo "Applying Gflag for AIX Agent Upgrade (magneto_master_agent_sw_set_force_upgradable=true)..."
                    echo "Please enter Cohesity UI Admin User Credentials:"
                    iris_cli cluster update-gflag service-name=magneto gflag-name=magneto_master_agent_sw_set_force_upgradable gflag-value=true effective-now=true reason="Set gflag to update aix java agent"

                    fi
                fi
            done
        fi
                    

        if [ $y == "6.6" ]; then 
            v6_6_agents=("AIX")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v6_6_agents[@]}"; do
                v6_6_string+="${v6_6_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v6_6_selection "$v6_6_string"

            for b in "${!v6_6_selection[@]}"; do
                if [ "${v6_6_selection[$b]}" == "true" ]; then
                    v6_6_selected+=("${v6_6_agents[$b]}")
                fi
            done
            echo "${v6_6_selected[@]}"

            for x in "${v6_6_selected[@]}"; do 
                if [ $x == "AIX" ]; then 
                    agent = 'cohesity_agent_6.6.0d_u6_p34_cpd_aix_java.bff'
                    valid_checkSum="60013063d51c46fcb7b67dded39c671ebba46f7e5b81eedbf67ff9d8023d5837"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    printf '\n'
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/$agent"  -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_6_agents[$x]+=" $agent"

                    echo "Applying Gflag for AIX Agent Upgrade (magneto_master_agent_sw_set_force_upgradable=true)..."
                    echo "Please enter Cohesity UI Admin User Credentials:"
                    iris_cli cluster update-gflag service-name=magneto gflag-name=magneto_master_agent_sw_set_force_upgradable gflag-value=true effective-now=true reason="Set gflag to update aix java agent"

                    fi
                fi
            done
        fi


        if [ $y == "6.6.0d_GoAgent" ]; then 
            v6_6d_agents=("Solaris_10_SPARC" "Solaris_11_SPARC")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v6_6d_agents[@]}"; do
                v6_6d_string+="${v6_6d_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v6_6d_selection "$v6_6d_string"

            for b in "${!v6_6d_selection[@]}"; do
                if [ "${v6_6d_selection[$b]}" == "true" ]; then
                    v6_6d_selected+=("${v6_6d_agents[$b]}")
                fi
            done
            echo "${v6_6d_selected[@]}"

            for x in "${v6_6d_selected[@]}"; do 
                if [ $x == "Solaris_10_SPARC" ]; then 
                    agent="cohesity_agent_6.6.0d_u6_p34_cpd_solaris_10"
                    valid_checkSum="a7196c86f74d64f9f59d28e761bac895b6ecd6313d64e3e8275b15ce0a398968"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.6.0d_u6_p34_cpd_new/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_6_0d_Go_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_11_SPARC" ]; then 
                    agent="cohesity_agent_6.6.0d_u6_p34_cpd_solaris"
                    valid_checkSum="fdd860e5dad19c0e8cea3ee152200a6520d92d6affb1bb9c8a665ea3b07cbd25"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.6.0d_u6_p34_cpd_new/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_6_0d_Go_agents[$x]+=" $agent"

                    fi
                fi
            done
        fi

        if [ $y == "6.6.0d_ent" ]; then 
            v6_6d_ent_agents=("AIX")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v6_6d_ent_agents[@]}"; do
                v6_6d_string+="${v6_6d_ent_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v6_6d_selection "$v6_6d_string"

            for b in "${!v6_6d_selection[@]}"; do
                if [ "${v6_6d_selection[$b]}" == "true" ]; then
                    v6_6d_ent_selected+=("${v6_6d_ent_agents[$b]}")
                fi
            done
            echo "${v6_6d_ent_selected[@]}"

            for x in "${v6_6d_ent_selected[@]}"; do 
                if [ $x == "AIX" ]; then 
                    agent="cohesity_agent_6.6.0d_ent_aix_java.bff"
                    valid_checkSum="6505214b18df308dde1db5b9fce604f2955ebcf0b9dfb40faa610a2978e076e4"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_6_0d_ent_agents[$x]+=" $agent"

                    echo "Applying Gflag for AIX Agent Upgrade (magneto_master_agent_sw_set_force_upgradable=true)..."
                    echo "Please enter Cohesity UI Admin User Credentials:"
                    iris_cli cluster update-gflag service-name=magneto gflag-name=magneto_master_agent_sw_set_force_upgradable gflag-value=true effective-now=true reason="Set gflag to update aix java agent"

                    fi
                fi
            done
        fi

        if [ $y == "6.8.1" ]; then 
            v6_8_1_agents=("AIX" "HP-UX" "Solaris_10_SPARC" "Solaris_11_SPARC" "Linux PowerPC")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v6_8_1_agents[@]}"; do
                v6_8_1_string+="${v6_8_1_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v6_8_1_selection "$v6_8_1_string"

            for b in "${!v6_8_1_selection[@]}"; do
                if [ "${v6_8_1_selection[$b]}" == "true" ]; then
                    v6_8_1_selected+=("${v6_8_1_agents[$b]}")
                fi
            done
            echo "${v6_8_1_selected[@]}"

            for x in "${v6_8_1_selected[@]}"; do 
                if [ $x == "AIX" ]; then 
                    agent="cohesity_agent_6.8.1_u2_p10_cpd_aix_java.bff"
                    valid_checkSum="f524782d1ee243d2eae89a098768c3ad01dcc8b99b43022744f67ada77cef07f"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.8.1_u2_p10/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_8_1_agents[$x]+=" $agent"

                    echo "Applying Gflag for AIX Agent Upgrade (magneto_master_agent_sw_set_force_upgradable=true)..."
                    echo "Please enter Cohesity UI Admin User Credentials:"
                    iris_cli cluster update-gflag service-name=magneto gflag-name=magneto_master_agent_sw_set_force_upgradable gflag-value=true effective-now=true reason="Set gflag to update aix java agent"

                    fi
                fi

                if [ $x == "HP-UX" ]; then 
                    agent="cohesity_java_agent_6.8.1_u2_p10_cpd_hpux.depot"
                    valid_checkSum="60579264b18778dbcdeb179a0cda485f136e618e5a76b1422cb244da95b29269"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.8.1_u2_p10/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_8_1_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_10_SPARC" ]; then 
                    agent="cohesity_java_agent_6.8.1_u2_p10_cpd_solaris_10_sparc"
                    valid_checkSum="326b720cd3e25350fb84c6fb02bcb16f4a09ea365610363f8c179f7a90d4a8a4"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.8.1_u2_p10/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_8_1_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_11_SPARC" ]; then 
                    agent="cohesity_java_agent_6.8.1_u2_p10_cpd_solaris_11_sparc"
                    valid_checkSum="01055a58c189aa370065ac6205ff4f6b288b7de9b7fc6b0acce12c6f8269e2a3"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.8.1_u2_p10/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_8_1_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Linux PowerPC" ]; then 
                    agent="cohesity-java-agent-6.8.1_u2_p10_cpd-1.ppc64le.rpm"
                    valid_checkSum=
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/6.8.1_u2_p10/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_6_8_1_agents[$x]+=" $agent"

                    fi
                fi
            done
        fi

        if [ $y == "7.0" ]; then 
            v7_0_agents=("AIX" "HP-UX" "Solaris_10_SPARC" "Solaris_10_x86_64" "Solaris_11_SPARC" "Solaris_11_x86_64" "Linux PowerPC")
            #opt_labels=("cloud" "on-prem" "virtual")

            for z in "${!v7_0_agents[@]}"; do
                v7_0_string+="${v7_0_agents[$z]};" # (${opt_labels[$i]});"
            done

            printf '\n'
            printf '\n'
            echo "Which Agents do you need to update for Cohesity v$y?"
            printf '\n'
            prompt_for_multiselect v7_0_selection "$v7_0_string"

            for b in "${!v7_0_selection[@]}"; do
                if [ "${v7_0_selection[$b]}" == "true" ]; then
                    v7_0_selected+=("${v7_0_agents[$b]}")
                fi
            done
            echo "${v7_0_selected[@]}"

            for x in "${v7_0_selected[@]}"; do 
                if [ $x == "AIX" ]; then 
                    agent="cohesity_agent_7.0_u1_hf1_cpd_aix_java.bff"
                    valid_checkSum="48f66a7963a529cf97e51355dfdb4414b9a6df7791e7f435338925532073fe01"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    echo "Applying Gflag for AIX Agent Upgrade (magneto_master_agent_sw_set_force_upgradable=true)..."
                    echo "Please enter Cohesity UI Admin User Credentials:"
                    iris_cli cluster update-gflag service-name=magneto gflag-name=magneto_master_agent_sw_set_force_upgradable gflag-value=true effective-now=true reason="Set gflag to update aix java agent"

                    fi
                fi

                if [ $x == "HP-UX" ]; then 
                    agent="cohesity_java_agent_7.0_u1_hf1_cpd_hpux.depot"
                    valid_checkSum="61f6cfe63c702e7b6e6def01591e403a71226bc0ff92eede0e1347a27f95d127"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_10_SPARC" ]; then 
                    agent="cohesity_java_agent_7.0_u1_hf1_cpd_solaris_10_sparc"
                    valid_checkSum="144d9c1b63e15ebe5f3395e39dd8ff18cdb686bc2c181a64d8a2ca019a147698"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_10_x86_64" ]; then 
                    agent="cohesity_java_agent_7.0_u1_hf1_cpd_solaris_10_x86_64"
                    valid_checkSum="07f84ff294353609324ebdf9fc7e2d698c9904f70cef5ab17ce12b02c029e099"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_11_SPARC" ]; then 
                    agent="cohesity_java_agent_7.0_u1_hf1_cpd_solaris_11_sparc"
                    valid_checkSum="7f3b846a2b85852583d93f2412e8061a5c1745e01630b0c50d3148f6a27b5cda"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Solaris_11_x86_64" ]; then 
                    agent="cohesity_java_agent_7.0_u1_hf1_cpd_solaris_11_x86_64"
                    valid_checkSum="1aa45e34a259d035457beaedb2650130d0bcd3171daabb9e9ce9019d732e9988"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi

                if [ $x == "Linux PowerPC" ]; then 
                    agent="cohesity-java-agent-7.0_u1_hf1_cpd-1.ppc64le.rpm"
                    valid_checkSum="ffa8286cbb1416d1fd8081a5ec0554d0e1dde9b22fc1cfcd49db433fc3716bae"
                    printf '\n'
                    printf '\n'
                    echo "Downloading Updated $x Agent: $agent"
                    curl "https://www.downloads.cohesity.com/artifacts/java_agent_cert_exp/7.0_u1_hf1/$agent" -o "/home/cohesity/bin/installers/$agent"

                    printf '\n'
                    checkSum "$agent" "$valid_checkSum"

                    if [ $checkSum_valid == "true" ]; then 
                        updated_7_0_agents[$x]+=" $agent"

                    fi
                fi
            done
        fi
    done
fi

write_log "$updated_6_5_1_agents" "$updated_6_6_agents" "$updated_6_6_0d_Go_agents" "$updated_6_6_0d_ent_agents" "$updated_6_8_1_agents" "$updated_7_0_agents"
