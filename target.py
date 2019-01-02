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
      tgresponse = client.describe_target_groups(
        Names=[
          os.environ['TargetGroupName'],
        ],
        PageSize=1
      )
      targetgroupArn = tgresponse['TargetGroups'][0]['TargetGroupArn']
      response = client.register_targets(
        TargetGroupArn=targetgroupArn,
        Targets=[
            {
                'Id': os.environ['LambdaARN']
            }
        ]
      )
      msg = "Target Created"
    elif event["RequestType"] == "Delete":
      tgresponse = client.describe_target_groups(
        Names=[
          os.environ['TargetGroupName'],
        ],
        PageSize=1
      )
      targetgroupArn = tgresponse['TargetGroups'][0]['TargetGroupArn']
      response = client.deregister_targets(
        TargetGroupArn=targetgroupArn,
        Targets=[
            {
                'Id': os.environ['LambdaARN']
            }
        ]
      )
      msg = "Target Deleted"
    else:
      msg = "Unknown Event: " + event["RequestType"]

    responseData = {}
    responseData['Data'] = msg
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'TargetCreated')
