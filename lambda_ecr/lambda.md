# Managing AWS Lambda Function with CloudFormation and AWS CLI

This guide provides steps to create, invoke, and delete an AWS Lambda function using AWS CloudFormation and AWS CLI.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- AWS CloudFormation template (`lambda.yaml`) for creating the Lambda function.
- A valid IAM role with permissions for the Lambda function.

## Steps

### 1. Create IAM Role for Lambda

Create an IAM role that AWS Lambda can assume to execute the function.

```sh
aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
```

### 2. Create Lambda Function Stack

Use AWS CloudFormation to create a stack that provisions the Lambda function. Ensure `lambda.yaml` contains the necessary configuration for your Lambda function.

```sh
aws cloudformation create-stack --template-body file://lambda.yaml --stack-name my-lambda-function
```

### 3. Invoke the Lambda Function

Invoke the Lambda function and save the response to `response.json`.

```sh
aws lambda invoke --function-name MyLambdaFunction response.json
```

### 4. Invoke the Lambda Function with Logs

Invoke the Lambda function and save the response to `response.json`, while also retrieving the logs and saving them to `log.txt`.

```sh
aws lambda invoke --function-name MyLambdaFunction response.json --log-type Tail --query 'LogResult' --output text | base64 -d > log.txt
```

### 5. Delete Lambda Function Stack

Delete the CloudFormation stack to remove the Lambda function and associated resources.

```sh
aws cloudformation delete-stack --stack-name my-lambda-function
```

## Summary

By following these steps, you can create, invoke, and delete an AWS Lambda function using CloudFormation and AWS CLI. Ensure you have the necessary IAM roles and permissions configured correctly to manage these resources.
