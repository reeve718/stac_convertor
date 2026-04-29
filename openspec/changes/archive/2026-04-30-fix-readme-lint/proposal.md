## Why

The README.md has multiple markdownlint violations (MD041, MD042, MD031, MD040, MD060, MD032) causing VSCode to display warnings. These are style issues that don't affect rendering but create noise in the editor.

## What Changes

- Move H1 heading (`# stac-convertor`) to first line - badges below
- Fix empty link `(#)` on CI badge line
- Add language specifier to fenced code blocks (`bash` for CLI examples)
- Add blank lines around fenced code blocks
- Fix table column style (add spaces around pipes for compact style)
- Add blank lines around lists

## Capabilities

### New Capabilities
None — this is a style/style fix that doesn't introduce new capabilities.

### Modified Capabilities
None — no spec-level behavior changes.

## Impact

- **Affected code**: `README.md` (markdown style fixes only)
- **Behavior**: README renders the same, just cleaner Markdown
