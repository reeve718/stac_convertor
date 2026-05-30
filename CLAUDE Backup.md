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

## Workflow Rules

All code changes MUST go through OpenSpec change workflow:

- Create a change with `/opsx:propose` or `/opsx:create`
- Implement with `/opsx:apply` or the subagent-driven-development skill
- Archive with `/opsx:archive` when complete
- Never modify code directly outside of a change

Explore mode is for thinking only:

- `/opsx:explore` is for investigation and discussion
- Code changes are NOT permitted in explore mode
- If implementation is needed, exit explore mode and create a change proposal first

## Documentation Enforcement

Any change that touches `src/cli.py` or adds/modifies CLI arguments MUST include an update to `README.md`. This is enforced via the OpenSpec per-artifact rule for tasks. The README is the source of truth for user-facing CLI documentation.
