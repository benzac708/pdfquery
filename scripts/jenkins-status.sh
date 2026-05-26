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

curl -fsS -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/job/$JOB_NAME/api/json" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); b=d.get("lastBuild"); print("job=%s build=%s building=%s result=%s" % (d.get("name"), b.get("number") if b else None, b.get("building") if b else None, b.get("result") if b else None))'
