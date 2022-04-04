#!/bin/bash
# PATH="$PATH:/home/cohesity/software/crux/bin/allssh.sh"

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski - August 12 2021                                                                  #"
echo "#Last Updated 12/10/2021                                                                                        #"
echo "#  -updated parameter choice section: parameters                                                                #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

printf '\n'
echo "Please enter Cluster address (ex: localhost:8053 or mycluster.mydomain.com): "
read -e url
printf '\n'
echo "Please enter a prefix to append to output files: "
read -e filename
printf '\n'
echo "Please enter a Local Cohesity Cluster UI domain (ex: LOCAL or your active directory domain): "
read -e domain
printf '\n'
echo "Please enter a Local Cohesity Cluster UI username: "
read -e username
printf '\n'
echo "Please enter a Local Cohesity Cluster UI password: "
read -es password
printf '\n'


#---------------------------------------------------------------------------------------------------------------#
#Run CONFIG data gathering commands.

printf '\n'
printf '\n'
echo "-------------------"
echo "CONFIG DATA COLLECTION"
echo "-------------------"
echo " "

printf '\n'
printf '\n'
echo "Making secLogs/CONFIG subdirectory to save all logs to..."
  mkdir secLogs 2> /dev/null
  mkdir secLogs/CONFIG 2> /dev/null
    sleep 5

#config_checks=("'ls -ltrGg ~/logs/*FATAL*|tail -4'" "'grep -i LDAP /home/cohesity/data/logs/bridge_exec.INFO'" "'iostat | grep -A 1 avg-cpu'")

printf '\n'
printf '\n'
echo "Running CONFIG Data Collection Commands and saving output to CONFIG-Logs folder..."
  sleep 5
printf '\n'

#Run config call which writes the output to the /tmp folder.
# for w in "${config_checks[@]}"
# do
#         source /home/cohesity/software/crux/bin/allssh.sh 
#         echo -e "\nCalling $w \n" 
#         allssh.sh $w | python -m json.tool >> secLogs/CONFIG/$filename-CONFIG-`date +%s`.json
# done

echo -e "\nPulling Cluster_config \n" 
cluster_config.sh fetch 2> /dev/null
cat /tmp/cluster_config > secLogs/CONFIG/$filename-CONFIG-CLUSTER_CONFIG-`date +%s`.json

echo -e "\nPulling FATAL_logs \n" 
/home/cohesity/software/crux/bin/allssh.sh 'ls -ltrGg /home/cohesity/data/logs/*FATAL*|tail -4' > secLogs/CONFIG/$filename-CONFIG-FATALS_logs-`date +%s`.yml

echo -e "\nPulling LDAP_errors \n" 
/home/cohesity/software/crux/bin/allssh.sh 'grep -i LDAP /home/cohesity/data/logs/bridge_exec.INFO' > secLogs/CONFIG/$filename-CONFIG-LDAP_errors-`date +%s`.json

echo -e "\nPulling IO_stats \n" 
/home/cohesity/software/crux/bin/allssh.sh 'iostat | grep -A 1 avg-cpu' > secLogs/CONFIG/$filename-CONFIG-IO_stats-`date +%s`.json

echo -e "\nPulling Cert_validation \n" 
curl -v "https://$url" &> /dev/stdout | tee -a secLogs/CONFIG/$filename-CONFIG-Cert_val-`date +%s`.json

#---------------------------------------------------------------------------------------------------------------#
#Run API data gathering commands.

printf '\n'
printf '\n'
echo "-------------------"
echo "API DATA COLLECTION"
echo "-------------------"
echo " "

printf '\n'
printf '\n'
echo "Making secLogs/API subdirectory to save all logs to..."
  mkdir secLogs 2> /dev/null
  mkdir secLogs/API 2> /dev/null
#  mkdir secLogs/API/$filename-API-certificates 2> /dev/null
    sleep 5

api_checks=(basicClusterInfo, activeDirectory, ldapProvider, domainControllers, antivirusGroups, icapConnectionStatus, infectedFiles, alerts, roles, users, groups, remoteClusters, vaults, viewBoxes, views, alertNotificationRules, idps, cluster, apps, protectionJobs, scheduler, protectionPolicies)
api_stats_checks=(storage, viewBoxes, vaults, protectionJobs)
#public/ldapProvider/{id}/status

endTime=$(date +%s%N)
startTime=$(($endTime - 7*86400000000000))

#echo $endTime
#echo $startTime

printf '\n'
printf '\n'
echo "Running API Data Collection Commands and saving output to API-Logs folder..."
printf '\n'
echo "This may take a few moments..."
  sleep 5
printf '\n'

#get token
token=`curl -X POST -k "https://$url/irisservices/api/v1/public/accessTokens" -H "accept: application/json" -H "content-type: application/json" -d "{ \"domain\": \"$domain\", \"password\": \"$password\", \"username\": \"$username\"}" | cut -d : -f 2 | cut -d, -f1 `

              echo "The Access Token is" $token

#Loop through each api call and write the output of each call to secLogs/API-Logs folder. Piping to json.tool to beautify.

echo -e "\nCalling certificates/webServer \n"

curl -X GET -k "https://$url/irisservices/api/v1/public/certificates/webServer" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-certificates-`date +%s`.json


echo -e "\nCalling backupjobsummary \n"

curl -X GET -k "https://$url/irisservices/api/v1/backupjobssummary?_includeTenantInfo=true&allUnderHierarchy=true&endTimeUsecs=$endTime&onlyReturnJobDescription=false&startTimeUsecs=$startTime&outputFormat=csv" -H "accept: application/json" -H "Authorization: Bearer $token" > secLogs/API/$filename-API-protectionSummary-`date +%s`.csv


