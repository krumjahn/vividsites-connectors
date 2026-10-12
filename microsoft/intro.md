# VividSites for Copilot Studio

All six library tools require a paid VividSites library account and a personal API key. Search templates, inspect previews, retrieve build prompts and obtain UI/3D component code. No anonymous access is supported. Generation, publishing, purchases and payment collection are outside the connector's scope.

## Custom connector

- Server name: VividSites
- Server URL: `https://www.vividsites.app/api/connector`
- Authentication: API key, header `Authorization`
- Credential value: `Bearer <personal VividSites API key>`
- Transport: Streamable HTTP

Alternatively import `apiDefinition.swagger.json`, which declares API-key security and Microsoft's `x-ms-agentic-protocol: mcp-streamable-1.0`. Tool definitions are discovered through authenticated MCP `tools/list`. Store the credential in the connection, never the published definition. Existing metered premium-prompt retrieval debits the customer's shared daily allowance; it does not initiate a payment or consume Create build credits.

Test `../review/cases.json` in a tenant. Schema validation does not establish runtime compatibility.

## Public certification

This is a custom-connector package, not a certified Marketplace offer. Public certification requires a verified Partner Center publisher, enrollment in Microsoft's program, supporting documentation, reviewer test access and authentication review. OAuth is not implemented; confirm API-key eligibility for the intended distribution route before submitting.

- [MCP onboarding](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
- [MCP certification](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-server-certification)

Support: support@vividsites.app · https://www.vividsites.app/support
