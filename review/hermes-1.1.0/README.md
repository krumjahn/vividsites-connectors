# Hermes 1.1.0 verification

Checked on November 12, 2026. This extends the existing paid-library branch, whose baseline was `5002f0e8ce690612bcea368fb2b7231719e95314`. It does not replace or claim approval of the separate free-component catalog proposal.

- `python3 -m unittest discover -s tests/hermes -v`: 22 offline tests passed. These use fixtures, not paid account credentials.
- `hermes plugins validate ./hermes --install-deps --json`: all 15 checks passed, security scan safe, zero warnings.
- `hermes plugins doctor ./hermes --ci`: actual discovery, parsing, import and registration passed, with seven tools and one hook.
- Hermes runtime approval check: the actual registered hook reached Hermes's approval gate; both `vividsites_get_build_prompt` and `vividsites_get_website_blueprint` were blocked in a non-interactive context without a human approval bridge. The search tool did not escalate. The check used Hermes's isolated Doctor loader, with sockets disabled. No service calls were made.
- `python3 scripts/verify-live.py`: anonymous initialization, discovery and all six service operations returned HTTP 401; an invalid key returned HTTP 401. Valid unpaid-account HTTP 403 and paid-account success were skipped because credentials were absent.
- `git diff --check`: passed.
- Independent source review identified malformed MCP result shapes that could have advanced to the metered prompt. Fixed with source-shape validation and regression coverage; re-review found no remaining blocker.

Hermes validation/runtime source: `NousResearch/hermes-agent` commit `b5f15a6d3188e94f815d504d5ebbeb926e1bd08a`. Validation, unit and live-access logs are alongside this file.

## Not verified or performed

- No paid VividSites credential was configured in this Hermes runtime. No claim of an authenticated end-to-end Hermes build is made.
- No unpaid-account credential was available. Invalid-key HTTP 401 is not evidence of valid unpaid-account HTTP 403.
- No website was built or deployed by the plugin. The blueprint retrieves design sources; Hermes's project tools perform the implementation.
- No merge, catalog admission, hackathon acceptance or social-video publication is part of this verification.
