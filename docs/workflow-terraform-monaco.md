# Format 3: Terraform & Monaco Configuration-as-Code

## Terraform

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
  "schemaVersion": 4,
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
