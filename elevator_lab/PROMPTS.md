# Agent prompts

Complete POLICY.md and PLAN.md and add S6 to scenarios.py first. Give each role SPEC.md, POLICY.md, PLAN.md, AGENTS.md and all six supplied Python files. Give the reviewer the **current implementations**, including your added scenario.

## Start in Copilot or Claude

1. In VS Code, open **File → Open Folder** and choose `elevator_lab` itself. Confirm models.py and SPEC.md appear at the workspace root.
2. Open Copilot Chat from the Copilot/Chat icon. Start a new chat using **New Chat (+)**. If your interface offers Ask, Plan and Agent, select **Agent**. Interfaces vary; a separate multi-agent window is not required.
3. If **Configure Tools** is available, search for **Run Subagent** and enable it if listed. Other Copilot interfaces delegate through a `task` tool instead; the prompt below requests whichever capability is available.
4. Use **Terminal → New Terminal**. Run `python --version`. On Windows, try `py --version` if that fails; on macOS/Linux, try `python3 --version`. Use a working Python 3.10+ command consistently and tell the coordinator which one worked. No package installation is needed.
5. Paste the builder prompt below. Watch for two actual worker/tool entries or delegated-session links, and expand them to inspect progress. Role headings in an answer are not evidence of separate workers.

For Claude Code, open its chat/terminal session in this same folder and use the same prompt. Claude inside Copilot's model picker still uses Copilot's tools and interface. Chat-only Claude can use the manual route below.

If delegation is unavailable or setup takes more than five minutes, use the separate-session route. Both routes earn the same marks.

## Automatic worker route

### Two builders

Replace `[PYTHON]` with your working command, such as `py`, before sending.

```text
Read AGENTS.md, SPEC.md, POLICY.md, PLAN.md and the Python files.
Confirm the workspace folder containing models.py and SPEC.md.
Use workspace-relative paths and the actual terminal shell.
My working Python command is [PYTHON].

Actually delegate to two separate implementation workers using the
available subagent or delegated-session tool. Do not simulate roles
or implement both files yourself. If delegation is unavailable, stop
and tell me.

1. Dispatcher Builder: implement choose_elevator in dispatcher.py only.
   Follow my POLICY.md and use rules.eligible_ids.
2. Display Builder: implement run_scenarios in app.py only, following
   SPEC.md and the shared Decision interface in models.py.

Give both workers the relevant shared context, exact workspace,
working Python command and permission to edit their owned file.
Preserve all other files. Use the supplied unittest tests, not pytest.
Workers must report whether they edited the workspace or returned code.

Wait for both workers to finish. Inspect the actual files before
integrating anything: do not reapply code already written there.
If outputs are elsewhere, integrate only the two owned files.
Then run from the folder containing models.py:
[PYTHON] -m unittest -v
[PYTHON] app.py

Report the worker executions, changed files, actual command output
and unresolved issues. Do not claim success for a failed command.
Stop for my inspection. Do not start the reviewer or make further fixes.
```

### Inspect the combined result

Wait for both workers to finish before editing their files. Check the Source Control diff and the final test/application output. If workers edited the shared folder, their changes are already there. If they used separate workspaces, integrate the two owned files first. A failed attempt to reapply an old stub is not proof that integration failed; inspect the current file.

### Reviewer: after integration

```text
Delegate one separate read-only review of the current combined code.
Give it SPEC.md, POLICY.md, PLAN.md, AGENTS.md and all current Python files.
Do not include the builders' assurances that the work is correct.
Check shared requirements, fidelity to my policy, and the app/dispatcher interface.
Also identify one possible tradeoff in my policy using a concrete scenario.
Report at most three concerns. For each, distinguish implementation defect,
policy inconsistency, or policy tradeoff. Name the rule/function and supporting case.
Label results not executed as predictions. No-defect conclusions are acceptable.
Use the confirmed workspace and working Python command. Read the actual files; do not infer correctness from the coordinator summary. Use unittest if executing tests.
Do not edit or fix files. Return findings for my decision.
```

## Separate-session route

In Copilot Chat, select **New Chat (+)** for the dispatcher builder. After it finishes, start another fresh chat for the display builder, then a third for review. Run them sequentially in the same folder. In Claude, use the equivalent new-session control. Attach/reference the shared context above and state your working Python command. Workers may edit their owned files directly; copy code yourself only when it was returned without being written. Record this as **manual coordination**, rather than automatic delegation.

### Session 1: dispatcher builder

```text
Implement dispatcher.py only, using SPEC.md, rules.eligible_ids and my POLICY.md.
Preserve the interface and implement the stated priorities and tie-breaker.
Do not change the policy or any other file. Return or write the complete file.
Report checks actually run and unresolved issues.
```

### Session 2: display builder

```text
Implement app.py only according to SPEC.md. Use the imported choose_elevator
and supplied Decision type, even if the dispatcher is not implemented yet.
Show each scenario's states, request, decision and reason. Do not duplicate
selection logic or change other files. Return or write the complete file.
Report checks actually run and unresolved issues.
```

### Session 3: reviewer

```text
Review the current combined implementation against SPEC.md and my POLICY.md.
Check the interface and my scenario predictions. Identify a possible policy
tradeoff using a concrete scenario. Report at most three concerns, distinguishing
implementation defects, policy inconsistencies and policy tradeoffs.
Name the relevant rule/function and evidence. Label unexecuted predictions.
A no-defect conclusion is acceptable. Do not edit files or provide automatic fixes.
```

After review, decide what is justified. Ask the relevant builder for a targeted correction if needed. Give a new invocation the current files and relevant context; do not assume it remembers an earlier run.
