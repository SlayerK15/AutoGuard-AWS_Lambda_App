from handlers.ec2_handler import stop_idle_ec2, delete_ebs_volume
from handlers.s3_handler import restrict_s3
from handlers.iam_handler import delete_unused_iam, fix_iam_policy
from handlers.cost_handler import delete_nat_lb

class ResourceFixer:
    def fix_all(self, region_issues):
        for region, issues in region_issues.items():
            for issue in issues:
                if issue.get('id') in issue.get('whitelist', []):
                    continue
                issue_type = issue['type']
                if issue_type == 'EC2_IDLE':
                    stop_idle_ec2(issue, region)
                elif issue_type == 'EBS_ORPHANED':
                    delete_ebs_volume(issue, region)
                elif issue_type == 'S3_PUBLIC':
                    restrict_s3(issue, region)
                elif issue_type == 'IAM_UNUSED':
                    delete_unused_iam(issue, region)
                elif issue_type == 'IAM_POLICY_OPEN':
                    fix_iam_policy(issue, region)
                elif issue_type == 'NAT_IDLE':
                    delete_nat_lb(issue, region)
