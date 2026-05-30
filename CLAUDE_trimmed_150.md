# CLAUDE.md

## Purpose
This repo uses OpenSpec for change definition and Superpowers for implementation planning and execution.[cite:23][cite:25][cite:26]

Treat OpenSpec as the source of truth for **what** to build and Superpowers as the default system for **how** to build it.[cite:22][cite:23][cite:26]

## Default workflow
Use this sequence for normal feature work:[cite:1][cite:22][cite:23]
1. `/opsx:propose <new idea>`
2. `/superpowers:write-plan`
3. `/superpowers:execute-plan`
4. Request code review
5. Finish the development branch
6. `/opsx:archive`

## Ownership
- OpenSpec owns proposal, specs, design, tasks, and archive state.[cite:23][cite:26]
- Superpowers owns plan writing, execution, subagent orchestration, TDD-style work, review flow, and branch finishing.[cite:1][cite:22][cite:25]
- If they overlap, OpenSpec decides scope; Superpowers decides execution strategy.[cite:22][cite:23][cite:26]

## Command rules

### `/opsx:propose <new idea>`
Create or update the OpenSpec change artifacts for the requested idea.[cite:23][cite:26]

Expected outputs usually include proposal, specs, design notes, and tasks.[cite:23]

### `/superpowers:write-plan`
Never reject this just because OpenSpec artifacts already exist.[cite:1][cite:22]

Interpret it as: create an implementation plan from the active OpenSpec change, optimized for subagent execution.[cite:1][cite:22][cite:25]

Before planning:
- Read the current OpenSpec artifacts.
- Use proposal, specs, design, and tasks as inputs.
- Preserve OpenSpec terminology and acceptance criteria where practical.
- Break work into small executable tasks with verification steps.[cite:1][cite:22][cite:25]

### `/superpowers:execute-plan`
Use Superpowers execution flow once a plan exists.[cite:1][cite:22]

Execution defaults:
- Prefer subagent-driven development for feature work that can be isolated by task.[cite:22]
- Prefer test-driven development for risky refactors, bug fixes, logic-heavy work, or weakly-tested code.[cite:22]
- Keep work traceable back to the OpenSpec tasks.[cite:23][cite:26]

During execution:
- Keep code changes minimal and scoped.
- Update task status against the OpenSpec change.
- Pause if requirements are unclear or conflict with the artifacts.[cite:23][cite:26]

### Code review
Review code against:
- OpenSpec proposal, spec, design, and tasks
- the implementation plan
- tests, regressions, and merge readiness.[cite:22][cite:26]

Call out:
- spec mismatches
- missing tests
- risky shortcuts
- unresolved finish blockers.[cite:22]

### Finishing the branch
Before finishing a branch:
- verify implementation tasks are done,
- verify tests and checks pass,
- verify review feedback is resolved or explicitly accepted.[cite:22][cite:28]

Do not archive the OpenSpec change before the branch is actually ready and accepted.[cite:23][cite:26]

### `/opsx:archive`
Archive only after implementation, review, and branch completion are done.[cite:23][cite:26]

Do not archive early.

## Active change selection
If a command does not name the change explicitly:
- infer the active change only when unambiguous,
- otherwise ask which change to use.[cite:23][cite:26]

Always state which change is being used before planning or execution.

## Conflict rule
If planning or execution reveals a gap, ambiguity, or conflict in OpenSpec artifacts:
1. stop,
2. explain the issue,
3. update the artifacts first,
4. then resume planning or execution.[cite:23][cite:26]

Do not silently override approved OpenSpec requirements.

## Practical defaults
- Use OpenSpec to define and close changes.[cite:23][cite:26]
- Use `/superpowers:write-plan` after proposal work; proposal does not replace execution planning.[cite:1][cite:22][cite:23]
- Use subagent-driven development by default for implementation.[cite:22]
- Use test-driven development when change risk is high.[cite:22]
- Run code review before finishing the branch.[cite:22]

## Progressive disclosure
Keep this file short and universal. Put detailed checklists and task-specific guidance in separate docs rather than expanding this root file.[cite:30][cite:37][cite:52][cite:54]

Suggested references:
- `.claude/workflows/openspec-superpowers.md`
- `.claude/workflows/review-checklist.md`
- `.claude/workflows/branch-finish.md`
