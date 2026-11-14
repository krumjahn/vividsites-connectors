# Online validation after reconnection — November 14, 2026

Checked the existing source PR at `e988245c704aa0441f547fbcb08abb624bc00db6` and catalog PR at `8325e44bd4b8c60e56474349469c4b6020535107` in clean detached worktrees. Earlier unrelated local edits were preserved.

The catalog continues to install runtime pin `ac045b1d3adfdfb663beb36a8586aa7728362d02`, subdirectory `hermes`. The only difference in that package at the checked source head is the approved banner image; runtime Python, manifest and skill bytes match the runtime pin. This evidence update changes no plugin files and does not require a new runtime pin.

## Fresh passes

- `python3 -m unittest discover -s tests/hermes -v`: **32 tests pass**. Python emits ResourceWarnings for synthetic HTTPError fixtures; these are test placeholders, not real secrets.
- Official `hermes plugins validate ../source-verified/hermes --install-deps --json`: **15 checks pass**, security scan **safe**, zero warnings. Hermes PM successfully prepared the isolated full Python environment. No dependency-preparation failure was reported. This supersedes the earlier DNS-blocked attempt.
- Official `hermes plugins doctor ../source-verified/hermes --ci`: real discovery/import/registration pass; **nine tools and one hook**.
- `scripts/verify-hermes-runtime.py`, run using the full PM-prepared interpreter with real VividSites keys explicitly unset: keyless magnetic-button retrieval returns **15,437 bytes**; free retrieval also succeeds with a synthetic invalid optional key; paid search rejects that key with **HTTP 401**; an empty scope after a keyed scope returns **missing_api_key**. Template slug, traversal and URL requests are refused by the free tool.
- Real Hermes unattended approval gate, using the current package loaded through Doctor with network disabled: both metered tools are blocked without a human present. No paid handler is dispatched. Free tools and non-metered search do not request allowance approval.
- Official catalog structural validator: the current listing including the banner passes with zero errors or warnings.
- Actual Hermes catalog loader/search: exact title **VividSites — Cinematic Website Design**, unchanged runtime pin, expected image URL, and a match for **cinematic website** are verified.
- `git diff --check`: passes in both clean checked worktrees.

Hermes validation/runtime source: `NousResearch/hermes-agent@342b54fa53f075685c66fc83a74e80872f1a99ec`. `HERMES_HOME` and `HERMES_RUNTIME_DIR` were isolated inside the task workspace. No services were enabled.

Logs: [unit tests](unit-tests.txt), [validation](validation.json), [Doctor](doctor.txt), [live runtime](runtime.json), [approval gate](approval.txt), [catalog](catalog.json). Logs contain metadata/hashes, not component source or real credentials.

## Preserved banner and listing

The catalog image URL remains pinned to `e988245c704aa0441f547fbcb08abb624bc00db6/hermes/docs/marketplace-banner.png`. The fetched image was visually inspected: readable VIVIDSITES and CINEMATIC WEBSITES text over abstract red/purple artwork. It is **1774 × 887**, exactly **2:1**, **1,902,298 bytes**, SHA-256 `91e30bd9441949a16372bb6599793a5cafe98853de443f2a124e283cad3c0560`. No duplicate or replacement artwork was created.

The upstream public website renderer inspected previously omits the separate title field and renders the internal name; the correct metadata does not establish display on every surface. Marketplace acceptance/display remains unverified.

## Still not passed or not run

- Valid paid-account success and valid unpaid-account HTTP 403: **not run; no test credentials supplied**. Synthetic invalid-key 401 is not an unpaid-account result.
- Metered build-prompt retrieval: **not requested; explicit allowance approval still required**.
- Complete Hermes-generated website: **not run**.
- Desktop masked-key save, persistence, reload and authenticated use: **not run**.
- Exact catalog-head CI at `8325e44bd4b8c60e56474349469c4b6020535107`: [Plugin Catalog CI run 43537268844](https://github.com/NousResearch/hermes-agent/actions/runs/43537268844) reports **action_required**, requiring maintainer approval. Other reported workflows at that head also require approval. No remote CI pass is claimed.
- No source PR workflow runs were reported for checked head `e988245c704aa0441f547fbcb08abb624bc00db6`.

Both existing PRs remain **draft**. No merge, deployment, paid allowance use, purchase, real health-data/token access, service enablement or unrelated-source publication occurred. Separate Apple Health work was not touched.
