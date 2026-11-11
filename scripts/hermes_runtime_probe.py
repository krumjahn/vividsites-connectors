#!/usr/bin/env python3
"""Load the Hermes package through Hermes 0.23.1 and record redacted outcomes.

Cases:
  missing  No VIVIDSITES_API_KEY. Hermes must fail closed before a request.
  live     A non-credential token against https://www.vividsites.app/api/connector.
  synthetic  Local MCP fixture. Not the VividSites catalog.

The process token is never printed. Evidence is status, error class, and whether
a catalog payload appeared.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import socket
import sys
import threading
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "hermes"
TOKEN = os.environ.get("HERMES_PROBE_TOKEN", "vs-test-redaction-not-a-credential")
LIVE_URL = "https://www.vividsites.app/api/connector"
SYNTHETIC_MARKER = "SYNTHETIC_FIXTURE_NOT_A_VIVIDSITES_CATALOG"


def redact(text: str) -> str:
    return text.replace(TOKEN, "[REDACTED]")


class Capture(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.lines.append(redact(self.format(record)))


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def prepare_home(home: Path, *, url: str | None = None) -> None:
    plugin_dir = home / "plugins" / "vividsites"
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
    shutil.copytree(PLUGIN, plugin_dir, ignore=shutil.ignore_patterns("__pycache__"))
    if url is not None:
        mcp_path = plugin_dir / "mcp.json"
        mcp = json.loads(mcp_path.read_text())
        mcp["mcpServers"]["vividsites"]["url"] = url
        mcp_path.write_text(json.dumps(mcp, indent=2) + "\n")
    (home / "config.yaml").write_text(
        "plugins:\n  enabled:\n    - vividsites\n",
        encoding="utf-8",
    )


def start_synthetic(port: int, token: str) -> threading.Thread:
    from mcp.server.mcpserver import MCPServer
    import uvicorn

    from mcp.types import ToolAnnotations

    server = MCPServer("synthetic-vividsites-fixture")

    @server.tool(
        annotations=ToolAnnotations(
            read_only_hint=True, destructive_hint=False, open_world_hint=False,
        )
    )
    def synthetic_status() -> str:
        """Return a fixed local marker. This is not a VividSites catalog result."""
        return SYNTHETIC_MARKER

    app = server.streamable_http_app(
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
        host="127.0.0.1",
    )

    async def guarded(scope, receive, send):
        if scope.get("type") == "http":
            headers = {key.decode().lower(): value.decode() for key, value in scope.get("headers", [])}
            if headers.get("authorization") != f"Bearer {token}":
                body = b'{"error":"synthetic_unauthorized","fixture":true}'
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
                })
                await send({"type": "http.response.body", "body": body})
                return
        await app(scope, receive, send)

    config = uvicorn.Config(guarded, host="127.0.0.1", port=port, log_level="warning")
    thread = threading.Thread(target=uvicorn.Server(config).run, name="synthetic-mcp", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return thread
        except OSError:
            time.sleep(0.05)
    raise RuntimeError("synthetic MCP server did not listen")


def run_discovery(home: Path, token: str | None, case_name: str) -> dict:
    os.environ["HERMES_HOME"] = str(home)
    os.environ.pop("HERMES_SAFE_MODE", None)
    if token is None:
        os.environ.pop("VIVIDSITES_API_KEY", None)
        env_file = home / ".env"
        if env_file.exists():
            env_file.unlink()
    else:
        os.environ["VIVIDSITES_API_KEY"] = token
        (home / ".env").write_text(f"VIVIDSITES_API_KEY={token}\n", encoding="utf-8")

    capture = Capture()
    capture.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
    root = logging.getLogger()
    root.addHandler(capture)
    root.setLevel(logging.INFO)

    from hermes_cli.plugins import get_plugin_manager
    from tools.mcp_tool import _server_connect_errors
    from tools.mcp_tool_discovery import discover_mcp_tools
    from tools.registry import registry

    # A previous case in this process must not satisfy discovery.
    get_plugin_manager().discover_and_load(force=True)
    tools = discover_mcp_tools()
    invocation = None
    synthetic_tools = [name for name in tools if name.endswith("synthetic_status")]
    if case_name == "synthetic" and synthetic_tools:
        raw = registry.dispatch(synthetic_tools[0], {})
        text = raw if isinstance(raw, str) else json.dumps(raw)
        invocation = {
            "tool": synthetic_tools[0],
            "marker": SYNTHETIC_MARKER in text,
            "length": len(text),
        }
    errors = {str(key): redact(str(value)) for key, value in _server_connect_errors.items()}
    loaded = [
        {"name": row["name"], "enabled": row["enabled"], "error": redact(str(row.get("error") or ""))}
        for row in get_plugin_manager().list_plugins()
        if row["name"] == "vividsites"
    ]
    text = "\n".join(capture.lines)
    catalog_markers = [marker for marker in ("BUILD PROMPT", "magnetic-button", "## HTML", "FIVE") if marker in text]
    return {
        "tools": tools,
        "connect_errors": errors,
        "loaded": loaded,
        "log_tail": capture.lines[-30:],
        "token_leaked": TOKEN in "\n".join(capture.lines) or TOKEN in json.dumps(errors),
        "catalog_markers": catalog_markers,
        "invocation": invocation,
    }


def classify(case: str, result: dict) -> dict:
    blob = json.dumps(result)
    if case == "missing":
        closed = "not set" in blob or "VIVIDSITES_API_KEY" in blob and "missing" in blob.lower()
        # The fail-closed message names ${VIVIDSITES_API_KEY}.
        closed = "is not set" in blob
        return {
            "case": case,
            "runtime": "hermes",
            "target": "no request" if closed else "unknown",
            "outcome": "fail_closed_missing_credential" if closed else "unexpected",
            "catalog_payload": bool(result["catalog_markers"]) or bool(result["tools"]),
            "token_leaked": result["token_leaked"],
            "detail": result["connect_errors"] or result["log_tail"][-8:],
        }
    if case == "live":
        denied = any(token in blob.lower() for token in ("401", "invalid_api_key", "authentication_required", "unauthorized"))
        return {
            "case": case,
            "runtime": "hermes",
            "target": LIVE_URL,
            "outcome": "live_denied" if denied and not result["tools"] else "unexpected",
            "catalog_payload": bool(result["catalog_markers"]) or bool(result["tools"]),
            "token_leaked": result["token_leaked"],
            "detail": result["connect_errors"] or result["log_tail"][-8:],
        }
    invoked = result.get("invocation") or {}
    return {
        "case": case,
        "runtime": "hermes",
        "target": "127.0.0.1 synthetic fixture",
        "outcome": "synthetic_tool_called" if invoked.get("marker") else "synthetic_failed",
        "invocation": invoked,
        "tool_names": result["tools"],
        "catalog_payload": bool(result["catalog_markers"]),
        "token_leaked": result["token_leaked"],
        "detail": result["connect_errors"] or result["log_tail"][-8:],
    }


def main() -> int:
    case = sys.argv[1]
    home = Path(sys.argv[2])
    home.mkdir(parents=True, exist_ok=True)
    if case == "synthetic":
        port = free_port()
        start_synthetic(port, TOKEN)
        prepare_home(home, url=f"http://127.0.0.1:{port}/mcp")
        result = run_discovery(home, TOKEN, case)
    elif case == "live":
        prepare_home(home)
        result = run_discovery(home, TOKEN, case)
    elif case == "missing":
        prepare_home(home)
        result = run_discovery(home, None, case)
    else:
        raise SystemExit(f"unknown case {case}")
    summary = classify(case, result)
    sys.stdout.write(redact(json.dumps(summary, indent=2)) + "\n")
    if summary.get("token_leaked") or summary.get("catalog_payload"):
        return 2
    if summary["outcome"] in {"unexpected", "synthetic_failed"}:
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        sys.stdout.write(redact(traceback.format_exc()))
        raise SystemExit(1)
