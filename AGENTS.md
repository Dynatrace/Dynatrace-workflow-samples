# Dynatrace Workflows - AI Assistant Instructions

This document provides comprehensive guidelines for creating syntactically correct Dynatrace Workflows. These instructions are designed for AI coding assistants including GitHub Copilot, Cursor, Claude Code, and Kiro.

## Overview

Dynatrace Workflows are automation solutions that allow you to orchestrate tasks, integrate with external systems, and automate responses to events. This repository contains sample workflows and code snippets for the Dynatrace AutomationEngine and Workflows app.

**Important**: There are **three distinct formats** for Dynatrace Workflows. **Never mix these formats**:

1. **Workflow Templates (YAML)** - For UI import/export
2. **API Format (JSON)** - For programmatic workflow management
3. **Terraform/Monaco** - For Configuration-as-Code deployments

---

## Pull Request Review Guidelines

When reviewing pull requests (automated or manual), verify the following:

### Workflow Syntax Validation

- [ ] **Correct format used**: YAML template, API JSON, or Terraform (never mixed)
- [ ] **schemaVersion is 3**: All workflows must use `schemaVersion: 3`
- [ ] **Valid YAML/JSON syntax**: No parsing errors
- [ ] **Task names match**: `name` field inside task matches the task key
- [ ] **Predecessors exist**: All referenced predecessor tasks are defined
- [ ] **Actions are valid**: Action names follow `app:action` pattern (e.g., `dynatrace.automations:execute-dql-query`)

### Security Review

- [ ] **No hardcoded secrets**: No API keys, tokens, passwords, or credentials in workflow files
- [ ] **Use `secret()` function**: Sensitive values should use `{{ secret('secret_name') }}`
- [ ] **Use connections**: External service credentials stored in Dynatrace connections
- [ ] **No internal URLs exposed**: No internal/private endpoints in HTTP actions

### Best Practices

- [ ] **Meaningful task names**: Descriptive names like `fetch_security_logs` instead of `task1`
- [ ] **Task descriptions**: Every task should have a description
- [ ] **Proper error handling**: Conditions check task states before proceeding
- [ ] **Dependencies declared**: All required apps listed in metadata dependencies
- [ ] **File naming**: Templates use `wftpl_*.yaml` naming convention

### DQL Query Review

- [ ] **Valid DQL syntax**: Queries use correct DQL operators and functions
- [ ] **Appropriate time ranges**: Queries don't fetch unbounded data
- [ ] **Proper filtering**: Queries include necessary filters to limit results
- [ ] **Result limits**: Large queries include `| limit N` or aggregation

### Jinja2 Template Review

- [ ] **Correct syntax**: Expressions use `{{ }}` for values, `{% %}` for logic
- [ ] **Valid function calls**: `event()`, `result()`, `execution()` used correctly
- [ ] **Proper escaping**: Quotes escaped correctly in nested expressions
- [ ] **Loop variables**: `withItems` loops use `_.item` or named variable correctly

### Review Comment Examples

When flagging issues, provide actionable feedback:

```
# Good review comment:
"Task 'send_alert' references predecessor 'get_data' but this task is not defined.
Add the missing task or update the predecessor reference."

# Good review comment:
"Hardcoded API key detected in HTTP action. Replace with:
Authorization: 'Bearer {{ secret(\"api_token\") }}'"
```

---

## Format 1: Workflow Templates (YAML) - UI Import/Export

This is the **easiest and recommended format** for most use cases. Templates are exported and imported via the Dynatrace Workflows UI.

### Structure

```yaml
metadata:
  version: "1"
  dependencies:
    apps:
      - id: dynatrace.automations
        version: ^1.840.0
      - id: dynatrace.aws.connector  # Example of an additional app
        version: ^1.0.0
  inputs: []

workflow:
  title: "Your Workflow Title"
  description: "Optional workflow description"

  tasks:
    task_name:
      name: task_name
      description: "Task description"
      action: dynatrace.automations:execute-dql-query
      input:
        query: |-
          fetch logs
          | limit 10
      position:
        x: 0
        y: 1
      predecessors: []
      conditions:
        states:
          previous_task: OK
        custom: "{{ result('previous_task').records | length > 0 }}"
        else: SKIP

  trigger: {}
  schemaVersion: 3
```

