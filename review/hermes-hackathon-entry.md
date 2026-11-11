# Hermes hackathon entry — owner review only

Do not post, do not open the catalog pull request, and do not submit the form. The parent does those steps after checking this file against the evidence.

## Form fields

| Field | Value |
| --- | --- |
| Plugin Title | VividSites |
| Plugin Description | Search VividSites templates, previews, build prompts, and UI or 3D components from Hermes. Each person uses their own paid library key. The plugin does not include a key. |
| Email Address | keith@rumjahn.com |
| Discord Username | feriosa2025 |
| X Demo Post Link | not posted |
| GitHub Link to your Hermes Plugin Pull Request | not opened |

Poster account for the X draft: @rumjahn. Tag in the draft: @NousResearch.

## Proposed X post

This matches the captured clip. It is not a successful paid-catalog retrieval.

```
VividSites loads in Hermes as a plugin. Your own paid library key stays in Hermes. This clip is Hermes 0.23.1: a missing key never leaves the machine, and the live connector returns 401 for a key that is not a paid entitlement. The local tool call is a synthetic fixture. No paid template is in the video.

@NousResearch
```

## What the clip is

`/opt/cursor/artifacts/hermes-live-probe-raw.mp4` is the terminal recording of Hermes 0.23.1. It is 42 seconds. This is the evidence. It shows the three JSON results below. It does not show a paid catalog result.

A HyperFrames caption pass was rendered to `/opt/cursor/artifacts/hermes-vividsites-evidence.mp4`. The headless capture did not load `proof.mp4` (the render log reports 404), so that file is captions on a blank frame. It is not the proof and must not be posted as the demo.

It shows three things:

1. Missing `VIVIDSITES_API_KEY`: Hermes fails closed and does not send the placeholder.
2. Live `POST https://www.vividsites.app/api/connector` with a non-credential: HTTP 401 `invalid_api_key`. No catalog payload.
3. A local MCP process on 127.0.0.1: Hermes called `mcp__vividsites__synthetic_status`. That result is a fixture, not VividSites.

Paid catalog retrieval was not run. There is no paid key in this environment.

## Catalog patch

`review/hermes-catalog-entry.yaml` is the proposed file for `NousResearch/hermes-agent` at `plugin-catalog/vividsites.yaml`. It is not an open pull request.

Pin: `cd0f68cd74ee1404811f64c8bf46bc1a405e27a8`

That commit contains `hermes/`. This review file is not part of that pin. `requires_env` is listed so the credential is visible. The package declares the variable as a portable `config_schema` secret rather than `plugin.yaml` `requires_env`, because a native manifest would stop Hermes from loading `mcp.json`. If catalog CI requires those lists to match a native manifest, drop `requires_env` from the entry or accept the portable declaration.

### Proposed catalog pull request text

Title: Add the VividSites connector plugin

Body:

```
VividSites connects Hermes to https://www.vividsites.app/api/connector over Streamable HTTP.

The package is portable (`plugin.json` + `mcp.json` in `hermes/`). Authorization is `Bearer ${VIVIDSITES_API_KEY}`, resolved from the active Hermes profile. An unset variable fails closed. The package contains no key and does not grant paid-template access. The server checks the caller's own key. `get_build_prompt` is not read-only; the package sets that server to `trust: untrusted`.

Surfaces: portable MCP server and one bundled skill. No Python, no desktop UI, no network calls except the connector the user configures.

Hermes 0.23.1 validated the package. A missing key failed closed. A non-credential against the live endpoint returned HTTP 401 `invalid_api_key` with no catalog payload. A local synthetic tool call is a fixture, not a paid retrieval. Unpaid HTTP 403 and a successful paid-account call were not run.

requires_hermes is >=0.23.1 because that release keeps portable header secrets across reconnects.
```

## Not proven

- HTTP 403 for a valid key on an unpaid account. `VIVIDSITES_UNPAID_API_KEY` was unset.
- A paid account initializing and calling the six tools.
- One account's key being unable to use another account. No second credential was available, and no other account was queried.

Direct requests without a key, including `search_sites` with `tier=free`, returned 401 `authentication_required` and no `result`. The connector does not have a free-only mode. The public component registry is a different URL. This plugin does not call it. `cinematic.json` on that registry was 404. All 112 registry items observed had `meta.free: true`. That flag was not treated as connector authorization.

## Verdict

Not ready to submit. The plugin loads, the missing-key path fails closed, and the live connector denies a non-entitled key. A paid-library success, the unpaid 403 path, and account scoping are still unproven. No production change was deployed.
