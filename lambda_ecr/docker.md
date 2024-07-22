
# Building and Pushing a Docker Image to Amazon ECR

This guide provides the steps to build a Docker image and push it to Amazon Elastic Container Registry (ECR) using AWS CLI.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- Docker installed on your local machine.
- An existing Amazon ECR repository.

## Steps

### 1. Login to AWS CLI

Ensure you are logged in to AWS CLI with the necessary permissions to access ECR.

### 2. Authenticate Docker to ECR

Run the following command to authenticate Docker to your Amazon ECR registry. Replace `us-east-1` with your AWS region and `992382722885` with your AWS account ID.

```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382722885.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Build the Docker Image

Navigate to the directory containing your Dockerfile and run the following command to build your Docker image. Replace `python:0.0.1` with your desired image tag.

```sh
docker build --no-cache --progress=plain -t python:0.0.1 .
```

### 4. Tag the Docker Image

Tag your Docker image with the ECR repository URI. Replace `992382722885.dkr.ecr.us-east-1.amazonaws.com` with your ECR repository URI and `python:0.0.1` with your image tag.

```sh
docker tag python:0.0.1 992382722885.dkr.ecr.us-east-1.amazonaws.com/python:0.0.1
```

### 5. Push the Docker Image to ECR

Finally, push your Docker image to Amazon ECR.

```sh
docker push 992382722885.dkr.ecr.us-east-1.amazonaws.com/python:0.0.1
```

## Summary

You have now successfully built a Docker image and pushed it to Amazon ECR. You can use this image in your AWS services such as Amazon ECS, Fargate, and others.