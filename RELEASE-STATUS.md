# Distribution status

Updated October 12, 2026 (Asia/Hong_Kong). Version 2.0.0 requires a paid account for every connector operation. Version 1.0.0's keyless instructions are obsolete. Published packages are not marketplace approvals.

Repository: https://github.com/krumjahn/vividsites-connectors

## Verification

- Backend paid-access tests: 10 passed, covering anonymous/invalid/unpaid denial, all paid plans, AppSumo revocation, lookup failures, batches, all six tools and the older MCP prompt endpoint.
- TypeScript and catalog checks passed. Local full build encountered existing Google Fonts network timeouts; deployment build status is tracked in [backend PR #22](https://github.com/micahc123/uiprompts/pull/22).
- Agent Plugins manifests and Microsoft OpenAPI pass their official schemas. Claude plugin and marketplace manifests pass `claude plugin validate`.
- Gemini v1.0.0 previously installed and connected in isolated profiles. This does not validate v2 paid authentication; v2 host runtime testing requires a paid account key.
- Other host authenticated runtimes are not yet verified. Configuration validation does not establish compatibility with every host or account.

## Marketplace progress

| Platform | Status |
| --- | --- |
| Gemini CLI | Repository published with gallery topic; sensitive API-key setting added; gallery listing unconfirmed |
| Cursor / Grok Bot | Package available; public listing and authenticated host setup unconfirmed |
| Muse | Submission form filled with hosted MCP, API-key auth and paid-only requirements; awaiting final review/submission |
| Claude / Cowork | Claude Code package updated; web clients require API-key header support; OAuth is not implemented |
| Kimi Work / Code | Manifest updated with bearerTokenEnvVar; paid host runtime test and public review pending |
| Qwen Work / Code | Code config requires an API key; Work authenticated setup/public listing unverified |
| Microsoft Copilot Studio | API-key OpenAPI definition ready; tenant test and public certification pending |
| GitHub Copilot | Personal CLI config and VS Code password-input config available; registry approval not claimed |
| Gemini consumer | API-key support must be verified in the eligible user's account; no OAuth integration |
| DeepSeek Cowork | Exact application must be identified before claiming compatibility or distribution |
| ChatGPT | Separate earlier keyless submission is obsolete after this change; it needs authenticated onboarding and a new review |

No marketplace submission or approval is claimed without a confirmation record.

## Reproduce checks

```sh
python3 scripts/verify-live.py
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

For authenticated checks, supply VIVIDSITES_API_KEY and optionally VIVIDSITES_UNPAID_API_KEY through the process environment. The script reports skipped credential-dependent checks. Never publish test keys. Manual host cases are in `review/cases.json`.

## Publisher materials

`review/listing.json` has the paid-only listing copy and policy links. `assets/icon.png` is the logo. The existing demo predates authentication changes and must not be represented as the current onboarding flow. `microsoft/intro.md` explains Microsoft-specific configuration and certification prerequisites.
