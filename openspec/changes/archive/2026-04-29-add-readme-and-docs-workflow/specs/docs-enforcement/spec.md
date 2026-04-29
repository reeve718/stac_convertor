## ADDED Requirements

### Requirement: OpenSpec tasks SHALL require README review for CLI changes

The OpenSpec configuration SHALL include a per-artifact rule for tasks that requires the developer to confirm or update `README.md` whenever the CLI surface changes.

#### Scenario: New CLI argument added
- **WHEN** a developer creates tasks for a change that adds or modifies CLI arguments in `src/cli.py`
- **THEN** the task list SHALL include a step to update `README.md`

#### Scenario: CLI change without README update
- **WHEN** a task touches `src/cli.py` and the developer skips README review
- **THEN** the change is considered incomplete per the OpenSpec rule

---

### Requirement: CLAUDE.md SHALL reference the documentation enforcement rule

The `CLAUDE.md` file SHALL reference that any CLI-related change requires README updates.

#### Scenario: Claude reads CLAUDE.md
- **WHEN** Claude Code reviews CLAUDE.md before working on a change
- **THEN** it finds a clear rule that CLI changes require README updates

---

### Requirement: README content SHALL reflect current CLI state

The `README.md` SHALL be kept in sync with the actual CLI implementation.

#### Scenario: CLI argument documented correctly
- **WHEN** a user reads `README.md` CLI reference
- **THEN** every listed argument exists in `src/cli.py` and vice versa
