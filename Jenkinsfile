#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/${GITHUB_ACTOR}/ccep-rag:latest"
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install -e .'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -c "from ccep.cli import main; print(\"CLI imports OK\")"'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t ccep-rag:latest .'
            }
        }
        stage('Push to GHCR') {
            when { branch 'main' }
            steps {
                withCredentials([string(credentialsId: 'GHCR_TOKEN', variable: 'TOKEN')]) {
                    sh "echo $TOKEN | docker login ghcr.io -u ${GITHUB_ACTOR} --password-stdin"
                    sh "docker tag ccep-rag:latest ${DOCKER_IMAGE}"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
