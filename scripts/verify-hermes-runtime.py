#!/usr/bin/env python3
"""Live, isolated Hermes checks; outputs hashes/metadata, never keys or source.

Run with a Hermes installation's Python. An already-supplied VIVIDSITES_API_KEY
enables extra unmetered paid reads. No build prompt, purchase or deployment runs.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main():
    # This test harness consumes only its inherited credential, never credential
    # files. The plugin itself resolves secrets through Hermes's scoped API.
    paid_key = os.environ.pop("VIVIDSITES_API_KEY", "")
    unpaid_key = os.environ.pop("VIVIDSITES_UNPAID_API_KEY", "")
    with tempfile.TemporaryDirectory(prefix="vividsites-combined-runtime-") as temporary:
        home = Path(temporary)
        (home / "bundled").mkdir()
        shutil.copytree(ROOT / "hermes", home / "plugins/vividsites", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (home / "config.yaml").write_text("plugins:\n  enabled:\n    - vividsites\n", encoding="utf-8")
        os.environ.update({"HERMES_HOME": str(home), "HERMES_BUNDLED_PLUGINS": str(home / "bundled"),
                           "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
        from agent.secret_scope import set_secret_scope, reset_secret_scope
        from hermes_cli.plugins import get_plugin_manager
        from tools.registry import registry

        manager = get_plugin_manager()
        manager.discover_and_load(force=True)

        def call(name, args):
            raw = registry.dispatch(name, args)
            value = json.loads(raw) if isinstance(raw, str) else raw
            if not isinstance(value, dict):
                raise AssertionError("Unexpected Hermes result shape")
            return value

        def component_summary(value):
            assert value.get("kind") == "free_component" and value.get("free") is True
            source = "\n".join(entry["content"] for entry in value["files"])
            assert len(source) > 200
            return {"slug": value["name"], "free": True, "source_bytes": len(source.encode()),
                    "source_sha256": hashlib.sha256(source.encode()).hexdigest()}

        summary = {"runtime": "Hermes", "plugin_version": "1.2.0"}
        token = set_secret_scope({})
        try:
            listed = call("list_free_components", {"query": "magnetic", "limit": 5})
            assert any(item["name"] == "magnetic-button" for item in listed["items"])
            summary["no_key_free_component"] = component_summary(call("get_free_component", {"slug": "magnetic-button"}))
            missing = call("vividsites_search_sites", {"query": "cinematic", "limit": 1})
            assert missing.get("error", {}).get("code") == "missing_api_key"
            summary["no_key_paid"] = "missing_api_key; plugin remains loaded"
            for slug in ("cinematic", "../secret", "https://evil.example/a"):
                assert call("get_free_component", {"slug": slug}).get("error")
            summary["free_refusals"] = ["template slug", "path traversal", "URL"]
        finally:
            reset_secret_scope(token)

        token = set_secret_scope({"VIVIDSITES_API_KEY": "invalid-vividsites-smoke-key"})
        try:
            summary["invalid_key_free_component"] = component_summary(call("get_free_component", {"slug": "magnetic-button"}))
            rejected = call("vividsites_search_sites", {"query": "cinematic", "limit": 1})
            assert rejected.get("error", {}).get("code") == "http_401"
            summary["invalid_key_paid"] = "http_401; no free fallback"
        finally:
            reset_secret_scope(token)

        # A new empty profile must not inherit the prior profile's key.
        token = set_secret_scope({})
        try:
            assert call("vividsites_search_sites", {}).get("error", {}).get("code") == "missing_api_key"
            summary["empty_profile_after_keyed_profile"] = "missing_api_key"
        finally:
            reset_secret_scope(token)

        if paid_key:
            token = set_secret_scope({"VIVIDSITES_API_KEY": paid_key})
            try:
                sites = call("vividsites_search_sites", {"query": "cinematic", "limit": 1})
                assert not sites.get("isError") and "error" not in sites, "Paid search failed; inspect account setup without logging secrets"
                structured = sites.get("structuredContent") or {}
                slugs = [item.get("slug") for item in structured.get("items", []) if isinstance(item, dict)]
                if not slugs:
                    text = "\n".join(block.get("text", "") for block in sites.get("content", []) if isinstance(block, dict))
                    slugs = re.findall(r"^([a-z0-9]+(?:-[a-z0-9]+)*)\s+—", text, flags=re.MULTILINE)
                assert slugs and isinstance(slugs[0], str), "Paid search returned no usable template slug"
                preview = call("vividsites_get_template_preview", {"slug": slugs[0]})
                assert not preview.get("isError") and "error" not in preview, "Paid preview failed"
                assert preview.get("content") or preview.get("structuredContent"), "Paid preview was empty"
                summary["paid_account"] = {"search": "passed", "preview": "passed", "slug": slugs[0]}
            finally:
                reset_secret_scope(token)
        else:
            summary["paid_account"] = "SKIP: no existing VIVIDSITES_API_KEY supplied"
        if unpaid_key:
            token = set_secret_scope({"VIVIDSITES_API_KEY": unpaid_key})
            try:
                rejected = call("vividsites_search_sites", {"query": "cinematic", "limit": 1})
                assert rejected.get("error", {}).get("code") == "http_403", "Expected a valid unpaid-account 403"
                summary["unpaid_account_free_component"] = component_summary(call("get_free_component", {"slug": "magnetic-button"}))
                summary["unpaid_account"] = "http_403 for paid tool; free retrieval passed"
            finally:
                reset_secret_scope(token)
        else:
            summary["unpaid_account"] = "SKIP: no existing VIVIDSITES_UNPAID_API_KEY supplied"
        summary["metered_build_prompt"] = "not requested"
        manager.unload()
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
