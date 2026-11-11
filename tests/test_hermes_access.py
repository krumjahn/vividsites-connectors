"""Free-component registry rules and a real Hermes invocation.

Paid-account success, unpaid HTTP 403, and account scoping are not tested.
An invalid connector key is not an unpaid entitlement. This plugin does not
send one. Evidence stores hashes and lengths, not component source.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, build_opener

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "hermes"
HERMES = Path("/tmp/hermes-venv/bin/hermes")
PY = Path("/tmp/hermes-venv/bin/python")


def load_registry():
    spec = importlib.util.spec_from_file_location("vividsites_free_registry", PLUGIN / "registry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REG = load_registry()


def item(name: str, free):
    meta = {} if free is None else {"free": free, "category": "ui", "group": "Buttons"}
    return {"name": name, "title": name, "meta": meta}


class ClassificationTests(unittest.TestCase):
    def test_only_boolean_true_is_free(self) -> None:
        self.assertEqual(REG.classification(item("a", True)), "free")
        self.assertEqual(REG.classification(item("a", False)), "not_free")
        self.assertEqual(REG.classification(item("a", None)), "unknown")
        self.assertEqual(REG.classification(item("a", "true")), "unknown")
        self.assertEqual(REG.classification({"name": "a"}), "unknown")

    def test_paid_unknown_and_unsafe_slugs_are_not_fetched(self) -> None:
        registry = {"items": [
            item("paid-widget", False),
            item("mystery-widget", None),
            item("magnetic-button", True),
        ]}
        fetched = []

        def fetcher(url):
            fetched.append(url)
            raise AssertionError(url)

        for slug in ("paid-widget", "mystery-widget", "../paid-widget", "https://evil.test/r/a.json", "cinematic", ""):
            with self.assertRaises(REG.RegistryError):
                REG.get_free_component(slug, registry=registry, fetcher=fetcher)
        self.assertEqual(fetched, [])

    def test_document_must_repeat_boolean_free_and_safe_paths(self) -> None:
        registry = {
            "items": [item("magnetic-button", True)],
            "_documents": {"magnetic-button": {
                "name": "magnetic-button",
                "meta": {"free": "true"},
                "files": [{"path": "ok.html", "content": "<div></div>"}],
            }},
        }
        with self.assertRaises(REG.RegistryError):
            REG.get_free_component("magnetic-button", registry=registry)
        registry["_documents"]["magnetic-button"]["meta"] = {"free": True}
        registry["_documents"]["magnetic-button"]["files"] = [{"path": "../secret.html", "content": "x"}]
        with self.assertRaises(REG.RegistryError):
            REG.get_free_component("magnetic-button", registry=registry)

    def test_redirect_is_refused(self) -> None:
        seen = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                if self.path == "/first":
                    self.send_response(302)
                    self.send_header("Location", "http://127.0.0.1/secret")
                    self.end_headers()
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"secret-body")

            def log_message(self, fmt, *args):
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            opener = build_opener(REG._RefuseRedirect)
            with self.assertRaises(REG.RegistryError):
                opener.open(Request(f"http://127.0.0.1:{server.server_address[1]}/first"), timeout=5)
        finally:
            server.shutdown()
        self.assertEqual(seen, ["/first"])


class LiveRegistryTests(unittest.TestCase):
    def test_real_free_component_and_refused_template_id(self) -> None:
        listed = REG.list_free_components("magnetic", limit=5)
        self.assertTrue(any(item["name"] == "magnetic-button" and item["kind"] == "component" for item in listed["items"]))
        got = REG.get_free_component("magnetic-button")
        content = got["files"][0]["content"]
        self.assertTrue(got["free"] is True)
        self.assertGreater(len(content), 200)
        self.assertNotIn("..", got["files"][0]["path"])
        digest = hashlib.sha256(content.encode()).hexdigest()
        with self.assertRaises(REG.RegistryError):
            REG.get_free_component("cinematic")
        self.evidence = {
            "name": got["name"],
            "kind": got["kind"],
            "free": True,
            "content_bytes": len(content),
            "content_sha256": digest,
            "template_slug_cinematic": "refused",
        }


class HermesRuntimeTests(unittest.TestCase):
    def test_validator_and_live_tool_call(self) -> None:
        if not HERMES.is_file():
            self.skipTest("Hermes 0.23.1 is not installed")
        with tempfile.TemporaryDirectory(prefix="hermes-validate-") as home:
            validate = subprocess.run(
                [str(HERMES), "plugins", "validate", str(PLUGIN)],
                check=False, capture_output=True, text=True, timeout=180,
                env={**os.environ, "HERMES_HOME": home},
            )
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
        self.assertIn("plugin.yaml parses", validate.stdout)
        self.assertIn("declared tools", validate.stdout)
        with tempfile.TemporaryDirectory(prefix="hermes-free-") as home:
            plugin_dir = Path(home) / "plugins" / "vividsites"
            shutil.copytree(PLUGIN, plugin_dir, ignore=shutil.ignore_patterns("__pycache__"))
            (Path(home) / "config.yaml").write_text("plugins:\n  enabled:\n    - vividsites\n", encoding="utf-8")
            proc = subprocess.run(
                [str(PY), str(ROOT / "scripts" / "hermes_runtime_probe.py"), home],
                check=False, capture_output=True, text=True, timeout=90,
            )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        summary = json.loads(proc.stdout)
        self.assertEqual(summary["component"]["name"], "magnetic-button")
        self.assertTrue(summary["component"]["free"])
        self.assertGreater(summary["component"]["content_bytes"], 200)
        self.assertEqual(summary["refused"], ["cinematic", "../secret", "https://evil.test/r/a.json"])
        self.assertEqual(set(summary["component"]), {"name", "kind", "free", "path", "content_bytes", "content_sha256"})
        (ROOT / "review" / "hermes-auth-evidence.json").write_text(json.dumps({
            "mode": "free-components-only",
            "paid_connector": "not shipped",
            "paid_403": "not tested; no unpaid key; invalid-key 401 is not this result",
            "paid_success": "not tested; no paid key",
            "account_scope": "not tested; no account credentials",
            "hermes": summary,
        }, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
