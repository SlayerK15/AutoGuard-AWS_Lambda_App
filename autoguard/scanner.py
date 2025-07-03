from handlers.ec2_handler import scan_idle_ec2, scan_orphaned_ebs
from handlers.s3_handler import scan_public_s3
from handlers.iam_handler import scan_unused_iam, analyze_iam_policies
from handlers.cost_handler import scan_unused_nat_lb
from handlers.compliance_handler import check_cis_benchmarks
from .config import (
    ALL_REGIONS,
    TARGET_ACCOUNTS,
    ORGANIZATION_WIDE,
    ORG_ROLE_NAME,
)
import boto3

class ResourceScanner:
    def _get_target_accounts(self):
        if ORGANIZATION_WIDE:
            org = boto3.client("organizations")
            return [a["Id"] for a in org.list_accounts()["Accounts"] if a["Status"] == "ACTIVE"]
        if TARGET_ACCOUNTS:
            return [a.strip() for a in TARGET_ACCOUNTS.split(",") if a.strip()]
        return [boto3.client("sts").get_caller_identity()["Account"]]

    def _assume(self, account_id):
        current = boto3.client("sts").get_caller_identity()["Account"]
        if account_id == current:
            return boto3.Session()
        creds = boto3.client("sts").assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{ORG_ROLE_NAME}",
            RoleSessionName="AutoGuard"
        )["Credentials"]
        return boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
        )

    def scan_all_regions(self):
        region_issues = {}
        for account in self._get_target_accounts():
            session = self._assume(account)
            region_issues[account] = {}
            for region in ALL_REGIONS:
                region_issues[account][region] = (
                    scan_idle_ec2(region, session) +
                    scan_orphaned_ebs(region, session) +
                    scan_public_s3(region, session) +
                    scan_unused_iam(region, session) +
                    analyze_iam_policies(region, session) +
                    scan_unused_nat_lb(region, session) +
                    check_cis_benchmarks(region, session)
                )
        return region_issues
