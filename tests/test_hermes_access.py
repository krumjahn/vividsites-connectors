"""Server-side connector denial and Hermes runtime checks.

Live cases record status and error codes only. They do not store catalog bodies.
A local Hermes fixture is labeled synthetic and is not production entitlement proof.
Unpaid (403) and cross-account scoping stay explicit skips without credentials.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "hermes"
ENDPOINT = "https://www.vividsites.app/api/connector"
HERMES = Path("/tmp/hermes-venv/bin/python")
PROBE = ROOT / "scripts" / "hermes_runtime_probe.py"
TOOLS = (
    "search_sites",
    "get_template_preview",
    "get_build_prompt",
    "search_components",
    "get_component",
    "video_prompt_formula",
)


def connector(method: str, params: dict, key: str | None) -> tuple[int, dict]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if key is not None:
        headers["Authorization"] = "Bearer " + key
    request = Request(ENDPOINT, json.dumps(payload).encode(), headers)
    try:
        with urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read(4000))
    except HTTPError as error:
        return error.code, json.loads(error.read(4000))


class PackageTests(unittest.TestCase):
    def test_header_is_a_profile_reference_not_a_secret(self) -> None:
        mcp = json.loads((PLUGIN / "mcp.json").read_text())
        server = mcp["mcpServers"]["vividsites"]
        self.assertEqual(server["url"], ENDPOINT)
        self.assertEqual(server["headers"]["Authorization"], "Bearer ${VIVIDSITES_API_KEY}")
        self.assertNotIn("plugin.yaml", {path.name for path in PLUGIN.iterdir()})
        manifest = json.loads((PLUGIN / "plugin.json").read_text())
        secret = manifest["extensions"]["com.nousresearch.hermes"]["config_schema"]["api_key"]
        self.assertEqual(secret["type"], "secret")
        self.assertEqual(secret["env"], "VIVIDSITES_API_KEY")
        self.assertEqual(
            manifest["extensions"]["com.nousresearch.hermes"]["servers"]["vividsites"]["trust"],
            "untrusted",
        )

    def test_root_portable_manifest_still_has_no_header(self) -> None:
        root = json.loads((ROOT / "mcp.json").read_text())
        self.assertNotIn("headers", root["mcpServers"]["vividsites"])

    def test_package_tree_has_no_credential_material(self) -> None:
        banned = ("sk-", "rk_live", "whsec_", "BEGIN PRIVATE", "keith@rumjahn.com", "feriosa2025")
        for path in PLUGIN.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for needle in banned:
                self.assertNotIn(needle, text, path)


class LiveServerTests(unittest.TestCase):
    def test_missing_and_invalid_credentials_do_not_return_paid_or_free_labeled_results(self) -> None:
        calls = [("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}),
                 ("tools/list", {})]
        calls += [("tools/call", {"name": name, "arguments": {}}) for name in TOOLS]
        calls.append(("tools/call", {"name": "search_sites", "arguments": {"query": "cinematic", "tier": "free", "limit": 1}}))
        evidence = []
        for method, params in calls:
            status, body = connector(method, params, None)
            self.assertEqual(status, 401, (method, params))
            self.assertEqual(body.get("error"), "authentication_required")
            self.assertNotIn("result", body)
            evidence.append({"auth": "none", "method": method, "tool": params.get("name"), "status": status, "error": body.get("error")})
        for key, label in (("invalid-vividsites-smoke-key", "invalid"), ("${VIVIDSITES_API_KEY}", "placeholder")):
            status, body = connector("tools/call", {"name": "get_build_prompt", "arguments": {"slug": "cinematic"}}, key)
            self.assertEqual(status, 401)
            self.assertEqual(body.get("error"), "invalid_api_key")
            self.assertNotIn("result", body)
            evidence.append({"auth": label, "tool": "get_build_prompt", "status": status, "error": body.get("error")})
        self.evidence = evidence

    def test_unpaid_and_account_scope_are_unproven_without_credentials(self) -> None:
        self.assertFalse(os.environ.get("VIVIDSITES_API_KEY"))
        self.assertFalse(os.environ.get("VIVIDSITES_UNPAID_API_KEY"))


class HermesRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        if not HERMES.is_file():
            self.skipTest("Hermes 0.23.1 venv is not installed")

    def test_validate_and_runtime_cases(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hermes-validate-") as home:
            validate = subprocess.run(
                ["/tmp/hermes-venv/bin/hermes", "plugins", "validate", str(PLUGIN)],
                check=False, capture_output=True, text=True, timeout=180,
                env={**os.environ, "HERMES_HOME": home},
            )
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
        self.assertIn("portable manifest", validate.stdout)
        summaries = []
        for case in ("missing", "live", "synthetic"):
            with tempfile.TemporaryDirectory(prefix=f"hermes-{case}-") as home:
                proc = subprocess.run(
                    [str(HERMES), str(PROBE), case, home],
                    check=False, capture_output=True, text=True, timeout=90,
                    env={**os.environ, "HERMES_HOME": home, "PYTHONDONTWRITEBYTECODE": "1"},
                )
            self.assertNotIn("vs-test-redaction-not-a-credential", proc.stdout + proc.stderr)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            summaries.append(json.loads(proc.stdout))
        self.assertEqual([item["outcome"] for item in summaries], [
            "fail_closed_missing_credential", "live_denied", "synthetic_tool_called",
        ])
        self.assertTrue(all(not item.get("catalog_payload") and not item.get("token_leaked") for item in summaries))
        out = ROOT / "review" / "hermes-auth-evidence.json"
        out.write_text(json.dumps({
            "hermes": "0.23.1",
            "live_denial_sample": "see unittest; bodies not stored",
            "unpaid_403": "UNPROVEN: VIVIDSITES_UNPAID_API_KEY unset",
            "account_scope": "UNPROVEN: no paid key and no second account",
            "free_only_connector": "not supported; tier=free without a key is authentication_required",
            "runtime": summaries,
        }, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
