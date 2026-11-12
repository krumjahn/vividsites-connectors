"""VividSites tools for Hermes, with profile-scoped credentials and quota approval."""
from pathlib import Path

from .client import call_tool
from .schemas import TOOLS
from .blueprint import SCHEMA as BLUEPRINT_SCHEMA, get_website_blueprint


def _require_prompt_approval(tool_name, **kwargs):
    if tool_name in {"vividsites_get_build_prompt", "vividsites_get_website_blueprint"}:
        return {
            "action": "approve",
            "message": (
                "Retrieve this VividSites build prompt or website blueprint? Premium prompts may consume "
                "one request from your existing daily library allowance. "
                "This does not buy credits, run a build, or publish a site."
            ),
        }
    return None


def _handler(remote_name):
    def invoke(args, **kwargs):
        return call_tool(remote_name, args)
    return invoke


def register(ctx):
    for remote_name, schema in TOOLS.items():
        ctx.register_tool(
            name=schema["name"],
            toolset="vividsites",
            schema=schema,
            handler=_handler(remote_name),
        )
    ctx.register_tool(
        name=BLUEPRINT_SCHEMA["name"],
        toolset="vividsites",
        schema=BLUEPRINT_SCHEMA,
        handler=get_website_blueprint,
    )
    ctx.register_hook("pre_tool_call", _require_prompt_approval)
    ctx.register_skill(
        "vividsites-library", Path(__file__).parent / "skills/vividsites-library/SKILL.md"
    )
