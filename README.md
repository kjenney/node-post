# node-post

NodeJS API using Lambda and PostgreSQL

## Routes



## AWS

This is deployed to AWS via CloudFormation using infra.yaml.

Presently we are using the following services:

- Lambda Functions
  - IAM Permissions
  - Cloudwatch Events and Rules
  - SNS
- RDS DB
  - Security Groups
- SecretsManager Secrets
- Code Build
- Application Load Balancer

A parent VPC stack is required.

Changes can be made at the Infrastructure level using this file (i.e. using DynamoDB instead of RDS).

## Secrets

Secrets are stored in AWS Secrets Manager. The RDS password is auto-generated. An example secret is stored in .env and is made available to the Lambda functions.

## Deploy

Code is deployed by creating a release in GitHub. This will automatically trigger a CodeBuild which will deploy the Lambda's.
