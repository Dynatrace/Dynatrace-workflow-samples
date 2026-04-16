# Workflow Templates — In-Product Reference Collection

> **⚠️ These templates are NOT meant to be used from this repository.**
>
> All templates in this directory are **available directly inside the Dynatrace product** as built-in workflow templates. They are maintained here **solely as a reference knowledge base for AI agents** generating new workflows —providing proven patterns, action usage, expression syntax, and architectural examples.
>
> **To use a template:** Open the Dynatrace Workflows app → Create workflow → Browse templates.

---

## Purpose

When an AI coding assistant generates a new Dynatrace Workflow, these templates serve as high-quality reference material for:

- Correct action syntax and input schemas
- Proven trigger configurations (problem events, schedules, custom events)
- Jinja2 expression patterns (`event()`, `result()`, `execution()`)
- Multi-workflow orchestration patterns (see [AWS DevOps Agent](aws-devops-agent/))
- Dynatrace Intelligence (`davis-copilot`) prompting and result handling
- Integration patterns for external systems (ServiceNow, Jira, Slack, Teams, PagerDuty, Ansible, GitHub, AWS)
- Error handling, conditional execution, and `withItems` looping

## Validating Templates with dtctl

Although these are in-product templates, you can use `dtctl` to validate newly generated workflows against them or to dry-run deploy:

```bash
# Validate a single template against a live environment
dtctl apply -f in-product-templates/dynatrace-intelligence-agents/alert-reduction-agent.workflow-template.yaml --dry-run --plain

# Batch-validate all templates in a category
for f in in-product-templates/dynatrace-intelligence-agents/*.yaml; do
  echo "=== $(basename $f) ===" && dtctl apply -f "$f" --dry-run --plain 2>&1 | tail -1
done
```

See [AGENTS.md](../AGENTS.md#dtctl--dynatrace-cli-for-workflow-management) for the full `dtctl` reference.

## Categories

| Folder | Templates | Description |
|--------|-----------|-------------|
| [dynatrace-intelligence-agents/](dynatrace-intelligence-agents/) | 9 | AI-powered agents using Dynatrace Intelligence (`davis-copilot`) for analysis, recommendations, and automated reporting |
| [aws-devops-agent/](aws-devops-agent/) | 6 | Multi-workflow orchestration bridging Dynatrace problem detection with the AWS DevOps Agent for investigation and mitigation |
| [incident-management/](incident-management/) | 6 | ITSM integrations: ServiceNow, PagerDuty, ownership-based routing, and notification |
| [notifications-and-reporting/](notifications-and-reporting/) | 3 | Notifications to Microsoft Teams and email with aggregated data |
| [remediation/](remediation/) | 2 | Event-driven and job-based remediation with Red Hat Ansible |
| [devops-automation/](devops-automation/) | 4 | Kubernetes ops, configuration management, package sync, and team import |
| [security/](security/) | 1 | Threat intelligence and triage data templates |

**Total: 31 templates**

## Key Patterns for AI Agents

### Dynatrace Intelligence (davis-copilot) Pattern

9 templates demonstrate the `davis-copilot` action for AI-driven analysis. Common pattern:
1. **Collect data** — DQL queries fetching metrics, logs, events, or security findings
2. **Invoke AI** — `davis-copilot` action with a structured prompt referencing query results
3. **Act on output** — Send email/Slack report, create Jira ticket, or generate GitHub PR

### Multi-Workflow Orchestration Pattern

The AWS DevOps Agent demonstrates a 6-workflow event-driven pipeline:
1. Problem events → bizevent queue
2. Scheduled dispatcher polls queue
3. Eligibility check via topology walk → invoke external agent API
4. Event-triggered handlers process investigation and mitigation responses

### Problem-Triggered Integration Pattern

13 templates use problem event triggers → query context → notify or remediate via external system.

### Scheduled Reporting Pattern

5 templates use cron-based schedules for periodic data collection, AI analysis, and email/Slack delivery.
