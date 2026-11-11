#!/bin/bash
# Real Hermes 0.23.1 free-component call. Prints the probe summary only.
set -u
PY=/tmp/hermes-venv/bin/python
HERMES=/tmp/hermes-venv/bin/hermes
cd /workspace
sleep 2
clear
echo "Hermes Agent $($HERMES --version | head -1)"
echo "FREE-ONLY plugin. Public components with meta.free true."
echo "Not templates. No API key. Paid connector is not called."
echo
echo "=== hermes plugins validate ./hermes ==="
home=$(mktemp -d)
HERMES_HOME="$home" "$HERMES" plugins validate ./hermes 2>/dev/null | sed -n '1,12p'
echo
echo "=== Hermes tool calls: one real free component, three refusals ==="
home=$(mktemp -d)
plugin="$home/plugins/vividsites"
mkdir -p "$plugin"
cp -a hermes/. "$plugin/"
printf 'plugins:\n  enabled:\n    - vividsites\n' > "$home/config.yaml"
"$PY" scripts/hermes_runtime_probe.py "$home" 2>/dev/null
echo
echo "Paid success, unpaid 403, and account scoping: not run."
echo "An invalid key 401 is not an unpaid-account result."
echo "Leave this window up."
sleep 8
