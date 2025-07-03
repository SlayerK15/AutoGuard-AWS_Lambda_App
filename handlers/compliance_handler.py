import boto3


def _check_root_mfa(session=None):
    session = session or boto3.Session()
    iam = session.client("iam")
    summary = iam.get_account_summary().get("SummaryMap", {})
    if summary.get("AccountMFAEnabled", 0) == 0:
        return {
            "type": "CIS_VIOLATION",
            "control": "1.5",
            "description": "Root account MFA not enabled",
        }
    return None


def _check_s3_encryption(region, session=None):
    session = session or boto3.Session()
    s3 = session.client("s3", region_name=region)
    findings = []
    for bucket in s3.list_buckets().get("Buckets", []):
        name = bucket["Name"]
        try:
            s3.get_bucket_encryption(Bucket=name)
        except Exception as e:
            if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
                findings.append(
                    {
                        "type": "CIS_VIOLATION",
                        "control": "2.1",
                        "bucket": name,
                        "description": "S3 bucket encryption disabled",
                    }
                )
    return findings


def check_cis_benchmarks(region, session=None):
    violations = []
    root_check = _check_root_mfa(session)
    if root_check:
        root_check["region"] = region
        violations.append(root_check)
    violations.extend(_check_s3_encryption(region, session))
    return violations
