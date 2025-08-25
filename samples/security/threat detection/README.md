# Threat detection in cloud native environments using Dynatrace Workflows

* `kubernetes_service_account_unauthorized_access.yaml` - DQL query aiming to detect potentially compromised K8s service accounts. This sample is part of a comprehensive [documented use case](https://dt-url.net/en230wg). Additional technical specifications, system requirements, and prerequisite configurations are available in the official Dynatrace documentation.

* `send-notifications-for-critical-threat-detection-findings.yaml` - sample workflow template that gets automatically triggered upon new threat detection findings are fired, retrieves impacted component ownership information and triggers notifications over Slack, MS Teams or email.
    * `threat-detection-finding-notification-sender.yaml` - sample sub-workflow that implements the notification forwarding based on the input information object.
