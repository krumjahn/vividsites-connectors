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

## Additional live passes — November 14

The existing saved review account was authenticated through VividSites's ordinary public login/profile APIs. Its existing **lifetime** entitlement and API key were used securely in isolated temporary Hermes profiles. No account entitlement changed and no purchase occurred. The key and login credentials were never included in logs or repository files.

- Real Hermes registry dispatch: paid template search and preview **pass** for `sanctum`; the full keyless/invalid-key/profile-isolation probe also passes again. See [paid runtime](runtime-paid.json).
- One explicitly user-authorized `vividsites_get_website_blueprint` invocation **passes**, including one complete premium prompt retrieval and the real preview. The registered approval hook was verified before dispatch; this harness used the user's explicit authorization, rather than exercising an interactive Hermes approval click. Response: **12,230 bytes**, SHA-256 `8e0b82ff52fa4b7f34900d14e0c9d13deb7a195788510969fb390a6b5cc2f065`. Lifetime access does not decrement a capped daily allowance; monthly-plan metering is therefore not proven. No additional prompt retrieval was attempted. See [retrieval metadata](authorized-retrieval.json). The paid prompt itself is not published here.
- Actual Desktop credential backend via FastAPI TestClient: **PUT /api/env** saves, **GET /api/env** redacts, the manifest field reports presence without its value, `.env` is private (**0600**), and `config.yaml` contains no key. A fresh process reloads the persisted key and successfully searches through the real Hermes plugin. See [persistence metadata](settings-persistence.json). This is backend integration coverage; it does not claim native Desktop UI verification.

These checks ran on source `71d60f0e2659038d0afe99c6ca107017a38d6fd1`, whose plugin bytes match the earlier checked source head. This follow-up changes evidence only.

## Authorized complete website build — November 14

The user explicitly authorized sending the retrieved Sanctum blueprint to the Codex model service for this one local build test, with no blueprint publication. **Hermes AIAgent generated the complete website**, using the unabridged blueprint already retrieved; **zero additional VividSites prompt retrievals** occurred. The private blueprint and generated HTML are not committed or deployed.

The generated single-file responsive site is **24,983 bytes**, SHA-256 `7459648e1055772f035a78cadd67c0ba3bacee23b0d34be747e8472fc5c3b781`. It uses inline CSS/JavaScript and the supplied cinematic video asset. Real Chrome validation through browser-harness passed:

- **1440 × 1000 desktop** and **390 × 844 mobile** render without horizontal overflow; screenshots were visually inspected locally.
- Every fragment navigation target exists. Desktop Visit navigation works; the visit dialog opens and closes through real clicks.
- Mobile navigation opens, navigates, closes and updates `aria-expanded`.
- The video decodes successfully (`readyState = 4`, duration **8.041667 seconds**). Scrolling to 1500 px advances it to **2.847791 seconds**.
- Emulated reduced motion disables animations and smooth scrolling and resets the video to zero.

The first harness attempt hit Hermes's implicit non-stream watchdog despite active Codex progress, and a streaming attempt hit its 12-second event-idle threshold. The same build test completed with streaming, the documented 120-second event timeout and automatic retry loops disabled. These are test-harness settings, not plugin changes. The prior approval rejection was resolved by the user's explicit destination-specific approval.

[Generation/preview metadata](generated-site-result.json), [Desktop validation scope](native-desktop-validation.json), [six settings-form tests](desktop-settings-form-tests.txt). No blueprint, generated HTML, screenshot, credentials or account identifiers are in these evidence files. The localhost preview tab/server and test app were closed; no persistent service was enabled.

## Verification limits and external admission steps

- Valid unpaid-account HTTP 403: **not run**. The discovered review account is lifetime, not unpaid. An existing valid unpaid test-account key is needed; invalid-key 401 is not equivalent. No account was created, downgraded or modified.
- Native Desktop masked-key entry/save/reload interaction: **not completed**. The isolated Desktop source build now succeeds, and all **six** actual settings-form tests pass (masked field, secret routing, clearing after save and input validation). Actual credential backend persistence and authenticated fresh-process reload already pass. The native app opened to its setup screen; Computer Use issued an app-access approval for **Electron**, which is still pending. The test app was closed. Neither form tests nor backend coverage are represented as a completed native UI test.
- Exact catalog-head CI at `8325e44bd4b8c60e56474349469c4b6020535107`: [Plugin Catalog CI run 43537268844](https://github.com/NousResearch/hermes-agent/actions/runs/43537268844) still reports **action_required**, requiring maintainer approval. Other reported workflows at that head also require approval. No remote CI pass is claimed.
- No source PR workflow runs were reported for `71d60f0e2659038d0afe99c6ca107017a38d6fd1`.

The plugin is **ready for maintainer review**, with the unpaid-account and native UI verification gaps disclosed. These additional test cases are not documented prerequisites for changing a submission from draft to ready. The complete website-build gate passes. GitHub's raw PR API reports the catalog mergeable with state `blocked`; this is not a content conflict. The source PR is also mergeable. No merge, deployment, purchase, real health-data/token access, service enablement or unrelated-source publication occurred. Separate Apple Health work was not touched.

## Submission readiness reassessment — November 14

Checked the current upstream [catalog submission guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/plugins/catalog-submission.md), including its admission rules, plus both PRs' review/comment threads. Neither PR has a reviewer request imposing additional checks. The guide requires a public loadable plugin, an exact SHA, accurate capabilities/disclosures, public extension surfaces and passing local `hermes plugins validate --install-deps`. Maintainer-approved CI and human review/merge remain admission requirements. It does not require a valid-unpaid-account live test or a native Desktop walkthrough before a PR can be marked ready for review. This is an agent plugin with a host-generated secret setting, not a custom Desktop renderer plugin.

Fresh validation ran directly against a clean checkout of exact catalog pin **`ac045b1d3adfdfb663beb36a8586aa7728362d02`**: **15 checks pass, security safe, no warnings**. See [exact-pin admission validation](pinned-admission-validation.json). The source follow-up contains evidence only; the pinned runtime and approved banner are unchanged.

A narrow recheck of existing VividSites environment variables, its known credential directory and project environment files found **no existing unpaid test key**. The existing review login has lifetime access. No account, credential or entitlement was created or changed. HTTP 403 error handling is covered by the passing synthetic adapter tests, but that is explicitly not a live unpaid-account result. Computer Use's Electron access card remains unapproved; the native walkthrough remains uncompleted. Existing real backend persistence, six settings-form tests and the complete Hermes build support review readiness without representing those gaps as passes.

The previous draft hold treated extra verification goals as submission prerequisites. The current assessment is to submit both existing PRs for maintainer review with these limits visible. The only external acceptance gate is now maintainer action: approve/run catalog CI, review the pinned plugin and decide whether to merge or request more evidence. No upstream merge or deployment is authorized or performed.
