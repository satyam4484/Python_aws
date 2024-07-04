pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                // Add your build commands here, for example:
                // sh 'mvn clean install'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Add your deploy commands here, for example:
                // sh 'scp target/my-app.jar user@server:/path/to/deploy'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Add any cleanup steps here
        }
        success {
            echo 'Build and Deploy succeeded!'
        }
        failure {
            echo 'Build and Deploy failed.'
        }
    }
}