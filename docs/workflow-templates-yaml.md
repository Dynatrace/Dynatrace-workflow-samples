# Format 1: Workflow Templates (YAML) - UI Import/Export

This is the **easiest and recommended format** for most use cases. Templates are exported and imported via the Dynatrace Workflows UI.

## Structure

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

### Optional Top-Level Workflow Fields

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

## Key Components

### 1. Metadata Section

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

### 2. Tasks

Each task has:
- **name**: Unique task identifier
- **description**: Human-readable description
- **action**: The action to execute (see [Actions Catalog](actions-catalog.md))
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

### 3. Conditions

Control task execution flow:

```yaml
conditions:
  states:
    previous_task: OK  # Wait for previous_task to complete successfully
  custom: "{{ result('previous_task').records | length > 0 }}"  # Custom Jinja2 condition
  else: SKIP  # Action if condition fails: SKIP or STOP
```

### 4. Triggers

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

### 5. Looping with withItems (For-Each)

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

## Common Workflow Actions

### Execute DQL Query
```yaml
action: dynatrace.automations:execute-dql-query
input:
  query: |-
    fetch logs
    | filter dt.entity.host == "{{ event()['dt.entity.host'] }}"
    | limit 10
```

### Run JavaScript
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

### HTTP Request
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

### Send Email
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

### Jira - Create Issue
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

### Slack - Send Message
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

### Microsoft Teams - Send Message
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

### Microsoft Teams - AdaptiveCard Example
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

### Get Ownership Information
```yaml
action: dynatrace.ownership:get-ownership-from-entity
input:
  entityIds: "{{ event()['dt.entity.host'] }}"
  responsibilities:
    - Security
    - Operations
  selectedTeamIdentifiers: []
```

### Run Sub-Workflow
```yaml
action: dynatrace.automations:run-workflow
input:
  workflowId: "workflow-uuid-here"
  workflowInput: '{{ result("prepare_input") | to_json }}'
```

### Get Connection Dynamically
```yaml
# Use connection() function to dynamically resolve connections
connection: "{{ connection('app:dynatrace.slack:connection', channel_name) }}"
```

## Template Expressions (Jinja2)

Workflows use Jinja2 templating for dynamic values:

### Access Event Data
```jinja2
{{ event()['dt.entity.host'] }}
{{ event()['event.name'] }}
{{ event()['event.status'] }}
```

### Access Task Results
```jinja2
{{ result('task_name').records }}
{{ result('task_name').records[0].fieldName }}
{{ result('task_name') | to_json }}
```

### Access Execution Context
```jinja2
{{ execution().id }}
{{ execution().workflow.id }}
{{ execution().started_at }}
{{ task().id }}
{{ now() }}
{{ platform_url() }}
```

### Filters and Functions
```jinja2
{{ result('task').records | length }}
{{ result('task').value | int }}
{{ data | to_json }}
{{ string_value | string }}
{{ list | map(attribute='name') }}
{{ "value" in list }}
```

### Conditionals
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

### Loop Variables (withItems)
```jinja2
{{ _.item }}           # Current item in loop
{{ _.item.property }}  # Access item properties
```

## Best Practices

1. **Use meaningful task names**: Use descriptive names like `fetch_security_logs` instead of `task1`
2. **Add descriptions**: Every task should have a clear description
3. **Handle errors**: Use conditions to check task states before proceeding
4. **Use SKIP vs STOP**: SKIP continues workflow, STOP halts it
5. **Version dependencies**: Always specify app versions in dependencies
6. **No secrets in templates**: Templates should not contain API keys, tokens, or passwords
7. **Use connections**: Store credentials in Dynatrace connections, reference by ID
8. **Test DQL queries**: Validate DQL queries in the Dynatrace UI before using in workflows
9. **Position tasks**: Use logical x,y positions for UI canvas clarity

## Example: Complete Workflow Template

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