#### Optional Top-Level Workflow Fields

When exporting workflows from the UI, you may see these additional fields:

```yaml
workflow:
  title: "Your Workflow Title"
  id: "workflow-uuid-here"           # Auto-generated UUID (optional in templates)
  description: "Workflow description"
  tasks: {}
  trigger: {}
  schemaVersion: 3
  result: null                        # Usually null
  input: {}                           # Workflow input parameters
  hourlyExecutionLimit: 1000          # Max executions per hour (default: 1000)
  type: STANDARD                      # Workflow type (STANDARD is default)
```

**Note**: When creating new workflow templates, you typically only need `title`, `tasks`, `trigger`, and `schemaVersion`. The other fields are auto-populated or have sensible defaults.

### Key Components

#### 1. Metadata Section

```yaml
metadata:
  version: "1"
  dependencies:
    apps:
      - id: dynatrace.automations  # Required for DQL, JavaScript, HTTP actions
        version: ^1.840.0
      - id: dynatrace.jira          # Add as needed
        version: ^1.0.0
      - id: dynatrace.slack         # Add as needed
        version: ^1.0.0
  inputs: []
```

**Common Apps/Connectors:**
- `dynatrace.automations` - Core workflow actions (DQL queries, JavaScript, HTTP requests)
- `dynatrace.jira` - Jira integration
- `dynatrace.slack` - Slack integration
- `dynatrace.msteams` - Microsoft Teams integration
- `dynatrace.email` - Email actions
- `dynatrace.ownership` - Team and ownership management
- `dynatrace.aws.connector` - AWS integrations
- `dynatrace.azure.connector` - Microsoft Entra ID (Azure) / Graph connector actions
- `dynatrace.kubernetes.connector` - Kubernetes API automation (typically via EdgeConnect)
- `dynatrace.redhat.ansible` - Red Hat Ansible Automation Platform / EDA integrations
- `dynatrace.servicenow` - ServiceNow integration
- `dynatrace.davis.workflow.actions` - Dynatrace Intelligence (Davis) workflow actions

This list is not exhaustive. Dynatrace regularly ships additional Workflow connectors (for example GitHub, GitLab, Microsoft 365, PagerDuty, Jenkins, Snowflake, Azure, Red Hat Ansible, and Text Processing). For the current catalog, see:
https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions

#### 2. Tasks

Each task has:
- **name**: Unique task identifier
- **description**: Human-readable description
- **action**: The action to execute (see Actions Catalog below)
- **input**: Action-specific parameters
- **position**: UI canvas position (x, y coordinates)
- **predecessors**: Array of task names that must complete before this task
- **conditions**: Optional execution conditions
- **active**: Optional boolean to enable/disable task

```yaml
tasks:
  example_task:
    name: example_task
    description: "Executes DQL query"
    action: dynatrace.automations:execute-dql-query
    input:
      query: |-
        fetch logs
        | filter dt.entity.host == "{{ event()['dt.entity.host'] }}"
        | limit 10
    position:
      x: 0
      y: 1
    predecessors: []
```

#### 3. Conditions

Control task execution flow:

```yaml
conditions:
  states:
    previous_task: OK  # Wait for previous_task to complete successfully
  custom: "{{ result('previous_task').records | length > 0 }}"  # Custom Jinja2 condition
  else: SKIP  # Action if condition fails: SKIP or STOP
```

#### 4. Triggers

**Manual Trigger** (default):
```yaml
trigger: {}
```

**Event Trigger**:
```yaml
trigger:
  eventTrigger:
    filterQuery: |-
      event.type == "DETECTION_FINDING"
      AND dt.security.risk.level == "CRITICAL"
    isActive: true
    uniqueExpression: null
    triggerConfiguration:
      type: event
      value:
        query: |-
          event.type == "DETECTION_FINDING"
          AND dt.security.risk.level == "CRITICAL"
        eventType: security.events  # Can be: events, security.events, bizevents, logs, etc.
```

**Schedule Trigger**:
```yaml
trigger:
  schedule:
    trigger:
      type: cron
      cron: "0 9 * * MON"  # Every Monday at 9 AM
    timezone: "Europe/Vienna"
    isActive: true
    isFaulty: false
    nextExecution: null
    filterParameters:
      earliestStart: "2024-01-01"
      earliestStartTime: "00:00"
    inputs: {}
```

