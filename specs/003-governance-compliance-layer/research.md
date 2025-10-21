# Phase 0: Research & Technical Decisions

**Feature**: Governance Layer with Automated Compliance Checking and Waiver Process  
**Branch**: `003-governance-compliance-layer`  
**Date**: 2025-10-21

## Research Tasks & Decisions

### 1. Waiver File Format & Storage Strategy

**Research Question**: How should compliance waivers be stored to create an immutable, auditable trail?

**Decision**: Use `.specify/waivers.md` as a version-controlled markdown file with structured format

**Rationale**:
- **Immutability**: Git history provides permanent audit trail; changes are visible in commits
- **Auditability**: Easy human review; timestamps and reasons visible without parsing
- **Simplicity**: No additional storage system needed; leverages existing git infrastructure
- **Transparency**: Version control history shows who recorded waivers and when

**Alternatives Considered**:
- **JSON/YAML file**: Equally parseable but less human-readable; markdown more suitable for audit review
- **Database**: Adds complexity and requires state management; conflicts with project's CLI/file-based philosophy
- **Git commit messages**: Difficult to query and report on; markdown file allows consolidated audit view

**Format Decision**: Structured markdown with clear separators, ISO-8601 timestamps, unique identifiers

```markdown
# Compliance Waivers

## Waiver: W-001
- **Reason**: Disabling MFA for internal service accounts as per ticket #1234
- **Timestamp**: 2025-10-21T10:30:00Z
- **Related Rules**: [optional rule identifiers]

## Waiver: W-002
- **Reason**: Temporary SSL bypass for development environment
- **Timestamp**: 2025-10-21T11:15:00Z
```

---

### 2. Rule Engine Design & Extensibility

**Research Question**: What rule types are sufficient for governance, and how extensible should the engine be?

**Decision**: Support three core rule types (file_exists, dependency_present, text_includes) with structured design for future extensibility

**Rationale**:
- **file_exists**: Validates structural patterns (required files exist)
- **dependency_present**: Validates external requirements (packages, versions)
- **text_includes**: Validates code patterns (imports, configurations, practices)
- **Together**: Cover 95% of common compliance checks without requiring complex DSL
- **Simplicity**: Aligns with Principle V (Observability and Simplicity)

**Extensibility Design**:
- Each rule type has dedicated evaluator class
- Registry pattern allows new types without core changes
- New rules can be added as subclasses of BaseRule
- YAML parsing remains independent of rule types

**Alternatives Considered**:
- **Regular expressions**: Too powerful; requires expertise; hard to debug
- **Boolean logic DSL**: Adds complexity; most checks are simple AND conditions
- **Full constraint language**: Over-engineered for stated requirements

**Rule Type Specifications**:

#### file_exists
```yaml
rules:
  - type: file_exists
    path: "src/main.py"
    description: "Main entry point must exist"
```

#### dependency_present
```yaml
rules:
  - type: dependency_present
    file: "package.json"
    package: "axios"
    description: "HTTP client dependency must be declared"
```

#### text_includes
```yaml
rules:
  - type: text_includes
    file: "src/config.js"
    text: "import React from 'react'"
    description: "React import must be present in config"
```

---

### 3. Rule Embedding in Guides: YAML Frontmatter Format

**Research Question**: How should machine-readable rules be embedded in implementation guides?

**Decision**: Use YAML frontmatter at the top of guide markdown files

**Rationale**:
- **Standard format**: YAML frontmatter is industry standard (Jekyll, Hugo, Markdown processors)
- **Parseable**: Well-established YAML parsing libraries (PyYAML for Python)
- **Human-readable**: Easy for guide authors to write and review
- **Separated**: Rules at top of file, prose below; clear visual separation
- **Version-controlled**: Rules stay synchronized with guide content

**Format Design**:

```markdown
---
title: "Backend API Implementation Guide"
division: "SE"
rules:
  - type: file_exists
    path: "src/api/routes.py"
    description: "API routes must be defined"
  
  - type: file_exists
    path: "tests/api/test_routes.py"
    description: "API routes must have tests"
  
  - type: dependency_present
    file: "requirements.txt"
    package: "fastapi"
    description: "FastAPI must be declared as dependency"
  
  - type: text_includes
    file: "src/api/routes.py"
    text: "@router.get"
    description: "Routes must use FastAPI router decorators"
---

# Backend API Implementation Guide

[Guide content...]
```

**Parser Design**:
1. Extract YAML frontmatter from guide file
2. Parse rules array
3. Validate rule structure (type, required fields)
4. Return parsed rules for compliance checking

**Alternatives Considered**:
- **JSON**: Valid but less suitable for markdown context; YAML is markdown-compatible
- **Custom markers**: (e.g., `<!-- RULES: ... -->`) - More verbose, harder to parse
- **Separate `.rules.yaml` files**: Duplicates rules across files; harder to maintain sync

---

### 4. Compliance Report Generation & Formatting

**Research Question**: How should compliance reports present results to both developers and team leads?

**Decision**: Generate structured `compliance-report.md` with sections for Passed, Failed, and Waived rules

