#!/usr/bin/env bash
# Remote backend roles with a published salary, as a table.
set -euo pipefail

curl -s "https://spinhire.io/api/jobs?q=backend&fmt=remote&lang=en&limit=100" \
  | jq -r '.jobs[] | select(.salary_min != null) | [.title, .company, .country, .salary] | @tsv' \
  | column -t -s $'\t'
