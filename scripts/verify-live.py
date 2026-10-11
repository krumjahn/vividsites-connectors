#!/usr/bin/env python3
"""Read-only checks against VividSites' deployed MCP server."""
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = os.environ.get("MCP_ENDPOINT") or json.loads((ROOT / "mcp.json").read_text())["mcpServers"]["vividsites"]["url"]


def request(method, params):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = Request(ENDPOINT, json.dumps(payload).encode(), {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    with urlopen(req, timeout=30) as response:
        result = json.load(response)
    assert "error" not in result, result
    return result["result"]


def call(name, arguments, expect_error=False):
    result = request("tools/call", {"name": name, "arguments": arguments})
    assert bool(result.get("isError")) == expect_error, result
    return result, "\n".join(c.get("text", "") for c in result.get("content", []))


def main():
    init = request("initialize", {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "vividsites-plugin-check", "version": "0.1.0"},
    })
    assert init["serverInfo"]["name"] == "vividsites"
    tools = request("tools/list", {})["tools"]
    names = {t["name"] for t in tools}
    for tool in tools:
        assert tool["annotations"] == {
            "readOnlyHint": True, "destructiveHint": False, "openWorldHint": False,
        }, tool
    assert {"search_sites", "get_template_preview", "get_build_prompt",
            "search_components", "get_component", "video_prompt_formula"} <= names
    _, sites = call("search_sites", {"query": "cinematic", "tier": "free", "limit": 3})
    assert "cinematic" in sites and "free" in sites
    preview, _ = call("get_template_preview", {"slug": "cinematic"})
    assert preview["structuredContent"]["poster"].startswith("https://")
    assert preview["structuredContent"]["video"].startswith("https://")
    _, prompt = call("get_build_prompt", {"slug": "cinematic"})
    assert "BUILD PROMPT" in prompt and "https://" in prompt
    components, _ = call("search_components", {"query": "magnetic button", "limit": 2})
    assert any(i["slug"] == "magnetic-button" for i in components["structuredContent"]["items"])
    _, code = call("get_component", {"slug": "magnetic-button"})
    assert all(part in code for part in ("## HTML", "## CSS", "## JS", "npx shadcn"))
    _, formula = call("video_prompt_formula", {})
    assert "FIVE" in formula
    _, missing = call("get_component", {"slug": "nonexistent-vividsites-test"}, expect_error=True)
    assert "Unknown component" in missing
    print(f"PASS: initialization, six tools, template search/preview/prompt, component search/source, formula, unknown slug ({ENDPOINT})")


if __name__ == "__main__":
    main()
