# AIDLC Outcome Evaluation Agent

Agentic, non-blocking quality gate workflow for the **AI-native Software Delivery Lifecycle (AIDLC)**. Evaluates deployments across six quality dimensions, runs a Site Reliability Guardian validation, synthesizes findings with Dynatrace Intelligence, and creates a structured GitHub issue with the evaluation report.

## Architecture

```
CI/CD Pipeline
     │
     │  SDLC event: deployment.finished
     ▼
┌─────────────────────────────────────────────────────────────┐
│  AIDLC Outcome Evaluation Agent (Dynatrace Workflow)        │
│                                                             │
│  ┌─────────────────────┐                                    │
│  │ 1. Prepare Context  │ ← deployment metadata from event   │
│  └─────────┬───────────┘                                    │
│            │                                                │
│  ┌─────────┴──────────────────────────────────────────┐     │
│  │ 2. Parallel Data Collection (6 DQL streams)        │     │
│  │                                                    │     │
│  │  ┌──────────┐ ┌─────────-─┐ ┌───────────┐          │     │
│  │  │ Golden   │ │Reliability│ │ Resource  │          │     │
│  │  │ Signals  │ │ (DAVIS)   │ │ Metrics   │          │     │
│  │  └──────────┘ └────────-──┘ └───────────┘          │     │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐           │     │
│  │  │ Security │ │  Error   │ │Dependency │           │     │
│  │  │ Findings │ │ Patterns │ │  Health   │           │     │
│  │  └──────────┘ └──────────┘ └───────────┘           │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                     │
│  ┌────────────────────┴──────────┐                          │
│  │ 3. SRG Validation             │ ← formal SLO evaluation  │
│  └────────────────────┬──────────┘                          │
│                       │                                     │
│  ┌────────────────────┴──────────┐                          │
│  │ 4. Dynatrace Intelligence     │ ← AI-synthesized verdict │
│  │    Outcome Analysis           │                          │
│  └────────────────────┬──────────┘                          │
│                       │                                     │
│  ┌────────────────────┴──────────┐                          │
│  │ 5. Synthesize Findings        │ ← structured report      │
│  └────────────────────┬──────────┘                          │
│                       │                                     │
│  ┌──────────┬─────────┴──────────┬──────────┐               │
│  │ GitHub   │  Bizevent Audit    │ Ownership │              │
│  │ Issue    │  Trail             │ Lookup    │              │
│  └──────────┘  └─────────────────┘ └─────────┘              │
│                                                             │
│  ┌──────────────────────────────────────────┐               │
│  │ 8. Notify (Slack/Teams) — optional       │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
GitHub Issue: structured evaluation report
Grail: aidlc.evaluation.completed bizevent (audit trail)
```

## AIDLC Mapping

This workflow serves two AIDLC phases:

| AIDLC Phase | Role in this workflow |
|---|---|
| **Phase 4 — Delivery & Release Gate** | SRG validation + performance/reliability checks produce verdict |
| **Phase 5 — Progressive Rollout Verification** | Post-deployment evaluation across all 6 dimensions |

Findings classify into the **3-Lane Remediation** model:
- **Lane A (Infrastructure)**: Resource exhaustion, scaling issues, capacity problems
- **Lane B (Code)**: Regressions, new error patterns, response time degradation
- **Lane C (Design)**: Systemic behavior mismatch, observability gaps, architectural issues

## Quality Dimensions

### 1. Performance (Golden Signals)
Compares post-deployment RED metrics against a pre-deployment baseline:
- P95/P99 response time regression (WARNING > 5%, FAIL > 15%)
- Error rate increase (WARNING > 0.5%, FAIL > 2%)
- Throughput drop (WARNING > 10%)

**DQL sources**: `dt.service.request.count`, `dt.service.request.failure_count`, `dt.service.request.response_time`

### 2. Reliability
- Active DAVIS problems on the service → FAIL
- SRG validation failure → FAIL
- New problems within evaluation window → WARNING

**DQL sources**: `events` (DAVIS_PROBLEM), SRG validation result

