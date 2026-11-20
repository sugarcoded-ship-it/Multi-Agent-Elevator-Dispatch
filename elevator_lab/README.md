# Two elevators, different priorities

A small office building has eight floors and two elevators. You design a dispatch policy, then coordinate two AI builders and a reviewer to implement and examine it. This program evaluates independent snapshots; it does not animate elevator journeys.

## Start

Use Python 3.10 or newer. No packages are required. In VS Code, choose **File → Open Folder → elevator_lab**, then **Terminal → New Terminal**. Confirm models.py and SPEC.md are in this folder.

Check `python --version`. If unavailable, try `py --version` on Windows or `python3 --version` on macOS/Linux. Substitute that working command throughout and tell your agents which command to use. The tests use Python’s built-in unittest, not pytest.

```sh
python -m unittest -v
```

The two implementation files are stubs: **six tests initially report NotImplementedError**. This is expected. After implementation:

```sh
python -m unittest -v
python app.py
```

Use `python3` or `py` consistently instead if that is your system's launcher. Run commands from this folder.

## Files

| File | Purpose / owner |
|---|---|
| SPEC.md | Supplied common requirements and model assumptions |
| models.py, rules.py | Supplied data structures and eligibility helper |
| scenarios.py | Five supplied scenarios; you add S6 |
| POLICY.md | Your priorities, selection rule and predictions |
| PLAN.md | Your short delegation plan |
| dispatcher.py | Dispatcher builder's implementation |
| app.py | Display builder's implementation |
| test_contract.py | Shared tests, independent of your preference policy |
| AGENTS.md, PROMPTS.md | Working instructions and role prompts |
| EVIDENCE.md | Your observed outcomes and decisions |

## Adding your scenario

Add a `Scenario` entry to SCENARIOS, following the supplied examples. Give it a name beginning `S6`. Use valid floors, directions, loads and stops from SPEC.md. Keep the original five entries.

> A useful variation changes a meaningful fact, such as an elevator's direction or an existing stop. Ask whether your policy should change its choice, and why.

## Agent access

Follow the **Start in Copilot or Claude** steps in PROMPTS.md, then use its copyable builder and reviewer prompts. Copilot and Claude are permitted. Use automatic implementation workers if available, or separate fresh sessions with you coordinating the outputs. Sequential sessions earn the same marks. If workers edit this folder directly, inspect their changes without copying them again. If a worker uses a separate folder/worktree, integrate its owned file into this folder before running the app. For a chat-only tool, provide files and copy the returned implementation yourself.

## Load readings

Each scenario supplies `Elevator.load_kg`, a simulated passenger-and-luggage sensor reading. The model limit is 520 kg (8 × 65 kg). Reserve 65 kg for the caller: 455 kg fits exactly; 456 kg does not. `load_kg / 65` is an occupancy estimate, not an exact count.