echo -e "\nCalling kerberos \n"

curl -X GET -k "https://$url/irisservices/api/v2/kerberos-providers" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-kerberos-`date +%s`.json


echo -e "\nCalling keystone \n"

curl -X GET -k "https://$url/irisservices/api/v2/keystones" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-keystone-`date +%s`.json


echo -e "\nCalling mcmConfig \n"

curl -X GET -k "https://$url/irisservices/api/v1/mcm/config" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-mcmConfig-`date +%s`.json


echo -e "\nCalling ldap \n"

curl -X GET -k "https://$url/irisservices/api/v1/public/tenants" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-ldap-`date +%s`.json


echo -e "\nCalling firewall \n"

curl -X GET -k "https://$url/irisservices/api/v1/nexus/firewall/list" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-firewall-`date +%s`.json


echo -e "\nCalling stats/vaults/providers \n"

curl -X GET -k "https://$url/irisservices/api/v1/public/stats/vaults/providers" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-stats_vaults_providers-`date +%s`.json


for x in $(echo ${api_checks[@]} | sed "s/,/ /g")
do
        echo -e "\nCalling $x \n"

        curl -X GET -k "https://$url/irisservices/api/v1/public/$x" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-$x-`date +%s`.json
 done


for x in $(echo ${api_stats_checks[@]} | sed "s/,/ /g")
do
        echo -e "\nCalling stats/$x \n"

        curl -X GET -k "https://$url/irisservices/api/v1/public/stats/$x" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-stats_$x-`date +%s`.json
 done


#---------------------------------------------------------------------------------------------------------------#
#Run IRIS_CLI data gathering commands.

printf '\n'
printf '\n'
echo "-------------------"
echo "IRIS_CLI DATA COLLECTION"
echo "-------------------"
echo " "

printf '\n'
printf '\n'
echo "Making secLogs/IRIS subdirectory to save all logs to..."
  mkdir secLogs/IRIS 2> /dev/null
    sleep 5

iris_checks=("alert ls" "syslog-server list" "user list" "role list" "cluster ls-gflags")
#"ad list-centrify-zones domain-name=$domain"

declare -A iris_filenames
iris_filenames=( [alert \ls]=alert [syslog-server list]=syslog [user list]=users [role list]=roles [cluster ls-gflags]=gflags )

printf '\n'
printf '\n'
echo "Running IRIS_CLI Data Collection Commands and saving output to IRIS_CLI-Logs folder..."
  sleep 5
printf '\n'

#Loop through each iris_cli call and write the output of each call to secLogs/IRIS_CLI-Logs folder
for y in "${iris_checks[@]}"
do
      d=${iris_filenames[$y]}
         
         echo -e "\nCalling $y \n"

         iris_cli -domain $domain -username $username -password "$password" $y > secLogs/IRIS/$filename-IRIS-$d-`date +%s`.json
 done

#---------------------------------------------------------------------------------------------------------------#
#Run HC_CLI data gathering commands.

printf '\n'
printf '\n'
echo "-------------------"
echo "HC_CLI DATA CHECKS"
echo "-------------------"
echo " "

printf '\n'
printf '\n'
echo "Making secLogs/HC subdirectory to save all logs to..."
  mkdir secLogs/HC 2> /dev/null
    sleep 5

hc_checks=(test-ids=10001, test-ids=10002, test-ids=10003, test-ids=10008, test-ids=10040)

declare -A hc_array
hc_array=( [test-ids=10001]=Hardware_HDD_dWord [test-ids=10002]=Hardware_HDD_Utility [test-ids=10003]=Binary_Files_Release_Version_Check [test-ids=10008]=NTP_Sync_Check [test-ids=10040]=SSD_Lifetime_Write_Limit_Check )

printf '\n'
printf '\n'
echo "Running HC_CLI Data Check Commands and saving output to HC_CLI-Logs folder."
printf '\n'
echo "This may take a few moments..."
  sleep 5
printf '\n'

#Loop through each hc_cli calls and write the output of each call to secLogs/HC_CLI-Logs folder
for z in $(echo ${hc_checks[@]} | sed "s/,/ /g")
do
      d=${hc_array[$z]}

         echo -e "\nCalling $z \n"
         
        #  sudo su cohesity hc_cli run -domain $domain -u $username -p '$password' -v --$z >> secLogs/HC/$filename-HC-$d-`date +%s`.json

         hc_cli run -domain $domain -u $username -p $password -v --$z >> secLogs/HC/$filename-HC-$d-`date +%s`.json

         #sudo hc_cli run -v -u $username -p $password --$z > secLogs/HC/$filename-HC-$d-`date +%s`.json || hc_cli run -v -u $username -p $password --$z >> secLogs/HC/$filename-HC-$d-`date +%s`.json

done
echo -e "\nCalling ALL HC_CLI Tests \n"

# sudo su cohesity hc_cli run -domain $domain -u $username -p '$password' -v --test-ids=all >> secLogs/HC/$filename-HC_CLI-ALL-`date +%s`.json

hc_cli run -domain $domain -u $username -p $password -v >> secLogs/HC/$filename-HC_CLI-ALL-`date +%s`.json

#---------------------------------------------------------------------------------------------------------------#

#Create tarball from files 
tar czvfP secLogs.tar.gz secLogs/

printf '\n'
echo "Files compressed in /home/support/secLogs.tar.gz. Please SCP this file to your desktop."
echo "Example: cget_token clusterID token /home/support/secLogs.tar.gz"
printf '\n'