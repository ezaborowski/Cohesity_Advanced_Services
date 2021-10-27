#!/bin/bash
# PATH="$PATH:/home/cohesity/software/crux/bin/allssh.sh"

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

echo -e "\nCalling FATAL_logs \n" 
/home/cohesity/software/crux/bin/allssh.sh 'ls -ltrGg ~/logs/*FATAL*|tail -4' > secLogs/CONFIG/$filename-CONFIG-FATALS_logs-`date +%s`.json

echo -e "\nCalling LDAP_errors \n" 
/home/cohesity/software/crux/bin/allssh.sh 'grep -i LDAP /home/cohesity/data/logs/bridge_exec.INFO' > secLogs/CONFIG/$filename-CONFIG-LDAP_errors-`date +%s`.json

echo -e "\nCalling IO_stats \n" 
/home/cohesity/software/crux/bin/allssh.sh 'iostat | grep -A 1 avg-cpu' > secLogs/CONFIG/$filename-CONFIG-IO_stats-`date +%s`.json

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

api_checks=(basicClusterInfo, activeDirectory, ldapProvider, domainControllers, antivirusGroups, icapConnectionStatus, infectedFiles, apps, alerts, roles, users, remoteClusters, vaults, viewboxes)
api_stats_checks=(storage, viewBoxes, vaults)
#public/ldapProvider/{id}/status

printf '\n'
printf '\n'
echo "Running API Data Collection Commands and saving output to API-Logs folder..."
  sleep 5
printf '\n'

#get token
token=`curl -X POST -k "$url/irisservices/api/v1/public/accessTokens" -H "accept: application/json" -H "content-type: application/json" -d "{ \"domain\": \"LOCAL\", \"password\": \"$password\", \"username\": \"$username\"}" | cut -d : -f 2 | cut -d, -f1 `

              echo "The Access Token is" $token

#Loop through each api call and write the output of each call to secLogs/API-Logs folder. Piping to json.tool to beautify.

        echo -e "\nCalling certificates/webServer \n"

        curl -X GET -k "$url/irisservices/api/v1/public/certificates/webServer" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-certificates-`date +%s`.json

for x in $(echo ${api_checks[@]} | sed "s/,/ /g")
do
        echo -e "\nCalling $x \n"

        curl -X GET -k "$url/irisservices/api/v1/public/$x" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-$x-`date +%s`.json
 done

        echo -e "\nCalling stats/vaults/providers \n"

        curl -X GET -k "$url/irisservices/api/v1/public/stats/vaults/providers" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-vaults_providers-stats-`date +%s`.json

for x in $(echo ${api_stats_checks[@]} | sed "s/,/ /g")
do
        echo -e "\nCalling $x \n"

        curl -X GET -k "$url/irisservices/api/v1/public/stats/$x" -H "accept: application/json" -H "Authorization: Bearer $token" | python -m json.tool > secLogs/API/$filename-API-$x-stats-`date +%s`.json
 done


#---------------------------------------------------------------------------------------------------------------#
#Run IRIS_CLI data gathering commands.

# printf '\n'
# printf '\n'
# echo "-------------------"
# echo "IRIS_CLI DATA COLLECTION"
# echo "-------------------"
# echo " "

# printf '\n'
# printf '\n'
# echo "Making secLogs/IRIS subdirectory to save all logs to..."
#   mkdir secLogs/IRIS 2> /dev/null
#     sleep 5

#iris_checks=("alert ls" "syslog-server list" "user list" "role list")
#"ad list-centrify-zones domain-name=$domain"

# printf '\n'
# printf '\n'
# echo "Running IRIS_CLI Data Collection Commands and saving output to IRIS_CLI-Logs folder..."
#   sleep 5
# printf '\n'

#Loop through each iris_cli call and write the output of each call to secLogs/IRIS_CLI-Logs folder
# for y in ${iris_checks[@]}
# do
#          echo -e "\nCalling $y \n"

#          iris_cli -username $username -password "$password" "$y" > secLogs/IRIS/$filename-IRIS-$y-`date +%s`.json
#  done

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

         echo -e "\nCalling $z \n"

         sudo hc_cli run -v -u $username -p $password --$z > secLogs/HC/$filename-HC-$z-`date +%s`.json

         echo -e "\nCalling $z \n"

         hc_cli run -v -u $username -p $password --$z >> secLogs/HC/$filename-HC-$z-`date +%s`.json
done

 #---------------------------------------------------------------------------------------------------------------#