#### 5. Looping with withItems (For-Each)

Process multiple items:

```yaml
send_notifications:
  name: send_notifications
  action: dynatrace.slack:slack-send-message
  input:
    channel: "{{ _.owner.slackChannel }}"
    message: "Alert for {{ _.owner.teamName }}"
  withItems: owner in {{ result('get_owners').slackChannels }}
  concurrency: 1  # Number of concurrent executions
  predecessors:
    - get_owners
```

### Common Workflow Actions

#### Execute DQL Query
```yaml
action: dynatrace.automations:execute-dql-query
input:
  query: |-
    fetch logs
    | filter dt.entity.host == "{{ event()['dt.entity.host'] }}"
    | limit 10
```

#### Run JavaScript
```yaml
action: dynatrace.automations:run-javascript
input:
  script: |-
    import { execution } from '@dynatrace-sdk/automation-utils';

    export default async function ({ execution_id }) {
      console.log("Processing data");
      const ex = await execution();
      const previousResult = await ex.result('previous_task');

      // Your custom logic here
      return {
        processed: true,
        count: previousResult.records.length
      };
    }
```

#### HTTP Request
```yaml
action: dynatrace.automations:http-function
input:
  url: "https://api.example.com/endpoint"
  method: "POST"
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer {{ secret('api_token') }}"
  payload: |-
    {
      "data": "{{ result('previous_task').value }}"
    }
```

#### Send Email
```yaml
action: dynatrace.email:send-email
input:
  to:
    - "user@example.com"
  cc: []
  bcc: []
  subject: "Alert: {{ event()['event.name'] }}"
  content: |-
    # Problem detected

    *Host*: {{ event()['dt.entity.host'] }}

    Details:
    {{ result('get_logs') | to_json }}

# Notes
# - You must specify at least one recipient in `to`, `cc`, or `bcc` (max 10 email addresses per field).
# - If recipients are generated via expressions, they must evaluate to a list of email addresses, for example:
#   {{ ["user1@domain.com", "user2@domain.com"] }}
# - The Email Connector supports Markdown-like formatting in `content` (for example `*italics*`, `**bold**`, `~~strike~~`,
#   headings with `#`, lists, tables, and `[label](https://example.com)` links).
# - No HTML support; images and JavaScript in the body are not supported (they will appear as plain text).
# - Keep message size well below 256 KiB: formatting is disabled at >= 256 KiB and larger payloads can cause the action to fail.
# - Emails are sent from `no-reply@apps.dynatrace.com` (you may need to whitelist this domain).
# - Workflows executing this action require the `email:emails:send` permission.
```

#### Jira - Create Issue
```yaml
action: dynatrace.jira:jira-create-issue
input:
  connectionId: ""  # Connection ID or empty for default
  project:
    id: "10000"
    key: "PROJ"
    name: "Project Name"
  issueType:
    id: "10001"
    name: "Bug"
  summary: "Issue from Dynatrace: {{ event()['event.name'] }}"
  description: |-
    Automated issue creation

    Details: {{ result('previous_task') | to_json }}
  priority:
    id: "2"
    name: "High"
  labels:
    - "dynatrace"
    - "automated"
```

#### Slack - Send Message
```yaml
action: dynatrace.slack:slack-send-message
input:
  connection: ""  # Select a Slack connection
  channel: ""      # Prefer Slack channel ID (recommended by docs)
  message: |-
    *Alert from Dynatrace*

    *Event*: {{ event()['event.name'] }}
    *Host*: {{ event()['dt.entity.host'] }}

# Notes
# - Allow external requests to `slack.com` (Settings > General > External requests).
# - Slack messages can be plain text/Slack Markdown, or a JSON Block Kit payload (see docs).
```

#### Microsoft Teams - Send Message
```yaml
action: dynatrace.msteams:send-message
input:
  connectionId: ""  # Select a Microsoft Teams webhook connection
  message: |-
    **Alert from Dynatrace**

    **Event**: {{ event()['event.name'] }}
    **Host**: {{ event()['dt.entity.host'] }}

