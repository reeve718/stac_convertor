## ADDED Requirements

### Requirement: README markdown style compliance
The README.md SHALL conform to markdownlint rules to avoid editor warnings.

#### Scenario: First line is H1 heading
- **WHEN** markdownlint checks README.md
- **THEN** MD041 passes (first line is a top-level heading)

#### Scenario: No empty links
- **WHEN** markdownlint checks README.md
- **THEN** MD042 passes (no empty links like `(#)`)

#### Scenario: Fenced code blocks properly formatted
- **WHEN** markdownlint checks README.md
- **THEN** MD031 passes (blank lines around fenced code blocks)
- **THEN** MD040 passes (language specifier specified)

#### Scenario: Table column style
- **WHEN** markdownlint checks README.md
- **THEN** MD060 passes (spaces around table pipes for compact style)

#### Scenario: Lists surrounded by blank lines
- **WHEN** markdownlint checks README.md
- **THEN** MD032 passes (blank lines around lists)
