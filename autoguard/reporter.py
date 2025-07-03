import json
import boto3
from integrations.slack_notifier import notify_slack
from integrations.webhook_notifier import send_webhook
from audit.logger import log_audit
from .config import SNS_TOPIC_ARN
from .report_utils import generate_web_report

class Reporter:
    def report(self, region_issues, label):
        summary = {
            f"{acct}:{region}": len(issues)
            for acct, regions in region_issues.items()
            for region, issues in regions.items()
        }
        report_url = generate_web_report(region_issues, label)
        message = (
            f"{label}\n\nSummary:\n{json.dumps(summary, indent=2)}\n\n"
            f"Detailed report: {report_url}"
        )
        boto3.client("sns").publish(
            TopicArn=SNS_TOPIC_ARN, Message=message, Subject=label
        )
        notify_slack(message)
        send_webhook(message)
        log_audit(label, region_issues)
