"""Keyless public components, kept separate from authenticated library tools."""
import json

from .registry import RegistryError, get_free_component, list_free_components


def _list(args, **kwargs):
    del kwargs
    try:
        if not isinstance(args, dict) or set(args) - {"query", "limit"}:
            raise RegistryError("expected query and limit only")
        return json.dumps(list_free_components(args.get("query", ""), args.get("limit", 20)), ensure_ascii=False)
    except RegistryError as exc:
        return json.dumps({"isError": True, "kind": "free_components", "error": str(exc)})


def _get(args, **kwargs):
    del kwargs
    try:
        if not isinstance(args, dict) or set(args) != {"slug"}:
            raise RegistryError("expected one component slug")
        return json.dumps(get_free_component(args["slug"]), ensure_ascii=False)
    except RegistryError as exc:
        return json.dumps({"isError": True, "kind": "free_component", "error": str(exc)})


def register_free_tools(ctx):
    for name, description, properties, required, handler in [
        ("list_free_components", "Search genuinely free public VividSites components. No account or key required. These are components, not full website templates.",
         {"query": {"type": "string", "maxLength": 80, "description": "Component name or title to find."},
          "limit": {"type": "integer", "minimum": 1, "maximum": 50}}, [], _list),
        ("get_free_component", "Get a public VividSites component only when the index and document both mark meta.free as boolean true. No key required. Does not retrieve templates or build prompts.",
         {"slug": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 64,
                   "description": "Exact component name from list_free_components."}}, ["slug"], _get),
    ]:
        ctx.register_tool(
            name=name, toolset="vividsites", description=description,
            schema={"name": name, "description": description, "parameters": {
                "type": "object", "properties": properties, "required": required, "additionalProperties": False,
            }}, handler=handler,
        )
