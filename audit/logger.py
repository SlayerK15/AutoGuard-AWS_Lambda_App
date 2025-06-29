import boto3, json
from datetime import datetime
from autoguard.config import AUDIT_S3_BUCKET

def log_audit(label, region_issues):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "label": label,
        "data": region_issues
    }
    key = f"audit/{datetime.utcnow().isoformat()}_{label}.json"
    boto3.client('s3').put_object(Bucket=AUDIT_S3_BUCKET, Key=key, Body=json.dumps(entry))
