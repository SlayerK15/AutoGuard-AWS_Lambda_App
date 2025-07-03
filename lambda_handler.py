import json
from autoguard.scanner import ResourceScanner
from autoguard.fixer import ResourceFixer
from autoguard.reporter import Reporter
from ai.monitor import analyze_anomalies, auto_scale

def lambda_handler(event, context):
    scanner = ResourceScanner()
    initial_issues = scanner.scan_all_regions()

    anomalies = analyze_anomalies(initial_issues)
    auto_scale(anomalies, "autoguard-scan-lambda")

    reporter = Reporter()
    reporter.report(initial_issues, "Initial Scan Report")

    fixer = ResourceFixer()
    fixer.fix_all(initial_issues)

    final_issues = scanner.scan_all_regions()
    reporter.report(final_issues, "Final Post-Remediation Report")

    summary = {
        f"{acct}:{region}": len(issues)
        for acct, regions in final_issues.items()
        for region, issues in regions.items()
    }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "AutoGuard scan and remediation completed successfully.",
            "summary": summary,
            "details": final_issues,
        })
    }
