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