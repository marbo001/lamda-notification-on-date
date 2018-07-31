import boto3
import re
import datetime
import requests

ec = boto3.client('ec2')
iam = boto3.client('iam')

"""
Lamda function to send a webhook post, to slack for instance, to remind you that a date has been reached
in order to clean up ec2 instances, or deprovision some other resources
This is a work in progress...
Derived from https://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups-2/

"""

def lambda_handler(event, context):
    account_ids = '<AWS ACCOUNT ID>'

    notify_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['NotifyOn']},
        {'Name': 'tag-value', 'Values': [notify_on]},
    ]
    instance_response = ec.describe_instances(instance-id=account_ids, Filters=filters)

    for inst in instace_response['Instances']:
        print "Posting %s" % inst['InstanceId']
        payload={"text":"Today is the day!"}
        r = requests.post('<WEBHOOK URL>', json=payload)
