import boto3

def check_cis_benchmarks(region):
    violations = [{"type": "CIS_VIOLATION", "control": "1.1", "region": region}]
    return violations
