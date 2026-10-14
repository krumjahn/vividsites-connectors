# VividSites in Codex

Every tool requires your own paid VividSites library account. Sign in at https://www.vividsites.app/mcp and obtain your personal API key. Your Codex or ChatGPT subscription does not include VividSites access.

## Codex CLI

In the terminal where you will launch Codex, enter the key without putting it in shell history:

```sh
printf 'VividSites API key: '
IFS= read -r -s VIVIDSITES_API_KEY
printf '\n'
export VIVIDSITES_API_KEY
codex mcp add vividsites --url https://www.vividsites.app/api/connector --bearer-token-env-var VIVIDSITES_API_KEY
codex mcp list
```

Start a fresh Codex session from that terminal. Use `/mcp` to inspect the connection and tools, then ask: **Find three cinematic website templates and show their previews.**

The configuration stores the environment-variable name, not the key. The variable must be available each time Codex starts; you can supply it from your own secret manager. Do not commit or paste the key into chat. Other Codex processes, including the IDE extension, must receive their own process environment containing the variable.

Alternatively merge [configs/codex.toml](../configs/codex.toml) into your Codex configuration. Preserve existing settings. Avoid adding the same server twice.

## Access and troubleshooting

401 means the key is missing, invalid or revoked. 403 means the account lacks paid library access. 503 means the access lookup is temporarily unavailable. A Create credit pack alone does not grant library access. Premium build-prompt retrieval can use the account's existing daily allowance.

The connector supplies assets for Codex to implement within your requested project. It does not run VividSites Create or deploy a site. This setup uses a custom MCP connection; it is not evidence of a public Codex marketplace listing.

Support: https://www.vividsites.app/support

Official reference: https://learn.chatgpt.com/docs/extend/mcp?surface=cli
