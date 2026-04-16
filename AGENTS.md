# Dynatrace Workflows - AI Assistant Instructions

Guidelines for creating syntactically correct Dynatrace Workflows. For AI coding assistants (GitHub Copilot, Cursor, Claude Code, Kiro).

**Important**: There are **three distinct formats**. **Never mix them**:

1. **Workflow Templates (YAML)** — UI import/export → [docs/workflow-templates-yaml.md](docs/workflow-templates-yaml.md)
2. **API Format (JSON)** — Programmatic management → [docs/workflow-api-json.md](docs/workflow-api-json.md)
3. **Terraform/Monaco** — Configuration-as-Code → [docs/workflow-terraform-monaco.md](docs/workflow-terraform-monaco.md)

## Detail Documents

Read these incrementally based on what you need:

| Document | When to read |
|----------|-------------|
| [docs/workflow-templates-yaml.md](docs/workflow-templates-yaml.md) | Creating/editing YAML workflow templates (most common) |
| [docs/workflow-api-json.md](docs/workflow-api-json.md) | Working with the Automation API |
| [docs/workflow-terraform-monaco.md](docs/workflow-terraform-monaco.md) | Terraform or Monaco deployments |
| [docs/actions-catalog.md](docs/actions-catalog.md) | Sample-oriented action reference (**not authoritative** — always verify against [official docs](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions) and the Workflows action picker) |
| [docs/workflow-patterns.md](docs/workflow-patterns.md) | Common workflow patterns (alerts, reports, remediation) |
| [docs/dtctl-cli.md](docs/dtctl-cli.md) | Validating, deploying, or managing workflows via CLI |
| [docs/in-product-templates.md](docs/in-product-templates.md) | Reference patterns from 31 production templates |

## Format Decision Guide

**Use Workflow Templates (YAML)** when: UI import/export, sharing examples, prototyping, simplest format.

**Use API Format (JSON)** when: programmatic management, CI/CD integration, bulk operations.

**Use Terraform** when: Infrastructure-as-Code, version control, multi-environment, state management.

---

## Pull Request Review Checklist

### Workflow Syntax
- [ ] Correct format used (YAML template, API JSON, or Terraform — never mixed)
- [ ] `schemaVersion` is 3
- [ ] Valid YAML/JSON syntax
- [ ] `name` field inside task matches the task key
- [ ] All predecessor tasks are defined
- [ ] Action names follow `app:action` pattern (e.g., `dynatrace.automations:execute-dql-query`)

### Security
- [ ] No hardcoded secrets — use `{{ secret('secret_name') }}`
- [ ] External credentials stored in Dynatrace connections
- [ ] No internal/private URLs in HTTP actions

### Quality
- [ ] Meaningful task names (e.g., `fetch_security_logs` not `task1`)
- [ ] Every task has a description
- [ ] Conditions check task states before proceeding
- [ ] All required apps listed in `metadata.dependencies`
- [ ] Templates use `wftpl_*.yaml` naming

### DQL Queries
- [ ] Valid DQL syntax
- [ ] Appropriate time ranges (not unbounded)
- [ ] Includes necessary filters
- [ ] Large queries include `| limit N` or aggregation

### Jinja2 Expressions
- [ ] `{{ }}` for values, `{% %}` for logic
- [ ] `event()`, `result()`, `execution()` used correctly
- [ ] Quotes escaped correctly in nested expressions
- [ ] `withItems` loops use `_.item` or named variable

---

## Generation Checklist

When generating a Dynatrace Workflow:

- [ ] Determine the correct format (Template YAML, API JSON, or Terraform)
- [ ] Never mix formats
- [ ] Include all required metadata/dependencies
- [ ] Use correct action names from the [actions catalog](docs/actions-catalog.md)
- [ ] Include proper task predecessors for sequencing
- [ ] Add conditions where appropriate
- [ ] Use Jinja2 expressions correctly
- [ ] Include meaningful task names and descriptions
- [ ] Set appropriate trigger configuration
- [ ] Validate `schemaVersion` is 3
- [ ] No secrets or tokens in the code
- [ ] Test DQL queries separately first
- [ ] Follow the [patterns](docs/workflow-patterns.md) from existing samples

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task always skipped | Check predecessor states and custom conditions |
| DQL returns no results | Verify query syntax and time range |
| JavaScript task fails | Check syntax errors, missing imports, async/await |
| Expressions not resolving | Verify Jinja2 syntax and task/event references |
| Connection not found | Ensure connection ID is correct and active |

## File Naming

- **Templates**: `wftpl_descriptive_name.yaml`
- **API Format**: `descriptive_name.json`
- **Terraform**: `workflow_name.tf`

## Resources

- [Dynatrace Workflows Documentation](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows)
- [Actions Catalog](https://docs.dynatrace.com/docs/analyze-explore-automate/workflows/actions)
- [DQL Documentation](https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language)
- [Terraform Provider](https://registry.terraform.io/providers/dynatrace-oss/dynatrace/latest/docs)
- [`samples/`](samples/) — Workflow examples in this repository
- [`in-product-templates/`](in-product-templates/) — 31 categorized production templates