### 3. Resource Efficiency / Cost
- CPU usage > 80% of limits → WARNING, > 95% → FAIL
- Memory usage > 85% of limits → WARNING, > 95% → FAIL
- OOM kills → FAIL
- Container restarts → WARNING
- CPU < 20% of requests → INFO (over-provisioned, cost opportunity)

**DQL sources**: `dt.kubernetes.container.cpu_usage`, `memory_working_set`, `requests_*`, `limits_*`, `restarts`, `oom_kills`

### 4. Security
- CRITICAL vulnerability → FAIL
- HIGH vulnerability → WARNING
- New detection findings since deployment → WARNING

**DQL sources**: `events` (VULNERABILITY_STATE_REPORT_EVENT, DETECTION_FINDING)

### 5. Observability Completeness
- No trace data → WARNING (blind spot)
- No log data → WARNING (blind spot)
- Empty metric queries → INFO (instrumentation gap)

### 6. Dependency Health
- Downstream error rate > 1% → WARNING
- Downstream response time degradation > 20% → WARNING
- Dependencies discovered via Smartscape topology

**DQL sources**: `dt.entity.service` (calls relationship), downstream RED metrics

## Setup

### Prerequisites

- Dynatrace environment with Grail enabled
- AutomationEngine (Workflows) installed
- Site Reliability Guardian app installed
- Services instrumented with OneAgent or OpenTelemetry
- CI/CD pipeline that can send SDLC events

### Step 1: Create an SRG Guardian

Create a guardian for your service with objectives covering your key SLOs. Example objectives:

| Objective | DQL Query | Threshold |
|-----------|-----------|-----------|
| P95 Response Time | `timeseries val = percentile(dt.service.request.response_time, 95), filter: dt.entity.service == "SERVICE-XXX" \| fields max = arrayMax(val)` | ≤ 500ms (warning: 300ms) |
| Error Rate | `timeseries { err = sum(dt.service.request.failure_count), total = sum(dt.service.request.count) }, filter: dt.entity.service == "SERVICE-XXX" \| fields rate = 100.0 * arraySum(err) / arraySum(total)` | ≤ 1% (warning: 0.5%) |
| Availability | `timeseries val = avg(dt.service.request.success_count) / avg(dt.service.request.count) * 100, filter: dt.entity.service == "SERVICE-XXX" \| fields min = arrayMin(val)` | ≥ 99.5% (warning: 99.9%) |

### Step 2: Configure the Workflow

1. Import the workflow template
2. Set the `objectId` in `run_srg_validation` to your guardian ID
3. Set the GitHub repository in `create_github_issue` URL
4. Store your GitHub PAT as a Dynatrace secret named `github_pat`
5. (Optional) Uncomment and configure the Slack/Teams notification task

### Step 3: Send SDLC Events from CI/CD

Your pipeline must send a `deployment.finished` event after each deployment:

```bash
curl -X POST \
  "https://${DT_ENV}.live.dynatrace.com/platform/ingest/v1/events.sdlc" \
  -H "Authorization: Api-Token ${DT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"event.type\": \"deployment.finished\",
    \"dt.entity.service\": \"${SERVICE_ENTITY_ID}\",
    \"service.name\": \"${SERVICE_NAME}\",
    \"service.namespace\": \"${K8S_NAMESPACE}\",
    \"deployment.id\": \"${DEPLOY_ID}\",
    \"deployment.version\": \"${VERSION}\",
    \"deployment.environment\": \"${ENV}\",
    \"vcs.repository.url\": \"${REPO_URL}\",
    \"vcs.ref.head.name\": \"${GIT_BRANCH}\",
    \"vcs.ref.revision\": \"${GIT_SHA}\"
  }"
```

**GitHub Actions example:**