# Notes
# - Allow external requests to the Power Automate webhook domain used by your connection.
# - Microsoft Teams supports Markdown cards or AdaptiveCard JSON (recommended for rich layouts).
# - Office 365 connectors are being retired; prefer Power Automate webhooks.
```

#### Microsoft Teams - AdaptiveCard Example
```yaml
action: dynatrace.msteams:send-message
input:
  connectionId: ""
  message: |-
    {
      "type": "AdaptiveCard",
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
      "version": "1.4",
      "body": [
        {
          "type": "TextBlock",
          "size": "Medium",
          "weight": "Bolder",
          "text": "Dynatrace report"
        },
        {
          "type": "FactSet",
          "facts": [
            {
              "title": "Event",
              "value": {{ (event()['event.name'] | string) | to_json }}
            },
            {
              "title": "Host",
              "value": {{ (event()['dt.entity.host'] | string) | to_json }}
            }
          ]
        }
      ]
    }

# Notes
# - Teams doesn't support Adaptive Cards Template Language; use Dynatrace expressions and `| to_json` for safe escaping.
```

#### Get Ownership Information
```yaml
action: dynatrace.ownership:get-ownership-from-entity
input:
  entityIds: "{{ event()['dt.entity.host'] }}"
  responsibilities:
    - Security
    - Operations
  selectedTeamIdentifiers: []
```

#### Run Sub-Workflow
```yaml
action: dynatrace.automations:run-workflow
input:
  workflowId: "workflow-uuid-here"
  workflowInput: '{{ result("prepare_input") | to_json }}'
```

#### Get Connection Dynamically
```yaml
# Use connection() function to dynamically resolve connections
connection: "{{ connection('app:dynatrace.slack:connection', channel_name) }}"
```

### Template Expressions (Jinja2)

Workflows use Jinja2 templating for dynamic values:

#### Access Event Data
```jinja2
{{ event()['dt.entity.host'] }}
{{ event()['event.name'] }}
{{ event()['event.status'] }}
```

#### Access Task Results
```jinja2
{{ result('task_name').records }}
{{ result('task_name').records[0].fieldName }}
{{ result('task_name') | to_json }}
```

#### Access Execution Context
```jinja2
{{ execution().id }}
{{ execution().workflow.id }}
{{ execution().started_at }}
{{ task().id }}
{{ now() }}
{{ platform_url() }}
```

#### Filters and Functions
```jinja2
{{ result('task').records | length }}
{{ result('task').value | int }}
{{ data | to_json }}
{{ string_value | string }}
{{ list | map(attribute='name') }}
{{ "value" in list }}
```

#### Conditionals
```jinja2
{% if result('task').records | length > 0 %}
  Records found
{% else %}
  No records
{% endif %}

{% for item in result('task').records %}
  - {{ item.name }}
{% endfor %}
```

#### Loop Variables (withItems)
```jinja2
{{ _.item }}           # Current item in loop
{{ _.item.property }}  # Access item properties
```

### Best Practices for Workflow Templates

1. **Use meaningful task names**: Use descriptive names like `fetch_security_logs` instead of `task1`
2. **Add descriptions**: Every task should have a clear description
3. **Handle errors**: Use conditions to check task states before proceeding
4. **Use SKIP vs STOP**: SKIP continues workflow, STOP halts it
5. **Version dependencies**: Always specify app versions in dependencies
6. **No secrets in templates**: Templates should not contain API keys, tokens, or passwords
7. **Use connections**: Store credentials in Dynatrace connections, reference by ID
8. **Test DQL queries**: Validate DQL queries in the Dynatrace UI before using in workflows
9. **Position tasks**: Use logical x,y positions for UI canvas clarity

### Example: Complete Workflow Template

```yaml
metadata:
  version: "1"
  dependencies:
    apps:
      - id: dynatrace.automations
        version: ^1.840.0
      - id: dynatrace.slack
        version: ^1.0.0
  inputs: []

