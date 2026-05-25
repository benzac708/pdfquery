#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/${env.GIT_REPO_OWNER ?: 'ccep'}/ccep-rag:latest"
        GIT_REPO_OWNER = sh(script: "echo ${env.GIT_URL} | sed -n 's|.*github.com/\\([^/]*\\).*|\\1|p'", returnStdout: true).trim()
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install -e .'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -c "from ccep.cli import main; print(\'CLI imports OK\')"'
                sh 'python3 -c "from ccep.embedder import Embedder; print(\'Embedder imports OK\')"'
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
                    sh 'echo $TOKEN | docker login ghcr.io -u $GIT_REPO_OWNER --password-stdin'
                    sh "docker tag ccep-rag:latest ${DOCKER_IMAGE}"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh 'docker compose -f /app/docker-compose.yml pull'
                sh 'docker compose -f /app/docker-compose.yml up -d'
                sh 'docker system prune -f'
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
