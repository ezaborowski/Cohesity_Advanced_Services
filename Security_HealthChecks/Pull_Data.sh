#!/bin/bash

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski                                                                                   #"
echo "#Last Updated 10/04/2021                                                                                        #"
echo "#  -updated section: ALL                                                                                        #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

#---------------------------------------------------------------------------------------------------------------#
#TESTING

# printf '\n'
# echo "Please enter the location you would like to save your logs: "
# echo "example: /Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Endo_Pharm"
# read -e filepath 
# printf '\n'

# declare -a clusterAccess

# while IFS= read clusterID clusterToken
# do
#     clusterAccess["$clusterID"]="$clusterToken"
# done < 

# while true
# do  
#     printf '\n'
#     echo "Please enter Cohesity Cluster ID: "
#         read -e clusterID 
    
#     printf '\n'
#     echo "Please enter corresponding Cohesity Cluster Token: "
#         read -e clusterToken
    
#     printf '\n'
#     echo "Type DONE below or click ENTER to input another Cluster: "
#         read -e input
        
#         if [ $input == "DONE" ]
#             then break
#         fi

# done 

#---------------------------------------------------------------------------------------------------------------#


#---------------------------------------------------------------------------------------------------------------#
#From .bashrc

# Created by Edmond Donegan edonegan@cohesity.com

# If not running interactively, don't do anything
[[ "$-" != *i* ]] && return

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# config option to remove auth errors in chrome.
# chrome://flags/#allow-insecure-localhost
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

support_tunnel="rt.cohesity.com"                                                     # Used for tunneling to the customer's site currently rt.cohesity.com
support_tunnel_user="cohesity"                                                       # Used for logging into the support tunnel currently rt.cohesity.com
support_tunnel_client_file="/home/cohesity/erinzaborowski/client_to_server_functions.sh"   # Assists in keeping standard functions and auto updates
support_tunnel_client_file_local=".client_to_server_functions.sh"                    # Where to save the local copy of the client file
localBackupFolder="bash_backups"                                                     # Name of the folder for local backups, saved in home directory
profileOriginal="/home/cohesity/erinzaborowski/.bashrc"                              # Location of original bash profile on the support server
#profileWindows="/home/cohesity/edonegan/standard_update.bashrc"                      # Location of latest bash profile on the support server for this OS
#profileMAC="/home/cohesity/edonegan/standard_update.bashrc"                          # Location of latest bash profile on the support server for this OS
#profileLinux="/home/cohesity/edonegan/standard_update.bashrc"                        # Location of latest bash profile on the support server for this OS
#profileLinuxWSL="/home/cohesity/edonegan/standard_update.bashrc"                     # Location of latest bash profile on the support server for this OS
#profileUnknownOs="/home/cohesity/edonegan/standard_update.bashrc"                    # Location of latest bash profile on the support server for this OS

ssh_options_trimmed="-o PreferredAuthentications=publickey,password \
                     -o StrictHostKeyChecking=no \
                     -o UserKnownHostsFile=/dev/null \
                     -o ServerAliveInterval=60 \
                     -o LogLevel=ERROR"


alias rtsh='ssh cohesity@rt.cohesity.com'
alias tf='ssh cohesity@rt.cohesity.com tf'

