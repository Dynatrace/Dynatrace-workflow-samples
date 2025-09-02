# Threat detection in cloud native environments using Dynatrace Workflows

* `kubernetes_service_account_unauthorized_access.yaml` - DQL query aiming to detect potentially compromised K8s service accounts. This sample is part of a comprehensive [documented use case](https://dt-url.net/en230wg). Additional technical specifications, system requirements, and prerequisite configurations are available in the official Dynatrace documentation.

* `instant-notification-for-critical-k8s-threat-detection-findings.yaml` - Workflow template that gets automatically triggered when new Kubernetes threat detection findings are generated, retrieves ownership information for impacted components and sends a notifications containing finding insights via Slack, Microsoft Teams, or email.

* `threat-detection-notification-sender.yaml` - A sample sub-workflow that handles notification delivery based on the provided input information object.
