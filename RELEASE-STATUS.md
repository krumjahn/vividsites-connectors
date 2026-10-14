# Distribution status

Updated October 14, 2026 (Asia/Hong_Kong). Version 2.0.0 requires a paid account for every connector operation. Version 1.0.0's keyless instructions are obsolete. Published packages are not marketplace approvals.

Repository: https://github.com/krumjahn/vividsites-connectors

## Verification

- Backend paid-access tests: 10 passed, covering anonymous/invalid/unpaid denial, all paid plans, AppSumo revocation, lookup failures, batches, all six tools and the older MCP prompt endpoint.
- TypeScript and catalog checks passed. The Vercel preview and production builds passed for [backend PR #22](https://github.com/micahc123/uiprompts/pull/22), now merged and deployed. Local build had encountered Google Fonts network timeouts.
- Agent Plugins manifests and Microsoft OpenAPI pass their official schemas. Claude plugin and marketplace manifests pass `claude plugin validate`.
- Gemini v1.0.0 previously installed and connected in isolated profiles. This does not validate v2 paid authentication; v2 host runtime testing requires a paid account key.
- Production: anonymous initialization/discovery/all six calls are denied; a real paid account successfully initialized and retrieved all six tool outputs, including the full prompt and component source. Unknown UUID keys return 401. [PR #23](https://github.com/micahc123/uiprompts/pull/23) corrects malformed UUID keys to 401; its preview build and live access-denial tests passed.
- Other host authenticated runtimes are not yet verified. Configuration validation does not establish compatibility with every host or account.

## Marketplace progress

| Platform | Status |
| --- | --- |
| Gemini CLI | Automatic-gallery publishing requirements verified October 14; official validation and isolated v2 release installation passed. Gallery index has not yet listed VividSites |
| Cline | Submitted October 14: [marketplace issue #2982](https://github.com/cline/mcp-marketplace/issues/2982). Cline SDK agent installation, MCP discovery and paid search passed; approval pending |
| Codex | Paid-account CLI setup guide and environment-token configuration published; installed Codex accepted the configuration. Native authenticated Codex connection not yet tested |
| Cursor | Submitted, confirmed by the publisher on October 14, 2026. Review/approval not yet confirmed |
| Grok Bot | Public listing and authenticated host setup unconfirmed |
| Muse | Submitted, confirmed by the publisher on October 12, 2026; approval not yet confirmed |
| Claude / Cowork | Draft saved in Claude portal; not submitted. v2.0.2 passed portal validation with 5 reviewer holds. OAuth remains required for the remote connector directory submission |
| Kimi Work / Code | Manifest updated with bearerTokenEnvVar; paid host runtime test and public review pending |
| Qwen Work / Code | Code config requires an API key; Work authenticated setup/public listing unverified |
| Microsoft Copilot Studio | API-key OpenAPI definition ready; tenant test and public certification pending |
| GitHub Copilot | VS Code setup guide and password-input config published and structurally checked; native VS Code runtime test and public registry approval pending |
| Gemini consumer | API-key support must be verified in the eligible user's account; no OAuth integration |
| DeepSeek Cowork | Exact application must be identified before claiming compatibility or distribution |
| ChatGPT | Previously submitted as a plugin, reconfirmed by the publisher; approval not confirmed. Earlier keyless configuration needs reconciliation with current paid-only access |

Submission status is based on portal evidence or the publisher’s explicit confirmation; submission does not imply approval.

## Reproduce checks

```sh
python3 scripts/verify-live.py
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

For authenticated checks, supply VIVIDSITES_API_KEY and optionally VIVIDSITES_UNPAID_API_KEY through the process environment. The script reports skipped credential-dependent checks. Never publish test keys. Manual host cases are in `review/cases.json`.

## Publisher materials

`review/listing.json` has the paid-only listing copy and policy links. `assets/icon.png` is the logo. The existing demo predates authentication changes and must not be represented as the current onboarding flow. `microsoft/intro.md` explains Microsoft-specific configuration and certification prerequisites.

## Cursor preparation — October 12, 2026

The native `.cursor-plugin/plugin.json` declares a required paid-account API-key variable and selects `configs/cursor-plugin.json`. The Cursor marketplace manifest selects the native package. Cursor’s official template validator and variable/schema checks passed, as did live anonymous/invalid-key denial checks. Native Cursor installation and credential UI have not yet been runtime-tested.

Historical status on October 12: the form was filled but not submitted while the paid external service terms were being checked. This is superseded by the publisher’s October 14 confirmation that the Cursor application has been submitted. No approval, terms clarification, or change to paid-account enforcement is implied by submission.

## Claude marketplace preparation — October 12, 2026

The Marketplace “Submit a plugin” link leads to the [plugin submission guide](https://claude.com/docs/plugins/submit) and [developer portal](https://claude.ai/directory/manage). The portal redirected to sign-in; no draft or submission confirmation was obtained.

Claude manifest v2.0.1 now declares a required sensitive `userConfig.VIVIDSITES_API_KEY` and the MCP header references `${user_config.VIVIDSITES_API_KEY}`. This replaces implicit environment credential access, as recommended by the [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist). Manifest and marketplace validation passed with local Claude Code 2.1.214. This is structural validation, not an authenticated Claude runtime test or portal validation.

The [directory guide](https://claude.com/docs/directory/publish) requires a separate MCP connector submission for a remote server owned by the plugin publisher. [Software Directory Policy section 5.D](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy) requires OAuth 2.0 for authenticated remote MCP servers. The current VividSites service is API-key only; OAuth remains an implementation prerequisite. No authentication bypass, free-access exception, or false OAuth declaration has been introduced. A dedicated review account is also required by policy section 3.D; no personal customer key has been shared with Anthropic.

### Signed-in portal validation — October 12, 2026

[Draft in Claude](https://claude.ai/directory/manage/plugins/4a3e11c0-3bde-4637-88e4-893369487185) saved in the publisher’s personal Pro organization. Source: repository root, main commit 562aa3b, plugin version 2.0.2. Directory validation passed with five policy holds: four concern VividSites-only credential references in the other hosts’ configurations; one concerns a documentation reference to the logo. The portal explicitly allows submission with these reviewer holds. Five additional warnings concern documented directory metadata fields ignored by the older manifest validator.

The portal preview initially inferred incorrect support and documentation links from the multi-platform README. Explicit display name, icon, support, documentation, privacy and terms fields now correct the listing; re-validation succeeded. Data-handling answers disclose personal-data reads/storage and retention longer than 30 days (account-linked usage records), no skill sends to undeclared services, and no child-directed purpose. Contact: support@vividsites.app. Compliance attestations were left unchecked because the remote authenticated server still lacks the required OAuth implementation. No submission or approval is claimed.

The custom-connector UI does offer API-key request headers under “No sign-in”; that custom installation capability does not remove the Software Directory Policy’s OAuth requirement. No personal API key was entered or shared, and no custom connector was added in this attempt.

## Gemini CLI gallery verification — October 14, 2026

Google’s [release guide](https://geminicli.com/docs/extensions/releasing/) uses automatic gallery discovery, with no submission form, issue, or email required. The repository is public, has the exact `gemini-cli-extension` topic, and contains `gemini-extension.json` at its root. GitHub’s topic search returned this repository. The repository description and manifest both disclose the paid-account requirement.

Gemini CLI 0.60.0 validation passed (`gemini extensions validate .`). A fresh isolated profile successfully installed from the public GitHub URL with `--consent --skip-settings`. `gemini extensions list` confirmed release v2.0.0, the VividSites MCP server, the library skill, and the API-key setting. Its manifest uses the sensitive key setting and Bearer header. The test intentionally skipped credentials and does not claim an authenticated Gemini tool call; the service’s paid-access verification is recorded above.

The public [gallery index](https://geminicli.com/extensions.json) returned HTTP 200 with 2,182 entries and no VividSites match on October 14. Its Last-Modified value was October 7, 2026 at 04:12:27 UTC, before our October 12 release. The current index does not establish why the extension is missing or whether a newer crawl has run. Status: publishing requirements met; gallery appearance pending. No manual submission or Google endorsement is claimed.

Reproduce the local checks:

```sh
gemini extensions validate .
gemini extensions install https://github.com/krumjahn/vividsites-connectors
gemini extensions list
```

For an isolated installation test, set `GEMINI_CLI_HOME` to a fresh temporary profile and pass `--consent --skip-settings`. Customers must configure their own paid-account key before using any tool.

## Cursor submission confirmed — October 14, 2026

The publisher confirmed that the Cursor marketplace application is already submitted. Do not duplicate the application or ask the publisher to submit it again. Grok Bot availability remains unconfirmed; mentioning Grok Bot in the application is optional, and the existing application need not be redone solely to add that wording. No reviewer response or approval has been observed.

## Cline submission and developer setup — October 14, 2026

Cline marketplace submission: https://github.com/cline/mcp-marketplace/issues/2982. The repository was checked for duplicates before submission. The template’s `server-submission` label was unavailable; the first labeled attempt created no issue, and the verified retry created one unlabeled issue. Review/approval remains pending.

Published `llms-install.md`, `configs/cline.json`, `configs/codex.toml`, `docs/codex.md`, `docs/vscode.md`, `assets/icon-400.png`, and sanitized `review/cline-installation.json`. The README links the setup guides. Cline uses an explicit Streamable HTTP transport and a privately replaced literal key placeholder. Codex stores the environment-variable name only. VS Code uses a masked password input. No credentials appear in these files.

Verification:

- Cline SDK 0.0.93 agent received only the installation guide and configured an isolated private profile through constrained setup controls. Its model provider was Cline’s supported `openai-codex-cli` integration with the existing ChatGPT login. Cline’s own MCP client initialized the hosted paid endpoint, discovered all six tools, and successfully called `search_sites`. The host supplied the paid credential privately, outside the model prompt. The installation trial completed successfully.
- The native Cline 3.0.71 executable stalled before its command handler on this Mac. The SDK trial is documented explicitly in the submission; native CLI and IDE UI verification is not claimed.
- Installed Codex accepted the server URL and `bearer_token_env_var` configuration through `codex mcp get vividsites --json` with temporary command-line config overrides; user settings were not changed. Native authenticated Codex MCP execution remains unverified.
- VS Code and Cline JSON and Codex TOML parsed and credential references/placeholders were checked. The icon is a 400×400 PNG. Native VS Code runtime execution remains unverified.
- `python3 scripts/verify-live.py` passed anonymous and invalid-key denial; absent unpaid/paid environment credentials were explicitly skipped. A separate real paid-account Cline SDK call succeeded. `git diff --check` passed, and a scan confirmed the actual test credential was absent from tracked public files and the submission body.

No free-access exception or change to backend access enforcement was made. All configuration examples continue requiring each customer’s own paid-account credential.