workflow:
  title: Security Alert Workflow
  description: "Monitors security events and sends Slack notifications"

  tasks:
    fetch_security_events:
      name: fetch_security_events
      description: "Query security events from the last hour"
      action: dynatrace.automations:execute-dql-query
      input:
        query: |-
          fetch events
          | filter event.type == "SECURITY_EVENT"
          | filter timestamp > now() - 1h
          | limit 100
      position:
        x: 0
        y: 1
      predecessors: []

    process_events:
      name: process_events
      description: "Process and filter critical events"
      action: dynatrace.automations:run-javascript
      input:
        script: |-
          import { execution } from '@dynatrace-sdk/automation-utils';

          export default async function () {
            const ex = await execution();
            const events = await ex.result('fetch_security_events');

            const criticalEvents = events.records.filter(e =>
              e.severity === 'CRITICAL'
            );

            return {
              criticalCount: criticalEvents.length,
              events: criticalEvents
            };
          }
      position:
        x: 0
        y: 2
      predecessors:
        - fetch_security_events
      conditions:
        states:
          fetch_security_events: OK

    send_slack_alert:
      name: send_slack_alert
      description: "Send alert to Slack channel"
      action: dynatrace.slack:slack-send-message
      input:
        channel: "#security-alerts"
        message: |-
          :rotating_light: *Critical Security Events Detected*

          Count: {{ result('process_events').criticalCount }}
          Time: {{ now() }}

          Details: {{ result('process_events').events | to_json }}
        connection: ""
      position:
        x: 0
        y: 3
      predecessors:
        - process_events
      conditions:
        states:
          process_events: OK
        custom: "{{ result('process_events').criticalCount > 0 }}"
        else: SKIP

  trigger:
    schedule:
      trigger:
        type: cron
        cron: "0 * * * *"  # Every hour
      timezone: "UTC"
      isActive: true
      isFaulty: false

  schemaVersion: 3
```

---

## Format 2: API Format (JSON)

Used for programmatic workflow management via the Automation API.

### API Endpoints

- **GET** `/platform/automation/v1/workflows` - List all workflows
- **GET** `/platform/automation/v1/workflows/{id}` - Get specific workflow
- **POST** `/platform/automation/v1/workflows` - Create workflow
- **PUT** `/platform/automation/v1/workflows/{id}` - Update workflow
- **DELETE** `/platform/automation/v1/workflows/{id}` - Delete workflow

### Structure

```json
{
  "title": "Workflow Title",
  "description": "Workflow description",
  "isPrivate": true,
  "triggerType": "Event",
  "schemaVersion": 3,
  "trigger": {
    "eventTrigger": {
      "isActive": true,
      "filterQuery": "event.type == 'CUSTOM_INFO'",
      "uniqueExpression": null,
      "triggerConfiguration": {
        "type": "event",
        "value": {
          "query": "event.type == 'CUSTOM_INFO'",
          "eventType": "events"
        }
      }
    }
  },
  "tasks": {
    "task_name": {
      "name": "task_name",
      "description": "Task description",
      "action": "dynatrace.automations:execute-dql-query",
      "input": {
        "query": "fetch logs | limit 10"
      },
      "position": {
        "x": 0,
        "y": 1
      },
      "predecessors": []
    }
  }
}
```

### Differences from YAML Template Format

1. **No metadata section** - Dependencies managed separately
2. **Different field names**:
   - `isPrivate` instead of included in trigger
   - `triggerType` as top-level field
3. **Tasks as object** - Tasks are key-value pairs, not array
4. **String escaping** - Jinja2 expressions need proper JSON escaping

### Example API Request

```bash
curl --request POST 'https://{tenant}.apps.dynatrace.com/platform/automation/v1/workflows' \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {token}' \
  --data '{
    "title": "API Created Workflow",
    "description": "Created via API",
    "isPrivate": true,
    "triggerType": "Manual",
    "schemaVersion": 3,
    "trigger": {},
    "tasks": {
      "query_logs": {
        "name": "query_logs",
        "action": "dynatrace.automations:execute-dql-query",
        "input": {
          "query": "fetch logs | limit 10"
        },
        "position": { "x": 0, "y": 1 },
        "predecessors": []
      }
    }
  }'
