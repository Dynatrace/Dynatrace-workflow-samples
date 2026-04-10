# Security

> **In-product templates — reference only.** See [parent README](../README.md) for details.

This category contains security-specific templates that don't use Dynatrace Intelligence. For AI-powered security workflows, see [Dynatrace Intelligence Agents](../dynatrace-intelligence-agents/) (Security Association Agent, Security Insights Report Agent, Vulnerability Verification Agent).

## Templates

| Template | Trigger | What It Does | Integrations |
|----------|---------|--------------|--------------|
| **Threat Triage Agent** | Data template (no executable trigger) | Contains threat intelligence reference data: CVE details, indicators (URLs, domains, file hashes), MITRE ATT&CK techniques | Threat Intelligence (input data) |

## Key Patterns

### Threat Intelligence Data Structure
The Threat Triage template demonstrates how to structure threat intelligence data within a workflow — CVE entries, IOCs (indicators of compromise), and MITRE ATT&CK mappings as structured task inputs.

## Key Learnings for AI Agents

1. **Data-only templates**: Workflows can serve as structured data containers for reference material
2. **Threat intel structure**: Use CVE IDs, IOC types (URL, domain, hash), and ATT&CK technique IDs as standardized fields
