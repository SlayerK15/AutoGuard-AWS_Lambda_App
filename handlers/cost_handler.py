import boto3

def scan_unused_nat_lb(region):
    ec2 = boto3.client('ec2', region_name=region)
    nats = ec2.describe_nat_gateways()['NatGateways']
    unused_nats = [{"type": "NAT_IDLE", "resource": nat['NatGatewayId']} for nat in nats if nat['State'] == 'available']
    return unused_nats

def delete_nat_lb(issue, region):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.delete_nat_gateway(NatGatewayId=issue['resource'])
