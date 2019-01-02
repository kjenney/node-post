#!/usr/bin/env bash

# A script to deploy a Lambda function to S3 for use by CloudFormation

rm -f function.zip
zip -r ../function.zip . -x "*.DS_Store"
mv ../function.zip .

aws s3api create-bucket --bucket node-post-bucket
aws s3 cp function.zip s3://node-post-bucket/
# aws lambda update-function-code --function-name nodepost \
#   --s3-bucket node-post-bucket \
#   --s3-key function.zip \
#   --publish

# aws iam create-role --assume-role-policy-document file://node-post-custom-lambda-role.json --role-name node-post-custom-lambda
# aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSLambdaExecute --role-name node-post-custom-lambda
# aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/ElasticLoadBalancingFullAccess --role-name node-post-custom-lambda
#
# aws lambda create-function --function-name create-target-group \
# --code S3Bucket=node-post-bucket,S3Key=function.zip --handler index.handler --runtime python3.6 \
# --role arn:aws:iam::161101091064:role/node-post-custom-lambda
