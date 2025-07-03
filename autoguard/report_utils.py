from datetime import datetime
import boto3
import json
from .config import AUDIT_S3_BUCKET

def generate_web_report(region_issues, label):
    """Create an HTML report in S3 and return its URL."""
    html = ["<html><body>", f"<h1>{label}</h1>"]
    for account, regions in region_issues.items():
        html.append(f"<h2>Account {account}</h2>")
        for region, issues in regions.items():
            html.append(f"<h3>Region {region}</h3><ul>")
            for issue in issues:
                html.append(f"<li>{json.dumps(issue)}</li>")
            html.append("</ul>")
    html.append("</body></html>")
    body = "\n".join(html)
    key = f"reports/{datetime.utcnow().isoformat()}.html"
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=AUDIT_S3_BUCKET,
        Key=key,
        Body=body,
        ContentType="text/html",
        ACL="public-read",
    )
    return f"https://{AUDIT_S3_BUCKET}.s3.amazonaws.com/{key}"