```yaml
- name: Notify Dynatrace of deployment
  run: |
    curl -X POST \
      "${{ secrets.DT_URL }}/platform/ingest/v1/events.sdlc" \
      -H "Authorization: Api-Token ${{ secrets.DT_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{
        "event.type": "deployment.finished",
        "dt.entity.service": "'"${{ vars.SERVICE_ENTITY_ID }}"'",
        "service.name": "'"${{ github.event.repository.name }}"'",
        "deployment.id": "deploy-${{ github.run_id }}",
        "deployment.version": "'"${{ github.sha }}"'",
        "deployment.environment": "production",
        "vcs.repository.url": "'"${{ github.server_url }}/${{ github.repository }}"'",
        "vcs.ref.head.name": "'"${{ github.ref_name }}"'",
        "vcs.ref.revision": "'"${{ github.sha }}"'"
      }'
```

## Querying Evaluation History

The workflow emits `aidlc.evaluation.completed` business events that you can query in Grail:

```dql
-- All evaluations for a service
fetch bizevents
| filter event.type == "aidlc.evaluation.completed"
| filter data.service.name == "my-service"
| fields timestamp, data.deployment.version, data.deployment.environment,
         data.evaluation.verdict, data.evaluation.confidence,
         data.evaluation.srg.status, data.evaluation.github.issue.url
| sort timestamp desc

-- Evaluation pass rate over time
fetch bizevents, from:now()-30d
| filter event.type == "aidlc.evaluation.completed"
| summarize total = count(),
            passed = countIf(data.evaluation.verdict == "PASS"),
            warned = countIf(data.evaluation.verdict == "WARNING"),
            failed = countIf(data.evaluation.verdict == "FAIL"),
            by: { data.service.name }
| fieldsAdd passRate = 100.0 * passed / total

-- Failed evaluations requiring attention
fetch bizevents, from:now()-7d
| filter event.type == "aidlc.evaluation.completed"
| filter data.evaluation.verdict == "FAIL"
| fields timestamp, data.service.name, data.deployment.version,
         data.evaluation.github.issue.url
| sort timestamp desc
```

## Customization

### Adjusting Evaluation Window

The default evaluation window is 30 minutes post-deployment with a 1-hour baseline. Adjust in `prepare_evaluation_context`:

```javascript
const evaluationWindowMinutes = 30;  // post-deployment observation
const baselineWindowHours = 1;       // pre-deployment baseline
```

For services with slow warm-up, increase to 60 minutes. For high-traffic services, 15 minutes may suffice.

### Adding Custom Quality Dimensions

Add new DQL collection tasks in Phase 2 (parallel with existing collectors). Wire them as predecessors to `run_srg_validation`, then reference their results in the `analyze_outcomes` prompt.

Example — adding a business KPI check:

```yaml
collect_business_kpis:
  name: collect_business_kpis
  action: dynatrace.automations:execute-dql-query
  input:
    query: |-
      fetch bizevents, from:now()-30m
      | filter event.type == "com.myapp.order.completed"
      | summarize orderCount = count(),
                  avgOrderValue = avg(order.value),
                  conversionRate = countIf(order.status == "SUCCESS") / count() * 100
  position:
    x: 4
    y: 2
  conditions:
    states:
      prepare_evaluation_context: OK
  predecessors:
  - prepare_evaluation_context
```

### Non-Kubernetes Environments

The resource metrics task targets Kubernetes workloads. For VM-based deployments, replace with host metrics:

```dql
timeseries {
  cpuUsage = avg(dt.host.cpu.usage),
  memUsage = avg(dt.host.memory.usage),
  diskUsage = avg(dt.host.disk.usage)
}, from: now()-1h, interval: 5m,
filter: in(dt.entity.host, array("HOST-XXX"))
```

## Limitations

- **GitHub issue creation** uses `http-function` (REST API) since there's no native GitHub issue action. Token stored as Dynatrace secret.
- **SRG guardian** must be pre-configured — the workflow validates against an existing guardian, it doesn't create objectives dynamically.
- **Baseline comparison** uses a simple time window (before/after deployment). For more sophisticated statistical comparison, extend the JavaScript tasks.
- **Non-blocking by design** — this workflow creates advisory findings, not hard deployment gates. To make it blocking, integrate with your CD tool's gate API.

## Files

| File | Description |
|------|-------------|
| `aidlc-outcome-evaluation-agent.workflow-template.yaml` | The Dynatrace workflow template |
| `aidlc-outcome-evaluation-agent.md` | This documentation |
