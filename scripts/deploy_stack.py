#!/usr/bin/env python3
"""Automate CloudFormation deployment for AutoGuard."""
import sys
import boto3

STACK_NAME = "AutoGuardStack"
TEMPLATE_FILE = "Cloudformation.yml"

def deploy(user_email: str):
    cf = boto3.client("cloudformation")
    with open(TEMPLATE_FILE) as f:
        template = f.read()

    print("Creating or updating stack...", flush=True)
    cf.create_stack(
        StackName=STACK_NAME,
        TemplateBody=template,
        Parameters=[{"ParameterKey": "UserEmail", "ParameterValue": user_email}],
        Capabilities=["CAPABILITY_NAMED_IAM"],
    )
    waiter = cf.get_waiter("stack_create_complete")
    waiter.wait(StackName=STACK_NAME)
    outputs = cf.describe_stacks(StackName=STACK_NAME)["Stacks"][0]["Outputs"]
    for out in outputs:
        print(f"{out['OutputKey']}: {out['OutputValue']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: deploy_stack.py your-email@example.com")
        sys.exit(1)
    deploy(sys.argv[1])
