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
            parallel {
                stage('Ruff Fix') {
                    steps { sh 'uvx ruff check --fix ccep/' }
                }
                stage('Ruff Check') {
                    steps { sh 'uvx ruff check ccep/' }
                }
            }
        }

        stage('Secrets Scan') {
            steps {
                sh '''
                  docker run --rm \
                    -v "$PWD:/repo" \
                    -w /repo \
                    ghcr.io/gitleaks/gitleaks:latest \
                    detect --no-banner --redact --source /repo
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'rm -rf .venv'
                sh 'uv venv .venv'
                sh 'uv pip install --python .venv/bin/python -e .'
                sh '.venv/bin/python -c "from ccep.cli import main; print(\\\"CLI imports OK\\\")"'
                sh '.venv/bin/python -c "from ccep.embedder import Embedder; print(\\\"Embedder imports OK\\\")"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh 'docker build -t ccep-rag:${IMAGE_TAG} -t ccep-rag:latest .'
                sh '''
                  docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v "$HOME/.cache/trivy:/root/.cache/" \
                    aquasec/trivy:latest \
                    image --no-progress --severity HIGH,CRITICAL --exit-code 1 ccep-rag:${IMAGE_TAG}
                '''
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
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                  for i in $(seq 1 10); do
                    if curl -fsS http://127.0.0.1:8501/_stcore/health >/dev/null; then
                      exit 0
                    fi
                    sleep 3
                  done
                  exit 1
                '''
            }
        }
    }
}
