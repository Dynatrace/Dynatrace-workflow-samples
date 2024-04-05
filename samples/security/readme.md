# Application Security Sample Workflows

Here, you can find some examples of how to operationalize security findings, such as vulnerabilities. 

## Getting Started with Security Findings Operationalization

For more information about how the security data is structured, refer to [Security data on Grail](https://docs.dynatrace.com/docs/platform-modules/application-security/security-data-on-grail) documentation.

### Approaches for Security Automation
You can trigger a workflow in 2 different ways:
1. Per change event - using the workflow trigger for every new vulnerability event reported on the granularity of the affected entity (for example, vulnerability A per process group B). This approach will trigger immediately, as soon as the triggering event will appear.
2. Periodical trigger - using the periodical query for events in the past time-period. This approach allows you to perform aggregations and a better deduplication of notifications.

## Sample Workflows
* `ms_teams_send_critical_vulnerabilities_per_affected_entity.yaml` - MS Teams notification for new critical vulnerabilities per affected entity (static channel assignment).
* `slack_send_critical_vulnerabilities_per_host.yaml` - Slack notification for new critical vulnerabilities aggregated per host (static channel assignment).
* `servicenow_create_ticket_per_host_static_assignment.yaml` - ServiceNow ticket creation for new critical vulnerabilities aggregated per host (static channel assignment).
* `jira_create_ticket_per_host_with_ownership.yaml` - Jira ticket creation for new critical vulnerabilities aggregated per host (ownership-based channel assignment).
* `ocsf_send_critical_vulnerabilities.yaml` - POST an HTTP request to a third-party tool for new critical vulnerabilities in the [Open Cyber Security Format (OCSF)](https://schema.ocsf.io/1.1.0/classes/vulnerability_finding?extensions=linux,win).
