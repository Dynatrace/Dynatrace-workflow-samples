# Ownership Team Imports Templates

Within this directory, you'll find templates designed for importing Ownership teams through Workflows. Our data sources for this process include Microsoft Entra ID and a custom file hosted on GitHub.

For a comprehensive guide on how to utilize workflows for importing new teams, please refer to the product documentation. This documentation also contains detailed information about the specific workflow action, "import_teams."

This folder provides templates for importing Ownership teams via Workflows.
As data sources, we will use Microsoft Entra ID and a custom file hosted in GitHub. 

Please check the [product documentation](https://docs.dynatrace.com/docs/manage/ownership/ownership-teams#import-teams), which describes how workflows allow to import of new teams. Moreover, the documentation also provides details for the utilized [workflow action `import_teams`](https://docs.dynatrace.com/docs/manage/ownership/ownership-app#import-teams).

## Microsoft Entra ID
This demo provides a workflow that queries groups from Microsoft Entra ID using the [Azure for Workflows app](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/microsoft-entra-id), which are then imported as teams in Dynatrace.
The created workflow gets triggered using a fixed schedule with a 720-minute interval.
To use this template, please upload the workflow template file `import_teams_from_entra_id.yaml` in the Workflows app.


## Teams from a custom source
This template provides a workflow that first fetches teams from a file hosted on GitHub containing team information in a custom format.
A mapping logic then transfers this team information into the structured format specified in the ownership configuration [JSON schema](https://docs.dynatrace.com/docs/dynatrace-api/environment-api/settings/schemas/get-schema) (`builtin:ownership.config`) that Dynatrace provides.
The second workflow action `import_teams` then imports the teams in Dynatrace.
To use this template, please upload the workflow template file `import_teams_from_custom_source.yaml` in the Workflows app.

Please note, that before executing this workflow, you need to add `raw.githubusercontent.com` to your [allowed outbound connections](https://developer.dynatrace.com/develop/functions/allow-outbound-connections/).