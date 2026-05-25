FROM jenkins/jenkins:lts

USER root

RUN curl -fsSL https://download.docker.com/linux/static/stable/aarch64/docker-compose-linux-aarch64 -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

RUN curl -fsSL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-aarch64 -o /usr/local/lib/docker/cli-plugins/docker-compose && \
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

USER jenkins

COPY --chown=jenkins:jenkins jenkins.yaml /var/jenkins_home/jenkins.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins.yaml
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

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
