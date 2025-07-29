pipeline {
    agent any

    environment {
        IMAGE_NAME = "datascientest"
        CONTAINER_NAME = "datascientest_container"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/clementa1/Jenkins-datascientest'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                }
            }
        }

        stage('Execute Script in Container') {
            steps {
                script {
                    sh "docker exec ${CONTAINER_NAME} python3 script.py"
                }
            }
        }

        stage('Stop and Remove Container') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME}"
                    sh "docker rm ${CONTAINER_NAME}"
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    echo "Logging out from Docker..."
                    sh 'docker logout'
                } catch (Exception e) {
                    echo "Docker logout skipped: ${e.getMessage()}"
                }

                try {
                    echo "Cleaning up dangling Docker images..."
                    sh "docker image prune -f"
                } catch (Exception e) {
                    echo "Image cleanup skipped: ${e.getMessage()}"
                }
            }
        }
    }
}
