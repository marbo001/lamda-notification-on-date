import boto3
import re
import datetime
import json
from botocore.vendored import requests
from botocore.exceptions import ClientError
from collections import defaultdict

ec = boto3.client('ec2')
iam = boto3.client('iam')

"""
Lamda function to sent a webhook post, to slack for instance, to remind you that a date has been reached on a resource
Derived from https://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups-2/
and
https://www.slsmk.com/using-python-and-boto3-to-get-instance-tag-information/

Set NotifyOn tag value on instance to YYYY-MM-DD format
"""

def lambda_handler(event, context):

    #filter instances that have a date tag equaling the current date
    notify_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['NotifyOn']},
        {'Name': 'tag-value', 'Values': [notify_on]},
    ]
    #collect instances 
    instance_response = ec.describe_instances(Filters=filters)
   
    instancelist = []
    
    for reservation in (instance_response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
   #send json payload to webhook
    if len(instancelist) != 0:
      payload={"text":"Time to review: " + json.dumps(instancelist)}
      r = requests.post('<WEBHOOK URL>', json=payload)
