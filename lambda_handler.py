from autoguard.scanner import ResourceScanner
from autoguard.fixer import ResourceFixer
from autoguard.reporter import Reporter

def lambda_handler(event, context):
    scanner = ResourceScanner()
    initial_issues = scanner.scan_all_regions()

    reporter = Reporter()
    reporter.report(initial_issues, "Initial Scan Report")

    fixer = ResourceFixer()
    fixer.fix_all(initial_issues)

    final_issues = scanner.scan_all_regions()
    reporter.report(final_issues, "Final Post-Remediation Report")

    return {
        'statusCode': 200,
        'body': 'AutoGuard scan and remediation completed successfully.'
    }
