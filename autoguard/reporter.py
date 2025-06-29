import json
import boto3
from integrations.slack_notifier import notify_slack
from integrations.webhook_notifier import send_webhook
from audit.logger import log_audit
from .config import SNS_TOPIC_ARN

class Reporter:
    def report(self, region_issues, label):
        summary = {region: len(issues) for region, issues in region_issues.items()}
        message = f"{label}\n\nSummary:\n{json.dumps(summary, indent=2)}"
        boto3.client('sns').publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject=label)
        notify_slack(message)
        send_webhook(message)
        log_audit(label, region_issues)
