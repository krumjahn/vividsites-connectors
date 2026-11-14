# Combined Hermes plugin verification: 1.2.0

Checked November 12, 2026. One plugin combines the keyless public-component implementation from PR #2 with the optional paid-library and website-blueprint implementation in PR #3. No service billing rules were changed.

## Passed

- 32 offline unit tests: public classification and document rechecks, safe slugs/paths, malformed file-list refusal, no public auth headers or secret resolution, paid missing-key handling without public fallback, complete blueprint sources, malformed-response rejection, allowance escalation, response limits, and existing authenticated-client contracts.
- Official `hermes plugins validate ./hermes --install-deps --json`: all 15 checks passed, security scan safe, zero warnings. The optional secret schema is valid; `requires_env` is empty.
- `hermes plugins doctor ./hermes --ci`: actual discovery, manifest parsing, import and registration pass, with nine tools and one hook.
- `scripts/verify-hermes-runtime.py`, running in real Hermes with a new isolated home and no API key: plugin loads and retrieves `magnetic-button` from the public registry. Source metadata and SHA-256 are in `runtime.json`; source code and secrets are not logged.
- The same runtime with a synthetic invalid optional key still retrieves the public component. A paid template search returns HTTP 401, with no anonymous fallback.
- Returning to an empty secret scope after the keyed scope produces `missing_api_key`, not the prior profile's key. This covers isolation for the tested sequential scopes, not a claim about every deployment mode.
- Template IDs, traversal slugs and URLs are refused by the free component tool.
- Actual Hermes unattended approval blocks both direct build prompts and blueprints; free tools and non-metered search do not escalate. This check uses the isolated Doctor loader with sockets disabled; it does not consume allowance.
- `git diff --check` passes.

Logs: `unit-tests.txt`, `validation.json`, `doctor.txt`, `runtime.json`, and `approval.txt`.

Hermes validation/runtime source: `NousResearch/hermes-agent` commit `b5f15a6d3188e94f815d504d5ebbeb926e1bd08a`.

## Still pending

No valid paid or unpaid key is configured in this test executor. The runtime probe explicitly skips authenticated paid-account search/preview and valid unpaid-account HTTP 403. An invalid-key 401 is not an unpaid-account result. No metered build prompt was requested, and no end-to-end Hermes website build is claimed.

The runtime probe injects scoped credentials using Hermes's supported secret API. The Desktop masked-setting save/persistence/reload path has not been exercised. Independent review found no access-isolation blocker; its malformed public file-list edge case was fixed with regression coverage.

The connected VividSites service can be checked separately, but success through another host is not proof that this Hermes credential path works. The runtime script supports securely supplied existing credentials for those next checks; it does not ask for, store, generate or log credentials.

Catalog CI and maintainer approval remain separate. This verification performs no merge, deployment, plan purchase, or social publication.
