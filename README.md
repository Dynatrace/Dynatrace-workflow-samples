# Dynatrace-workflow-samples

This repository collects sample workflows and javascripts snippets for Dynatrace AutomationEngine and the Workflows app. 

## Getting Started with Dynatrace AutomationEngine

To get started please have a look into [Dynatrace AutomationEngine](https://www.dynatrace.com/support/help/shortlink/automationengine) and [Workflows](https://www.dynatrace.com/support/help/shortlink/workflows) documentation.

## License
[Apache License v2.0](LICENSE).

## AI Assistant Instructions

If you're using GitHub Copilot, Cursor, Claude Code, Kiro, or other AI coding assistants to generate Dynatrace Workflows, comprehensive instructions are available in [AGENTS.md](AGENTS.md). This guide covers:
- Workflow syntax and structure for all three formats (YAML templates, API JSON, Terraform)
- Common workflow actions and patterns
- Template expressions (Jinja2)
- **dtctl** — Dynatrace CLI for workflow validation, deployment, and execution
- Pull request review guidelines
- Best practices and troubleshooting
- Complete examples

## Validating Workflows with dtctl

[`dtctl`](https://github.com/dynatrace-oss/dtctl) is the official kubectl-style Dynatrace CLI. Use it to validate and deploy workflows:

```bash
# Install
brew install dynatrace-oss/tap/dtctl

# Authenticate
dtctl auth login --context my-env --environment "https://<env-id>.apps.dynatrace.com"

# Extract the flat/API workflow from a template export
yq '.workflow' my-workflow-template.yaml > my-workflow.yaml

# Validate the extracted workflow (dry-run — no deployment)
dtctl apply -f my-workflow.yaml --dry-run --plain

# Deploy the extracted workflow
dtctl apply -f my-workflow.yaml --plain
```

See [the dtctl reference](docs/dtctl-cli.md) for the full dtctl reference.

## Repository Structure

### [`in-product-templates/`](in-product-templates/) — In-Product Template Reference

> **⚠️ These templates are NOT meant to be used from this repository.** They are available directly inside the Dynatrace product as built-in workflow templates. They are maintained here **solely as a reference knowledge base for AI agents** generating new workflows.

31 categorized in-product workflow templates covering:

| Category | Templates | Highlights |
|----------|-----------|------------|
| [Dynatrace Intelligence Agents](in-product-templates/dynatrace-intelligence-agents/) | 9 | AI-powered automation using `davis-copilot` |
| [AWS DevOps Agent](in-product-templates/aws-devops-agent/) | 6 | Multi-workflow orchestration pipeline |
| [Incident Management](in-product-templates/incident-management/) | 6 | ServiceNow, PagerDuty, ownership routing |
| [Notifications & Reporting](in-product-templates/notifications-and-reporting/) | 3 | Microsoft Teams, email summaries |
| [Remediation](in-product-templates/remediation/) | 2 | Red Hat Ansible (EDA + job templates) |
| [DevOps Automation](in-product-templates/devops-automation/) | 4 | K8s ops, GitOps, config management |
| [Security](in-product-templates/security/) | 1 | Threat intelligence data templates |

### [`samples/`](samples/) — Community Workflow Samples

Community-contributed workflow samples and code snippets for direct use.

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