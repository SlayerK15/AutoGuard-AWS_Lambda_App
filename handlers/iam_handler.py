import boto3

def scan_unused_iam(region):
    iam = boto3.client('iam')
    users = iam.list_users()
    unused_users = []
    for user in users['Users']:
        last_used = iam.get_user(UserName=user['UserName'])['User'].get('PasswordLastUsed')
        if not last_used:
            unused_users.append({"type": "IAM_UNUSED", "user": user['UserName']})
    return unused_users

def delete_unused_iam(issue, region):
    iam = boto3.client('iam')
    iam.delete_user(UserName=issue['user'])

def analyze_iam_policies(region):
    iam = boto3.client('iam')
    policies = iam.list_policies(Scope='Local')['Policies']
    permissive_policies = []
    for policy in policies:
        permissive_policies.append({"type": "IAM_POLICY_OPEN", "policy": policy['Arn']})
    return permissive_policies

def fix_iam_policy(issue, region):
    iam = boto3.client('iam')
    iam.delete_policy(PolicyArn=issue['policy'])
