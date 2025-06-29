from handlers.ec2_handler import scan_idle_ec2, scan_orphaned_ebs
from handlers.s3_handler import scan_public_s3
from handlers.iam_handler import scan_unused_iam, analyze_iam_policies
from handlers.cost_handler import scan_unused_nat_lb
from handlers.compliance_handler import check_cis_benchmarks
from .config import ALL_REGIONS

class ResourceScanner:
    def scan_all_regions(self):
        region_issues = {}
        for region in ALL_REGIONS:
            region_issues[region] = (
                scan_idle_ec2(region) +
                scan_orphaned_ebs(region) +
                scan_public_s3(region) +
                scan_unused_iam(region) +
                analyze_iam_policies(region) +
                scan_unused_nat_lb(region) +
                check_cis_benchmarks(region)
            )
        return region_issues
