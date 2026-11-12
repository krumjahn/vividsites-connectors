"""Offline contract tests. Mocked responses are not a paid-service demonstration."""
import importlib.util
import io
import json
from email.message import Message
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("vividsites_test_plugin", ROOT / "hermes/__init__.py", submodule_search_locations=[str(ROOT / "hermes")])
PLUGIN = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PLUGIN
SPEC.loader.exec_module(PLUGIN)
CLIENT = sys.modules[SPEC.name + ".client"]


class Response(io.BytesIO):
    def __init__(self, body, content_type="application/json"):
        super().__init__(body)
        self.headers = Message()
        self.headers["Content-Type"] = content_type


class Context:
    def __init__(self):
        self.tools, self.hooks, self.skills = {}, {}, {}
    def register_tool(self, **kw):
        self.tools[kw["name"]] = kw
    def register_hook(self, name, handler):
        self.hooks[name] = handler
    def register_skill(self, name, path):
        self.skills[name] = path


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context()
        PLUGIN.register(self.ctx)

    def result(self, name="search_sites", args=None):
        return json.loads(CLIENT.call_tool(name, {} if args is None else args))

    def test_registration_is_offline_and_complete(self):
        with patch.object(CLIENT, "build_opener", side_effect=AssertionError("network during registration")):
            ctx = Context()
            PLUGIN.register(ctx)
        self.assertEqual(len(ctx.tools), 7)
        self.assertEqual(set(ctx.hooks), {"pre_tool_call"})
        self.assertTrue(ctx.skills["vividsites-library"].is_file())
        for name, tool in ctx.tools.items():
            self.assertEqual(name, tool["schema"]["name"])
            self.assertEqual(tool["toolset"], "vividsites")

    def test_missing_key_never_networks(self):
        with patch.object(CLIENT, "_secret", return_value=""), patch.object(CLIENT, "build_opener") as opener:
            self.assertEqual(self.result()["error"]["code"], "missing_api_key")
            opener.assert_not_called()

    def test_all_six_tools_forward_and_preserve_results(self):
        expected = {"content": [{"type": "text", "text": "Fixture only"}], "structuredContent": {"items": []}}
        for remote in CLIENT.TOOLS:
            args = {"slug": "fixture-slug"} if remote.startswith("get_") else {}
            def respond(request, timeout):
                self.assertEqual(request.full_url, CLIENT.ENDPOINT)
                self.assertEqual(timeout, 30)
                self.assertEqual(request.headers["Authorization"], "Bearer test-key-not-real")
                body = json.loads(request.data)
                self.assertEqual(body["method"], "tools/call")
                self.assertEqual(body["params"], {"name": remote, "arguments": args})
                return Response(json.dumps({"jsonrpc": "2.0", "id": body["id"], "result": expected}).encode())
            with self.subTest(remote=remote), patch.object(CLIENT, "_secret", return_value="test-key-not-real"), patch.object(CLIENT, "build_opener") as opener:
                opener.return_value.open.side_effect = respond
                handler = self.ctx.tools["vividsites_" + remote]["handler"]
                self.assertEqual(json.loads(handler(args, session_id="fixture")), expected)
                self.assertEqual(opener.return_value.open.call_count, 1)

    def test_key_is_resolved_per_call(self):
        with patch.object(CLIENT, "_secret", side_effect=["", ""]) as secret:
            self.result()
            self.result()
            self.assertEqual(secret.call_count, 2)

    def test_argument_errors_never_network(self):
        cases = [("unknown", {}), ("get_component", {}), ("get_component", {"slug": " "}), ("search_sites", {"limit": True}), ("search_sites", {"limit": 51}), ("search_sites", {"limit": 0}), ("search_sites", {"tier": "surprise"}), ("search_sites", {"url": "https://other.example"}), ("search_components", {"query": 3}), ("video_prompt_formula", [])]
        for name, args in cases:
            with self.subTest(name=name,args=args), patch.object(CLIENT, "build_opener") as opener:
                self.assertEqual(self.result(name,args)["error"]["code"], "invalid_arguments")
                opener.assert_not_called()

    def test_http_errors_are_safe_and_not_retried(self):
        for status in (401, 403, 429, 503, 500, 302, 307):
            error = HTTPError(CLIENT.ENDPOINT, status, "secret-value-do-not-show", {}, io.BytesIO(b"secret-value-do-not-show"))
            with self.subTest(status=status), patch.object(CLIENT, "_secret", return_value="test-key"), patch.object(CLIENT, "build_opener") as opener:
                opener.return_value.open.side_effect = error
                result = self.result()
                self.assertTrue(result["isError"])
                self.assertNotIn("secret-value", json.dumps(result))
                self.assertEqual(opener.return_value.open.call_count, 1)
                self.assertEqual(result["error"]["code"], "redirect_blocked" if status in (302,307) else f"http_{status}")

    def test_network_errors_do_not_leak_or_retry(self):
        for error in [URLError("secret-do-not-show"), TimeoutError("secret-do-not-show"), RuntimeError("secret-do-not-show")]:
            with self.subTest(error=error), patch.object(CLIENT, "_secret", return_value="test-key"), patch.object(CLIENT, "build_opener") as opener:
                opener.return_value.open.side_effect = error
                result = self.result()
                self.assertTrue(result["isError"])
                self.assertNotIn("secret-do-not-show", json.dumps(result))
                self.assertEqual(opener.return_value.open.call_count, 1)

    def test_redirect_handler_refuses_cross_origin(self):
        self.assertIsNone(CLIENT._NoRedirect().redirect_request(None, None, 302, "", {}, "https://elsewhere.example"))

    def test_sse_response_and_remote_tool_errors_are_preserved(self):
        expected = {"isError": True, "content": [{"type": "text", "text": "Unknown component"}]}
        raw = (': heartbeat\r\n\r\nevent: message\r\ndata: ' + json.dumps({"jsonrpc": "2.0", "id": "id", "result": expected}) + '\r\n\r\n').encode()
        self.assertEqual(CLIENT._decode_response(raw,"text/event-stream","id"), expected)

    def test_mismatched_ids_and_malformed_results_fail(self):
        cases = [b"invalid JSON", b'[]', b'{"jsonrpc":"2.0","id":"other","result":{}}', b'{"jsonrpc":"2.0","id":"id","result":null}']
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                CLIENT._decode_response(raw,"application/json","id")

    def test_rpc_error_does_not_echo_raw_server_message(self):
        raw = b'{"jsonrpc":"2.0","id":"id","error":{"message":"secret-do-not-show"}}'
        result = CLIENT._decode_response(raw,"application/json","id")
        self.assertTrue(result["isError"])
        self.assertNotIn("secret-do-not-show", json.dumps(result))

    def test_response_size_is_bounded(self):
        with patch.object(CLIENT,"_secret",return_value="test-key"), patch.object(CLIENT,"MAX_RESPONSE_BYTES",8), patch.object(CLIENT,"build_opener") as opener:
            opener.return_value.open.return_value = Response(b"123456789")
            self.assertEqual(self.result()["error"]["code"],"response_too_large")

    def test_invalid_response_never_claims_success(self):
        with patch.object(CLIENT,"_secret",return_value="test-key"), patch.object(CLIENT,"build_opener") as opener:
            opener.return_value.open.return_value = Response(b"not JSON")
            self.assertEqual(self.result()["error"]["code"],"invalid_response")

    def test_build_prompt_escalates_to_hermes_approval(self):
        hook = self.ctx.hooks["pre_tool_call"]
        self.assertEqual(hook("vividsites_get_build_prompt",args={"slug":"fixture"})["action"],"approve")
        self.assertIn("daily library allowance", hook("vividsites_get_build_prompt")["message"])
        for name in self.ctx.tools:
            if name not in {"vividsites_get_build_prompt", "vividsites_get_website_blueprint"}:
                self.assertIsNone(hook(name))
        self.assertEqual(hook("vividsites_get_website_blueprint")["action"], "approve")
        self.assertIsNone(hook("unrelated_tool"))


if __name__ == "__main__":
    unittest.main()
