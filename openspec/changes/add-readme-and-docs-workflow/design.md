## Context

The `stac_convertor` project is a GeoJSON to STAC converter with a Typer CLI. It has:
- Source code in `src/` with tests in `tests/`
- A `pyproject.toml` with dependencies (`pyproj`, `typer`)
- An OpenSpec workflow for managing changes
- No user-facing documentation

## Goals / Non-Goals

**Goals:**
- Produce a `README.md` that enables a new user to install and run the tool in under 5 minutes
- Document the CLI interface (all arguments, options, examples)
- Prevent documentation rot by enforcing README review on CLI changes

**Non-Goals:**
- Write a full developer guide (that belongs in `docs/`)
- Document every internal module (implementation docs)
- Rewrite `CLAUDE.md` completely — only add the enforcement rule

## Decisions

### 1. README.md content structure

Sections in order:
1. Badge strip (build, license, Python version)
2. One-line description
3. Installation (pip, editable dev install)
4. Quick start (single command with sample data)
5. CLI reference (`geojson2stac --help` output)
6. Configuration / how CRS transform works
7. Development setup (clone, install deps, run tests)
8. License

**Why:** Matches the standard README layout used in most Python CLI tools on GitHub. New users can scan top-to-bottom and get everything they need.

### 2. Enforce README update via OpenSpec per-artifact rule

Update `openspec/config.yaml` with:
```yaml
rules:
  tasks:
    - "For any change touching src/cli.py or adding CLI arguments, README.md MUST be updated"
```

**Why:** OpenSpec already has a per-artifact rule system. This avoids introducing a new external tool or hook. CLAUDE.md will also be updated to reference this rule.

**Alternatives considered:**
- Pre-commit hook: Too easy to bypass, requires every developer to install it
- GitHub Actions CI check: Requires CI setup, adds friction for small project
- CLAUDE.md alone: Not enforced automatically, only applies to AI agents

### 3. README goes in repo root, not `docs/`

**Why:** Standard GitHub convention — `README.md` in root is auto-rendered on the repo homepage. `docs/` is for supplementary documentation.

## Risks / Trade-offs

- **Docs drift from implementation** → Mitigated by OpenSpec rule. Human reviewer must confirm README is current.
- **README gets too long** → Keep it to ~100 lines. Developer docs go in `docs/` if needed later.
