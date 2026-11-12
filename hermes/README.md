# VividSites for Hermes

Search cinematic website templates, compare previews, retrieve complete build prompts, and get editable UI or 3D component code directly from Hermes.

Ask Hermes: **“Use VividSites to build a beautiful cinematic website for my architecture studio. Choose a design, adapt it to my content, and show me the finished preview.”**

Hermes searches real designs, retrieves a complete website blueprint, and uses its normal project tools to implement and check the result. You do not need to orchestrate each library call. The plugin supplies design sources; Hermes performs the build. A VividSites catalog preview is never presented as your generated website.

**Every tool requires a personal API key and a paid VividSites library account.** Your AI assistant subscription and VividSites Create credits do not include library access. Legacy `free` catalog labels describe assets, not connector eligibility.

## Install

Requires Hermes 0.23.1 or newer. This package lives in the `hermes/` subdirectory so existing Claude, Cursor, Gemini, and portable manifests remain unchanged.

This paid-library version is currently on the prerelease branch, not the default branch or the approved Hermes catalog. Install the branch explicitly:

```sh
hermes plugins install krumjahn/vividsites-connectors/hermes --ref feat/hermes-plugin-hackathon-2026
hermes plugins enable vividsites
```

For a reproducible install, replace the branch after `--ref` with the full 40-character commit SHA you reviewed. Do not use `hermes plugins install vividsites` until maintainers have admitted a catalog entry for this version. The existing free-component catalog proposal is a different, more limited implementation.

Get your personal key at [VividSites MCP setup](https://www.vividsites.app/mcp). Hermes prompts for `VIVIDSITES_API_KEY` using its secret input. Configure it through Hermes, never in chat or a committed file. Restart the Hermes session after enabling the plugin. Installing this package does not purchase a VividSites plan. [Plans](https://www.vividsites.app/pricing).

For a local review, run `hermes plugins validate /absolute/path/to/hermes --install-deps` and `hermes plugins doctor /absolute/path/to/hermes --ci` before installing. Do not confuse the repository's root portable package with this native Hermes package.

## Try it

- “Find three cinematic website templates and show me their previews.”
- “Get the complete build prompt for the template I chose.”
- “Find a magnetic button and show its HTML, CSS, and JavaScript.”
- “Build a cinematic architecture website using the best matching template and a magnetic button.”

The plugin exposes seven tools:

| Tool | Result |
| --- | --- |
| `vividsites_search_sites` | Ranked template matches |
| `vividsites_get_template_preview` | Library page, poster, video, and live preview when present |
| `vividsites_get_build_prompt` | Complete build instructions and asset URLs |
| `vividsites_search_components` | UI and 3D component matches |
| `vividsites_get_component` | Source, dependencies, and installation guidance |
| `vividsites_video_prompt_formula` | Cinematic video prompt guidance, not generated media |
| `vividsites_get_website_blueprint` | Real preview, complete build prompt, and source for up to two selected components in one package |

The blueprint accepts `template_slug` and optional `component_slugs`, all from search results. It fetches the preview and components first, then requests the build prompt once. A failed read stops the workflow before prompt allowance is used. Errors identify the failed stage and whether a build-prompt request was attempted. Prompts and source are preserved without truncation; unusually large packages return an explicit size error instead.

The bundled `vividsites:vividsites-library` skill explains the search, preview, and implementation workflow. Returned code is source material. It is not executed by this plugin, and it cannot authorize unrelated actions.

## Allowance and approval

Premium build-prompt retrieval may consume one request from your existing daily library allowance. The `pre_tool_call` hook sends every `vividsites_get_build_prompt` and `vividsites_get_website_blueprint` call to Hermes's human-approval gate. It does not approve the request itself. Hermes owns the approval and unattended-run behavior; the plugin never disables those guards.

There are no automatic retries, including on timeouts, because a timed-out request may already have consumed allowance. Check usage before retrying. Other library reads do not consume the build-prompt allowance.

This plugin does not run VividSites Create builds, publish websites, generate video, purchase plans or credits, or initiate payments.

## Security and data disclosure

- On an explicit tool call, the plugin sends the tool name, its arguments, and your API key over HTTPS to `https://www.vividsites.app/api/connector`. The endpoint is fixed. Search text is therefore shared with VividSites.
- Credentials are resolved for each call using Hermes's documented `agent.secret_scope.get_secret`. No `.env`, browser profile, keychain, token store, or credential file is read directly. The plugin never stores or logs a key.
- Redirects are rejected. Credentials are never forwarded to a redirect target. The client enforces a 30-second timeout and an 8 MiB response limit per service request. A blueprint makes two to four sequential requests and has a 16 MiB aggregate source limit.
- There are no shell commands, executable downloads, self-updaters, background jobs, file writes, or telemetry. Local reads are limited to this plugin's bundled skill. Python standard library only; no additional dependencies.
- Authentication errors, inactive plans, service failures, and limits return explicit errors. No anonymous endpoint fallback is attempted.
- Original code is MIT licensed. Retrieved templates, prompts, components, names, and logos retain their own terms. Installing the plugin grants no additional catalog license or account entitlement.

## Tests

From the connector repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/hermes -v
hermes plugins validate ./hermes --install-deps
hermes plugins doctor ./hermes --ci
```

The unit suite uses fixture responses and tests all seven registrations, request forwarding, profile-safe key resolution, approval escalation, invalid input, access failures, redirects, timeouts, bounded responses, JSON/SSE parsing, complete blueprint preservation, and stopping before quota use on earlier failures. Passing fixture tests is not proof of a paid live connection.

An optional existing service smoke check is `python3 scripts/verify-live.py`. It reports paid-account checks as skipped when no key is supplied. For a real demo, use a valid paid-account key in Hermes, record real tool results, and clearly show any failures. No demo recording or paid-service result is bundled here.

[Website](https://www.vividsites.app) · [Support](https://www.vividsites.app/support) · [Privacy](https://www.vividsites.app/privacy) · [Terms](https://www.vividsites.app/terms)
