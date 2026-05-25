FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    docker-compose && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages uv
RUN curl -fsSL https://github.com/sigstore/cosign/releases/download/v3.0.6/cosign-linux-arm64 -o /usr/local/bin/cosign && \
    chmod +x /usr/local/bin/cosign

RUN ln -sf python3 /usr/bin/python

# Match host docker group GID for socket access
RUN groupadd -g 121 docker && usermod -aG docker jenkins

USER jenkins

COPY --chown=jenkins:jenkins jenkins.yaml /var/jenkins_home/jenkins.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins.yaml
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true"

RUN jenkins-plugin-cli --plugins \
  pipeline-stage-view \
  workflow-aggregator \
  git \
  docker-workflow \
  blueocean \
  configuration-as-code \
  job-dsl \
  credentials-binding \
  github \
  github-branch-source \
  pipeline-github-lib \
  docker-java-api
