pipeline {
    agent any

    environment {
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

        stage('Deploy') {
            steps {
                sh 'docker-compose -f /app/docker-compose.yml down || true'
                sh 'docker-compose -f /app/docker-compose.yml up -d --build'
                sh 'docker system prune -f'
            }
        }
    }
}
