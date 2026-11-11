#!/usr/bin/env python3
"""Enable the free-only plugin in a scratch Hermes home and call it."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HOME = Path(sys.argv[1])
os.environ["HERMES_HOME"] = str(HOME)
os.environ.pop("HERMES_SAFE_MODE", None)
os.environ.pop("VIVIDSITES_API_KEY", None)

from hermes_cli.plugins import get_plugin_manager
from tools.registry import registry

get_plugin_manager().discover_and_load(force=True)


def call(name: str, args: dict) -> dict:
    raw = registry.dispatch(name, args)
    text = raw if isinstance(raw, str) else json.dumps(raw)
    return json.loads(text)


listed = call("list_free_components", {"query": "magnetic", "limit": 5})
got = call("get_free_component", {"slug": "magnetic-button"})
content = got["files"][0]["content"]
refused = []
for slug in ("cinematic", "../secret", "https://evil.test/r/a.json"):
    result = call("get_free_component", {"slug": slug})
    if "error" not in result:
        raise SystemExit(f"slug was not refused: {slug}")
    refused.append(slug)

summary = {
    "runtime": "hermes",
    "mode": "free-components-only",
    "listed": [{"name": item["name"], "kind": item["kind"], "free": item["free"]} for item in listed["items"]],
    "component": {
        "name": got["name"],
        "kind": got["kind"],
        "free": got["free"],
        "path": got["files"][0]["path"],
        "content_bytes": len(content),
        "content_sha256": __import__("hashlib").sha256(content.encode()).hexdigest(),
    },
    "refused": refused,
}
if got["kind"] != "free_component" or got["free"] is not True or len(content) < 200:
    raise SystemExit("live free component was not returned")
sys.stdout.write(json.dumps(summary, indent=2) + "\n")
