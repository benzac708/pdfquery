pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/benzac708/ccep-rag:latest"
    }

    stages {
        stage('Lint') {
            steps {
                sh 'pip install ruff -q'
                sh 'ruff check ccep/'
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -e . -q'
                sh 'python3 -c "from ccep.cli import main; print(\"CLI imports OK\")"'
                sh 'python3 -c "from ccep.embedder import Embedder; print(\"Embedder imports OK\")"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                withCredentials([string(credentialsId: 'GHCR_TOKEN', variable: 'TOKEN')]) {
                    sh 'docker build -t ccep-rag:latest .'
                    sh 'echo "$TOKEN" | docker login ghcr.io -u benzac708 --password-stdin'
                    sh "docker tag ccep-rag:latest ${DOCKER_IMAGE}"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "$GHCR_TOKEN" | docker login ghcr.io -u benzac708 --password-stdin'
                sh 'docker-compose down || true'
                sh 'docker-compose pull'
                sh 'docker-compose up -d'
                sh 'docker system prune -f'
            }
        }
    }
}
