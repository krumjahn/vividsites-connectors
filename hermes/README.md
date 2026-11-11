# VividSites for Hermes

Hermes Agent loads this directory as a portable plugin and connects to the hosted VividSites connector. The package does not contain an API key. Hermes reads `VIVIDSITES_API_KEY` from the active profile secret store and sends it as `Authorization: Bearer`. If that variable is missing or empty, Hermes refuses the connection before the request instead of sending the literal placeholder.

This package does not grant paid-template access. The server at `https://www.vividsites.app/api/connector` checks the caller's own key on every request, including initialization, discovery, and all six tools. A catalog label of `free` is not an entitlement. There is no plugin-side bypass and no shared key.

Requires Hermes Agent 0.23.1 or newer. That release resolves `${VIVIDSITES_API_KEY}` in a portable plugin's HTTP headers and keeps the resolved header across reconnects. There is no `plugin.yaml` beside these files: Hermes treats a native manifest as the plugin and then does not load this `mcp.json`.

## Install

From a checkout of this repository:

```sh
hermes plugins install ./hermes
```

Catalog installation, after a reviewed pin exists, would be `hermes plugins install vividsites`. No catalog pull request is open.

When Hermes asks, enter the personal key from [VividSites MCP setup](https://www.vividsites.app/mcp). A paid library plan is required for this connector. If the installer does not prompt, put the key in the active profile `.env` (normally `~/.hermes/.env`):

```dotenv
VIVIDSITES_API_KEY=your-personal-paid-library-key
```

The Desktop or TUI plugin settings form stores the same variable through Hermes's credential route. It does not write the key into `config.yaml`. Restart Hermes after saving it. Do not paste the key into chat, a shell transcript, or this repository.

Hermes may warn that `settings.api_key` is unset when the key exists only in `.env`. Header resolution still uses `VIVIDSITES_API_KEY`. An unset or empty value fails closed and does not send the placeholder.

Enable the plugin if it is still off:

```sh
hermes plugins enable vividsites
```

`get_build_prompt` is not marked read-only by the server and may consume the account's existing daily allowance. This package sets that MCP server to `trust: untrusted`, so Hermes asks before a tool call that is not annotated read-only. That prompt is not the entitlement check. The server still decides.

## What the connector does

| Tool | Result |
| --- | --- |
| `search_sites` | Ranked template matches |
| `get_template_preview` | Library URL, poster, video, and live preview when available |
| `get_build_prompt` | Complete build instructions and asset URLs |
| `search_components` | UI and 3D component matches |
| `get_component` | Component source, dependencies, and installation command |
| `video_prompt_formula` | Cinematic video prompt guidance |

The connector does not run VividSites Create builds, publish sites, or take payment.

## Access, as enforced by the server

Checked against production on November 11, 2026, without a paid key. Status and error code only. No catalog body was stored.

- No credential, an empty bearer, and `tier=free` on `search_sites`: HTTP 401 `authentication_required`. The response has no `result`.
- A non-key and the literal text `${VIVIDSITES_API_KEY}`: HTTP 401 `invalid_api_key`. The response has no `result`.
- The same denial covers initialization, discovery, and all six tools.

These calls do not prove the unpaid-account HTTP 403 path or that one account's key is limited to that account. Those need credentials this environment does not have. A local mock cannot prove production entitlement.

The public website describes a Free plan that can browse templates and use the component library, including `https://www.vividsites.app/r/<component>.json`, and a paid plan for the MCP connector. The connector used here is the paid MCP endpoint. It does not serve a free-only mode. Items in the public component registry carry `meta.free: true`. A template slug checked on that registry (`cinematic.json`) was HTTP 404. This plugin does not call the registry, because the registry is not the connector and missing connector metadata is not a reason to treat a template as free.

Website terms prohibit bypassing access controls and republishing templates or build prompts. Component code on the website is under MIT-0. This package does not copy either into the repository.

## Check

```sh
hermes plugins validate ./hermes
python3 -m unittest tests.test_hermes_access
```

The unittest calls the live connector for denial cases and, when Hermes 0.23.1 is installed, loads this plugin through Hermes. It redacts the test token before writing evidence.
