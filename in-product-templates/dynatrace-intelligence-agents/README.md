# Dynatrace Intelligence Agents

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 9 templates demonstrate AI-powered automation using the `dynatrace.davis.workflow.actions:davis-copilot` action (Dynatrace Intelligence). Each workflow collects domain-specific data via DQL, passes it to the AI for analysis, and acts on the structured output.

## Templates

| Template | Trigger | What It Does |
|----------|---------|--------------|
| **Alert Reduction Agent** | Schedule (weekly) | Analyzes alert statistics, identifies spammy configurations, emails executive summary |
| **Database Operations Agent** | Problem (SERVICE_SLOWDOWN) | Queries slow DB spans, checks monitoring coverage, provides AI root-cause analysis and recommendations |
| **Infrastructure Optimization Agent** | On-Demand | Collects K8s CPU/memory, host disk/network metrics; generates AI cost-optimization report via email |
| **Kubernetes Operations Agent** | On-Demand | Detects K8s workload misconfigurations; AI generates YAML fixes; creates Jira tickets |
| **Kubernetes Troubleshooting Agent** | Event (K8s anomaly) | Collects K8s metrics on anomaly; AI generates recommendations; optionally creates GitHub PR with fixes |
| **Mobile Crash Remediation Agent** | Problem (mobile crash) | Fetches crash data; AI generates impact summary, title, and fix code snippet; creates notebook |
| **Security Association Agent** | Problem (Error/Slowdown/Availability) | Correlates problems with security findings; AI calculates association score (0–100%); notifies via email/Slack |
| **Security Insights Report Agent** | Schedule (weekly) | Queries vulnerability, detection, and compliance findings; AI generates executive security summary |
| **Vulnerability Verification Agent** | Event (critical dependency vuln) | AI analyzes critical vulnerability; generates YAML fix recommendations; creates Jira ticket |

## Common Pattern

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│ Trigger      │────▶│ DQL Queries   │────▶│ davis-copilot  │────▶│ Action       │
│ (problem/    │     │ (collect      │     │ (analyze &     │     │ (email/Jira/ │
│  schedule/   │     │  context)     │     │  recommend)    │     │  Slack/PR)   │
│  event)      │     └──────────────┘     └────────────────┘     └──────────────┘
└─────────────┘
```

## Integrations Used

- **Dynatrace Intelligence** (`davis-copilot`) — all 9 templates
- **Email** — Alert Reduction, Infrastructure Optimization, Security Association, Security Insights Report
- **Jira** — Kubernetes Operations, Vulnerability Verification
- **Slack** — Security Association
- **GitHub** — Kubernetes Troubleshooting (PR creation)

## Key Learnings for AI Agents

1. **Prompt structure**: All `davis-copilot` prompts include collected DQL data as context and request structured analysis or recommendations
2. **Multi-step AI**: Mobile Crash Remediation uses `davis-copilot` twice — once for title/summary, once for fix code
3. **Conditional AI invocation**: Database Operations checks if monitoring data exists before invoking AI
4. **Output routing**: AI results are typically formatted and sent to email, Jira, Slack, or used to create PRs/notebooks
