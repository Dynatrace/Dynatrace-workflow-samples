# Incident Management

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 6 templates demonstrate ITSM integration patterns — creating, searching, and updating incidents in ServiceNow and PagerDuty, with notification routing via Slack and email based on entity ownership.

## Templates

| Template | Trigger | What It Does | Integrations |
|----------|---------|--------------|--------------|
| **Comments or Creates a ServiceNow Incident** | Problem Event (all categories) | Searches for existing ServiceNow incidents by correlation ID; comments on existing or creates new | ServiceNow |
| **Create ServiceNow Incident & Notify via Slack** | On-Demand | Creates ServiceNow incident with problem details; sends Slack notification with incident link | ServiceNow, Slack |
| **Create PagerDuty Incident from Problem Event** | On-Demand | Creates PagerDuty incident with event title, details, and incident key | PagerDuty |
| **List PagerDuty On-Call Users** | On-Demand | Retrieves current on-call roster from PagerDuty | PagerDuty |
| **Search ServiceNow Incidents & Notify via Slack** | On-Demand (schedulable) | Queries recent ServiceNow incidents; JavaScript formats summary with stats; sends to Slack | ServiceNow, Slack |
| **Send Email for Problems Based on Ownership** | Problem Event (Errors) | Resolves entity owners via ownership data; sends problem summary email to responsible team | Email, Ownership |

## Key Patterns

### Idempotent Incident Creation (Search-First)
The "Comments or Creates" template demonstrates the best practice of searching for existing incidents before creating new ones — preventing duplicate incidents for the same problem.

### Ownership-Based Routing
The email template uses `dynatrace.ownership:get-ownership-from-entity` to dynamically resolve the responsible team and route notifications to the correct owners.

### Multi-Channel Notification
Several templates combine ITSM actions (create incident) with messaging actions (Slack notification) in a single workflow.

## Key Learnings for AI Agents

1. **Always search before creating**: When integrating with ITSM, check for existing incidents to avoid duplicates
2. **Use correlation IDs**: Link Dynatrace problems to ITSM incidents for bidirectional traceability
3. **Combine ITSM + messaging**: Create the incident AND notify the team in the same workflow
4. **Ownership-driven routing**: Use Dynatrace ownership data to dynamically determine notification targets
