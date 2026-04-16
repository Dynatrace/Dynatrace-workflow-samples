# Actions Catalog Reference

> **Disclaimer**: This is a _sample-oriented reference_ to help AI assistants and contributors working in this repository. It is **not** the authoritative catalog of all actions available in Dynatrace Workflows. Connectors, action IDs, and capabilities change across releases. Always verify against the **official documentation** and your environment's **Workflows action picker** before relying on any specific action ID.
>
> **Authoritative source**: <https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions>

---

## Core Automation Actions (`dynatrace.automations`)

| Action | Description |
|--------|-------------|
| `execute-dql-query` | Execute a DQL query |
| `run-javascript` | Run custom JavaScript code |
| `http-function` | Make HTTP requests to external or internal endpoints |
| `run-workflow` | Execute another workflow (sub-workflow orchestration) |
| `sleep` | Wait for a specified duration |
| `ingest-bizevent` | Ingest business events for custom event pipelines |

---

## Dynatrace-Native Integrations

### Dynatrace Intelligence (`dynatrace.davis.workflow.actions:*`)
| Action | Description |
|--------|-------------|
| `davis-copilot` | AI-powered analysis, recommendations, and content generation (previously `davis-analyze`) |

> [Docs →](https://docs.dynatrace.com/docs/dynatrace-intelligence/use-cases/dynatrace-intelligence-for-workflows)

### Email (`dynatrace.email:*`)
| Action | Description |
|--------|-------------|
| `send-email` | Send email notifications |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/email)

### Ownership (`dynatrace.ownership:*`)
| Action | Description |
|--------|-------------|
| `get-ownership-from-entity` | Get entity owners (for routing notifications and tasks) |
| `import-teams-to-settings` | Import teams from external identity providers |

> [Docs →](https://docs.dynatrace.com/docs/deliver/ownership-app)

### Site Reliability Guardian (`dynatrace.site.reliability.guardian:*`)
| Action | Description |
|--------|-------------|
| `validate` | Execute a Site Reliability Guardian validation directly in a workflow |

> [Docs →](https://docs.dynatrace.com/docs/deliver/site-reliability-guardian#automation)

### Synthetic for Workflows
| Action | Description |
|--------|-------------|
| _(execute on-demand monitors)_ | Execute synthetic monitors on-demand at selected locations within workflows |

> [Docs →](https://docs.dynatrace.com/docs/observe/digital-experience/synthetic-on-grail/synthetic-for-workflows)

### Business Observability
| Action | Description |
|--------|-------------|
| _(generate business events)_ | Generate business events from automated tasks to connect monitoring data with business information |

> [Docs →](https://docs.dynatrace.com/docs/observe/business-observability/bo-events-capturing)

### Text Processing (`dynatrace.text.processing:*`)
| Action | Description |
|--------|-------------|
| `get-yaml-value` / `set-yaml-value` | Read and write YAML fields |
| `get-json-value` / `set-json-value` | Read and write JSON fields |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/text-processing)

---

## Third-Party Connector Integrations

### Jira (`dynatrace.jira:*`)
| Action | Description |
|--------|-------------|
| `jira-create-issue` | Create a Jira issue |
| `jira-update-issue` | Update an existing issue |
| `jira-add-comment` | Add a comment to an issue |
| `jira-transition-issue` | Change issue status |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/jira)

### Slack (`dynatrace.slack:*`)
| Action | Description |
|--------|-------------|
| `slack-send-message` | Send message to a channel |
| `slack-send-message-user` | Send a direct message to a user |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/slack)

### Microsoft Teams (`dynatrace.msteams:*`)
| Action | Description |
|--------|-------------|
| `send-message` | Send message (Markdown card or AdaptiveCard JSON) |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/microsoft-teams)

### Microsoft 365 (`dynatrace.microsoft365.connector:*`)
| Action | Description |
|--------|-------------|
| `send-email` | Send formatted email via Microsoft 365 (supports Markdown formatting, up to 10 recipients per field) |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/microsoft365)

### Microsoft Entra ID (`dynatrace.azure.connector:*`)
| Action | Description |
|--------|-------------|
| `get-groups` | List groups from Microsoft Entra ID |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/microsoft-entra-id)

### Microsoft Azure (`dynatrace.azure.connector:*`)
| Action | Description |
|--------|-------------|
| _(Azure resource operations)_ | Interact with Azure resources via the Azure Connector |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/azure)

