# dtctl — Dynatrace CLI for Workflow Management

`dtctl` is the official kubectl-style CLI for Dynatrace. It provides **workflow validation, deployment, execution, and monitoring** — making it essential for development and CI/CD workflows.

## Installation

```bash
# macOS
brew install dynatrace-oss/tap/dtctl

# Linux
tar -xzf dtctl_linux_amd64.tar.gz && sudo mv dtctl /usr/local/bin/

# Windows — download from https://github.com/dynatrace-oss/dtctl/releases

# Verify
dtctl version
```

## Authentication & Context

```bash
# Login to an environment
dtctl auth login --context my-env --environment "https://<env-id>.apps.dynatrace.com"

# Verify connectivity
dtctl doctor
dtctl ctx
dtctl auth whoami

# Switch between environments
dtctl config get-contexts
dtctl config use-context <name>
```

## Workflow Validation (Dry-Run)

**This is the recommended way to validate workflows before deployment:**

```bash
# Validate API-format workflow (flat YAML with title/tasks at top level)
dtctl apply -f workflow.yaml --dry-run --plain

# Validate a .workflow-template.yaml file (has metadata/workflow wrapper — extract first)
yq '.workflow' my-template.workflow-template.yaml | dtctl apply -f - --dry-run --plain

# Show what would change
dtctl diff -f workflow.yaml

# Preview with diff details
dtctl apply -f workflow.yaml --show-diff --plain
```

**Safe deployment pattern:**
```bash
dtctl apply -f workflow.yaml --dry-run --plain    # 1. Validate
dtctl diff -f workflow.yaml                        # 2. Review changes
dtctl apply -f workflow.yaml --plain               # 3. Deploy
```

## Important: Template Format vs. API Format

**`dtctl` expects the API format** (flat structure with `title`, `tasks`, `trigger` at top level).
The `.workflow-template.yaml` files in this repository use the **template format** (with a `metadata`/`workflow` wrapper for UI import). If you pass a template file directly to `dtctl apply`, it will be misinterpreted as a dashboard.

**To validate template files with `dtctl`**, extract the `workflow` section first:

```bash
# Extract workflow section and validate via dtctl (requires yq)
yq '.workflow' my-template.workflow-template.yaml | dtctl apply -f - --dry-run --plain

# Or use a temporary file
yq '.workflow' my-template.workflow-template.yaml > /tmp/wf.yaml && \
  dtctl apply -f /tmp/wf.yaml --dry-run --plain
```

## Validate Templates

To verify templates from `in-product-templates/` or `samples/` against a live environment:

```bash
# Validate a single template (extract workflow section first)
yq '.workflow' in-product-templates/dynatrace-intelligence-agents/alert-reduction-agent.workflow-template.yaml \
  | dtctl apply -f - --dry-run --plain

# Validate all templates in a category
for f in in-product-templates/dynatrace-intelligence-agents/*.yaml; do
  echo "=== $f ===" && yq '.workflow' "$f" | dtctl apply -f - --dry-run --plain 2>&1 | tail -1
done

# Validate entire directory tree
find in-product-templates samples -name "*.workflow-template.yaml" -exec sh -c \
  'echo "=== {} ===" && yq ".workflow" "{}" | dtctl apply -f - --dry-run --plain 2>&1 | tail -1' \;
```

> **Alternative without yq** (using Python):
> ```bash
> python3 -c "import yaml,sys,tempfile,os; d=yaml.safe_load(open(sys.argv[1])); \
>   f=tempfile.NamedTemporaryFile('w',suffix='.yaml',delete=False); \
>   yaml.dump(d['workflow'],f); f.close(); print(f.name)" my-template.yaml \
>   | xargs -I{} dtctl apply -f {} --dry-run --plain
> ```

## DQL Validation

Validate DQL queries embedded in workflows before operationalizing them:

```bash
# Verify query syntax
dtctl verify query "fetch logs | limit 10" --fail-on-warn

# Execute to test results
dtctl query "fetch logs | filter loglevel == \"ERROR\" | limit 10" -o json --plain

# From file with variables
dtctl query -f query.dql --set host=HOST-123 --set timerange=2h -o json --plain
```

## Workflow Lifecycle Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `dtctl get workflows` | List workflows | `dtctl get wf --mine -o json --plain` |
| `dtctl describe workflow` | Show details | `dtctl describe wf <id> -o yaml` |
| `dtctl apply -f` | Create/update | `dtctl apply -f workflow.yaml --plain` |
| `dtctl diff -f` | Compare versions | `dtctl diff -f workflow.yaml` |
| `dtctl exec workflow` | Run workflow | `dtctl exec wf <id> --wait --timeout 10m` |
| `dtctl logs` | View execution logs | `dtctl logs wfe <id> --follow` |
| `dtctl history` | Version history | `dtctl history wf <id>` |
| `dtctl delete workflow` | Remove | `dtctl delete wf <id> --plain` |

Resource aliases: `workflow` → `wf`, `workflow-execution` → `wfe`

## Template Variables (Go Template Syntax)

dtctl supports Go template variables for parameterized deployment:

```yaml
# In workflow YAML
title: "{{.environment}} Deployment"
owner: "{{.team}}"
trigger:
  schedule:
    cron: '{{.schedule | default "0 0 * * *"}}'
```

```bash
# Deploy with variables
dtctl apply -f workflow.yaml --set environment=prod --set team=platform --plain
```

## Output Formats

```bash
dtctl <command> -o json --plain    # JSON (best for parsing)
dtctl <command> -o yaml --plain    # YAML
dtctl <command> -o csv --plain     # CSV
dtctl <command> -o table           # Human-readable (default)
dtctl <command> --agent            # Optimized for AI agents (= -o json --plain)
```

## Development Workflow (Recommended)

```bash
# 1. Set up context
dtctl auth login --context dev --environment "https://env.apps.dynatrace.com"
dtctl doctor

# 2. Validate DQL queries first
dtctl verify query "fetch logs | filter ..." --fail-on-warn

# 3. Validate workflow
#    For API-format YAML (flat structure):
dtctl apply -f my-workflow.yaml --dry-run --plain
#    For .workflow-template.yaml files (metadata/workflow wrapper):
yq '.workflow' my-template.workflow-template.yaml | dtctl apply -f - --dry-run --plain

# 4. Deploy
dtctl apply -f my-workflow.yaml --plain

# 5. Test execution
dtctl exec wf <id> --wait --timeout 5m --plain

# 6. Check results
dtctl logs wfe <execution-id> --follow
```
