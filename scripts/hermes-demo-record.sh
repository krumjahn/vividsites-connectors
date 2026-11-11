#!/bin/bash
# Real Hermes 0.23.1 probe. Stdout is the redacted JSON from the probe.
# Stderr from Hermes is discarded here so the recording stays readable;
# the probe's own assertions still fail the script if a case is wrong.
set -u
PY=/tmp/hermes-venv/bin/python
HERMES=/tmp/hermes-venv/bin/hermes
cd /workspace
sleep 2
clear
echo "Hermes Agent $($HERMES --version | head -1)"
echo "Package: hermes/  endpoint: https://www.vividsites.app/api/connector"
echo "No paid key in this environment. No catalog body is printed."
echo
echo "=== 1 missing key: Hermes fail-closed, no HTTP request ==="
home=$(mktemp -d)
"$PY" scripts/hermes_runtime_probe.py missing "$home" 2>/dev/null
echo
echo "=== 2 live connector: real POST, not a fixture ==="
home=$(mktemp -d)
"$PY" scripts/hermes_runtime_probe.py live "$home" 2>/dev/null
echo
echo "=== 3 local synthetic fixture: not the VividSites catalog ==="
home=$(mktemp -d)
"$PY" scripts/hermes_runtime_probe.py synthetic "$home" 2>/dev/null
echo
echo "Paid catalog retrieval: not run."
echo "Leave this window up."
sleep 8
