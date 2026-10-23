# MCP distribution follow-through — October 23, 2026

These files prepare metadata for the existing paid VividSites remote MCP. A file in this repository is not a marketplace approval or an upstream registry publication.

## Status

- **Cline:** existing submission [cline/mcp-marketplace#2982](https://github.com/cline/mcp-marketplace/issues/2982) remains open with no reviewer comments as checked October 23. It was submitted October 14. Its website/setup link was updated in place with Cline campaign tags; no duplicate application was opened. `review/distribution/cline-entry.json` is a draft for the newer [Cline registry format](https://github.com/cline/marketplace/blob/main/CONTRIBUTING.md), not a submitted PR to that registry. Ask maintainers about migration before opening a second application.
- **GitHub / VS Code:** a manual nomination was emailed to GitHub's published partnerships intake on October 23. It explicitly says upstream publication is pending, describes API-key authentication and paid access, and does not claim a native VS Code runtime test. No approval or listing is confirmed.
- **Upstream MCP Registry:** `server.json` is schema-valid preparation only. No publish or publisher-authentication operation has been performed for this update. A live registry search timed out, so absence of any historical entry was not independently established. Before publishing, check for an existing name and endpoint to prevent duplication. Proposed namespace: `io.github.krumjahn/vividsites`; metadata version `2.0.2` matches the current distribution manifest.
- **Devin / Windsurf successor:** [CognitionAI/devin-marketplace](https://github.com/CognitionAI/devin-marketplace) is the [official Devin plugin marketplace](https://docs.devin.ai/product-guides/plugins#from-the-marketplace), and managed manifests sync to Devin CLI and Desktop. No VividSites entry or prior PR was found. A plugin is prepared under `plugins/vividsites`; nothing was submitted to Cognition. Opening a PR accepts its [CLA](https://github.com/CognitionAI/devin-marketplace/blob/main/CLA.md), so approval is required first. Its contribution instructions also require a successful installed-plugin tool call, which remains unperformed.
- **Legacy Cascade:** [official documentation](https://docs.devin.ai/desktop/cascade/mcp) says there is no MCP marketplace. A Devin plugin approval must not be described as a legacy Cascade listing.

## Prepared metadata

- `server.json`: remote-only Streamable HTTP; canonical endpoint `https://www.vividsites.app/api/connector`; required secret Authorization header with a user-supplied API key. The public repository contains connector configuration and review materials, not the hosted application's source code.
- `review/distribution/cline-entry.json`: `verified: false`, `featured: false`, canonical `creative` and `software` tags, explicit paid requirement and literal private-key placeholder. Before a Cline registry PR, place it at `registry/mcps/vividsites/entry.json` and use `../../../schemas/mcp.schema.json` as its schema path. The current CLI installation command has not been runtime-tested.
- `plugins/vividsites/.devin-plugin/plugin.json`: dedicated Devin package with inline HTTP server and `${VIVIDSITES_API_KEY}` credential placeholder. Its icon is copied from the existing public repository asset. Install this subdirectory, not the repository root. The root Claude package has a Claude-specific `${user_config.VIVIDSITES_API_KEY}` placeholder that is not a valid plain Devin credential name.
- A later upstream Devin contribution should reference this subdirectory at a tested immutable commit, or copy this same narrow package into its marketplace. Do not submit both forms.

Every tool requires an active paid library account. There is no anonymous or unpaid access, and OAuth is not implemented. Premium build prompts may consume the existing library allowance. The connector does not build or publish sites, purchase credits, initiate payments or generate media. MIT licensing covers connector materials, not retrieved assets or paid service access.

## Verification on October 23

- Upstream `server.json` passed the [2025-12-11 JSON schema](https://github.com/modelcontextprotocol/static/blob/main/schemas/2025-12-11/server.schema.json).
- Cline metadata passed current common schema plus MCP type, slug, tags, install argument and unverified/unfeatured checks. This was not a full marketplace `npm run validate` or native client test.
- The dedicated Devin package passed the official marketplace `scripts/validate.py --fix` and `--fetch` in an isolated one-authored-plugin fixture. That fixture had no upstream pins, so this does not verify an eventual marketplace commit reference or authenticated Devin runtime.
- Live anonymous initialization and tool discovery returned HTTP 401. A deliberately invalid API key also returned HTTP 401. No real key was provided to these smoke checks.
- The Cline-tagged setup page returned HTTP 200 and retained its query string.
- The existing [October 14 Cline SDK test](../review/cline-installation.json) remains historical evidence: paid initialization, all six tools discovered, search successful. Paid-account tests and native VS Code/Devin tool calls were not rerun in this update.

## Attribution links

Use `https://www.vividsites.app/mcp` with:

- Cline: `utm_source=cline`
- GitHub MCP Registry nomination: `utm_source=github_mcp_registry`
- Shared upstream registry metadata: `utm_source=mcp_registry`
- Devin/Desktop: `utm_source=windsurf_devin`
- All four: `utm_medium=mcp_directory&utm_campaign=developer_distribution`

These query parameters distinguish setup-page clicks only. They do not prove backend capture, a unique person, MCP connection, retrieval, usable outcome or paid conversion. Keep the canonical API endpoint unchanged. Treat MCP client identity and website acquisition source as separate measurements; do not attribute all upstream-registry clients to GitHub.

## Remaining publishing steps

1. Approve and complete the official MCP publisher's GitHub device authorization for the personal namespace, if no suitable existing publisher session is available. The normal command is `mcp-publisher login github`; its fresh code is entered at the official GitHub device page. Never place tokens in files, URLs, chat or commits. GitHub namespace authentication does not require repository write scopes. Review the [official authentication guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx) and [registry terms](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/terms-of-service.mdx) first.
2. Publish only after checking namespace and endpoint uniqueness, then read the returned active/latest registry entry. GitHub onboarding is still manually curated; upstream publication is not automatic GitHub acceptance.
3. Obtain Cognition CLA acceptance and verify a paid-account Devin tool call before its marketplace PR. Use Devin's private Connect controls or an authorized local environment for the key, not a model prompt. Validate the actual full submission and immutable pin before opening it.