# Get cluster information, sets locals
function Tinfo () {
if [ $# -ne 1 ]; then
  echo "${FUNCNAME[0]} [clusterid]"
else
  cinfo=`ssh cohesity@rt.cohesity.com tf "^${1}:"| tail -1  | awk 'BEGIN{FS=":"}{print $3","$4","$5}'`
   if [ "$cinfo" == "" ]; then
      echo " clusterid $1 not found"
   else
     cli_port=`echo $cinfo | awk 'BEGIN{FS=","}{print $1}'`
     cname=`echo $cinfo | awk 'BEGIN{FS=","}{print $2}'`
     gui_port=`echo $cinfo | awk 'BEGIN{FS=","}{print $3}'`
    fi
fi
}

# Connect to cluster shell using Tinfo
function tfs () {
if [ $# -ne 1 ]; then
  echo "${FUNCNAME[0]} [clusterid]"
else
  Tinfo $1
  if [ "$cinfo" == "" ]; then
    echo " clusterid $1 not found"
  else
    ssh -tt cohesity@rt.cohesity.com cssh $cli_port
  fi
fi
}

# Connect to cluster shell using Tinfo and prompt for custom password
function tfsp () {
if [ $# -ne 1 ]; then
  echo "${FUNCNAME[0]} [clusterid]"
else
  Tinfo $1
  if [ "$cinfo" == "" ]; then
    echo " clusterid $1 not found"
  else
    ssh -tt cohesity@rt.cohesity.com ssh -p $cli_port localhost
  fi
fi
}

# Connect to cluster GUI in local window
function tfg () {
if [ $# -ne 1 ]; then
  echo "${FUNCNAME[0]} [clusterid]"
else
  Tinfo $1
  if [ "$cinfo" == "" ]; then
    echo " clusterid $1 not found"
  else
    if [ -z "$(ps ax | grep '[s]sh -fN' | grep $gui_port)" ]; then
      echo "connecting $gui_port to  $gui_port"
      ssh -fN -L $gui_port:rt.cohesity.com:$gui_port cohesity@rt.cohesity.com $1 gui $cname
    else
      echo " # ---- UI TUNNEL to $cname IN USE -----------------# "
    fi
    open -g https://localhost:$gui_port
  fi
fi
}

# Connect to cluster GUI in local window and cluster CLI
function tfc () {
if [ $# -ne 1 ]; then
  echo "${FUNCNAME[0]} [clusterid]"
else
  Tinfo $1
  if [ "$cinfo" == "" ]; then
    echo " clusterid $1 not found"
  else
    if [ -z "$(ps ax | grep '[s]sh -fN' | grep $gui_port)" ]; then
      echo "connecting $gui_port to  $gui_port"
      echo ssh -fN -L $gui_port:rt.cohesity.com:$gui_port cohesity@rt.cohesity.com $1 gui $cname
      echo open -g https://localhost:$gui_port
    else
      " # ---- UI TUNNEL to $cname IN USE -----------------# "

	fi
    open -g https://localhost:$gui_port
  fi

#  open -g https://localhost:$gui_port
#    fi
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ] &&
       [ -n "$(ps ax | grep '[s]sh -p' | grep $cli_port)" ]; then
       echo " # ---- CLI TUNNEL to $cname IN USE ----------------# "
    else
      if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
        ssh -p $cli_port -tt  cohesity@localhost
      else
        ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com $1 cli $cname
        ssh -p $cli_port -tt  cohesity@localhost
      fi
#    fi
  fi
fi
}

function process_token() {
  clusterid=$1
  base64_encoded_token=$2
  raw_token=`echo $base64_encoded_token | base64 -d`
  prefix=${raw_token:0:3}
  rm -f ~/c.$clusterid
  echo '-----BEGIN EC PRIVATE KEY-----' >> ~/c.$clusterid
  echo ${raw_token:3} | tr ' ' '\n' >> ~/c.$clusterid
  printf %s '-----END EC PRIVATE KEY-----' >> ~/c.$clusterid
  chmod 600 ~/c.$clusterid
}

function tfc_token () {
if [ $# -ne 2 ]; then
  echo "${FUNCNAME[0]} [clusterid] [token]"
else
  Tinfo $1
  process_token $1 "${@:2:2}"
  if [ "$cinfo" != "" ]; then
    if [ -z "$(ps ax | grep '[s]sh -fN' | grep $gui_port)" ]; then
      echo "*** Connecting GUI port $gui_port to $gui_port ***"
      ssh -fN -L $gui_port:rt.cohesity.com:$gui_port cohesity@rt.cohesity.com
      open -g https://localhost:$gui_port
    else
      echo " # ---- GUI TUNNEL to $cname GUI port $gui_port IN USE ---- # "
      open -g https://localhost:$gui_port
    fi
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ] &&
      [ -n "$(ps ax | grep '[s]sh -p' | grep $cli_port)" ]; then
      echo " # ---- CLI TUNNEL to $cname CLI port $cli_port IN USE ---- # "
    else
      if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
        ssh -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p $cli_port support@localhost
      else
        ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com $1 cli $cname
        ssh -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p $cli_port support@localhost
      fi
    fi
  fi
fi
}

function cssh_token () {
if [ $# -ne 2 ]; then
  echo "${FUNCNAME[0]} [clusterid] [token]"
else
  Tinfo $1
  process_token $1 "${@:2:2}"
  if [ "$cinfo" != "" ]; then
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ] &&
      [ -n "$(ps ax | grep '[s]sh -p' | grep $cli_port)" ]; then
      echo " # ---- CLI TUNNEL to $cname CLI port $cli_port IN USE ---- # "
    else
      if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
        ssh -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p $cli_port support@localhost
      else
        ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com $1 cli $cname
        ssh -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p $cli_port support@localhost
      fi
    fi
  fi
fi
}

function cget_token () {
if [ $# -ne 3 ]; then
  echo "${FUNCNAME[0]} [clusterid] [token] [file]"
else
  Tinfo $1
  process_token $1 "${@:2:2}"
  if [ "$cinfo" != "" ]; then
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
      echo " # ---- Downloading file $3 from /home/support/ to current location via Port $cli_port for $cname ---- # "
      scp -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p -P $cli_port support@localhost:$3 .
      echo " # ---- If successful, file $3 is downloaded from /home/support/ to current location via Port $cli_port for $cname ---- # "
    else
      echo " # ---- Setting up SSH and downloading file $3 from /home/support/ to current location via Port $cli_port for $cname ---- # "
      ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com $1 cli $cname
      scp -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p -P $cli_port support@localhost:$3 .
      echo " # ---- If successful, file $3 is downloaded from /home/support/ to current location via Port $cli_port for $cname ---- # "
    fi
  fi
fi
}

function cput_token () {
if [ $# -ne 3 ]; then
  echo "${FUNCNAME[0]} [clusterid] [token] [file]"
else
  Tinfo $1
  process_token $1 "${@:2:2}"
  if [ "$cinfo" != "" ]; then
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
      echo " # ---- Uploading file $3 to /home/support/ via Port $cli_port for $cname ---- # "
      scp -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p -P $cli_port $3 support@localhost:~/.
      echo " # ---- If successful, file $3 is uploaded to /home/support/ via Port $cli_port for $cname ---- # "
    else
      echo " # ---- Setting up SSH and uploading file $3 to /home/support/ via Port $cli_port for $cname ---- # "
      ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com $1 cli $cname
      scp -o UserKnownHostsFile=/dev/null -o PreferredAuthentications=publickey -i ~/c.$1 -p -P $cli_port $3 support@localhost:~/.
      echo " # ---- If successful, file $3 is uploaded to /home/support/ via Port $cli_port for $cname ---- # "
    fi
  fi
fi
}
# Copies file from cluster to local
function Copull () {
if [ $# -ne 2 ]; then
  echo "${FUNCNAME[0]} [clusterid] [file] "
else
    Tinfo $1
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $cli_port)" ]; then
        scp  -P $cli_port cohesity@localhost:$2 .
    else
        echo " set up sssh and copy "
        ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com ;
        scp  -P $cli_port cohesity@localhost:$2 .
    fi
fi
}

# Push file to cluster from local
function Copush () {
if [ $# -ne 2 ]; then
  echo "${FUNCNAME[0]} [clusterid] [file]"
else
    Tinfo $1
    if [ -n "$(ps ax | grep '[s]sh -fN' | grep $1)" ]; then
        scp  -P $cli_port $2 cohesity@localhost:/tmp
    else
        ssh -fN -L $cli_port:rt.cohesity.com:$cli_port cohesity@rt.cohesity.com ;
        scp  -P $cli_port $2 cohesity@localhost:/tmp
 fi
fi
}

# ct lists open ssh tunnels
function ct () { ps ax | grep '[s]sh -fN'| awk '{ $9=""; print }'; }

#ctk kills all open ssh tunnels
function ctk () { pkill -f 'ssh -fN'; }

#---------------------------------------------------------------------------------------------------------------#

declare -a clusterAccess

clusterAccess=( [2825687123695835]=JDEkTUhjQ0FRRUVJRWp4RzJadG5vbzJxdEY3VUZyREszaDlaV3phOE8vcnIvVDlSSDBLSkhIR29Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUUzMXB6ZGl5TlgrSG5WSkdXRXEza1BrRFc0Z2h3Vng0U2VCM0UzUjBjbU1DNUtOMURndEg3Cm5hTnJKN2VaU3cvYzhveDZMeHNqOWpGVTJyZS9uQzNUOWc9PQ== [6596972967231183]=JDEkTUhjQ0FRRUVJR0tUUG91WFJxc2JhTEZ6SkF4ME1sT041NkZqNlNCeFRKd0tlNGNMSzJrTG9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVHR3BMZnRuN283L2xqMGtDdWt1T3hZbU1KOENqY3VHdEg2aDJxTkRadzNkU1RrT3FabDZDClFjdTlybXRrZWpzTitkRXpFNytDUnc3cHc4WjFMYVRPMWc9PQ== [6546675880294234]=JDEkTUhjQ0FRRUVJRWdRV1JBUFNMUkhZOTZla0NXNnNhdXBLV2RUdVBNYWJHbWc1b1R5RlI3RW9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVCOWFmcklqRlY4MnlZdFNmV2R1eG9SSGdUSGFzYnU1ZElCZXBDYy85OXdaclB6b2Rrd29EClE3ZmNFa0ZmV3REaEhKTG5oOGlNS2ZXd0ZyQy9wclBPdlE9PQ== [196266034736418]=JDEkTUhjQ0FRRUVJS3FCZVRqQlYwSEpVZmo4bERESjU2MEtvOEdyZDN1cnhWNENsc2xNZ2tua29Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVqWDJ6ZHlOWlBkcTdNa1NwbWhNa3lPbkx6K0c1OUF4WUx1NWtiNFFHU0FFMmZmMGxnR2JjCnNnemg2Yi9JdDh1T0oxdENaTk1mN0UrM3J1QkRTMEx5R1E9PQ== [2598148347132640]=JDEkTUhjQ0FRRUVJTXhqNTJrd3I3SFhBNDlWZnZvbzVVSmZqK0JhOE1OSllhZ01ramptNHR2MW9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUUyMmxMU0hleHQvTU84VzJza293QmhkaUVEWStieTVORDhzYzc2K1lxdlBTbVU4d0xZa3JHCkV0N0RvY2NJdnNjbjUrUUg1bmdKWVhuZGJyVy9CNVRiUEE9PQ== [6550182419101614]=JDEkTUhjQ0FRRUVJRFpObFlxOURrQUhyQUhzR2R1QlJoRnZFL3BGQWZGcGpUb1J1UVYrUTJkNW9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUUyWXhRSGhCOHNCaDl2T0NMd3o2SVFoWTJDc05FU1cxTk5xVk84bzhUOEhtR3NCOTJrOVFUCjdER25tV1NmN1k0aU5nd0d5bDQ5eEpJM0d3MXVsTW5zU3c9PQ== [7898537120366324]=JDEkTUhjQ0FRRUVJR0p0VUxwSHZCclNmN3FxbnJ2aG1yZ2h5eTRtZHRBVFI5Tzc2ZFZLaGRnYm9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVsZUdFSEdVMTlMRmI1SGJOYkYwSjU2dER6U0pHY3BSWTlNR0R4TU1mbFhCVzQydGM4akZtCnpUTmV3ckdGbTZuc0JKUjg5eHBUMEJOdTU5TWFNTk1Zb2c9PQ== [4825452905365191]=JDEkTUhjQ0FRRUVJTkx3eUpMVEtEZkp5YUVYK3hSbDJqYkEwc0UyaFh6RFJmV3pqN1FMckNyUG9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVHL1Z6Wks4cEdieWJuL200V0hEVTJ6TWFUSHZKdTZ6N1VNMzZoSXV1RXJqQWc5YXpkV1F2CmY4b042eVl6OFhEcDFta1JjZXhlVk5PRFNZMVZyRHRCWXc9PQ== [5807357701073471]=JDEkTUhjQ0FRRUVJRTVRZURDWGlUbHU4V21SeDFiejdFSU9iR2VUMVZPM01WRSsyQXhqV3NLb29Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVPamVSb2t3UGNncC9iaTN5emN2KzkraGFEUGh2NkdlK0w2bVVLRU5HcUg2UElBazZyWnZmCkx1KzFjYUUyTGtvWWxMajBRTUZHbU9vTE14Q0M2ckZDNHc9PQ== [318299134699867]=JDEkTUhjQ0FRRUVJS3RIeG5pSVpVZ2syc0FzT0Nad0dtL3JTRVorMXFHU0FDMW9qRms4Vm4xaW9Bb0dDQ3FHU000OQpBd0VIb1VRRFFnQUVHbmUvYzNuVGdLN2xxOFRUWjJjV0M5Z096ZnNLMGQyMnlWaHNaSXZzVWN3ZmdZbHdLSU5WCkhrZmU2SjRadEk2OCtQN2hQQ25BSDdQK0pwempoWE9tQlE9PQ==)

project=Endo_Pharm

cd Documents/Source_Files/Professional_Services/PROJECTS/$project/HealthCheck

for y in "${!clusterAccess[@]}"
do
    mkdir $y 2> /dev/null
done

for z in "${!clusterAccess[@]}"
do
    cd $z
    yes | cget_token $z ${clusterAccess[$z]} /tmp/cluster_config 
    yes | cget_token $z ${clusterAccess[$z]} /home/support/secLogs/CONFIG-Logs/* 
    yes | cget_token $z ${clusterAccess[$z]} /home/support/secLogs/API-Logs/*
    yes | cget_token $z ${clusterAccess[$z]} /home/support/secLogs/IRIS_CLI-Logs/*
    yes | cget_token $z ${clusterAccess[$z]} /home/support/secLogs/HC_CLI-Logs/*
    cd .. 
done