# Common Workflow Patterns and Examples

## Pattern 1: Event-Triggered Alert with Ownership

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

## Pattern 2: Scheduled Report

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

## Pattern 3: Conditional Branch with Multiple Paths

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

## Pattern 4: Multi-Step Remediation

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
