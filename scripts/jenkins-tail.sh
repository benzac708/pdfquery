#!/usr/bin/env bash
set -euo pipefail

BUILD_NUMBER="${1:-}"
JOB_NAME="${2:-pdfquery}"
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
JENKINS_USER="${JENKINS_USER:-admin}"
JENKINS_TOKEN="${JENKINS_TOKEN:-}"

if [[ -z "$JENKINS_TOKEN" ]]; then
  echo "JENKINS_TOKEN is required" >&2
  exit 1
fi

if [[ -z "$BUILD_NUMBER" ]]; then
  BUILD_NUMBER="$(curl -fsS -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/job/$JOB_NAME/api/json" | python3 -c 'import sys,json; d=json.load(sys.stdin); b=d.get("lastBuild"); print(b.get("number") if b else "")')"
fi

if [[ -z "$BUILD_NUMBER" ]]; then
  echo "No build number available" >&2
  exit 1
fi

curl -fsS -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/job/$JOB_NAME/$BUILD_NUMBER/consoleText"
