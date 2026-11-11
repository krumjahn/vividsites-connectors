# Hermes hackathon entry — owner review only

Do not post, do not open the catalog pull request, and do not submit the form. The parent does those steps after checking this file against the evidence.

This entry is FREE-ONLY. It covers public components, not templates and not build prompts.

## Form fields

| Field | Value |
| --- | --- |
| Plugin Title | VividSites free components |
| Plugin Description | Lists and fetches public VividSites components whose registry meta.free value is boolean true. Components only. No paid templates, no build prompts, and no API key. |
| Email Address | keith@rumjahn.com |
| Discord Username | feriosa2025 |
| X Demo Post Link | not posted |
| GitHub Link to your Hermes Plugin Pull Request | not opened |

Poster account for the X draft: @rumjahn. Tag in the draft: @NousResearch.

## Proposed X post

This matches the free-component recording. It does not claim a paid-library result.

```
Free VividSites components now load in Hermes. The plugin reads the public registry and returns a component only when meta.free is true. magnetic-button came back as a component. A template id, a path, and a URL were refused. No key, no paid templates.

@NousResearch
```

## What the clip is

`/opt/cursor/artifacts/hermes-free-components-raw.mp4` is the terminal recording of Hermes 0.23.1. It shows `hermes plugins validate` accepting `plugin.yaml`, then a real `get_free_component` result for `magnetic-button` (`free: true`, 15425 bytes, kind `free_component`) and refusals for `cinematic`, `../secret`, and `https://evil.test/r/a.json`.

`/opt/cursor/artifacts/hermes-free-components-captioned.mp4` is that recording with a HyperFrames caption band. The terminal pixels are in the frame. The band covers the lower lines, so the raw recording is the full JSON. The caption states the same result: `magnetic-button`, `meta.free` true, 15425 bytes, and the three refusals. It is 18 seconds. It is not a paid-catalog demo.

## Catalog patch

`review/hermes-catalog-entry.yaml` is the proposed file for `NousResearch/hermes-agent` at `plugin-catalog/vividsites.yaml`. It is not an open pull request.

Pin: `4e2e8a9ab1f40836554d6eb9994875fbea0ccf8e`

`requires_env` is empty. There is no key.

### Proposed catalog pull request text

Title: Add the VividSites free-component plugin

Body:

```
Free-only VividSites components for Hermes.

The package is native: plugin.yaml and __init__.py in hermes/. hermes plugins validate on 0.23.1 reports that plugin.yaml parses, __init__.py loads, and the declared tools match register(). A portable mcp.json is not shipped. With plugin.yaml present, the loader would ignore mcp.json.

Tools: list_free_components and get_free_component. They read https://www.vividsites.app/r/registry.json and https://www.vividsites.app/r/<slug>.json. A component is returned only when meta.free is the boolean true on the index and again on the document. Unknown, false, missing, and non-boolean classifications are refused before a component fetch. Slugs are a single path segment. Redirects and other hosts are refused.

These records are components, not templates. The paid connector is not called. No API key is required or included. Paid-account success, unpaid HTTP 403, and account scoping are not claimed. An invalid-key 401 is a different result and was not used as a substitute.

A Hermes process called get_free_component("magnetic-button") and received the public component (15425 bytes). cinematic, a traversal slug, and a URL were refused.
```

## Not claimed

- Unpaid HTTP 403. No unpaid key exists. An invalid key is not that result.
- Paid-account success. No paid key exists.
- Account scoping. No account credentials were used.

## Verdict

The free-only plugin loads, passes the current validator, and returned one real free component through Hermes. It is not a paid-connector submission. No production change was deployed. Nothing has been posted.
