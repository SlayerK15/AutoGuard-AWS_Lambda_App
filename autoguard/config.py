import os

ALL_REGIONS = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "eu-west-1", "eu-west-2", "eu-central-1", "ap-south-1"
]
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AUDIT_S3_BUCKET = os.getenv("AUDIT_S3_BUCKET")
WHITELIST = os.getenv("WHITELIST", "").split(",")
