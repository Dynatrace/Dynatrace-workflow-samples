# Remediation

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 2 templates demonstrate automated remediation patterns using Red Hat Ansible — both Event-Driven Ansible (EDA) and Automation Controller job templates.

## Templates

| Template | Trigger | What It Does | Integrations |
|----------|---------|--------------|--------------|
| **Mitigate Dynatrace Problem with RH Event-Driven Ansible** | On-Demand | Sends problem event details to Ansible EDA controller; notifies Slack of remediation trigger | Red Hat Ansible EDA, Slack |
| **Trigger Ansible Job Template for Problem Events** | Problem Event (SLOWDOWN) | Launches Ansible job template; polls job status; sends completion summary via email | Red Hat Ansible Automation Controller |

## Key Patterns

### Event-Driven vs Job-Based Remediation
- **EDA** (`send-event-to-eda`): Fire-and-forget event to a rulebook — EDA decides what to do based on event content
- **Job Template** (`launch-job-template` + `list-job-status`): Explicit job invocation with polling for completion status

### Post-Remediation Notification
Both templates notify after triggering remediation — via Slack (EDA) or email (job template) — so operators know remediation was initiated.

## Key Learnings for AI Agents

1. **Two Ansible patterns**: EDA for event-driven (reactive) remediation, job templates for pre-defined runbooks
2. **Include problem context**: Pass Dynatrace problem details (entity, event name, status) to Ansible for context-aware remediation
3. **Confirm remediation**: Always notify after triggering remediation so operators are aware
