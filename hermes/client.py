"""Bounded stdlib MCP client for VividSites' stateless Streamable HTTP service.

The service accepts standalone tools/call requests (see scripts/verify-live.py).
No credentials are stored or cached, and no redirects or automatic retries occur.
"""
from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4

from .schemas import TOOLS

ENDPOINT = "https://www.vividsites.app/api/connector"
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
TIMEOUT_SECONDS = 30


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A redirect must never forward the user's Authorization header.
        return None


def _secret():
    # Resolve on every call so multiplexed Hermes profiles never share a key.
    from agent.secret_scope import get_secret
    return (get_secret("VIVIDSITES_API_KEY") or "").strip()


def _error(code, message):
    return json.dumps({"isError": True, "error": {"code": code, "message": message}})


def _validate_arguments(name, arguments):
    if name not in TOOLS:
        raise ValueError("Unknown VividSites tool.")
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object.")
    params = TOOLS[name]["parameters"]
    if set(arguments) - set(params["properties"]):
        raise ValueError("Unrecognized tool argument.")
    for field in params["required"]:
        if field not in arguments:
            raise ValueError(f"Missing required argument: {field}.")
    for field, value in arguments.items():
        spec = params["properties"][field]
        if spec["type"] == "string":
            if not isinstance(value, str) or (spec.get("minLength") and not value.strip()):
                raise ValueError(f"{field} must be a non-empty string." if spec.get("minLength") else f"{field} must be a string.")
        elif type(value) is not int or not spec["minimum"] <= value <= spec["maximum"]:
            raise ValueError(f"{field} must be an integer from 1 to 50.")
        if "enum" in spec and value not in spec["enum"]:
            raise ValueError(f"Unsupported value for {field}.")


def _decode_response(raw, content_type, request_id):
    text = raw.decode("utf-8")
    if content_type == "text/event-stream":
        messages = []
        for event in text.replace("\r\n", "\n").split("\n\n"):
            data = "\n".join(line[5:].lstrip(" ") for line in event.splitlines() if line.startswith("data:"))
            if data:
                messages.append(json.loads(data))
    elif content_type == "application/json":
        messages = [json.loads(text)]
    else:
        raise ValueError("Unsupported response content type.")
    for message in messages:
        if isinstance(message, dict) and message.get("id") == request_id and message.get("jsonrpc") == "2.0":
            if "error" in message:
                return {"isError": True, "error": {"code": "mcp_error", "message": "VividSites rejected the request. Check the supplied tool arguments and account access."}}
            result = message.get("result")
            if isinstance(result, dict):
                return result
    raise ValueError("No matching MCP response.")


def call_tool(name, arguments):
    try:
        _validate_arguments(name, arguments)
    except ValueError as exc:
        return _error("invalid_arguments", str(exc))
    try:
        key = _secret()
        if not key:
            return _error("missing_api_key", "Configure VIVIDSITES_API_KEY through Hermes using a paid-account key from https://www.vividsites.app/mcp. Do not paste it into chat.")
        request_id = str(uuid4())
        payload = {"jsonrpc": "2.0", "id": request_id, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
        request = Request(ENDPOINT, json.dumps(payload).encode("utf-8"), {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": "Bearer " + key,
            "User-Agent": "vividsites-hermes/1.0.0",
        }, method="POST")
        with build_opener(_NoRedirect()).open(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                return _error("response_too_large", "VividSites returned more than the 8 MiB response limit. Narrow the request.")
            result = _decode_response(raw, response.headers.get_content_type(), request_id)
        return json.dumps(result, ensure_ascii=False)
    except HTTPError as exc:
        messages = {
            401: "The VividSites API key is invalid or revoked. Update it in Hermes credential settings.",
            403: "An active paid VividSites library plan is required. Create credits alone do not grant library access.",
            429: "VividSites rejected the request due to a rate or allowance limit. Check the account before retrying.",
            503: "VividSites could not verify access right now. Try again later.",
        }
        if 300 <= exc.code < 400:
            return _error("redirect_blocked", "VividSites redirected the request. No credentials were forwarded; update the plugin only after reviewing the endpoint change.")
        return _error("http_" + str(exc.code), messages.get(exc.code, "VividSites returned an HTTP error. No automatic retry was attempted."))
    except (URLError, TimeoutError, OSError):
        return _error("connection_error", "Could not complete the VividSites request. No automatic retry was attempted; check allowance usage before retrying a build prompt.")
    except (ValueError, UnicodeError):
        return _error("invalid_response", "VividSites returned an unexpected response. No automatic retry was attempted.")
    except Exception:
        # Never leak a secret or server body through exception text into a chat.
        return _error("client_error", "The VividSites request could not be completed. Check Hermes and plugin versions.")
