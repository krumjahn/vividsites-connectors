# Distribution status

Updated October 12, 2026 (Asia/Hong_Kong). Version 2.0.0 requires a paid account for every connector operation. Version 1.0.0's keyless instructions are obsolete. Published packages are not marketplace approvals.

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
| Gemini CLI | Repository published with gallery topic; sensitive API-key setting added; gallery listing unconfirmed |
| Cursor | Native package prepared and publisher form filled. Not submitted: Publisher Terms section 3.1 needs clarification for paid-only external service access |
| Grok Bot | Public listing and authenticated host setup unconfirmed |
| Muse | Submitted, confirmed by the publisher on October 12, 2026; approval not yet confirmed |
| Claude / Cowork | Draft saved in Claude portal; not submitted. v2.0.2 passed portal validation with 5 reviewer holds. OAuth remains required for the remote connector directory submission |
| Kimi Work / Code | Manifest updated with bearerTokenEnvVar; paid host runtime test and public review pending |
| Qwen Work / Code | Code config requires an API key; Work authenticated setup/public listing unverified |
| Microsoft Copilot Studio | API-key OpenAPI definition ready; tenant test and public certification pending |
| GitHub Copilot | Personal CLI config and VS Code password-input config available; registry approval not claimed |
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

The publisher form is filled but not submitted. [Publisher Terms section 3.1](https://cursor.com/marketplace-publisher-terms) prohibits direct or indirect fees for access/use of a Marketplace plugin. Whether an existing paid VividSites subscription is allowed needs clarification; no terms acceptance or free-access change has been made.

## Claude marketplace preparation — October 12, 2026

The Marketplace “Submit a plugin” link leads to the [plugin submission guide](https://claude.com/docs/plugins/submit) and [developer portal](https://claude.ai/directory/manage). The portal redirected to sign-in; no draft or submission confirmation was obtained.

Claude manifest v2.0.1 now declares a required sensitive `userConfig.VIVIDSITES_API_KEY` and the MCP header references `${user_config.VIVIDSITES_API_KEY}`. This replaces implicit environment credential access, as recommended by the [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist). Manifest and marketplace validation passed with local Claude Code 2.1.214. This is structural validation, not an authenticated Claude runtime test or portal validation.

The [directory guide](https://claude.com/docs/directory/publish) requires a separate MCP connector submission for a remote server owned by the plugin publisher. [Software Directory Policy section 5.D](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy) requires OAuth 2.0 for authenticated remote MCP servers. The current VividSites service is API-key only; OAuth remains an implementation prerequisite. No authentication bypass, free-access exception, or false OAuth declaration has been introduced. A dedicated review account is also required by policy section 3.D; no personal customer key has been shared with Anthropic.

### Signed-in portal validation — October 12, 2026

[Draft in Claude](https://claude.ai/directory/manage/plugins/4a3e11c0-3bde-4637-88e4-893369487185) saved in the publisher’s personal Pro organization. Source: repository root, main commit 562aa3b, plugin version 2.0.2. Directory validation passed with five policy holds: four concern VividSites-only credential references in the other hosts’ configurations; one concerns a documentation reference to the logo. The portal explicitly allows submission with these reviewer holds. Five additional warnings concern documented directory metadata fields ignored by the older manifest validator.

The portal preview initially inferred incorrect support and documentation links from the multi-platform README. Explicit display name, icon, support, documentation, privacy and terms fields now correct the listing; re-validation succeeded. Data-handling answers disclose personal-data reads/storage and retention longer than 30 days (account-linked usage records), no skill sends to undeclared services, and no child-directed purpose. Contact: support@vividsites.app. Compliance attestations were left unchecked because the remote authenticated server still lacks the required OAuth implementation. No submission or approval is claimed.

The custom-connector UI does offer API-key request headers under “No sign-in”; that custom installation capability does not remove the Software Directory Policy’s OAuth requirement. No personal API key was entered or shared, and no custom connector was added in this attempt.
