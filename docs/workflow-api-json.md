# Format 2: API Format (JSON)

Used for programmatic workflow management via the Automation API.

## API Endpoints

- **GET** `/platform/automation/v1/workflows` - List all workflows
- **GET** `/platform/automation/v1/workflows/{id}` - Get specific workflow
- **POST** `/platform/automation/v1/workflows` - Create workflow
- **PUT** `/platform/automation/v1/workflows/{id}` - Update workflow
- **DELETE** `/platform/automation/v1/workflows/{id}` - Delete workflow

## Structure

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

## Differences from YAML Template Format

1. **No metadata section** - Dependencies managed separately
2. **Different field names**:
   - `isPrivate` instead of included in trigger
   - `triggerType` as top-level field
3. **Tasks as object** - Tasks are key-value pairs, not array
4. **String escaping** - Jinja2 expressions need proper JSON escaping

## Example API Request

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
