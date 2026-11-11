"""VividSites tools for Hermes, with profile-scoped credentials and quota approval."""
from pathlib import Path

from .client import call_tool
from .schemas import TOOLS


def _require_prompt_approval(tool_name, **kwargs):
    if tool_name == "vividsites_get_build_prompt":
        return {
            "action": "approve",
            "message": (
                "Retrieve this VividSites build prompt? Premium prompts may consume "
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
    ctx.register_hook("pre_tool_call", _require_prompt_approval)
    ctx.register_skill(
        "vividsites-library", Path(__file__).parent / "skills/vividsites-library/SKILL.md"
    )
