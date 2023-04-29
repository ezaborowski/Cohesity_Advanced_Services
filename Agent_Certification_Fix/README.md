# Agent Certification Fix using Bash

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This is a simple bash script which will download and disseminate the new Cohesity Agents with updated Certificates across the Cohesity Cluster. This will allow using the Cohesity UI to update all Cohesity Source Agents.

IMPORTANT: The /home/cohesity/bin/installers/agent_installer_files.json file must be manually updated to ensure updating Cohesity Agents from the UI is possible. Instructions will be printed out to the console, as well as to the manualUpdatesNEEDED log which will be located in the same directory the script is installed to.

## Components

* agent_cert_fix.sh: the main bash script 

## Download the Script

Please SSH into the Cohesity CLI using the 'support' User, and elevate to the 'cohesity' User by running the following:

```bash
sudo su cohesity
```

To Download the agent_cert_fix.sh script, please run the following commands: 

```bash
# download commands
curl -O https://raw.githubusercontent.com/ezaborowski/Cohesity_Advanced_Services/main/Agent_Certification_Fix/agent_cert_fix.sh
chmod +x agent_cert_fix.sh

# end download commands
```

## How to Run Script

Ensure the script is being running from a Node on the Cohesity Cluster:

```bash
./agent_cert_fix.sh
```