# Notifications and Reporting

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 3 templates demonstrate notification and reporting patterns — sending formatted alerts and summaries to Microsoft Teams and email with aggregated observability data.

## Templates

| Template | Trigger | What It Does | Integrations |
|----------|---------|--------------|--------------|
| **Container Vulnerability Notification to Microsoft Teams** | On-Demand (configurable) | Queries `security.events` for critical container vulnerabilities; sends formatted Teams message with finding details | Microsoft Teams, Security |
| **Send Email with Aggregated Log Summary** | On-Demand (schedulable) | Queries error logs from last 24h; groups by content prefix; creates table with sample messages and clickable trace links | Email |
| **Send Pod Logs to Microsoft Teams** | Problem Event (K8s pods) | Retrieves pod logs via K8s connector; formats adaptive card with pod details and logs; sends to Teams | Microsoft Teams, Kubernetes |

## Key Patterns

### Adaptive Cards for Microsoft Teams
Pod logs template uses JSON AdaptiveCard schema for rich, structured Teams messages — better than plain text for displaying structured data.

### DQL Aggregation for Reporting
Log summary template uses DQL `summarize` and `groupBy` to aggregate error patterns before formatting — keeping email content concise and actionable.

### Clickable Trace Links
Log summary template generates deep links into Dynatrace distributed traces using `platform_url()` — enabling direct investigation from the notification.

## Key Learnings for AI Agents

1. **Use AdaptiveCards for Teams**: Structured card layouts are more readable than plain text for tabular data
2. **Aggregate before notifying**: Use DQL summarization to prevent notification overload
3. **Include deep links**: Add `platform_url()` links to let recipients jump directly into Dynatrace for investigation
