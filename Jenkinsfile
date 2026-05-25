pipeline {
    agent any

    environment {
      DOCKER_IMAGE = "ghcr.io/benzac708/ccep-rag:latest"
      PIP_REQUIRE_VIRTUALENV = "0"
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    env.IMAGE_TAG = sh(script: 'git rev-parse --short=12 HEAD', returnStdout: true).trim()
                }
            }
        }

        stage('Lint') {
            steps {
                sh 'uvx ruff check --fix ccep/'
                sh 'uvx ruff check ccep/'
            }
        }

        stage('Test') {
            steps {
                sh 'uv pip install --user -e .'
                sh 'python3 -c "from ccep.cli import main; print(\\\"CLI imports OK\\\")"'
                sh 'python3 -c "from ccep.embedder import Embedder; print(\\\"Embedder imports OK\\\")"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh 'docker build -t ccep-rag:${IMAGE_TAG} -t ccep-rag:latest .'
                sh 'echo "$GHCR_TOKEN" | docker login ghcr.io -u benzac708 --password-stdin'
                sh "docker tag ccep-rag:${IMAGE_TAG} ghcr.io/benzac708/ccep-rag:${IMAGE_TAG}"
                sh "docker tag ccep-rag:latest ghcr.io/benzac708/ccep-rag:latest"
                sh "docker push ghcr.io/benzac708/ccep-rag:${IMAGE_TAG}"
                sh "docker push ghcr.io/benzac708/ccep-rag:latest"
            }
        }

        stage('Deploy') {
            steps {
                sh 'IMAGE_TAG=${IMAGE_TAG} docker-compose -p ccep-rag -f /app/docker-compose.yml pull app'
                sh 'IMAGE_TAG=${IMAGE_TAG} docker-compose -p ccep-rag -f /app/docker-compose.yml up -d --no-build'
                sh 'docker system prune -f'
            }
        }
    }
}
