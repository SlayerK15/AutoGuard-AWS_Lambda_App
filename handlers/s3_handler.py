import boto3

def scan_public_s3(region):
    s3 = boto3.client('s3', region_name=region)
    buckets = s3.list_buckets()
    public_buckets = []
    for bucket in buckets['Buckets']:
        acl = s3.get_bucket_acl(Bucket=bucket['Name'])
        for grant in acl['Grants']:
            if grant.get('Grantee', {}).get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                public_buckets.append({"type": "S3_PUBLIC", "bucket": bucket['Name']})
    return public_buckets

def restrict_s3(issue, region):
    s3 = boto3.client('s3', region_name=region)
    s3.put_public_access_block(
        Bucket=issue['bucket'],
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
