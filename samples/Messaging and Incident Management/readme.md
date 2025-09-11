
# Messaging and Incident Management Sample Workflows

Here, you can find some examples of how to create tickets in Jira, calculate severity for SerivceNow incident creation, and send emails.

## Getting Started 

For more information refer to the documentation at
* Email: https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/email
* Jira: https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/jira
* ServiceNow: https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/service-now

## Sample Workflows 
* `ServiceNow_calculate_severity_based_on_impact.yaml` - ServiceNow incident creation workflows, which shows an example on how to calculate severity
* `Jira and Slack w targeted messaging.json` - Create tickets in Jira, leverage ownership information to target the correct users 
* `wftpl_send_email.yaml` - Send Emails with Dynatrace workflows
* 'wftpl_sample_servicenow_incident_man.yaml' - Create or updates incidents in ServiceNow


## Create or udpate incidents in ServiceNow 
Template: wftpl_sample_servicenow_incident_man.yaml

This sample workflow reacts to a DAVIS problem once the root cause has been identified, enriches the description with information like logs, searches for the CI in ServiceNow CMDB, calculates impact and urgency and creates or updates a ServiceNow Incident: 

- Trigger: The additional custom filter query triggers the workflow once the root cause has been identified and omits events if  the system is in maintenance. Adjust the tags according to your needs.
- get_cmdb_ci: Searches for entries in the CMDB base class referencing correlation_id. This requires the ServiceNow Service Graph Connector to map entties between Dynatrace and ServiceNow.
- get_support_group: identifies the owner of the entity based on the root-cause-entity. See https://docs.dynatrace.com/docs/deliver/ownership for more information
- get_problem_impact and estimate_problem_urgency: examples on calculating impact and urgency. The JavaScript actions allows you to customize the calculation according to your needs
- search, comment, or create incidents: incidents are either created or updated to prevent duplicate tickets. 


<img width="3728" height="1892" alt="image" src="https://github.com/user-attachments/assets/4b355a3b-bd75-49ae-9498-6a1d8d6e9a88" />


