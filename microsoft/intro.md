# VividSites for Copilot Studio

Search cinematic website templates, inspect previews, retrieve free build prompts, and obtain UI and 3D component source code. This connection is a public, unauthenticated library integration. Premium prompts, site generation, deployment, purchases and account operations are outside its scope.

## Private custom connector

Use the Copilot Studio MCP onboarding wizard with:

- Server name: VividSites
- Server URL: `https://www.vividsites.app/api/connector`
- Authentication: None
- Transport: Streamable HTTP

Alternatively import `apiDefinition.swagger.json` into Power Apps as an OpenAPI custom connector. It follows Microsoft's published MCP endpoint example and uses `x-ms-agentic-protocol: mcp-streamable-1.0`. The six tool definitions are discovered through MCP `tools/list`; they are not six separate REST endpoints.

Test all cases in `../review/cases.json` within Copilot Studio. An imported schema alone does not establish runtime compatibility.

## Public certification

This is a custom-connector starting package, not a certified Marketplace offer. Microsoft's public certification guide requires a verified Partner Center publisher enrolled in the Microsoft 365 and Copilot program, supporting metadata and documentation, test access, and an approved authentication method. The current free package intentionally has no authentication; certification eligibility for this configuration must be resolved before submission. Do not represent it as OAuth-enabled or invent test credentials.

The existing service supports bearer API keys for entitled accounts, but this release does not bundle authenticated premium access. Adding that scope needs separate entitlement and quota tests and corresponding listing updates.

Sources:

- [MCP onboarding and OpenAPI example](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
- [Microsoft MCP certification](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-server-certification)

Support: support@vividsites.app · https://www.vividsites.app/support
