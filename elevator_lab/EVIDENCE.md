# My experiment results

Name / student ID: Natthakul Yikusung 6680972

Tool, visible software version and model(s): Claude Code (CLI), model Claude Opus 5.5 (`claude-opus-5-5`) for the coordinator and all three workers; Claude Code version 2.1.329. Python 3.13.7 (`python3`).

Route: automatic workers. Claude Code started two separate background implementation workers in parallel, then one separate read-only reviewer after integration.

## Agent outputs

| Role | What it delivered | Brief excerpt or screenshot link |
|---|---|---|
| Dispatcher builder | Edited dispatcher.py directly in the workspace (no other file). Implemented my rules 1–4 using `eligible_ids`, with the tie-breaker lower `load_kg` then A, and a reason naming the deciding rule. Reported 6/6 tests OK. | "Rule 3: both eligible; B is the only idle elevator, so passengers in the moving car are not delayed." [screenshot] |
| Display builder | Edited app.py directly in the workspace (no other file). Shows the scenario name, both cars, the request, `Selected: A/B/WAIT` and the reason; returns the decisions; no dispatch logic. | Its first test run had 4 `NotImplementedError` errors (dispatcher still a stub); its re-run after the dispatcher was done showed 6/6 OK. [screenshot] |
| Reviewer | No implementation defects. Three concerns: (1) policy inconsistency, the S6 prediction text "195 kg ≤ 520"; (2) policy inconsistency, the Rule 3 reason claims "passengers ... not delayed" even in S3, where A already stops at 5; (3) policy tradeoff, Rule 3 ignores stop overlap and load. | "I found no implementation defects. dispatcher.py follows POLICY.md exactly, and app.py only displays the decision it gets back." [screenshot] |

## Compare with my predictions

Actual `python3 app.py` output (final run, after the Rule 3 reason correction):

| Scenario | Expected selection | Actual selection and reason | Matches my policy? |
|---|---|---|---|
| S1 | B | B: "Rule 3: both eligible; B is the only idle elevator, and my policy prefers an idle car over a moving one so the moving car's passengers get no extra pickup." | Yes |
| S3 | B | B: same Rule 3 reason, plus "(A already stops at floor 5, but the idle car is still preferred)." | Yes |
| S6 | B | B: same Rule 3 reason as S1 | Yes |

Other scenarios: S2 → B (Rule 3), S4 → B ("Rule 2: B is the only eligible elevator."), S5 → WAIT ("Rule 1: no elevator is eligible ...").

- Supplied suite command and actual result: `python3 -m unittest -v` → `Ran 6 tests in 0.000s` / `OK` (all 6 pass, both before and after the correction).
- One review finding or concern I checked: Concern 2, policy inconsistency in `dispatcher.choose_elevator`, Rule 3 reason string. Evidence: in S3, A already has a stop at floor 5 (stops 5, 1), so using A would add no extra stop. The fixed reason "so passengers in the moving car are not delayed" overstates the benefit there. My decision: fix it, because SPEC R3 requires an accurate explanation. I sent a targeted correction back to the dispatcher builder (reason text only, selection logic unchanged).
- Change made, if needed: dispatcher.py's Rule 3 reason now states the policy rule itself ("my policy prefers an idle car over a moving one ...") and, when the moving car already stops at the caller's floor, says so ("A already stops at floor 5, but the idle car is still preferred"). Selection logic is unchanged: the rerun gave the same choices for S1–S6 (B, B, B, B, WAIT, B) and 6/6 tests OK. The selections did not change because the reviewer found no implementation defect. Concern 1 is a misreading: "195 kg" in my S6 row is A's 130 kg plus the caller's 65 kg (195 ≤ 520), the same check as `load_kg + 65 <= 520`. The wording could say "130 + 65 = 195 kg ≤ 520" to be clearer. Concern 3 is the tradeoff I already accepted in POLICY.md, so I kept the policy.
- Does my policy serve my stated priority? Mostly, yes. **Benefit (S1):** A is moving down from 8 with about 2 passengers, and B is idle at 4, one floor from the caller. My policy sends B, so A's passengers get no extra stop at 5. **Cost/limitation (S3):** A is already stopping at 5, so sending A would cost its passengers almost nothing. My rule still sends B, starting an extra trip and taking away the only free car. The reviewer's made-up case is sharper: an idle car at 455 kg would still be chosen over an empty passing car, because my rule ignores load once one car is idle. The policy is implemented correctly but protects passengers aboard bluntly, not in every case.
- What did I have to coordinate between the agents? The two builders ran at the same time on files that depend on each other. The display builder's first test run failed with 4 `NotImplementedError` errors because dispatcher.py was still a stub, and passed only after the dispatcher builder finished. I waited for both, checked with `git diff --stat` that only dispatcher.py and app.py had changed, then ran the tests and app myself before starting the reviewer with only the current files (not the builders' claims).
