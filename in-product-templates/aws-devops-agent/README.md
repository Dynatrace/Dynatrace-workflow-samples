# AWS DevOps Agent — Multi-Workflow Orchestration

> **In-product templates — reference only.** See [parent README](../README.md) for details.

These 6 templates form a **complete end-to-end orchestration pipeline** that bridges Dynatrace problem detection with the AWS DevOps Agent for automated investigation and mitigation of AWS-related issues. They must be deployed together.

## Pipeline Architecture

```
Problem Event                                    AWS DevOps Agent Cloud API
     │                                                    ▲    │
     ▼                                                    │    ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 01 Queue │───▶│ 02 Poll  │───▶│ 03 Check │───▶│ 04 Inv.  │    │ 05 Comp. │───▶│ 06 Mitig.│
│ Problems │    │ Dispatch │    │ Eligible │    │ Response │    │ Response │    │ Response │
│          │    │ (1 min)  │    │ + Invoke │    │ Handler  │    │ Handler  │    │ Handler  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
 bizevent        DQL + sub-      topology         event           event           event
 trigger         workflow        walk             trigger         trigger         trigger
```

## Templates (in execution order)

| # | Template | Trigger | Role |
|---|----------|---------|------|
| 01 | Queue Potentially AWS-Relevant Problems | Problem Event (Error/Slowdown/Availability) | Ingests problem as `readyForAnalysis` bizevent |
| 02 | Dispatch Pending Analysis | Schedule (every 1 min) | Polls for unprocessed events; invokes workflow 03 for each |
| 03 | Check Eligibility & Invoke AWS DevOps Agent | Sub-workflow (from 02) | Topology walk: services → databases → Lambda/RDS/EC2; if AWS resources found, calls AWS DevOps Agent API with HMAC signature |
| 04 | Handle Investigation Responses | Event (investigation_summary journal) | Attaches investigation findings (symptoms, gaps) to problem as custom annotation |
| 05 | Handle Investigation Completed | Event (TASK_UPDATED + COMPLETED) | Checks mitigation not yet requested; invokes AWS agent mitigation API |
| 06 | Handle Mitigation Responses | Event (mitigation_summary journal) | Attaches mitigation plan (action, reasoning, steps) to problem annotation |

## Key Patterns

### Bizevent-Based Queueing
Workflow 01 uses `ingestbizevent` to create a durable event queue. Workflow 02 polls this queue via DQL, enabling decoupled, reliable processing.

### Topology-Based AWS Relevance Check
Workflow 03 performs a multi-hop Smartscape traversal: problem entities → services → databases → AWS resources (Lambda, RDS, EC2). Only problems with sufficient AWS resource association proceed.

### HMAC-Authenticated Webhook Calls
Workflows 03 and 05 call the AWS DevOps Agent Cloud API using HTTP requests with HMAC signature authentication — a pattern for secure external agent invocation.

### Event-Driven Response Handling
Workflows 04, 05, and 06 use custom event triggers listening for specific journal record types, demonstrating asynchronous multi-workflow coordination.

### Custom Problem Annotations
Investigation and mitigation results are attached to Dynatrace problems as custom annotations, keeping all context in one place.

## Key Learnings for AI Agents

1. **Multi-workflow orchestration**: Use bizevents for durable event queues between workflows
2. **Topology walks**: Chain DQL queries to traverse Smartscape relationships for relevance scoring
3. **External agent integration**: HMAC-signed webhooks for secure API calls to external agent services
4. **Event-driven pipelines**: Use custom event triggers to coordinate async multi-workflow flows
5. **Problem enrichment**: Attach structured findings to problems via custom annotations and troubleshooting notebooks
