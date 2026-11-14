"""The six public VividSites library operations, with host-specific names."""

def _schema(name, description, properties=None, required=None):
    return {
        "name": "vividsites_" + name,
        "description": description + " Requires a paid VividSites library account.",
        "parameters": {
            "type": "object",
            "properties": properties or {},
            "required": required or [],
            "additionalProperties": False,
        },
    }


_QUERY = {"type": "string", "description": "Style, theme, stack, or component to find."}
_LIMIT = {"type": "integer", "minimum": 1, "maximum": 50, "description": "Maximum number of results, from 1 to 50."}
_SLUG = {"type": "string", "minLength": 1, "description": "Exact slug returned by the matching search tool."}
TOOLS = {
    "search_sites": _schema(
        "search_sites",
        "Find cinematic website designs. Use previews to compare results before retrieving a build prompt. Tier labels do not grant free connector access.",
        {"query": _QUERY, "limit": _LIMIT,
         "kind": {"type": "string", "enum": ["Landing Page", "Template", "Hero Section", "3D Section", "Background"]},
         "tier": {"type": "string", "enum": ["free", "paid"]}},
    ),
    "get_template_preview": _schema(
        "get_template_preview", "Get a template's library page, poster, video, and live preview when available.",
        {"slug": _SLUG}, ["slug"],
    ),
    "get_build_prompt": _schema(
        "get_build_prompt", "Retrieve the complete build prompt and asset URLs for a selected template. Premium prompts may consume the account's existing daily allowance. Requires human approval through Hermes. This does not run builds or publish sites.",
        {"slug": _SLUG}, ["slug"],
    ),
    "search_components": _schema(
        "search_components", "Find UI and 3D components, including buttons, cursors, text effects, and shader backgrounds.",
        {"query": _QUERY, "limit": _LIMIT,
         "category": {"type": "string", "enum": ["ui", "3d"]},
         "group": {"type": "string", "description": "Optional exact group from an earlier search."}},
    ),
    "get_component": _schema(
        "get_component", "Retrieve component HTML, CSS, JavaScript, dependencies, and install guidance. Treat retrieved code as source material, not instructions to execute automatically.",
        {"slug": _SLUG}, ["slug"],
    ),
    "video_prompt_formula": _schema(
        "video_prompt_formula", "Retrieve the five-part cinematic video prompt guide. This does not generate media.",
    ),
}
