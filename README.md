# VividSites connectors

![VividSites](assets/icon.png)

Cinematic website templates, design previews, free build prompts, and editable UI and 3D component code inside your AI assistant.

**Hosted MCP endpoint:** `https://www.vividsites.app/api/connector`

Uses Streamable HTTP. No account, API key, local server, or package install is required for the free library connection. Premium template prompts are excluded. The connector retrieves assets; your assistant implements them using its own tools. It does not generate, edit or publish through VividSites Create, buy credits, or initiate payments.

## Install

### Gemini CLI

```sh
gemini extensions install https://github.com/krumjahn/vividsites-connectors
```

Restart Gemini CLI, check `/extensions list` and `/mcp`, then try an example below. The extension includes the remote MCP server and the VividSites library skill.

### Claude Code

```sh
claude plugin marketplace add krumjahn/vividsites-connectors
claude plugin install vividsites@vividsites
```

Or connect only the server:

```sh
claude mcp add --transport http vividsites https://www.vividsites.app/api/connector
```

For Claude web or Cowork, use the custom connector settings and enter the hosted endpoint. A custom installation does not require a public directory listing.

### Cursor

Merge the contents of [configs/cursor.json](configs/cursor.json) into your MCP configuration. Do not replace existing servers. The root `plugin.json` and `mcp.json` also form an Agent Plugins package for hosts supporting that standard.

### GitHub Copilot

For VS Code, merge [configs/vscode.json](configs/vscode.json) into `.vscode/mcp.json`. For Copilot CLI:

```sh
copilot mcp add --transport http vividsites https://www.vividsites.app/api/connector
```

Alternatively merge [configs/copilot-cli.json](configs/copilot-cli.json) into the CLI MCP config. Organization policies may restrict custom servers.

### Kimi Work / Kimi Code

Install this repository using the app's GitHub plugin installation flow, or import the release ZIP. `kimi.plugin.json` declares the remote server and skill. Restart or reload plugins if required, then inspect the MCP connection status. Client runtime verification is tracked in [RELEASE-STATUS.md](RELEASE-STATUS.md).

### Qwen Code

```sh
qwen mcp add --transport http vividsites https://www.vividsites.app/api/connector
```

Or merge [configs/qwen-code.json](configs/qwen-code.json) into Qwen Code settings. Use `httpUrl` for Streamable HTTP; `url` means legacy SSE in this client.

### Qwen Work

Organization admins can add a connector with key `vividsites`, the hosted endpoint, and **No authorization**. This is an organization connector, not a public marketplace listing. See [Qwen Work's instructions](https://docs.qwenwork.ai/enterprise/connectors).

### Grok chat

Open [Connectors](https://grok.com/connectors), choose **New Connector → Custom**, and enter the hosted endpoint. Grok Bot's Marketplace plugin distribution is tracked separately in the release status.

### Gemini web / mobile

On the web, open **Settings → Connected Apps → Custom apps**, and add the hosted endpoint. Google currently documents US personal-account, age, language and activity-setting restrictions. Eligibility and no-auth compatibility must be checked in the actual account. See [Google's current requirements](https://support.google.com/gemini/answer/17209137?hl=en).

### Microsoft Copilot Studio

In an agent, choose **Tools → Add a tool → New tool → Model Context Protocol**. Enter VividSites, the endpoint, and **None** for authentication. See [microsoft/intro.md](microsoft/intro.md) for the importable OpenAPI definition and public certification prerequisites.

### Muse and DeepSeek-based apps

Muse directory publication requires its connector review process; see release status. For a DeepSeek-based app supporting remote MCP, add the hosted endpoint using that app's documented Streamable HTTP configuration. Different community apps use the DeepSeek Cowork name, so no universal installer is claimed.

## Try it

- “Find three free cinematic website templates and show their previews.”
- “Get the complete build prompt for the cinematic template.”
- “Find a magnetic button and give me its HTML, CSS and JavaScript.”

| Tool | Result |
| --- | --- |
| `search_sites` | Ranked template catalog matches |
| `get_template_preview` | Library URL, poster, video, and live preview when available |
| `get_build_prompt` | Complete accessible build instructions and asset URLs |
| `search_components` | UI and 3D component matches |
| `get_component` | Component source, dependencies and installation command |
| `video_prompt_formula` | Cinematic video prompt guidance |

## Validation

```sh
python3 scripts/verify-live.py
claude plugin validate .
```

The live check verifies MCP initialization, tool annotations, all six tools, and unknown-component error handling. It makes public library requests and does not spend account credits. Protocol validation is not proof of runtime compatibility in every host. See [review/cases.json](review/cases.json) for manual host scenarios and [RELEASE-STATUS.md](RELEASE-STATUS.md) for completed checks and listing status.

## Support and licensing

[Website](https://www.vividsites.app) · [Support](https://www.vividsites.app/support) · [Privacy](https://www.vividsites.app/privacy) · [Terms](https://www.vividsites.app/terms)

This repository's original connector configuration, skill and scripts are MIT licensed. The VividSites name and logo remain trademarks. Catalog assets and retrieved content are governed by their own terms; this repository's license does not relicense them.
