"""Public component access stays available independently of the paid connector."""
import io
import json
import sys
import unittest
from unittest.mock import patch
from urllib.error import URLError

from test_plugin import PLUGIN, CLIENT, Context

REGISTRY = sys.modules[PLUGIN.__name__ + ".registry"]
FREE = sys.modules[PLUGIN.__name__ + ".free_tools"]


def item(name="magnetic-button", free=True):
    return {"name": name, "title": "Magnetic Button", "meta": {"free": free}}


def document(free=True, path="components/button.html"):
    return {**item(free=free), "files": [{"path": path, "content": "<button>Real fixture source</button>"}]}


class FreeToolsTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context()
        PLUGIN.register(self.ctx)

    def call(self, name, args):
        return json.loads(self.ctx.tools[name]["handler"](args))

    def test_registration_and_free_calls_never_resolve_a_key_or_call_paid_service(self):
        with patch.object(CLIENT, "_secret", side_effect=AssertionError("free must not read a key")), \
             patch.object(CLIENT, "build_opener", side_effect=AssertionError("paid connector called")), \
             patch.object(REGISTRY, "fetch_json", return_value={"items": [item()]}) as public, \
             patch.object(FREE, "get_free_component", return_value=document()) as get:
            self.assertEqual(self.call("list_free_components", {"query": "magnetic"})["count"], 1)
            self.assertEqual(self.call("get_free_component", {"slug": "magnetic-button"})["name"], "magnetic-button")
            public.assert_called_once()
            get.assert_called_once_with("magnetic-button")

    def test_only_boolean_true_is_free(self):
        for flag, expected in [(True, "free"), (False, "not_free"), ("true", "unknown"), (1, "unknown"), (None, "unknown")]:
            with self.subTest(flag=flag):
                self.assertEqual(REGISTRY.classification(item(free=flag)), expected)
        self.assertEqual(REGISTRY.classification({"meta": {}}), "unknown")

    def test_unclassified_or_paid_records_are_not_fetched(self):
        index = {"items": [item("paid-widget", False), item("unknown-widget", None), item()]}
        for slug in ("paid-widget", "unknown-widget", "cinematic", "../secret", "https://evil.example/a", ""):
            with self.subTest(slug=slug), patch.object(REGISTRY, "fetch_json") as fetch:
                with self.assertRaises(REGISTRY.RegistryError):
                    REGISTRY.get_free_component(slug, registry=index, fetcher=fetch)
                fetch.assert_not_called()

    def test_document_rechecks_free_flag_and_source_paths(self):
        for flag, path in [(False, "good.html"), ("true", "good.html"), (True, "../secret"),
                           (True, "..\\secret"), (True, "C:/secret"), (True, "/secret")]:
            with self.subTest(flag=flag,path=path):
                with self.assertRaises(REGISTRY.RegistryError):
                    REGISTRY.get_free_component("magnetic-button", registry={"items": [item()], "_documents": {"magnetic-button": document(flag, path)}})
        result = REGISTRY.get_free_component("magnetic-button", registry={"items": [item()], "_documents": {"magnetic-button": document()}})
        self.assertTrue(result["free"])
        self.assertEqual(result["files"][0]["content"], "<button>Real fixture source</button>")

    def test_invalid_tool_arguments_fail_before_public_network(self):
        cases = [("list_free_components", []), ("list_free_components", {"url": "x"}), ("list_free_components", {"limit": True}),
                 ("list_free_components", {"query": None}), ("get_free_component", {}), ("get_free_component", {"slug": "../secret"}),
                 ("get_free_component", {"slug": "x", "extra": 1})]
        for name, args in cases:
            with self.subTest(name=name,args=args), patch.object(REGISTRY, "fetch_json") as fetch:
                self.assertTrue(self.call(name,args)["isError"])
                fetch.assert_not_called()

    def test_public_requests_have_no_authorization_header(self):
        class Response(io.BytesIO):
            def geturl(self):
                return "https://www.vividsites.app/r/registry.json"
        with patch.object(REGISTRY,"build_opener") as opener:
            opener.return_value.open.return_value = Response(b'{"items":[]}')
            REGISTRY.fetch_json("https://www.vividsites.app/r/registry.json")
        request = opener.return_value.open.call_args.args[0]
        self.assertIsNone(request.get_header("Authorization"))

    def test_redirects_and_network_failures_are_safe(self):
        with self.assertRaises(REGISTRY.RegistryError):
            REGISTRY._RefuseRedirect().redirect_request(None,None,302,"",{},"https://elsewhere.example")
        for error in (TimeoutError("do not expose"), URLError("do not expose")):
            with self.subTest(error=error), patch.object(REGISTRY,"build_opener") as opener:
                opener.return_value.open.side_effect=error
                with self.assertRaisesRegex(REGISTRY.RegistryError,"registry unreachable"):
                    REGISTRY.fetch_json("https://www.vividsites.app/r/registry.json")

    def test_paid_missing_key_has_free_next_step_but_no_automatic_fallback(self):
        with patch.object(CLIENT,"_secret",return_value=""), patch.object(CLIENT,"build_opener") as paid, patch.object(REGISTRY,"fetch_json") as public:
            result=self.call("vividsites_search_sites",{"query":"architecture"})
        self.assertEqual(result["error"]["code"],"missing_api_key")
        self.assertIn("list_free_components",result["error"]["message"])
        paid.assert_not_called()
        public.assert_not_called()

    def test_free_tools_are_never_quota_gated(self):
        for name in ("list_free_components", "get_free_component"):
            self.assertIsNone(self.ctx.hooks["pre_tool_call"](name))


if __name__ == "__main__":
    unittest.main()
