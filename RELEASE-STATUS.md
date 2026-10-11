# Distribution status

Updated October 12, 2026 (Asia/Hong_Kong). A published repository or a working MCP endpoint does not imply marketplace approval.

## Verification

- Live MCP: initialization, all six library tools, safety annotations, preview URLs, component source, and unknown-slug error handling passed.
- Agent Plugins: plugin.json and mcp.json pass their official JSON schemas.
- Claude Code: plugin and marketplace manifests pass `claude plugin validate`.
- Shared skill: passes the skill-creator validator.
- Gemini CLI: installed successfully into an isolated test configuration; connection check pending.
- Microsoft: OpenAPI 2.0 schema validates. Not imported into a tenant or certified.
- Other host runtimes: not yet tested; configuration follows the linked host documentation.

## Marketplace progress

| Platform | Status | Next step |
| --- | --- | --- |
| Gemini CLI | Public package being prepared | Publish repository with gemini-cli-extension topic; gallery crawl and validation are external |
| Cursor / Grok Bot | Submission package ready; Cursor portal requires sign-in | Sign in at https://cursor.com/marketplace/publish and submit the repository; verify Grok Bot availability separately |
| Muse | Listing copy and endpoint ready; portal not yet inspected successfully | Submit at https://muse.ai/platform |
| Claude / Cowork | Remote endpoint and plugin bundle ready | Submit through Claude developer directory portal on a paid account |
| Kimi Work | Plugin manifest, skill and ZIP source ready | Install/test personal plugin, then plugin details → envelope → apply to official marketplace |
| Qwen Work | Organization connector setup documented | Add endpoint with No authorization; public publisher route remains unverified |
| Microsoft Copilot Studio | Custom connector schema and documentation ready | Tenant test, verified publisher enrollment, and authentication eligibility for public certification remain outstanding |
| GitHub Copilot | Remote MCP configs ready | Users can install directly; no curated registry approval claimed |
| Gemini consumer | Custom MCP setup documented | Requires an eligible account; no-auth compatibility not yet tested |
| DeepSeek Cowork | Generic remote MCP endpoint available | Exact application must be identified before claiming support or marketplace publication |
| ChatGPT | Existing separate submission previously recorded as in review | No change made to that submission; current portal status not rechecked |

Browser submission work was interrupted by Chrome's remote-debugging permission gate. The automatic approval helper reported missing macOS Accessibility permission. No marketplace submission is claimed without a confirmation page or record.

## Reproduce checks

```sh
python3 scripts/verify-live.py
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

Manual host smoke test: search three free designs; preview `cinematic`; retrieve its full prompt; search and retrieve `magnetic-button`; retrieve video guidance; confirm unknown component is an error and unsupported publishing/purchases are not attempted. Full prompts are in `review/cases.json`.

## Publisher materials

`review/listing.json` contains the description, support contact, policy URLs, endpoint and existing demo. `assets/icon.png` is the existing VividSites logo. `microsoft/intro.md` describes Microsoft-specific scope and remaining certification requirements.
