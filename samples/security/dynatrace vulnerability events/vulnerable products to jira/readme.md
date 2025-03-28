# Jira Ticket creation Workflow(s)

This folder contains the templates for the AppSec ticket automation demoed on the 27th of May 2024 in
the [Automation Guild](https://community.dynatrace.com/t5/Automation-Guild/All-Guild-Meetings-recordings-in-this-single-spot/td-p/243437)

These workflows combine Security Events on Grail with Release Monitoring to deduplicate vulnerabilities per Product
and to get them synced to Jira.

## How to make operational

* As these workflows depend on each other make sure that you exchange the placeholder `<sub-workflow-id>` with the
  actual id of the deployed ticket_creation_sub-workflow. Also ensure to replace the `<jira-base-url>` in the
  sub-workflow with your actual jira url to have correct tracking links in Dynatrace