```

---

## Format 3: Terraform Configuration

Used for Configuration-as-Code deployments with the Dynatrace Terraform provider.

### Prerequisites

Provider: `dynatrace-oss/dynatrace`
Documentation: https://registry.terraform.io/providers/dynatrace-oss/dynatrace/latest/docs

### Resource: dynatrace_automation_workflow

```hcl
resource "dynatrace_automation_workflow" "example" {
  title       = "Terraform Managed Workflow"
  description = "Created and managed by Terraform"

  actor  = "environment"
  owner  = "john.doe@example.com"
  private = true

  tasks {
    task {
      name        = "query_logs"
      description = "Execute DQL query"
      action      = "dynatrace.automations:execute-dql-query"
      active      = true

      position {
        x = 0
        y = 1
      }

      input = jsonencode({
        query = "fetch logs | limit 10"
      })
    }

    task {
      name        = "process_results"
      description = "Process query results"
      action      = "dynatrace.automations:run-javascript"
      active      = true

      position {
        x = 0
        y = 2
      }

      conditions {
        states = {
          query_logs = "OK"
        }
      }

      input = jsonencode({
        script = <<-EOT
          import { execution } from '@dynatrace-sdk/automation-utils';

          export default async function () {
            const ex = await execution();
            const logs = await ex.result('query_logs');
            return { count: logs.records.length };
          }
        EOT
      })

      predecessors = ["query_logs"]
    }
  }

  trigger {
    event {
      active = true

      config {
        davis_event {
          entity_tags_match = "all"

          on_problem_close {
            enabled = true
          }

          types = ["CUSTOM_INFO"]
        }
      }
    }
  }
}
```

### Terraform Variables and Secrets

```hcl
# Use Terraform variables
variable "slack_channel" {
  type    = string
  default = "#alerts"
}

resource "dynatrace_automation_workflow" "with_variables" {
  title = "Workflow with Variables"

  tasks {
    task {
      name   = "send_slack"
      action = "dynatrace.slack:slack-send-message"

      input = jsonencode({
        channel    = var.slack_channel
        message    = "Alert triggered"
        connection = ""
      })

      position {
        x = 0
        y = 1
      }
    }
  }
}
```

### Important Terraform Notes

1. **Input encoding**: Always use `jsonencode()` for task inputs
2. **Multi-line strings**: Use `<<-EOT ... EOT` heredoc syntax for scripts
3. **Conditions**: Define as nested blocks with proper HCL syntax
4. **Predecessors**: Array of task names as strings
5. **State management**: Terraform tracks workflow state; updates modify existing workflows
6. **Not compatible with YAML**: Terraform format is distinct; don't try to convert YAML directly

---

## Monaco Configuration-as-Code

Monaco uses a different YAML format (not compatible with workflow templates).

### Structure

```yaml
config:
  - workflow:
      name: "monaco-managed-workflow"
      template: workflow.json
      skip: false
