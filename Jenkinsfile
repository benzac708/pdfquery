pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/benzac708/ccep-rag:latest"
        PIP_REQUIRE_VIRTUALENV = "0"
    }

    stages {
        stage('Lint') {
            steps {
                sh 'pip install ruff -q --break-system-packages'
                sh 'python3 -m ruff check --fix ccep/'
                sh 'python3 -m ruff check ccep/'
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -e . -q --break-system-packages'
                sh 'python3 -c "from ccep.cli import main; print(\\\"CLI imports OK\\\")"'
                sh 'python3 -c "from ccep.embedder import Embedder; print(\\\"Embedder imports OK\\\")"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh 'docker build -t ccep-rag:latest .'
                sh 'echo "$GHCR_TOKEN" | docker login ghcr.io -u benzac708 --password-stdin'
                sh "docker tag ccep-rag:latest ${DOCKER_IMAGE}"
                sh "docker push ${DOCKER_IMAGE}"
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose -f /app/docker-compose.yml down || true'
                sh 'docker-compose -f /app/docker-compose.yml up -d --build'
                sh 'docker system prune -f'
            }
        }
    }
}
