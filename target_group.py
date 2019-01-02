import os
import os.path
import sys

envLambdaTaskRoot = os.environ["LAMBDA_TASK_ROOT"]
print("LAMBDA_TASK_ROOT env var:"+os.environ["LAMBDA_TASK_ROOT"])
print("sys.path:"+str(sys.path))

sys.path.insert(0,envLambdaTaskRoot+"/NewBotoVersion")
print("sys.path:"+str(sys.path))
import botocore
import boto3

print("boto3 version:"+boto3.__version__)
print("botocore version:"+botocore.__version__)

import cfnresponse
msg = ""

def handler(event, context):
    client = boto3.client('elbv2')
    if event["RequestType"] == "Create":
      response = client.create_target_group(
        Name=os.environ['TargetGroupName'],
        TargetType='lambda',
        HealthCheckEnabled=True,
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=65,
        HealthCheckTimeoutSeconds=60,
        HealthyThresholdCount=4,
        UnhealthyThresholdCount=2
      )
      targetgroupArn = response['TargetGroups'][0]['TargetGroupArn']
      msg = "Target Group Created"
    elif event["RequestType"] == "Delete":
      targetgroupResp = client.describe_target_groups(
        Names=[
          os.environ['TargetGroupName'],
        ],
        PageSize=1
      )
      targetgroupArn = response['TargetGroups'][0]['TargetGroupArn']
      if targetgroupArn != "":
        response = client.delete_target_group( TargetGroupArn=targetgroupArn )
        msg = "Target Group Deleted"
      else:
        msg = "Could not find Target Group to be deleted"
    else:
      msg = "Unknown Event: " + event["RequestType"]

    responseData = {}
    responseData['Data'] = msg
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, targetgroupArn)
