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

`/opt/cursor/artifacts/hermes-live-probe-raw.mp4` is the untouched terminal recording of Hermes 0.23.1.

`/opt/cursor/artifacts/hermes-vividsites-evidence.mp4` is that recording, trimmed to the terminal and captioned in HyperFrames. Captions do not replace the terminal. The clip is under 90 seconds.

It shows three things:

1. Missing `VIVIDSITES_API_KEY`: Hermes fails closed and does not send the placeholder.
2. Live `POST https://www.vividsites.app/api/connector` with a non-credential: HTTP 401 `invalid_api_key`. No catalog payload.
3. A local MCP process on 127.0.0.1: Hermes called `mcp__vividsites__synthetic_status`. That result is a fixture, not VividSites.

Paid catalog retrieval was not run. There is no paid key in this environment.

## Catalog patch

`review/hermes-catalog-entry.yaml` is the proposed file for `NousResearch/hermes-agent` at `plugin-catalog/vividsites.yaml`. It is not an open pull request. The `sha` field is the vividsites-connectors commit that contains `hermes/`.

## Not proven

- HTTP 403 for a valid key on an unpaid account. `VIVIDSITES_UNPAID_API_KEY` was unset.
- A paid account initializing and calling the six tools.
- One account's key being unable to use another account. No second credential was available, and no other account was queried.

Direct requests without a key, including `search_sites` with `tier=free`, returned 401 `authentication_required` and no `result`. The connector does not have a free-only mode. The public component registry is a different URL. This plugin does not call it. `cinematic.json` on that registry was 404. All 112 registry items observed had `meta.free: true`. That flag was not treated as connector authorization.

## Verdict

Not ready to submit. The plugin loads, the missing-key path fails closed, and the live connector denies a non-entitled key. A paid-library success, the unpaid 403 path, and account scoping are still unproven. No production change was deployed.
