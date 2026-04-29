## Context

README.md has multiple markdownlint violations causing VSCode warnings:
- MD041: First line should be H1 (badges come first)
- MD042: Empty link `(#)` on CI badge
- MD031: Fenced code blocks need surrounding blank lines
- MD040: Fenced code blocks missing language specifier
- MD060: Table column style needs spaces around pipes
- MD032: Lists need surrounding blank lines

## Goals / Non-Goals

**Goals:**
- Fix all markdownlint violations in README.md
- Maintain readability and visual structure

**Non-Goals:**
- No changes to actual content or documentation content
- No changes to how README renders
- No new features

## Decisions

### Move H1 heading first, badges after

**Decision:** Reorder so `# stac-convertor` is the first line, followed by badge line.

**Rationale:** MD041 requires first line to be a top-level heading. The solution is to move the H1 before the badges.

**Alternatives considered:**
- Suppress MD041 via .markdownlint.json — wrong direction, hides the problem
- Remove badges — reduces useful information

### Fix empty link `(#)` to `[![CI]...](#)` 

**Decision:** The CI badge link is already a valid fragment-only link. Remove it entirely since `#` points to current page with no content.

**Rationale:** MD042 flags empty links. The CI badge doesn't need to link anywhere useful.

### Add `bash` language to fenced code blocks

**Decision:** Add `bash` language specifier to code blocks at lines 28 and 36.

**Rationale:** MD040 requires language specifier. `bash` is appropriate for shell commands.

### Add blank lines around fenced code blocks

**Decision:** Add blank lines before/after code blocks at lines 28 and 36.

**Rationale:** MD031 requires blank lines around fenced code blocks.

### Fix table column style with spaces

**Decision:** Add space after `|` and before next `|` in table at line 41.

**Current:** `|---|---|---|`
**Fixed:** `| --- | --- | --- |`

**Rationale:** MD060 compact style requires spaces around pipes.

### Add blank lines around lists

**Decision:** Add blank line before list at line 63 (Supported input CRS).

**Rationale:** MD032 requires lists to be surrounded by blank lines.

## Risks / Trade-offs

No significant risks. This is a purely cosmetic fix that doesn't affect rendered output.
