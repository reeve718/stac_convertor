## Why

The project has no user-facing documentation. Anyone cloning the repo has no guidance on how to install or use the convertor. Additionally, the OpenSpec workflow lacks a rule requiring documentation updates when the CLI changes, leading to docs rot.

## What Changes

- Add `README.md` with installation, usage, and CLI reference
- Update `CLAUDE.md` to require README updates as part of any CLI-related change
- Configure OpenSpec with a per-artifact rule enforcing this

## Capabilities

### New Capabilities

- `readme`: User-facing README covering installation, quick start, CLI reference, and examples
- `docs-enforcement`: OpenSpec rule requiring README review/update when CLI surface changes

### Modified Capabilities

- (none)

## Impact

- New file: `README.md`
- Modified file: `CLAUDE.md` (add docs-enforcement rule)
- Modified file: `openspec/config.yaml` (add per-artifact rule for tasks)
