# DevOps Automation

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 4 templates demonstrate DevOps automation patterns — Kubernetes operations, configuration management, package synchronization, and team management.

## Templates

| Template | Trigger | What It Does | Integrations |
|----------|---------|--------------|--------------|
| **Auto-Annotate K8s Pods Based on Problem Events** | Problem Event (K8S_POD) | Queries Smartscape for affected pods; patches pod annotations with `metadata.dynatrace.com/problems` | Kubernetes |
| **Get and Set Image Version in YAML** | On-Demand | Reads image version from Pod YAML; updates to new version — template for GitOps config management | — |
| **Import Microsoft Entra ID Groups as Ownership Teams** | On-Demand (schedulable) | Fetches Microsoft Entra ID groups via Azure connector; imports as Dynatrace ownership teams | Microsoft Entra ID |
| **Package Version Sync** | On-Demand (schedulable) | Fetches `package.json` and `package-lock.json` from GitHub; syncs versions; creates PR with changes | GitHub |

## Key Patterns

### Kubernetes Resource Patching
Auto-annotate template uses `dynatrace.kubernetes.connector:patch-resource` to directly modify K8s resources — useful for tagging, labeling, and annotating based on Dynatrace events.

### JSON/YAML Manipulation
Image version and package sync templates use `get-yaml-value`/`set-yaml-value` and `get-json-value`/`set-json-value` actions for structured data manipulation inside workflows.

### GitHub Content Management
Package sync template uses `get-content` and `create-or-replace-file` GitHub actions to read, modify, and commit files — a GitOps automation pattern.

### Identity Sync
Entra ID template bridges identity provider groups to Dynatrace ownership — keeping team assignments in sync with the organization's directory.

## Key Learnings for AI Agents

1. **K8s connector for direct ops**: Use the Kubernetes connector for patching, annotating, and managing resources directly from workflows
2. **Structured data actions**: Use `get/set-yaml-value` and `get/set-json-value` for configuration file manipulation
3. **GitOps via GitHub connector**: Read, modify, and PR changes to Git repositories directly from workflows
4. **Ownership sync**: Import teams from identity providers to maintain consistent Dynatrace ownership
