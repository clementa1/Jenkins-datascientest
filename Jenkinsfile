pipeline {
    agent any

    environment {
        DOCKER_ID = "dstdockerhub"
        DOCKER_IMAGE = "datascientestapi"
        DOCKER_TAG = "v.${BUILD_ID}.0"
        DOCKERHUB_CREDENTIALS = credentials('docker_jenkins')
    }

    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version || echo "Docker not found!"'
            }
        }

        stage('Building') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Testing') {
            steps {
                sh 'python -m unittest'
            }
        }

        stage('Deploying') {
            steps {
                script {
                    sh '''
                    docker rm -f datascientest_api || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG .
                    docker run -d -p 8000:8000 --name datascientest_api $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('User Acceptance') {
            steps {
                input(
                    message: 'Proceed to push to main?',
                    ok: 'Push it!',
                    parameters: [
                        string(defaultValue: 'yes', description: 'Confirm action', name: 'confirmation')
                    ]
                )
            }
        }

        stage('Pushing and Merging') {
            parallel {
                stage('Pushing Image') {
                    steps {
                        script {
                            if (!env.DOCKERHUB_CREDENTIALS_USR || !env.DOCKERHUB_CREDENTIALS_PSW) {
                                error("DockerHub credentials are missing!")
                            }
                        }
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        sh 'docker push $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG'
                    }
                }
                stage('Merging') {
                    steps {
                        echo 'Merging done'
                    }
                }
            }
        }
    }

    post {
        always {
            node {
                script {
                    try {
                        sh 'docker logout'
                    } catch (Exception e) {

                input(
                    message: 'Proceed to push to main?',
                    ok: 'Push it!',
                    parameters: [
                        string(defaultValue: 'yes', description: 'Confirm action', name: 'confirmation')
                    ]
                )
            }
        }

        stage('Pushing and Merging') {
            parallel {
                stage('Pushing Image') {
                    steps {
                        script {
                            if (!env.DOCKERHUB_CREDENTIALS_USR || !env.DOCKERHUB_CREDENTIALS_PSW) {
                                error("DockerHub credentials are missing!")
                            }
                        }
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        sh 'docker push $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG'
                    }
                }
                stage('Merging') {
                    steps {
                        echo 'Merging done'
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    sh 'docker logout'
                } catch (Exception e) {
                    echo "Docker logout skipped: ${e.getMessage()}"
                }
            }
        }
    }
}
