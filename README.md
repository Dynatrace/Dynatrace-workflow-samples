# Dynatrace-workflow-samples

This repository collects sample workflows and javascripts snippets for Dynatrace AutomationEngine and the Workflows app. 

## Getting Started with Dynatrace AutomationEngine

To get started please have a look into [Dynatrace AutomationEngine](https://www.dynatrace.com/support/help/shortlink/automationengine) and [Workflows](https://www.dynatrace.com/support/help/shortlink/workflows) documentation.

## License
[Apache License v2.0](LICENSE).

## How to leverage workflow and code samples

### Workflow import

You can export and import a workflow via
- Downloading a template YAML from [Workflows App](https://docs.dynatrace.com/docs/shortlink/workflows-manage)
- [JSON via API](https://github.com/Dynatrace/Dynatrace-workflow-samples/tree/main/howtoimportexport) 
- [Configuration-as-Code (Monaco / Terraform)](https://docs.dynatrace.com/docs/shortlink/configuration-as-code)
  -- Be aware, that the files are not compatible, as Monaco JSONs contain escaping and uses another YAML format to fill placeholders.

### Code snippets

Within a workflow, click on "new task", select "Run Javascript" and copy/paste the snippet into the Javascript action.

## How to contribute 

### Export a workflow

Export your workflow as a **template** and make sure that you have no secrets, specific URLs, and alike in the resulting `.yaml` file.

Also make sure you have the proper versions of depending apps referenced within the file. Use generally available versions and no dev version of any app that you used in the environment.

### Create a pull request and upload your contribution 

Create a pull request and upload your contribution to the [samples/](samples/) directory (for instance, `samples/my-sample-name`). Please follow [our contribution guide](CONTRIBUTING.md).