# List View Contents using PowerShell

Warning: this code is provided on a best effort basis and is not in any way officially supported or sanctioned by Cohesity. The code is intentionally kept simple to retain value as example code. The code in this repository is provided as-is and the author accepts no liability for damages resulting from its use.

This powershell script Exports all Entra ID objects, as well as Imports Entra ID Users and associates newly created User to appropriate User Groups. This script also purges the all exported Entra ID data older than 30 days by default (but a different number of days can be defined at runtime).

## Components

* ADexport_UI.ps1: the main powershell script
* wrapper.bat: the wrapper to call from Windows Task Scheduler

Place both files in a folder together, then run the script like so:

(if only Exporting Entra ID data with custom days to expire old Exports)
```powershell
 ./ADexport_UI.ps1 -days 15
```
(if only Importing Entra ID data)
```powershell
./ADexport_UI.ps1 -restore $True -export $False
```

## Authentication Parameters (can be defined at runtime or directly in script Parameters section)

* -clientId: (mandatory) comma-delimited list of Entra ID Client ID(s) associated with newly Registered EntraExport App
* -tenantId: (mandatory) comma-delimited list of Entra ID Tenant ID(s) associated with newly Registered EntraExport App
* -certThumbprint: (mandatory) comma-delimited list of Certificate Thumbprint(s) created for access to newly Registered EntraExport App (used for Backup)
* -clientSecret: (mandatory for restoration) comma-delimited list of Client Secret Value(s) created for access to newly Registered EntraExport App (used for Recovery)

## Other Parameters (can be defined at runtime or directly in script Parameters section)

* -cohView: (mandatory) SMB address to access the Cohesity View
* -export: (optional) switch for utilizing script to Export Azure AD contents (default is True)
* -restore: (optional) switch for utilizing script to Restore to Azure AD (default is False)
* -days: (optional) amount of Days to keep backed up data on Cohesity View (default is 30 days)


## Necessary Entra ID Preparation

* Login to Microsoft Azure Portal
* Open App Registrations and Register a new App for the 'EntraExport' script
* Choose the 'Certificates' tab and click 'Upload certificate' (you will need to prepare a self-signed certificate to upload, and also install locally on the server you are running the script from) 
* Select 'API permissions' from the left-hand pane and click 'Add a permission'
* Select the 'APIs my organization uses' tab, then choose 'Microsoft Graph'
* Select 'Application permissions' and checkmark the following permissions:
    * Directory.Read.All
    * Policy.Read.All
    * IdentityProvider.Read.All
    * Organization.Read.All
    * User.Read.All
    * EntitlementManagement.Read.All
    * UserAuthenticationMethod.Read.All
    * IdentityUserFlow.Read.All
    * APIConnectors.Read.All
    * AccessReview.Read.All
    * AccessReview.ReadWrite.All
    * AccessReview.ReadWrite.Membership
    * Agreement.Read.All
    * Policy.Read.PermissionGrant
    * PrivilegedAccess.Read.AzureResources
    * PrivilegedAccess.Read.AzureAD
    * Application.Read.All
    * AuthenticationContext.Read.All
    * UserAuthenticationMethod.Read.All
    * OrgSettings-AppsAndServices.Read.All
    * IdentityProvider.Read.All
    * AgreementAcceptance.Read.All
    * PrivilegedAccess.Read.AzureADGroup
    * IdentityUserFlow.Read.All
    * IdentityRiskyUser.Read.All
    * User.ReadWrite.All
    * User.Export.All
    * DeviceManagementConfiguration.Read.All
    * RoleManagementPolicy.Read.AzureADGroup
    * Group.Read.All
    * GroupMember.Read.All

* Click 'Add permissions'
* Click 'Grant admin consent for Default Directory'
* Input Mandatory Values below in Parameters section
