# VividSites in VS Code with GitHub Copilot

Every tool requires your own paid VividSites library account. Obtain your API key from https://www.vividsites.app/mcp. Your GitHub Copilot subscription does not include VividSites access.

1. Open the project where you want to use VividSites.
2. Merge [configs/vscode.json](../configs/vscode.json) into `.vscode/mcp.json`. Keep existing `servers` and `inputs` entries. The file contains only a password-input reference, so no personal key is committed.
3. Run **MCP: List Servers**, select **vividsites**, and start the server. Confirm that you trust the declared VividSites endpoint when VS Code requests it.
4. Enter your own key in VS Code's masked input prompt.
5. Open Copilot Chat in Agent mode, enable the VividSites tools, and ask: **Find three cinematic website templates and show their previews.**

Expected discovery: six tools, including template search, previews, build prompts, component search/source and video prompt guidance. Verify a real tool result before considering installation complete. Workspace or enterprise policies may require your administrator to enable MCP.

## Access and troubleshooting

401 means the key is missing, invalid or revoked. 403 means the account lacks paid library access. 503 means the access lookup is temporarily unavailable. Premium prompt retrieval can consume the account's existing daily allowance. Re-enter a replaced key through VS Code's input controls; never write it into the shared JSON, chat, or a URL.

The connector retrieves assets for Copilot to use in your requested project. It does not generate or deploy sites through VividSites Create. The configuration is a custom MCP setup, not a certified Microsoft marketplace listing.

Support: https://www.vividsites.app/support

Official reference: https://code.visualstudio.com/docs/agent-customization/mcp-servers
