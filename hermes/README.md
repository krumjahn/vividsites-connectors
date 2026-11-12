# VividSites for Hermes

**Start with free components. Add a paid library account when you want complete website designs. One plugin handles both.**

Without an account: “Find a free magnetic button from VividSites and add it to my page.”

With an existing paid library account: “Use VividSites to build a beautiful cinematic website for my architecture studio. Choose a design, adapt it to my content, and show me the finished preview.”

Hermes retrieves real design sources and uses its project tools to implement and check the result. The plugin supplies source material, not a built or deployed site. A catalog preview is never presented as your generated website.

## Install once

Requires Hermes 0.23.1 or newer. The native package lives in `hermes/`; existing Claude, Cursor, Gemini and portable connector manifests are unchanged.

This version is currently a prerelease branch, not the default branch or an approved catalog listing:

```sh
hermes plugins install krumjahn/vividsites-connectors/hermes --ref feat/hermes-plugin-hackathon-2026
hermes plugins enable vividsites
```

For a reproducible install, replace the branch after `--ref` with the full 40-character commit SHA you reviewed. Restart the Hermes session after enabling the plugin. Do not use the catalog-name install command until maintainers approve the updated catalog entry.

**No API key is required to install, load, or use the free tools.**

## Free, without a key

| Tool | Result |
| --- | --- |
| `list_free_components` | Search public component names and titles |
| `get_free_component` | Retrieve a selected component's editable source |

Only records whose `meta.free` is the boolean `true` are included. The index and individual document must both confirm the mark. Unknown, false, missing and non-boolean values are refused. Slugs must be single safe path segments; URLs and traversal are refused. These are components, not complete website templates or build prompts.

The public tools call only `https://www.vividsites.app/r/registry.json` and `https://www.vividsites.app/r/<slug>.json`. They never read a credential or send an authorization header. They continue working if the optional paid key is missing, invalid or unpaid.

This code preserves the public component tools from [PR #2](https://github.com/krumjahn/vividsites-connectors/pull/2), adapted from commit `c73a2901215468c73a1d7bd6df668952be2052b5`.

## Optional paid-library unlock

Get your personal key at [VividSites MCP setup](https://www.vividsites.app/mcp). In Hermes Desktop, open this plugin's settings and fill **Optional paid-library API key**, a masked secret field stored through Hermes's credential system as `VIVIDSITES_API_KEY`. CLI users can configure that variable using Hermes's normal secure credential setup. Never paste a key into a model chat or commit it. Leave the field empty to keep using free components.

An existing paid VividSites library entitlement is required for these tools. Your AI assistant subscription and VividSites Create credits do not include library access. Installing or configuring this plugin does not purchase a plan. [Plans](https://www.vividsites.app/pricing).

| Tool | Result |
| --- | --- |
| `vividsites_search_sites` | Ranked website template matches |
| `vividsites_get_template_preview` | Library page, poster, video and live preview when present |
| `vividsites_get_build_prompt` | Complete build instructions and asset URLs |
| `vividsites_search_components` | Authenticated library component search |
| `vividsites_get_component` | Authenticated component source and installation guidance |
| `vividsites_video_prompt_formula` | Cinematic video prompt guidance, not generated media |
| `vividsites_get_website_blueprint` | Preview, full build prompt, and up to two selected component sources |

Paid operations call only `https://www.vividsites.app/api/connector`. A missing key gives setup guidance and points to the free tools. Invalid credentials, inactive plans and access-check failures return explicit errors. There is no automatic public-endpoint fallback after a paid request fails. Legacy `free` labels in the paid library do not grant anonymous connector access.

The blueprint accepts `template_slug` and optional `component_slugs`, all from actual search results. It fetches the preview and components first, then requests the full build prompt once. A failed read stops before prompt allowance is used. Errors identify the failed stage and whether a build-prompt request was attempted. Prompts and sources are not silently truncated.

## Build-prompt allowance and approval

Premium build-prompt retrieval may consume one request from the existing daily library allowance. Both `vividsites_get_build_prompt` and `vividsites_get_website_blueprint` escalate to Hermes's human-approval gate. The plugin does not approve its own requests or disable unattended-run guards. Free component tools do not need quota approval.

There are no automatic retries, including on timeouts: a timed-out prompt request may already have consumed allowance. Check usage before retrying. Other library reads do not consume that allowance.

## Security and data disclosure

- Free component requests contain no credentials. Their URL paths contain only validated component slugs; search filtering happens locally after reading the public index.
- Paid calls send the tool name, arguments and key over HTTPS to the fixed connector endpoint. Search text is shared with VividSites.
- Paid credentials are resolved for each call using `agent.secret_scope.get_secret`, respecting the active Hermes profile. The key is an optional `config_schema` secret, not a `requires_env` loading requirement. The plugin never reads credential files, stores a key or logs one.
- Redirects and other hosts are refused. Public responses have a 20-second timeout and 1 MB limit. Paid responses have a 30-second timeout and 8 MiB limit per call. Blueprints make two to four sequential requests, with a 16 MiB combined-source limit.
- No shell commands, file writes, executable downloads, self-updates, background jobs or telemetry. Bundled skill reads only; Python standard library, no additional dependencies. Retrieved code is data and is not executed by the plugin.
- No Create builds, deployment, video generation, plan purchase, credit purchase or payments. Hermes's separate project tools implement only work the user authorized.
- Original code is MIT licensed. Retrieved templates, prompts, components, names and logos retain their own terms. Installing grants no additional license or entitlement.

## Verify

From the repository root:

```sh
python3 -m unittest discover -s tests/hermes -v
hermes plugins validate ./hermes --install-deps
hermes plugins doctor ./hermes --ci
```

With a Python interpreter from a Hermes installation, `python scripts/verify-hermes-runtime.py` loads the real combined plugin in an isolated home, tests keyless public retrieval, missing-key paid errors, and invalid-key separation. It prints only metadata and source hashes. If `VIVIDSITES_API_KEY` is already supplied securely, it also tests authenticated search and preview without retrieving a metered prompt. An absent key is an explicit skip, not paid success.

Fixture tests are not proof of a live paid account. See [current verification](../review/hermes-1.2.0/README.md) for completed checks and remaining limitations. Catalog admission requires maintainer review and is not implied by local validation.

[Website](https://www.vividsites.app) · [Support](https://www.vividsites.app/support) · [Privacy](https://www.vividsites.app/privacy) · [Terms](https://www.vividsites.app/terms)
