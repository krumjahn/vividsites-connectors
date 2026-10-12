# VividSites connectors

![VividSites](assets/icon.png)

Cinematic website templates, previews, complete build prompts, and editable UI and 3D component code inside your AI assistant. **Every tool requires a paid VividSites library account.** There is no anonymous or unpaid connector access.

Sign in at [VividSites MCP setup](https://www.vividsites.app/mcp), purchase a [library plan](https://www.vividsites.app/pricing) if needed, and connect your personal API key in the assistant's credential settings. Your assistant subscription does not include VividSites access.

- Endpoint: `https://www.vividsites.app/api/connector`
- Transport: Streamable HTTP
- Authentication: `Authorization: Bearer <VIVIDSITES_API_KEY>` (or `x-api-key`)
- Missing/invalid/revoked key: HTTP 401; unpaid account: HTTP 403; unavailable entitlement check: HTTP 503.
- Access is checked on every request, including initialization, discovery and all six tools. Existing paid library plans and active AppSumo library entitlements are supported.
- Premium prompt retrieval on metered plans uses the existing daily allowance shared with the website. Other reads do not consume that allowance. Create build credits are separate and do not grant library access by themselves.

The connector supplies library assets. It does not run VividSites Create builds, publish sites, purchase credits or initiate payments. Store keys in host credential settings; never paste them into model chats, URLs or shared repositories. OAuth sign-in is not implemented.

## Install

### Gemini CLI

```sh
gemini extensions install https://github.com/krumjahn/vividsites-connectors
```

The extension requests your VividSites API key as a sensitive installation setting. To update it, run `gemini extensions config vividsites`. Restart, inspect `/mcp`, and try an example below. See [Gemini extension settings](https://geminicli.com/docs/extensions/reference/).

### Claude Code

Supply `VIVIDSITES_API_KEY` through your local environment, then install:

```sh
claude plugin marketplace add krumjahn/vividsites-connectors
claude plugin install vividsites@vividsites
```

The `.mcp.json` manifest reads that environment variable in its Authorization header. No key is bundled. Alternatively add the remote endpoint and Bearer header through your client's private MCP configuration.

### Cursor / GitHub Copilot CLI

Merge [Cursor config](configs/cursor.json) or [Copilot CLI config](configs/copilot-cli.json) into your **personal** MCP configuration. Replace `YOUR_VIVIDSITES_API_KEY` locally using the host's credential/configuration controls. These are literal placeholders, not environment references. Never commit the completed configuration.

### VS Code / GitHub Copilot

Merge [configs/vscode.json](configs/vscode.json) into `.vscode/mcp.json`. VS Code prompts for the key through a password input; the shared file contains only the input reference. See [VS Code input variables](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

### Kimi Work / Kimi Code

Install this repository through the app's GitHub plugin flow or import the release ZIP. `kimi.plugin.json` reads the bearer token from `VIVIDSITES_API_KEY` using `bearerTokenEnvVar`. Make that variable available to the client and reload the plugin. The feature follows the [Kimi MCP documentation](https://www.kimi.com/en/help/kimi-code/cli-mcp); authenticated host runtime verification remains pending.

### Qwen Code

Merge [configs/qwen-code.json](configs/qwen-code.json) into Qwen Code settings and supply `VIVIDSITES_API_KEY` in the client's environment. `httpUrl` selects Streamable HTTP. See [Qwen MCP setup](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/).

### Portable Agent Plugins

The root `plugin.json` and `mcp.json` use Agent Plugins 1.0.0. That standard has no portable secret-reference field and forbids expansion inside HTTP headers. The root `mcp.json` therefore supplies only the endpoint: configure its Bearer credential through the host's secure auth controls. A host without API-key header support cannot connect; installing the package alone does not grant access. See the [Agent Plugins auth contract](https://agent-plugins.org/specification#streamable-http-and-legacy-http-sse).

### Muse, Qwen Work, Grok, Gemini consumer and Claude web / Cowork

Add the hosted MCP endpoint and configure API-key/Bearer authentication **only if the host supports it**. Public directory submission and authenticated compatibility are separate from a custom installation. Do not select “No authorization”; this server rejects unauthenticated requests. OAuth-only hosts require a future OAuth integration. See [distribution status](RELEASE-STATUS.md) for verified progress; support is not claimed for every similarly named app.

### Microsoft Copilot Studio

Use the MCP onboarding wizard with API-key authentication, header `Authorization`, and the value `Bearer <your key>`. [microsoft/intro.md](microsoft/intro.md) includes an OpenAPI definition and certification prerequisites. This is not a certified Marketplace listing.

### DeepSeek-based apps

For a specific app supporting remote MCP and API-key headers, configure the endpoint and Bearer credential. Different apps use the DeepSeek Cowork name; no universal installer or marketplace listing is claimed.

## Try it with your paid account

- “Find three cinematic website templates and show their previews.”
- “Get the complete build prompt for the cinematic template.”
- “Find a magnetic button and give me its HTML, CSS and JavaScript.”

| Tool | Result |
| --- | --- |
| `search_sites` | Ranked template matches |
| `get_template_preview` | Library URL, poster, video, and live preview when available |
| `get_build_prompt` | Complete build instructions and asset URLs; may consume an existing daily allowance |
| `search_components` | UI and 3D component matches |
| `get_component` | Component source, dependencies and installation command |
| `video_prompt_formula` | Cinematic video prompt guidance |

Some results retain legacy catalog labels such as `free`. Those labels do not grant free connector access. All six tools require the paid account.

## Validation

```sh
python3 scripts/verify-live.py
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
```

The live script always checks anonymous and invalid-key denial. If `VIVIDSITES_API_KEY` is supplied securely in its environment, it additionally checks paid initialization and all six tools using an unmetered catalog prompt. It never prints the key. An optional `VIVIDSITES_UNPAID_API_KEY` tests HTTP 403. Skipped credential-dependent checks are reported explicitly. Backend tests separately cover all paid plans, revoked entitlements, both routes, batches and database failures. See [review cases](review/cases.json) and [release status](RELEASE-STATUS.md).

## Support and licensing

[Website](https://www.vividsites.app) · [Support](https://www.vividsites.app/support) · [Privacy](https://www.vividsites.app/privacy) · [Terms](https://www.vividsites.app/terms)

Original connector configuration, skill and scripts are MIT licensed. The name and logo remain trademarks. Catalog assets and retrieved content retain their own terms; this license does not relicense them or grant paid account access.
