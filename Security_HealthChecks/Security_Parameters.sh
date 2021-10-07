#!/bin/bash

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski                                                                                   #"
echo "#Last Updated 10/04/2021                                                                                        #"
echo "#  -updated section: ALL                                                                                        #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

cluster_config.sh fetch 

sourceDir=/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Endo_Pharm
cluster=

slide4parameters=("cluster_name" "cluster_id" "cluster_target_software_version" "hardware_model" "view_box_vec" "all_nodes_reachable" "domain_name_vec")

slide1parameters=("dns_domain_name" "kerberos_server_name" "disabled_trusted_domain_vec" "trusted_domain_discovery_disabled" "ldap_root_dn" )

slide5parameters=("gateway" "")

interfaceGroups=("interface_group_vec")

activeDirectory=("active_directory_config")

#Iterate through parameters to output values to screen.

echo "Slide 1 Parameters" >> parameters.json

for i in "${slide1parameters[@]}"
    do
        slide1=$(grep $i $source/$cluster/cluster_config) | python -m json.tool >> $source/$cluster/$cluster-parameters.json 

        echo $slide1

#Count how many occurences are present.
    echo "NODE COUNT DATA" >> $source/$cluster/$cluster-parameters.json

        nodeCount=$(grep -o node_vec $source/$cluster/cluster_config) | python -m json.tool >> $source/$cluster/$cluster-parameters.json
       
        echo "Node Count is: " $nodeCount

#Interface Group Data
    echo "INTERFACE GROUP DATA" >> $source/$cluster/$cluster-parameters.json

        interface=$(grep -A 13 $interfaceGroups $source/$cluster/cluster_config) | python -m json.tool >> $source/$cluster/$cluster-parameters.json 

#Active Directory Data
    echo "ACTIVE DIRECTORY DATA" >> $source/$cluster/$cluster-parameters.json

        activeDir=$(grep -A 45 $activeDirectory $source/$cluster/cluster_config) | python -m json.tool >> $source/$cluster/$cluster-parameters.json 

