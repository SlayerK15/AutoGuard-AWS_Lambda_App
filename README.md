# AutoGuard - AWS Lambda Security Scanner

**AutoGuard** is a serverless application that scans your AWS environment for security issues, attempts simple remediation, and emails you a report. It runs entirely in AWS Lambda so there are no servers to manage.

## Features

- **Multi-Resource Scanning** for EC2, S3, IAM, cost anomalies and basic compliance.
- **Auto-Remediation** of common problems (public S3 buckets, unused IAM users, idle NAT gateways, etc.).
- **Organization-wide Support** with optional cross-account scanning.
- **Immediate Results** – the `/scan` API returns a JSON summary when the scan finishes.
- **Detailed Reporting** uploaded to S3 and sent through SNS email. A dashboard page lets you view any report by URL.
- **Slack & Custom Webhook Alerts** via environment variables.
- **Scheduled Scans** using CloudWatch Events.
- **AI-based Monitoring** detects anomalies and automatically scales the Lambda concurrency.

## How It Works

1. **Trigger a Scan:** Send a POST request to the `/scan` endpoint or click **Run Scan** in `static/index.html`.
2. **Scanning:** Lambda invokes modular handlers that look for misconfigurations, compliance issues and unused resources across all selected accounts and regions.
3. **Auto-Remediation:** The fixer module attempts to remedy issues such as public S3 buckets or idle EC2 instances.
4. **Reporting:** A summary is returned in the HTTP response. A full HTML report is generated and stored in S3, then an email is sent through SNS with the link. Optional Slack and webhook notifications are also sent.
5. **Audit Logs & AI:** Every scan is logged to S3. Issue counts are analysed; if anomalies are found the Lambda concurrency is scaled up automatically.

The architecture is completely provisioned through CloudFormation. A helper script `scripts/deploy_stack.py` creates the stack with minimal interaction, including the API Gateway, Lambda function, SNS topic and CloudWatch Events rule.

![Architecture Diagram](assets/image.svg)

## Quick Start

1. **Deploy** using the helper script (requires AWS credentials configured):
   ```bash
   python3 scripts/deploy_stack.py you@example.com
   ```
   This creates the stack defined in `Cloudformation.yml` and subscribes the specified email to SNS notifications.
2. **Update** the `API_ENDPOINT` variable in `static/index.html` with the URL output by the stack.
3. **Run a Scan** either with `curl`:
   ```bash
   curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/scan
   ```
   or open `static/index.html` in your browser and click **Run Scan**.
4. **Check Your Email** for the detailed report, or open `static/dashboard.html` and paste the S3 URL provided in the email.

## Environment Variables

The Lambda function reads the following variables (configured automatically by the template):

| Variable            | Description                                     |
|---------------------|-------------------------------------------------|
| `SNS_TOPIC_ARN`     | SNS topic used for email notifications          |
| `AUDIT_S3_BUCKET`   | S3 bucket for audit logs and HTML reports       |
| `SLACK_WEBHOOK_URL` | Optional Slack incoming webhook for alerts      |
| `WEBHOOK_URL`       | Optional generic webhook for alerts             |
| `TARGET_ACCOUNTS`   | Comma-separated account IDs for multi-account   |
| `ORGANIZATION_WIDE` | `true` to scan all accounts in the organization |
| `ORG_ROLE_NAME`     | IAM role name for cross-account access          |

A sample `.env` file is included for local testing.

## Project Layout

```
autoguard-aws_lambda_app/
├── autoguard/            # scanning, fixing and reporting modules
├── handlers/             # resource-specific handlers
├── ai/                   # anomaly detection utilities
├── audit/                # audit log helper
├── integrations/         # Slack and generic webhook modules
├── static/               # minimal web UI and dashboard
├── scripts/              # deployment helper
├── Cloudformation.yml    # infrastructure template
└── lambda_handler.py     # Lambda entry point
```

## Development

1. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Lint/compile:
   ```bash
   python3 -m py_compile $(git ls-files '*.py')
   ```
3. Run tests (none yet):
   ```bash
   pytest -q
   ```

## Feature Status

| Feature/Idea                                                         | Status     |
|----------------------------------------------------------------------|-----------|
| Core AWS resource scanning (EC2, S3, IAM, cost, compliance)          | ✅        |
| Modular handler architecture                                         | ✅        |
| Auto-remediation for common issues                                   | ✅        |
| Audit logging and reporting with email via SNS                       | ✅        |
| Automated deployment with CloudFormation                             | ✅        |
| Static webpage and minimal UI to trigger scans                       | ✅        |
| Multi-account and organization-wide scanning                         | ✅        |
| Enhanced security and compliance checks (partial CIS)                | ✅        |
| SNS template with detailed web report                                | ✅        |
| Web dashboard for extended reporting                                 | ✅        |
| AI integration for monitoring and auto-scaling                       | ✅ basic  |
| Slack and webhook alert integrations                                 | ✅        |
| Built-in scheduler via CloudWatch Events                             | ✅        |
| Immediate HTTP scan results                                          | ✅        |

AutoGuard aims to provide hands-off, always-on security scanning for your AWS accounts. Feel free to extend the handlers or reporting modules to customize the tool for your environment.

