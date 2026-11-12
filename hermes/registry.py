"""Free VividSites components from the public registry.

Only items whose meta.free value is the boolean true are readable. Missing,
false, or any other classification is refused. Callers pass a slug, never a
URL. Redirects are refused. This module does not call the paid connector.
"""
from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

HOST = "www.vividsites.app"
REGISTRY_PATH = "/r/registry.json"
MAX_BYTES = 1_000_000
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
USER_AGENT = "vividsites-hermes-free/1.2.0"


class RegistryError(Exception):
    """Fail closed. The message is safe to show; it contains no response body."""


class _RefuseRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RegistryError("redirect refused")


def _allowed_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        raise RegistryError("host refused")
    if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
        raise RegistryError("url refused")
    if parsed.path not in {REGISTRY_PATH} and not _component_path(parsed.path):
        raise RegistryError("path refused")
    return f"https://{HOST}{parsed.path}"


def _component_path(path: str) -> str | None:
    prefix, suffix = "/r/", ".json"
    if not (path.startswith(prefix) and path.endswith(suffix)):
        return None
    slug = path[len(prefix):-len(suffix)]
    if path != f"{prefix}{slug}{suffix}" or not SLUG_RE.fullmatch(slug):
        return None
    return slug


def component_url(slug: str) -> str:
    if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug) or len(slug) > 64:
        raise RegistryError("slug refused")
    return _allowed_url(f"https://{HOST}/r/{slug}.json")


def fetch_json(url: str) -> dict:
    exact = _allowed_url(url)
    opener = build_opener(_RefuseRedirect)
    request = Request(exact, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=20) as response:
            final = urlsplit(response.geturl())
            if response.geturl() != exact or final.scheme != "https" or final.hostname != HOST:
                raise RegistryError("response url refused")
            if final.path != urlsplit(exact).path or final.query or final.fragment:
                raise RegistryError("response path refused")
            body = response.read(MAX_BYTES + 1)
    except RegistryError:
        raise
    except HTTPError as error:
        raise RegistryError(f"registry http {error.code}") from None
    except (URLError, TimeoutError, OSError):
        raise RegistryError("registry unreachable") from None
    if len(body) > MAX_BYTES:
        raise RegistryError("response too large")
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, UnicodeError):
        raise RegistryError("registry json refused") from None
    if not isinstance(data, dict):
        raise RegistryError("registry json refused")
    return data


def classification(item: object) -> str:
    """Return free, not_free, or unknown. Only boolean true is free."""
    if not isinstance(item, dict):
        return "unknown"
    meta = item.get("meta")
    if not isinstance(meta, dict) or "free" not in meta or type(meta.get("free")) is not bool:
        return "unknown"
    return "free" if meta.get("free") is True else "not_free"


def _items(registry: dict) -> list[dict]:
    items = registry.get("items")
    if not isinstance(items, list):
        raise RegistryError("registry shape refused")
    return [item for item in items if isinstance(item, dict)]


def free_index(registry: dict | None = None) -> list[dict]:
    document = registry if registry is not None else fetch_json(f"https://{HOST}{REGISTRY_PATH}")
    free = []
    for item in _items(document):
        if classification(item) != "free":
            continue
        name = item.get("name")
        if not isinstance(name, str) or len(name) > 64 or not SLUG_RE.fullmatch(name):
            continue
        meta = item["meta"]
        free.append({
            "name": name,
            "title": item.get("title") if isinstance(item.get("title"), str) else name,
            "category": meta.get("category") if isinstance(meta.get("category"), str) else "",
            "group": meta.get("group") if isinstance(meta.get("group"), str) else "",
            "free": True,
            "kind": "component",
        })
    return free


def list_free_components(query: str = "", limit: int = 20, registry: dict | None = None) -> dict:
    if not isinstance(query, str) or len(query) > 80 or any(char in query for char in "/\\:?#"):
        raise RegistryError("query refused")
    if type(limit) is not int or not 1 <= limit <= 50:
        raise RegistryError("limit refused")
    needle = query.casefold().strip()
    matches = [
        item for item in free_index(registry)
        if not needle or needle in item["name"].casefold() or needle in item["title"].casefold()
    ]
    return {"kind": "free_components", "count": len(matches), "items": matches[:limit]}


def get_free_component(slug: str, registry: dict | None = None, fetcher=fetch_json) -> dict:
    url = component_url(slug)
    index = free_index(registry)
    if not any(item["name"] == slug for item in index):
        raise RegistryError("not a free component")
    if registry is not None:
        documents = registry.get("_documents")
        document = documents.get(slug) if isinstance(documents, dict) else None
    else:
        document = fetcher(url)
    if not isinstance(document, dict):
        raise RegistryError("component document refused")
    if document.get("name") != slug or classification(document) != "free":
        raise RegistryError("component classification refused")
    files = []
    for entry in document.get("files") or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        content = entry.get("content")
        if not isinstance(path, str) or not isinstance(content, str):
            continue
        if path.startswith(("/", "\\")) or "\\" in path or ":" in path or ".." in path.split("/"):
            raise RegistryError("component path refused")
        files.append({"path": path, "content": content})
    if not files:
        raise RegistryError("component content refused")
    meta = document["meta"]
    return {
        "kind": "free_component",
        "name": slug,
        "title": document.get("title") if isinstance(document.get("title"), str) else slug,
        "free": True,
        "category": meta.get("category") if isinstance(meta.get("category"), str) else "",
        "group": meta.get("group") if isinstance(meta.get("group"), str) else "",
        "files": files,
    }
