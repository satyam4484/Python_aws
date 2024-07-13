
# Jenkins Setup and Docker Image Deployment to AWS ECR on Ubuntu 22.04 LTS

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Update and Install Java](#step-1-update-and-install-java)
3. [Step 2: Install Jenkins](#step-2-install-jenkins)
4. [Step 3: Enable and Start Jenkins](#step-3-enable-and-start-jenkins)
5. [Step 4: Install Git](#step-4-install-git)
6. [Step 5: Access Jenkins](#step-5-access-jenkins)
7. [Step 6: Add AWS Credentials in Jenkins](#step-6-add-aws-credentials-in-jenkins)
8. [Step 7: Install Docker](#step-7-install-docker)
9. [Step 8: Install Jenkins Plugins](#step-8-install-jenkins-plugins)
10. [Step 9: Create AWS ECR Repository](#step-9-create-aws-ecr-repository)
11. [Step 10: Create IAM Role in AWS](#step-10-create-iam-role-in-aws)
12. [Step 11: Install AWS CLI](#step-11-install-aws-cli)
13. [Step 12: Jenkins Pipeline Script](#step-12-jenkins-pipeline-script)

## Prerequisites
- An Ubuntu 22.04 LTS instance.
- AWS account with permissions to create ECR repositories and IAM roles.

## Step 1: Update and Install Java
```bash
sudo apt update
sudo apt install openjdk-17-jre -y
java -version
```

## Step 2: Install Jenkins
```bash
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y
```

## Step 3: Enable and Start Jenkins
```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

## Step 4: Install Git
```bash
sudo apt install git -y
```

## Step 5: Access Jenkins
- Open your browser and go to `http://<Instance_IP>:8080`
- Retrieve the Jenkins administrator password:
  ```bash
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
- Follow the instructions on the Jenkins setup page to complete the configuration and create a Jenkins user.

## Step 6: Add AWS Credentials in Jenkins
- Go to `Manage Jenkins` > `Credentials` > `System` > `Global credentials (unrestricted)` > `Add Credentials`.
- Select `Username with password`, and add your AWS `Access Key ID` and `Secret Access Key`.

## Step 7: Install Docker
```bash
sudo apt install docker.io -y
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart jenkins
```

## Step 8: Install Jenkins Plugins
- Go to `Manage Jenkins` > `Manage Plugins` > `Available Plugins`.
- Install the following plugins:
  - Docker
  - Docker Pipeline
  - Amazon ECR plugin

## Step 9: Create AWS ECR Repository
- Go to AWS ECR and create a new repository to push the Docker image.

## Step 10: Create IAM Role in AWS
- Create an IAM role with the `AmazonEC2ContainerRegistryFullAccess` policy attached.

## Step 11: Install AWS CLI
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Step 12: Jenkins Pipeline Script
Create a Jenkins Pipeline job with the following script to build and push a Docker image to AWS ECR:

```groovy
pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'  // Replace with your AWS region
        ECR_REPOSITORY = 'python'  // Replace with your ECR repository name
        AWS_ACCOUNT_ID='992382722885' 
        IMAGE_TAG = "${env.Version}"  // Using the build ID as the image tag
        IMAGE = "${ECR_REPOSITORY}:${IMAGE_TAG}"
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_URL="${ECR_URL}/${IMAGE}"
    }

    stages {
        stage('Display Environment Variables') {
            steps {
                script {
                    echo "AWS Region: ${AWS_REGION}"
                    echo "ECR Repository: ${ECR_REPOSITORY}"
                    echo "AWS Account ID: ${AWS_ACCOUNT_ID}"
                    echo "Image Tag: ${IMAGE_TAG}"
                    echo "Image: ${IMAGE}"
                    echo "Ecr url: ${ECR_URL}"
                
                }
            }
        }
        stage('SCM Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/satyam4484/Python_aws'
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId:"Aws_Credential",usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        sh 'echo "Building image" '
                        sh 'echo ${AWS_ACCESS_KEY_ID}'

                        sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}"

                        image = docker.build "${IMAGE}" 

                        sh "docker tag ${IMAGE} ${ECR_URL}/${ECR_REPOSITORY}:${IMAGE_TAG}"

                        sh "docker push ${IMAGE_URL}"
                        
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Docker image built and pushed to ECR successfully!'
        }
        failure {
            echo 'Failed to build and push Docker image to ECR.'
        }
    }
}