# node-post

NodeJS API deployed to AWS Lambda. Uses RDS PostgreSQL and Application Load Balancer. Also uses AWS Code Deploy for releases.

## Routes

- hello: generic hello world in JSON
- products: two hard-coded products in JSON

## AWS

This is deployed to AWS via CloudFormation using infra.yaml.

Presently we are using the following services:

- Lambda Functions
  - IAM Permissions
  - Cloudwatch Events and Rules
  - SNS
- Application Load Balancer
- RDS DB
  - Security Groups
- SecretsManager Secrets
- Code Build

A parent VPC stack is required. A sample VPC template (vpc.yaml) is included.

Changes can be made at the Infrastructure level using this file (i.e. using DynamoDB instead of RDS).

### IMPORTANT ###

Presently CloudFormation does not support Load Balancer Target Groups using Lambda targets. Therefore we need to create a custom resource using a Lambda. Presently the Python boto libraries for communicating with the AWS API are outdated in the Lambda execution environment. Therefore we need to manually deploy the code to S3 before we create the stack.

To deploy the Lambda:

```
pip install -r requirements.txt -t .
npm install pg
./deploy_lambda.sh
```
Once the Lambda has been deployed you can deploy the CloudFormation stack in the CLI or in the console.

## Secrets

Secrets are stored in AWS Secrets Manager. The RDS password is auto-generated. An example secret is stored in .env and is made available to the Lambda functions.

## Deploy

Code is deployed by creating a release in GitHub. This will automatically trigger a CodeBuild which will deploy the Lambda's.
