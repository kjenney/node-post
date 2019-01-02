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
    elb_client = boto3.client('elbv2')
    lambda_client = boto3.client('lambda')
    tgresponse = elb_client.describe_target_groups(
      Names=[
        os.environ['TargetGroupName'],
      ],
      PageSize=1
    )
    targetgroupArn = tgresponse['TargetGroups'][0]['TargetGroupArn']
    if event["RequestType"] == "Create":
      response = lambda_client.add_permission(
            FunctionName=os.environ['LambdaARN'],
            StatementId='AddingPermissionforELB',
            Action='lambda:InvokeFunction',
            Principal='elasticloadbalancing.amazonaws.com',
            SourceArn=targetgroupArn
      )
      msg = "Permissions Added"
    elif event["RequestType"] == "Delete":
      response = lambda_client.remove_permission(
            FunctionName=os.environ['LambdaARN'],
            StatementId='AddingPermissionforELB'
      )
      msg = "Permissions Removed"
    else:
      msg = "Unknown Event: " + event["RequestType"]

    responseData = {}
    responseData['Data'] = msg
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'TargetCreated')
