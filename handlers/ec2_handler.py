import boto3

def scan_idle_ec2(region):
    ec2 = boto3.client('ec2', region_name=region)
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    idle_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            idle_instances.append({"type": "EC2_IDLE", "id": instance['InstanceId']})
    return idle_instances

def stop_idle_ec2(issue, region):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=[issue['id']])

def scan_orphaned_ebs(region):
    ec2 = boto3.client('ec2', region_name=region)
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    orphaned_volumes = [{"type": "EBS_ORPHANED", "volume_id": vol['VolumeId']} for vol in volumes['Volumes']]
    return orphaned_volumes

def delete_ebs_volume(issue, region):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.delete_volume(VolumeId=issue['volume_id'])
