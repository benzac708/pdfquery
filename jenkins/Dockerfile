FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y --no-install-recommends docker-compose && \
    rm -rf /var/lib/apt/lists/*

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
