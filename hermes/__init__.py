"""Hermes plugin: free VividSites components only."""
from __future__ import annotations

import json
from pathlib import Path

from .registry import RegistryError, get_free_component, list_free_components


def _result(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _list(args: dict, **kwargs) -> str:
    del kwargs
    try:
        query = args.get("query", "") if isinstance(args, dict) else ""
        limit = args.get("limit", 20) if isinstance(args, dict) else 20
        return _result(list_free_components(query if query is not None else "", 20 if limit is None else limit))
    except RegistryError as error:
        return _result({"error": str(error), "kind": "free_components"})


def _get(args: dict, **kwargs) -> str:
    del kwargs
    slug = args.get("slug") if isinstance(args, dict) else None
    try:
        if not isinstance(slug, str):
            raise RegistryError("slug refused")
        return _result(get_free_component(slug))
    except RegistryError as error:
        return _result({"error": str(error), "kind": "free_component"})


def register(ctx) -> None:
    skill = Path(__file__).resolve().parent / "skills" / "vividsites-library" / "SKILL.md"
    ctx.register_skill(
        "vividsites-library",
        skill,
        "Retrieve public VividSites components marked free. Does not retrieve paid templates or build prompts.",
    )
    ctx.register_tool(
        name="list_free_components",
        toolset="vividsites",
        description="List public VividSites components whose registry meta.free value is boolean true.",
        schema={
            "name": "list_free_components",
            "description": "List free VividSites components. These are components, not templates. Paid templates and build prompts are not available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Optional name or title filter."},
                    "limit": {"type": "integer", "description": "Maximum items to return, from 1 to 50."},
                },
            },
        },
        handler=_list,
    )
    ctx.register_tool(
        name="get_free_component",
        toolset="vividsites",
        description="Fetch one public VividSites component marked meta.free true.",
        schema={
            "name": "get_free_component",
            "description": "Fetch one free VividSites component by slug. Refuses unknown, unpaid, and non-component ids. Does not accept a URL.",
            "parameters": {
                "type": "object",
                "required": ["slug"],
                "properties": {
                    "slug": {"type": "string", "description": "Component slug, such as magnetic-button."},
                },
            },
        },
        handler=_get,
    )
