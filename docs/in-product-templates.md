# In-Product Workflow Template Reference

The `in-product-templates/` directory contains **31 production-quality templates** organized into 7 categories. These are in-product templates maintained here as AI reference material for generating new workflows.

## Template Categories

| Category | Count | Key Actions |
|----------|-------|-------------|
| `dynatrace-intelligence-agents/` | 9 | `davis-copilot`, DQL, email, Jira, GitHub |
| `aws-devops-agent/` | 6 | `ingestbizevent`, `run-workflow`, `http-function`, custom events |
| `incident-management/` | 6 | `snow-*`, `create-incident` (PagerDuty), `get-ownership-from-entity` |
| `notifications-and-reporting/` | 3 | `send-message` (Teams), `send-email`, AdaptiveCards |
| `remediation/` | 2 | `launch-job-template`, `send-event-to-eda` (Ansible) |
| `devops-automation/` | 4 | `patch-resource` (K8s), `get/set-yaml-value`, `get-content` (GitHub) |
| `security/` | 1 | Threat intelligence data structure |

## Architectural Patterns from Templates

### Pattern: Dynatrace Intelligence Agent (9 templates)
The most common agentic pattern: collect context → invoke AI → act on analysis.

```yaml
# Step 1: Collect domain data
collect_data:
  action: dynatrace.automations:execute-dql-query
  input:
    query: |-
      fetch ...  # domain-specific query

# Step 2: Invoke Dynatrace Intelligence
analyze:
  action: dynatrace.davis.workflow.actions:davis-copilot
  input:
    prompt: |-
      Analyze the following data and provide recommendations:
      {{ result('collect_data').records | to_json }}
  predecessors: [collect_data]

# Step 3: Act on results (email, Jira, Slack, GitHub PR)
notify:
  action: dynatrace.email:send-email
  input:
    subject: "AI Analysis Report"
    content: "{{ result('analyze').response }}"
  predecessors: [analyze]
```

Key variations:
- **Multiple DQL queries** feeding a single AI prompt (Security Insights Report uses 3 queries)
- **Multi-step AI** — invoke `davis-copilot` twice for different analysis aspects (Mobile Crash Remediation)
- **Conditional AI** — check data existence before AI invocation (Database Operations)
- **AI → Action** — AI generates YAML fixes → create Jira ticket or GitHub PR (K8s Operations, K8s Troubleshooting)

### Pattern: Multi-Workflow Orchestration (AWS DevOps Agent)
For complex, multi-stage scenarios requiring asynchronous coordination:

1. **Bizevent queue**: Use `ingestbizevent` to create a durable event buffer
2. **Scheduled dispatcher**: Poll queue with DQL on schedule; invoke sub-workflows for each item
3. **Sub-workflow invocation**: Use `run-workflow` to trigger parameterized processing workflows
4. **Event-driven response handlers**: Listen for external system callbacks via custom event triggers
5. **Problem enrichment**: Attach findings to problems via custom annotations and notebooks

### Pattern: Idempotent ITSM Integration (Incident Management)
Always search before creating to prevent duplicates:

```yaml
search_existing:
  action: dynatrace.servicenow:snow-search-incidents
  input:
    query: "correlation_id={{ event()['event.id'] }}"

create_or_update:
  action: dynatrace.servicenow:snow-create-incident  # or snow-update-record
  predecessors: [search_existing]
  conditions:
    custom: "{{ result('search_existing').records | length == 0 }}"
```

### Pattern: Ownership-Based Routing
Route notifications dynamically based on entity ownership:

```yaml
get_owners:
  action: dynatrace.ownership:get-ownership-from-entity
  input:
    entityIds: "{{ event()['dt.entity.host'] }}"
    responsibilities: [Operations]

notify_owner:
  action: dynatrace.email:send-email
  input:
    to: "{{ result('get_owners') ... }}"
  predecessors: [get_owners]
```

### Pattern: Dual Ansible Remediation
Two styles for Ansible integration:
- **Event-Driven Ansible** (`send-event-to-eda`): Fire-and-forget to an EDA controller — rulebook decides the action
- **Job Templates** (`launch-job-template` + `list-job-status`): Explicit invocation with status polling

## Trigger Type Reference (from templates)

| Trigger | Usage | Example |
|---------|-------|---------|
| Problem Event | 13 templates | `event.kind == "DAVIS_PROBLEM"` with category filters |
| On-Demand (manual) | 8 templates | `trigger: {}` |
| Schedule (cron) | 5 templates | `cron: "0 9 * * MON"` for weekly reports |
| Custom Event | 3 templates | `event.type == "DETECTION_FINDING"` for security events |
| Sub-workflow | 2 templates | Invoked by `run-workflow` from parent |
