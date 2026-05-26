#!/usr/bin/env bash
set -euo pipefail

JOB_NAME="${1:-pdfquery}"
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
JENKINS_USER="${JENKINS_USER:-admin}"
JENKINS_TOKEN="${JENKINS_TOKEN:-}"

if [[ -z "$JENKINS_TOKEN" ]]; then
  echo "JENKINS_TOKEN is required" >&2
  exit 1
fi

cookie_jar="$(mktemp)"
trap 'rm -f "$cookie_jar"' EXIT

curl -sS -c "$cookie_jar" -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/crumbIssuer/api/json" > /tmp/jenkins-crumb.json
crumb_field="$(python3 -c 'import json; print(json.load(open("/tmp/jenkins-crumb.json"))["crumbRequestField"])')"
crumb="$(python3 -c 'import json; print(json.load(open("/tmp/jenkins-crumb.json"))["crumb"])')"

code="$(curl -sS -o /dev/null -w '%{http_code}' \
  -X POST \
  -b "$cookie_jar" \
  -u "$JENKINS_USER:$JENKINS_TOKEN" \
  -H "$crumb_field: $crumb" \
  "$JENKINS_URL/job/$JOB_NAME/build")"

echo "queued $code"
