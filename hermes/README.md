# VividSites free components for Hermes

This directory is a native Hermes plugin. `plugin.yaml` plus `__init__.py` is what the current Hermes validator admits, and it is what the loader runs. A portable `plugin.json` without `plugin.yaml` validates as a portable package, but catalog admission text also asks for `plugin.yaml`. Putting `plugin.yaml` next to a portable `mcp.json` makes the loader take the native manifest and skip `mcp.json`. This package therefore does not ship `mcp.json`.

It lists and fetches public components from `https://www.vividsites.app/r/registry.json` when `meta.free` is the boolean `true`. The same flag is checked again on the component document. These records are components. They are not templates and not build prompts.

There is no API key. The paid connector at `/api/connector` is not called. Paid-account success, unpaid HTTP 403, and account scoping are not claimed. An invalid key on that other endpoint is not an unpaid-account result, and this plugin does not send one.

## Access rules

- The slug must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. URLs, dots, and `..` are refused before any request.
- The index must contain that slug with `meta.free: true`. Anything missing, false, or non-boolean is refused and not fetched.
- The only requests are `https://www.vividsites.app/r/registry.json` and `https://www.vividsites.app/r/<slug>.json`.
- Redirects are refused. Query strings, userinfo, and other hosts are refused.

VividSites publishes the component library as free, including under the MIT-0 terms on the website. This plugin still requires the registry's own `meta.free: true` mark. The website terms are not used to reclassify a record that lacks that boolean.

## Install

Requires Hermes Agent 0.23.1 or newer.

```sh
hermes plugins install ./hermes
hermes plugins enable vividsites
```

No environment variable is required.

## Check

```sh
hermes plugins validate ./hermes
python3 -m unittest tests.test_hermes_access
```
