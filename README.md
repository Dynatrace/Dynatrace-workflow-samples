# Dynatrace-workflow-samples

This repository collects sample workflows and javascripts snippets for Dynatrace Automation Engine. 

## Getting Started with Dynatrace Automation Engine

To get started with Dynatrace Workflow Automation Engine see [the documentation](https://www.dynatrace.com/support/help/platform/automationengine).

##License
[Apache License v2.0](https://github.com/dynatrace-oss/xxxx/blob/main/LICENSE).

## How to leverage workflow and code samples
### Workflow import

You can import a workflow via API, via workflow UI (cooming soon) or via Monaco (cooming soon). 
1.) API Import 
Here you can find the OpenAPI 3.0 specification: https://<yourtenant>.apps.dynatrace.com/platform/swagger-ui/index.html?urls.primaryName=Automation#/workflows

<to be validated and improved>
Use <POST> /workflows to import the workflow
You can find an example http call in /howtoimportorexport. 

Alternativately you'll find a workflow example which leverages the API to import workflows. 
Import this workflow and run the workflow for further imports.

2.) Workflow UI Import
cooming soon

3.) Monaco 
cooming soon

### Code snippets
Within a workflow, click on "new task", select "Run Javascript" and copy/paste the snippet into the Javascript ation.

## How to contribute 

### Export a workflow

You can export a workflow via API, via workflow UI (cooming soon) or via Monaco (cooming soon). 
1.) API Import 
Here you can find the OpenAPI 3.0 specification: https://<yourtenant>.apps.dynatrace.com/platform/swagger-ui/index.html?urls.primaryName=Automation#/workflows

<to be validated and improved>
Use <GET> /workflows respectively <GET> /workflows/{id} to export one or all workflows
You can find an example http call in /howtoimportorexport. 

Alternativately you'll find a workflow example which leverages the API to export workflows. 
Import this workflow and run the workflow for further exports.

2.) Workflow UI Import
cooming soon

3.) Monaco 
cooming soon

### Create a pull request and upload your contribution 
Create a pull request and upload your contribution to /samples/<category>. 