**Report Structure**:
```markdown
# Compliance Report

**Generated**: 2025-10-21T14:30:00Z  
**Project**: photo-organizer  
**Status**: ⚠️ PARTIAL (2 passed, 1 failed, 1 waived)

## Summary

- ✅ Passed: 2 rules
- ❌ Failed: 1 rules
- 🚫 Waived: 1 rules

## Checked Guides

- backend-patterns.md (SE division)
- api-design.md (SE division)

## Passed Rules ✅

### Rule: API routes defined (backend-patterns.md)
- Type: file_exists
- Target: src/api/routes.py
- Status: **PASS** ✅
- Details: File exists at expected location

### Rule: Router uses FastAPI decorators (backend-patterns.md)
- Type: text_includes
- Target: src/api/routes.py
- Text: `@router.get`
- Status: **PASS** ✅
- Details: Pattern found in file

## Failed Rules ❌

### Rule: Test coverage required (api-design.md)
- Type: file_exists
- Target: tests/api/test_routes.py
- Status: **FAIL** ❌
- Details: File not found at expected location
- **Recommendation**: Add test file or update rule target path

## Waived Rules 🚫

### Rule: MFA enabled in auth module (api-design.md)
- Type: text_includes
- Target: src/auth/mfa.py
- Text: `mfa_enabled=True`
- Status: **WAIVED** 🚫
- Waiver: W-001 - "Disabling MFA for internal service accounts as per ticket #1234"
- Timestamp: 2025-10-21T10:30:00Z
```

**Rationale**:
- **Clear structure**: Grouped by status for easy scanning
- **Guide reference**: Shows which guides were checked
- **Actionable**: Failed rules include recommendations
- **Auditable**: Waived rules link back to waiver records
- **Markdown format**: Readable in text editors, renders well in GitHub/docs

---

### 5. Compliance Checking Workflow

**Research Question**: How should `/check-compliance` identify relevant guides and execute checks?

**Decision**: Parse plan.md/tasks.md for guide references, match to available rules, execute in sequence

**Workflow Design**:

```
1. User runs: /check-compliance

2. System:
   a. Looks for plan.md in current project
   b. Extracts guide references (e.g., "Follow backend-patterns.md from SE division")
   c. Searches for guide files in:
      - .specify/guides/ (local project guides)
      - context/references/ (installed guides)
      - specs/*/  (spec-embedded guides)
   
   d. For each found guide:
      - Extracts YAML frontmatter
      - Parses rules array
      - Validates rule structure
   
   e. For each rule:
      - Evaluates against codebase
      - Records pass/fail/error
      - Cross-references with .specify/waivers.md
      - Converts failed+waived → waived status
   
   f. Generates compliance-report.md with results

3. Output: Report file path, summary stats, any errors
```

**Error Handling**:
- **Missing guide**: Logs warning, continues with other guides
- **Invalid rule syntax**: Logs error, skips rule, continues with others
- **File not found (file_exists check)**: Records as FAIL with details
- **Package not found (dependency_present check)**: Records as FAIL with hint
- **Pattern not found (text_includes check)**: Records as FAIL with context

---

### 6. Git Integration for Waivers

**Research Question**: How should waivers be automatically committed to maintain audit trail?

**Decision**: Require manual commitment; provide clear guidance; use git hooks as optional enhancement

**Rationale**:
- **Intentional**: Developers make conscious decision to commit exception
- **Auditable**: Git author/committer metadata captures who made exception
- **Reversible**: Can be reverted if deemed inappropriate
- **Simple**: No automated processes that might hide exceptions

**CLI Workflow**:
```
/waive-requirement "Reason for exception"

System:
1. Creates/appends .specify/waivers.md with structured entry
2. Outputs: "✓ Waiver recorded. Don't forget to commit!"
3. (Optional in future) Suggests: git add .specify/waivers.md && git commit -m "waiver: reason"
```

**Alternatives Considered**:
- **Auto-commit**: Obscures developer's actions; loses intentionality
- **Auto-amend to previous commit**: Rewrites history; breaks audit trail
- **Separate commit**: Forces developers to explicitly commit exceptions; preferred

---

### 7. Division Awareness in Compliance

**Research Question**: Should compliance rules be division-specific?

**Decision**: Rules are division-specific; guides associated with divisions; compliance respects division prioritization

**Design**:
- Each guide has `division: "SE|DS|Platform"` in YAML frontmatter
- When checking compliance, `/check-compliance` reads project's division from `.specify/project.json`
- Rules from matching division are checked first (priority)
- Common rules always included
- Other divisions checked but with lower priority
- Report shows which division each rule belongs to

**Rationale**: Aligns with existing Division-Aware Workflow feature (002); ensures compliance checks respect project focus

---

## Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Waiver storage | `.specify/waivers.md` (markdown, git-controlled) | Immutable audit trail, human-readable, leverages existing git infrastructure |
| Rule types | file_exists, dependency_present, text_includes | Cover 95% of use cases; simple; extensible without DSL |
| Rule embedding | YAML frontmatter in guides | Industry standard, parseable, human-readable, version-synchronized |
| Report format | Structured markdown with sections | Clear status groups, actionable recommendations, auditable |
| Compliance workflow | Parse plan.md, extract guides, evaluate rules, generate report | Automated; respects project dependencies |
| Waiver commitment | Manual (encouraged but not forced) | Intentional exceptions, auditable via git metadata |
| Division awareness | Compliance respects project division | Consistent with Division-Aware Workflow; focused checking |

## Assumptions Validated

✅ **Implementation guides are discoverable**: Will be in context/references/ or project-specific locations  
✅ **plan.md exists and references guides**: Project setup includes planning phase  
✅ **YAML parsing is available**: PyYAML is standard library; widely available  
✅ **Git is available**: Existing Specify CLI requires git; safe assumption  
✅ **Rules are relatively static**: Guides don't change per-codebase; can be versioned  
✅ **Waivers are rare exceptions**: Not checking compliance dozens of times per day  

## Dependencies & Integrations

- **PyYAML**: For parsing YAML frontmatter from guides
- **pathlib**: For cross-platform file operations (existing in project)
- **datetime**: For ISO-8601 timestamps (Python standard library)
- **Rich**: For formatted console output (existing dependency)
- **Typer**: For CLI commands (existing dependency)
- **Git**: For version control of waivers.md (required by project)