```

With corresponding `workflow.json`:
```json
{
  "title": "{{ .name }}",
  "description": "Managed by Monaco",
  "schemaVersion": 3,
  "tasks": {
    "example": {
      "name": "example",
      "action": "dynatrace.automations:execute-dql-query",
      "input": {
        "query": "{{ .query }}"
      }
    }
  }
}
```

**Note**: Monaco format includes escaping and uses different YAML structure with placeholders. See Monaco documentation for details.

---

## Actions Catalog Reference

### Core Automation Actions (dynatrace.automations)

- `execute-dql-query` - Execute DQL query
- `run-javascript` - Run custom JavaScript code
- `http-function` - Make HTTP requests
- `run-workflow` - Execute another workflow
- `sleep` - Wait for specified duration

### Integration Actions

**Jira** (`dynatrace.jira:*`)
- `jira-create-issue` - Create Jira issue
- `jira-update-issue` - Update existing issue
- `jira-add-comment` - Add comment to issue
- `jira-transition-issue` - Change issue status

**Slack** (`dynatrace.slack:*`)
- `slack-send-message` - Send message to channel
- `slack-send-message-user` - Send DM to user

**Microsoft Teams** (`dynatrace.msteams:*`)
- `send-message` - Send message (Markdown card or AdaptiveCard JSON)

**Email** (`dynatrace.email:*`)
- `send-email` - Send email

**ServiceNow** (`dynatrace.servicenow:*`)
- `snow-create-incident` - Create incident
- `snow-search` / `snow-search-incidents` - Search records/incidents
- `snow-comment-on-incident` - Add comment to incident
- `snow-get-groups` - Fetch groups (used for team import/routing)

Notes (docs):
- Connector setup, required permissions, and the full list of available ServiceNow actions are documented here: https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/service-now
- ServiceNow workflow actions require granting Workflows the `app-settings:objects:read` permission (in addition to general Workflows permissions).
- The ServiceNow connector also provides actions like resolve incident, create/update record, and general comment actions; use the Workflows action picker to select the action and copy the exact `action` ID (avoid guessing).

**AWS** (`dynatrace.aws.connector:*`)
- `s3-list-buckets`, `s3-put-object`, etc.
- `lambda-invoke` - Invoke Lambda function
- `ec2-*` - EC2 operations

**Azure / Microsoft Entra ID** (`dynatrace.azure.connector:*`)
- `get-groups` - List groups (Microsoft Entra ID)

**Red Hat Ansible** (`dynatrace.redhat.ansible:*`)
- `launch-job-template` - Launch an Automation Controller job template
- `send-event-to-eda` - Send an event to Event-Driven Ansible

**Dynatrace Intelligence (Davis)** (`dynatrace.davis.workflow.actions:*`)
- `davis-analyze` - Run Davis analysis

**Kubernetes** (`dynatrace.kubernetes.connector:*`)
- `delete` - Delete resources (for example: `dynatrace.kubernetes.connector:delete`)

Note: Kubernetes Connector actions resemble `kubectl` operations (apply, delete, get/list, logs, patch, rollout restart, wait). Exact action IDs can vary by connector version—prefer selecting from the Workflows action picker and keep `metadata.dependencies.apps` in sync.

**Ownership** (`dynatrace.ownership:*`)
- `get-ownership-from-entity` - Get entity owners
- `import-teams-to-settings` - Import teams

For additional connectors and their actions (GitHub, GitLab, Microsoft 365, PagerDuty, Jenkins, Snowflake, Azure, Red Hat Ansible, Text Processing, and more), refer to the official catalog:
https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions

---

## Creating Workflows: Decision Guide

### Use Workflow Templates (YAML) when:
- Creating workflows for manual import/export
- Sharing workflow examples
- Quick prototyping and testing
- You want the simplest format
- Working primarily in the UI

### Use API Format (JSON) when:
- Programmatically managing workflows
- Automating workflow deployment
- Integrating with CI/CD pipelines
- Bulk operations (create/update many workflows)

### Use Terraform when:
- Managing workflows as Infrastructure-as-Code
- Version controlling workflow definitions
- Multi-environment deployments
- You use Terraform for other Dynatrace config
- Need state management and drift detection

---

## Common Patterns and Examples

### Pattern 1: Event-Triggered Alert with Ownership

```yaml
workflow:
  title: Alert with Ownership Routing
  tasks:
    get_owners:
      action: dynatrace.ownership:get-ownership-from-entity
      input:
        entityIds: "{{ event()['dt.entity.host'] }}"
        responsibilities: ["Operations"]

    send_alert:
      action: dynatrace.slack:slack-send-message
      input:
        channel: "{{ _.owner.slackChannel }}"
        message: "Alert for your team"
      withItems: owner in {{ result('get_owners').slackChannels }}
      predecessors: ["get_owners"]

  trigger:
    eventTrigger:
      filterQuery: "event.type == 'CUSTOM_INFO'"
      isActive: true
```

### Pattern 2: Scheduled Report

```yaml
workflow:
  title: Daily Error Report
  tasks:
    fetch_errors:
      action: dynatrace.automations:execute-dql-query
      input:
        query: |-
          fetch logs
          | filter loglevel == "ERROR"
          | filter timestamp > now() - 24h
          | summarize count(), by: {dt.entity.service}

    send_report:
      action: dynatrace.email:send-email
      input:
        to: ["team@example.com"]
        subject: "Daily Error Report - {{ now() | date('%Y-%m-%d') }}"
        content: "{{ result('fetch_errors').records | to_json }}"
      predecessors: ["fetch_errors"]

  trigger:
    schedule:
      trigger:
        type: cron
        cron: "0 9 * * *"
      timezone: "UTC"