### ServiceNow (`dynatrace.servicenow:*`)
| Action | Description |
|--------|-------------|
| `snow-create-incident` | Create an incident |
| `snow-search` / `snow-search-incidents` | Search records/incidents |
| `snow-comment-on-incident` | Add comment to an incident |
| `snow-update-record` | Update existing ServiceNow records |
| `snow-get-groups` | Fetch groups (team import/routing) |

> The ServiceNow connector also provides actions like resolve incident, create/update record, and general comment actions. Use the Workflows action picker to select the action and copy the exact `action` ID.
>
> ServiceNow workflow actions require granting Workflows the `app-settings:objects:read` permission (in addition to general Workflows permissions).
>
> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/service-now)

### AWS (`dynatrace.aws.connector:*`)
| Action | Description |
|--------|-------------|
| `s3-list-buckets` | List S3 buckets |
| `s3-put-object` | Upload objects to S3 |
| `lambda-invoke` | Invoke a Lambda function |
| `ec2-*` | EC2 operations (start, stop, describe, etc.) |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/aws)

### Red Hat Ansible (`dynatrace.redhat.ansible:*`)
| Action | Description |
|--------|-------------|
| `launch-job-template` | Launch an Automation Controller job template |
| `send-event-to-eda` | Send an event to Event-Driven Ansible |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/red-hat/redhat-ansible)

### Kubernetes (`dynatrace.kubernetes.connector:*`)
| Action | Description |
|--------|-------------|
| `patch-resource` | Patch K8s resources (annotations, labels, etc.) |
| `get-logs` | Retrieve pod/container logs |
| `delete` | Delete Kubernetes resources |
| _(additional)_ | Apply, get/list, rollout restart, wait — resembles `kubectl` operations |

> Exact action IDs can vary by connector version. Prefer selecting from the Workflows action picker and keep `metadata.dependencies.apps` in sync.
>
> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/kubernetes-automation)

### PagerDuty (`dynatrace.pagerduty:*`)
| Action | Description |
|--------|-------------|
| `create-incident` | Create a PagerDuty incident from a problem event |
| `list-on-calls` | List current on-call users and schedules |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/pagerduty)

### GitHub (`dynatrace.github:*`)
| Action | Description |
|--------|-------------|
| `get-content` | Read files from GitHub repositories |
| `create-or-replace-file` | Create or update files in GitHub repos |
| `create-pull-request` | Create GitHub pull requests with changes |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/github)

### GitLab (`dynatrace.gitlab:*`)
| Action | Description |
|--------|-------------|
| `create-file` | Create a new file in a new branch |
| `get-file` | Get a file from a repository |
| `update-file` | Update a file (creates a new branch) |
| `delete-file` | Delete a file (creates a new branch) |
| `create-merge-request` | Create a merge request |
| `get-merge-request` | Get a single merge request |
| `list-merge-requests` | List merge requests |
| `merge-merge-request` | Merge a merge request (with optional squash) |
| `update-merge-request` | Update an existing merge request |
| `create-merge-request-note` | Add a note to a merge request |
| `create-issue` | Create a new issue |
| `edit-issue` | Edit an existing issue |
| `list-issues` | List issues with filters |
| `get-pipeline-status` | Get pipeline status |
| `trigger-pipeline` | Trigger a new pipeline run |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/gitlab)

### Jenkins (`dynatrace.jenkins:*`)
| Action | Description |
|--------|-------------|
| `get-job-info` | Get status information about a Jenkins pipeline job |
| `trigger-build` | Trigger a Jenkins pipeline job (optionally await result) |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/jenkins)

### Snowflake (`dynatrace.snowflake:*`)
| Action | Description |
|--------|-------------|
| `execute-statement` | Execute a single SQL statement on Snowflake and return the result |
| `store-statement-result` | Execute a SQL statement and store the result directly in Grail (as bizevents or lookup data) |

> [Docs →](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions/snowflake)

---

## Important Notes

- **Action IDs shown above are illustrative examples** derived from documentation and samples in this repository. They may not match the exact IDs in your Dynatrace environment or version. Always use the **Workflows action picker** in the Dynatrace UI to confirm the correct action ID.
- **New connectors are added regularly** via the Dynatrace Hub. This file cannot keep pace with every release. Check the [official connectors page](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions) for the latest list.
- **App dependencies**: Every connector action requires the corresponding app listed in `metadata.dependencies.apps` in your workflow definition. The action picker in the UI handles this automatically; when authoring YAML manually, ensure you include the right app IDs.
