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

Final demo, independent video review passed: `/opt/cursor/artifacts/hermes-free-components-final.mp4`. Duration 18.733 seconds. It is the raw terminal recording trimmed to 00:05.820–00:24.550, with a 120px caption band added above the unscaled terminal. Captions do not cover the output. The held frame shows `magnetic-button`, `"free": true`, the `refused` array, and the lines that paid success, unpaid 403, and account scoping were not run.

The earlier raw file and the 18-second lower-third cut are not the review cut. The lower-third covered the refusal lines.

## Local checks, not catalog CI

`hermes plugins validate --install-deps` passed on the working tree and on a Hermes install of public commit `4e2e8a9ab1f40836554d6eb9994875fbea0ccf8e`, subdirectory `hermes`. No Python dependencies are declared. This is not a Hermes catalog CI run. Logs:

- `review/hermes-validate-install-deps.txt` exit 0
- `review/hermes-pin-install.txt` exit 0
- `review/hermes-pin-validate-install-deps.txt` exit 0
- `review/hermes-unittest.txt` exit 0 (`python3 -m unittest tests.test_hermes_access -v`, 6 tests)
- `review/hermes-fixture-denials.txt` fixture refusals, no network fetch

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
