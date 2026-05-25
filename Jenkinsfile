pipeline {
    agent any

    environment {
      DOCKER_IMAGE = "ghcr.io/benzac708/pdfquery:latest"
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
                    steps { sh 'uvx ruff check --fix pdfquery/' }
                }
                stage('Ruff Check') {
                    steps { sh 'uvx ruff check pdfquery/' }
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
                sh '.venv/bin/python -c "from pdfquery.cli import main; print(\\\"CLI imports OK\\\")"'
                sh '.venv/bin/python -c "from pdfquery.embedder import Embedder; print(\\\"Embedder imports OK\\\")"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh 'docker build -t pdfquery:${IMAGE_TAG} -t pdfquery:latest .'
                sh '''
                  docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v "$HOME/.cache/trivy:/root/.cache/" \
                    aquasec/trivy:latest \
                    image --no-progress --severity CRITICAL --ignore-unfixed --exit-code 1 pdfquery:${IMAGE_TAG}
                '''
                sh 'echo "$GHCR_TOKEN" | docker login ghcr.io -u benzac708 --password-stdin'
                sh "docker tag pdfquery:${IMAGE_TAG} ghcr.io/benzac708/pdfquery:${IMAGE_TAG}"
                sh "docker tag pdfquery:latest ghcr.io/benzac708/pdfquery:latest"
                sh "docker push ghcr.io/benzac708/pdfquery:${IMAGE_TAG}"
                sh "docker push ghcr.io/benzac708/pdfquery:latest"
                sh '''
                  COSIGN_PASSWORD="$COSIGN_PASSWORD" \
                  cosign sign --yes \
                    --key "$COSIGN_PRIVATE_KEY" \
                    -a git_commit=${IMAGE_TAG} \
                    -a repository=benzac708/pdfquery \
                    ghcr.io/benzac708/pdfquery:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                  cosign verify --key "$COSIGN_PUBLIC_KEY" ghcr.io/benzac708/pdfquery:${IMAGE_TAG}
                '''
                sh 'IMAGE_TAG=${IMAGE_TAG} docker-compose -p pdfquery -f /app/docker-compose.yml down --remove-orphans || true'
                sh 'IMAGE_TAG=${IMAGE_TAG} docker-compose -p pdfquery -f /app/docker-compose.yml pull app'
                sh 'IMAGE_TAG=${IMAGE_TAG} docker-compose -p pdfquery -f /app/docker-compose.yml up -d --no-build'
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                  for i in $(seq 1 10); do
                    if docker run --rm --network host curlimages/curl:latest -fsS http://127.0.0.1:8501/_stcore/health >/dev/null 2>&1; then
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
