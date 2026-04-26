Use the OpenSpec change as the source of truth.

Read:
- openspec/changes/<change-name>/proposal.md
- openspec/changes/<change-name>/design.md
- openspec/changes/<change-name>/tasks.md
- openspec/changes/<change-name>/specs/

Do not re-brainstorm requirements.
Use Superpowers only to:
1. create an implementation plan from these docs
2. execute with TDD, code review, and verification
3. keep implementation aligned with the OpenSpec spec

## Documentation Enforcement

Any change that touches `src/cli.py` or adds/modifies CLI arguments MUST include an update to `README.md`. This is enforced via the OpenSpec per-artifact rule for tasks. The README is the source of truth for user-facing CLI documentation.