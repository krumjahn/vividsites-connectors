"""Blueprint orchestration tests. All service responses here are fixtures."""
import json
import sys
import unittest
from unittest.mock import patch

from test_plugin import PLUGIN

BLUEPRINT = sys.modules[PLUGIN.__name__ + ".blueprint"]


class BlueprintTests(unittest.TestCase):
    def result(self, args=None):
        return json.loads(BLUEPRINT.get_website_blueprint({"template_slug": "cinematic"} if args is None else args))

    def test_complete_sources_are_preserved_and_prompt_is_requested_once_last(self):
        responses = []

        def remote(name, args):
            value = {"content": [{"type": "text", "text": "UNABRIDGED " + name + "\nhttps://assets.example/film.mp4"}],
                     "structuredContent": {"slug": args["slug"], "fixture": True}}
            responses.append(value)
            return json.dumps(value)

        with patch.object(BLUEPRINT, "call_tool", side_effect=remote) as call:
            result = self.result({"template_slug": "cinematic", "component_slugs": ["magnetic-button", "blur-text"]})
        self.assertEqual([c.args[0] for c in call.call_args_list], ["get_template_preview", "get_component", "get_component", "get_build_prompt"])
        self.assertEqual(result["preview"], responses[0])
        self.assertEqual(result["components"][0]["source"], responses[1])
        self.assertEqual(result["components"][1]["source"], responses[2])
        self.assertEqual(result["build_prompt"], responses[3])
        self.assertIn("No website has been built", result["status"])
        self.assertNotIn("isError", result)

    def test_no_components_needs_only_two_calls(self):
        with patch.object(BLUEPRINT, "call_tool", return_value='{"content":[{"type":"text","text":"fixture"}]}') as call:
            result = self.result()
        self.assertEqual(call.call_count, 2)
        self.assertEqual(result["components"], [])

    def test_bad_arguments_never_call_service(self):
        bad = [[], None, {}, {"template_slug": "../secret"}, {"template_slug": "https://example.com"},
               {"template_slug": "x" * 101}, {"template_slug": "x", "brief": "unrecognized"},
               {"template_slug": "x", "component_slugs": "button"}, {"template_slug": "x", "component_slugs": ["x", "x"]},
               {"template_slug": "x", "component_slugs": ["a", "b", "c"]}, {"template_slug": "x", "component_slugs": [None]},
               {"template_slug": "x", "component_slugs": [["x"]]}]
        for args in bad:
            with self.subTest(args=args), patch.object(BLUEPRINT, "call_tool") as call:
                result = json.loads(BLUEPRINT.get_website_blueprint(args))
                self.assertEqual(result["error"]["code"], "invalid_arguments")
                call.assert_not_called()

    def test_read_failure_never_spends_prompt_allowance(self):
        good = '{"content":[{"type":"text","text":"preview fixture"}]}'
        failure = '{"isError":true,"error":{"code":"http_403","message":"paid plan required"}}'
        for responses, expected in [([failure], "preview"), ([good, failure], "component:button")]:
            with self.subTest(expected=expected), patch.object(BLUEPRINT, "call_tool", side_effect=responses) as call:
                result = self.result({"template_slug": "cinematic", "component_slugs": ["button"]})
            self.assertTrue(result["isError"])
            self.assertEqual(result["failed_step"], expected)
            self.assertFalse(result["build_prompt_request_attempted"])
            self.assertNotIn("get_build_prompt", [c.args[0] for c in call.call_args_list])

    def test_prompt_timeout_does_not_retry_or_claim_success(self):
        responses = ['{"content":[{"type":"text","text":"preview"}]}',
                     '{"isError":true,"error":{"code":"connection_error","message":"timeout"}}']
        with patch.object(BLUEPRINT, "call_tool", side_effect=responses) as call:
            result = self.result()
        self.assertEqual(call.call_count, 2)
        self.assertTrue(result["build_prompt_request_attempted"])
        self.assertTrue(result["isError"])
        self.assertEqual(result["completed_steps"], ["preview"])
        self.assertEqual(result["failed_step"], "build_prompt")
        self.assertIn("Check account allowance", result["next_step"])

    def test_remote_text_error_and_empty_or_malformed_response_fail_closed(self):
        for response in ['{"isError":true,"content":[{"type":"text","text":"unknown slug"}]}', '{}', '[]', 'null', 'broken', '{"content":[]}',
                         '{"content":"bad shape"}', '{"content":[{}]}', '{"structuredContent":true}',
                         '{"content":[{"type":"text","text":23}]}', '{"content":[{"type":"text","text":" "}]}']:
            with self.subTest(response=response), patch.object(BLUEPRINT, "call_tool", return_value=response) as call:
                result = self.result()
            self.assertTrue(result["isError"])
            self.assertFalse(result["build_prompt_request_attempted"])
            self.assertEqual(call.call_count, 1)

    def test_size_limit_stops_before_prompt_without_truncating(self):
        with patch.object(BLUEPRINT, "MAX_BLUEPRINT_BYTES", 5), patch.object(BLUEPRINT, "call_tool", return_value='{"content":[{"type":"text","text":"large fixture"}]}') as call:
            result = self.result()
        self.assertEqual(result["error"]["code"], "blueprint_too_large")
        self.assertFalse(result["build_prompt_request_attempted"])
        self.assertEqual(call.call_count, 1)

    def test_size_limit_after_prompt_reports_consumption_uncertainty(self):
        responses = ['{"content":[{"type":"text","text":"small"}]}', json.dumps({"content": [{"type": "text", "text": "x" * 300}]})]
        with patch.object(BLUEPRINT, "MAX_BLUEPRINT_BYTES", 150), patch.object(BLUEPRINT, "call_tool", side_effect=responses) as call:
            result = self.result()
        self.assertEqual(result["error"]["code"], "blueprint_too_large")
        self.assertTrue(result["build_prompt_request_attempted"])
        self.assertEqual(call.call_count, 2)


if __name__ == "__main__":
    unittest.main()