```

### Pattern 3: Conditional Branch with Multiple Paths

```yaml
workflow:
  title: Severity-Based Routing
  tasks:
    check_severity:
      action: dynatrace.automations:execute-dql-query
      input:
        query: "fetch events | filter event.id == '{{ event()['event.id'] }}'"

    high_priority:
      action: dynatrace.slack:slack-send-message
      input:
        channel: "#critical"
        message: "CRITICAL: Immediate action required"
      predecessors: ["check_severity"]
      conditions:
        states:
          check_severity: OK
        custom: "{{ result('check_severity').records[0].severity == 'CRITICAL' }}"

    low_priority:
      action: dynatrace.slack:slack-send-message
      input:
        channel: "#alerts"
        message: "Info: Review when available"
      predecessors: ["check_severity"]
      conditions:
        states:
          check_severity: OK
        custom: "{{ result('check_severity').records[0].severity != 'CRITICAL' }}"
```

### Pattern 4: Multi-Step Remediation

```yaml
workflow:
  title: Auto-Remediation Workflow
  tasks:
    detect_issue:
      action: dynatrace.automations:execute-dql-query
      input:
        query: "fetch logs | filter loglevel == 'ERROR'"

    attempt_fix:
      action: dynatrace.automations:http-function
      input:
        url: "https://api.example.com/restart"
        method: "POST"
      predecessors: ["detect_issue"]
      conditions:
        states:
          detect_issue: OK

    verify_fix:
      action: dynatrace.automations:execute-dql-query
      input:
        query: "fetch logs | filter loglevel == 'ERROR'"
      predecessors: ["attempt_fix"]

    escalate_if_failed:
      action: dynatrace.slack:slack-send-message
      input:
        channel: "#ops-escalation"
        message: "Auto-remediation failed, manual intervention needed"
      predecessors: ["verify_fix"]
      conditions:
        custom: "{{ result('verify_fix').records | length > 0 }}"
```

---

## Validation and Testing

Before deploying workflows:

1. **Test DQL queries** in Notebooks or DQL explorer
2. **Validate JSON syntax** for API format
3. **Test JavaScript code** in the workflow editor
4. **Check app versions** are available in your environment
5. **Verify connections** are properly configured
6. **Test with manual trigger** before enabling automation
7. **Review execution logs** for errors

---

## Troubleshooting

### Common Issues

**Issue**: Task always skipped
- **Solution**: Check predecessor states and custom conditions

**Issue**: DQL query returns no results
- **Solution**: Verify query syntax and time range

**Issue**: JavaScript task fails
- **Solution**: Check for syntax errors, missing imports, or async/await issues

**Issue**: Template expressions not resolving
- **Solution**: Verify Jinja2 syntax and that referenced tasks/events exist

**Issue**: Connection not found
- **Solution**: Ensure connection ID is correct and connection is active

---

## Additional Resources

- **Dynatrace Documentation**: https://docs.dynatrace.com/docs/analyze-explore-automate/workflows
- **Actions Catalog**: https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions
- **DQL Documentation**: https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language
- **Terraform Provider**: https://registry.terraform.io/providers/dynatrace-oss/dynatrace/latest/docs
- **Workflow Samples**: This repository contains many examples in the `samples/` directory

---

## File Naming Conventions

When creating workflow files in this repository:

- **Templates**: `wftpl_descriptive_name.yaml`
- **API Format**: `descriptive_name.json`
- **Terraform**: `workflow_name.tf`
- **Documentation**: `README.md` or `readme.md`

---

## Summary Checklist for AI Assistants

When generating a Dynatrace Workflow:

- [ ] Determine the correct format (Template YAML, API JSON, or Terraform)
- [ ] Never mix formats
- [ ] Include all required metadata/dependencies
- [ ] Use correct action names from the catalog
- [ ] Include proper task predecessors for sequencing
- [ ] Add conditions where appropriate
- [ ] Use Jinja2 expressions correctly
- [ ] Include meaningful task names and descriptions
- [ ] Set appropriate trigger configuration
- [ ] Validate schemaVersion is 3
- [ ] No secrets or tokens in the code
- [ ] Test DQL queries separately first
- [ ] Follow the patterns from existing samples

---

*This guide is maintained for use by AI coding assistants. For human-readable documentation, see the official Dynatrace documentation.*
