# AutoGuard AWS Scanner & Remediation

Scans AWS environments across regions for misconfigured, idle, or risky resources. Applies automatic remediation and sends alerts via SNS, Slack, and custom Webhooks.

## Deployment (AWS Lambda)

- Zip and upload to AWS Lambda
- Set up environment variables
- Trigger periodically via CloudWatch events

## Environment Variables
- `SNS_TOPIC_ARN`
- `SLACK_WEBHOOK_URL`
- `WEBHOOK_URL`
- `AUDIT_S3_BUCKET`
- `WHITELIST`

## Run Locally
```bash
pip install -r requirements.txt
python lambda_handler.py
