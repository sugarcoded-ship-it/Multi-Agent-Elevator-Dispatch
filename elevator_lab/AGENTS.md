# Working instructions

Read SPEC.md, POLICY.md and the completed PLAN.md explicitly. Do not assume this instruction file is automatically loaded by every tool.

- Dispatcher builder: implement dispatcher.py only. Use eligible_ids and the student's policy. Do not silently choose a different objective or tie-breaker.
- Display builder: implement app.py only. Use the declared Decision interface. Do not duplicate dispatch logic.
- Reviewer: inspect the current combined implementation, policy and scenarios. Report findings without editing files. Distinguish a code defect from a policy tradeoff.
- Keep models.py, rules.py, SPEC.md and test_contract.py unchanged. The student owns policy/scenario changes.
- Use the standard library. Report checks actually executed and label predictions.
- Do not commit, push, install packages or create extra workers. Stop for the student's integration/review decision.

After both builder outputs are integrated, the student may make or delegate targeted corrections. Run `python -m unittest -v` and `python app.py` from this folder.

## Workspace and checks

Confirm the folder containing models.py and SPEC.md. Use actual workspace paths without HTML-encoding them. Use the Python command confirmed by the student and commands compatible with the terminal shell. Tests use unittest; no pytest installation is needed. Each worker reports whether it edited its owned file directly or returned code. The coordinator waits for both workers, inspects the files, and avoids reapplying changes already present. Report failed commands and actual final results accurately.
