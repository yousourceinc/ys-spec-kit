# Phase 1: Data Model & Domain Entities

**Feature**: Governance Layer with Automated Compliance Checking and Waiver Process  
**Branch**: `003-governance-compliance-layer`  
**Date**: 2025-10-21

## Core Entities

### 1. Waiver

**Purpose**: Record a formal exception to a compliance requirement with reason, timestamp, and audit trail

**Fields**:
- `id`: Unique identifier (W-XXX format, auto-incremented)
- `reason`: Plain-text explanation for the exception (single line, max 500 chars)
- `timestamp`: ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ)
- `related_rules`: Optional list of rule identifiers this waiver addresses
- `created_by`: Optional author information (captured from git config if available)

**Persistence**: Stored in `.specify/waivers.md` as markdown structure

**Validation Rules**:
- `reason` is required and non-empty
- `timestamp` must be valid ISO-8601
- `id` must be unique within project
- Entries are immutable (no updates, only new entries)

**Example**:
```
## Waiver: W-001
- **Reason**: Disabling MFA for internal service accounts as per ticket #1234
- **Timestamp**: 2025-10-21T10:30:00Z
- **Related Rules**: [auth-mfa-enabled]
```

**State Transitions**:
- Created → Immutable (no updates)
- Can be reviewed in git history
- Waivers are never deleted; only marked as superseded by new waivers with different reasons

---

### 2. Compliance Rule

**Purpose**: Represent a machine-readable requirement from an implementation guide

**Fields**:
- `id`: Unique identifier within guide (e.g., "api-routes-defined")
- `type`: Rule type (file_exists, dependency_present, text_includes)
- `target`: Primary target (file path or filename)
- `condition`: Secondary condition (package name for dependency_present, text pattern for text_includes)
- `description`: Human-readable explanation
- `guide_id`: Source guide identifier
- `division`: Associated division (SE, DS, Platform)

**Validation Rules**:
- `type` must be one of: file_exists, dependency_present, text_includes
- `target` must be non-empty
- `description` is required
- `guide_id` identifies source guide

**Type-Specific Fields**:

#### file_exists
```yaml
- type: file_exists
  path: "src/api/routes.py"
  description: "API routes must be defined"
```

#### dependency_present
```yaml
- type: dependency_present
  file: "package.json"
  package: "axios"
  description: "HTTP client dependency required"
```

#### text_includes
```yaml
- type: text_includes
  file: "src/config.js"
  text: "import React from 'react'"
  description: "React must be imported in config"
```

**Extraction**: Parsed from YAML frontmatter in implementation guides

**Example Guide with Rules**:
```markdown
---
title: "Backend API Implementation"
division: "SE"
rules:
  - id: api-routes-defined
    type: file_exists
    path: "src/api/routes.py"
    description: "API routes module required"
  
  - id: tests-present
    type: file_exists
    path: "tests/api/test_routes.py"
    description: "API tests required"
---

# Backend API Implementation Guide
[content...]
```

---

### 3. Compliance Rule Evaluation Result

**Purpose**: Represent the result of evaluating a single rule against codebase

**Fields**:
- `rule_id`: Reference to rule
- `rule_type`: Type of rule (file_exists, dependency_present, text_includes)
- `status`: Result status (pass, fail, error, waived)
- `message`: Details about the result
- `target`: What was checked
- `guide_id`: Source guide
- `division`: Associated division
- `waiver_id`: Optional reference to waiver if status is "waived"
- `timestamp`: When evaluation occurred

**Status Values**:
- `pass`: Rule requirement satisfied
- `fail`: Rule requirement not satisfied
- `error`: Rule couldn't be evaluated (syntax error, parsing error)
- `waived`: Rule failed but has corresponding waiver

**Example Results**:
```
pass: "✅ File found at src/api/routes.py"
fail: "❌ File not found at tests/api/test_routes.py"
error: "⚠️ Invalid rule syntax in guide backend-patterns.md"
waived: "🚫 MFA check waived by W-001"
```

---

### 4. Compliance Report

**Purpose**: Aggregated results of a compliance check run

**Fields**:
- `project_name`: Name of project being checked
- `branch`: Current git branch
- `timestamp`: When report was generated
- `total_rules_evaluated`: Count of rules checked
- `pass_count`: Number of passed rules
- `fail_count`: Number of failed rules
- `waived_count`: Number of waived rules
- `error_count`: Number of unevaluated rules (errors)
- `guides_checked`: List of guides that were analyzed
- `divisions_checked`: Divisions covered in this check
- `results`: Array of rule evaluation results
- `summary`: Markdown-formatted summary

**Persistence**: Written to `compliance-report.md`

**Example Report Structure**:
```markdown
# Compliance Report

**Generated**: 2025-10-21T14:30:00Z
**Status**: ⚠️ PARTIAL (2 passed, 1 failed, 1 waived)

## Summary
- ✅ Passed: 2 rules
- ❌ Failed: 1 rules
- 🚫 Waived: 1 rules

## Checked Guides
- backend-patterns.md (SE)
- api-design.md (SE)

[Detailed sections for each status...]
```

---

### 5. Implementation Guide

**Purpose**: Document that defines best practices and contains machine-readable compliance rules

**Fields**:
- `id`: Unique guide identifier
- `title`: Display name
- `division`: Associated division (SE, DS, Platform)
- `rules`: Array of Compliance Rules
- `content`: Markdown content (prose)
- `version`: Guide version
- `location`: File path to guide

**Frontmatter Structure**:
```yaml
---
title: "Backend API Implementation"
division: "SE"
version: "1.0"
rules:
  - id: api-routes-defined
    type: file_exists
    path: "src/api/routes.py"
    description: "API routes required"
---
```

**Extraction Logic**:
1. Read guide file
2. Extract YAML frontmatter (if present)
3. Parse rules array
4. Return parsed rules for compliance checking

---

### 6. Project Planning Reference

**Purpose**: Link compliance rules to project plans via guide references

**Fields**:
- `plan_file`: Path to plan.md
- `tasks_file`: Path to tasks.md
- `referenced_guides`: List of guides mentioned in plan.md or tasks.md
- `project_division`: Division specified for project

**Extraction Logic**:
1. Read plan.md and tasks.md
2. Search for guide references (e.g., "Follow backend-patterns.md")
3. Extract guide names/paths
4. Match to available guide files
5. Return list of guides to check

**Example**:
```
Plan mentions: "Implementation should follow backend-patterns.md from SE guides"
→ System extracts: ["backend-patterns.md"]
→ System locates: context/references/SE/backend-patterns.md
→ System evaluates: Rules from that guide
```

---

## Entity Relationships

```
Implementation Guide
├── contains: Array of Compliance Rules
│   └── Rule
│       ├── evaluates against: Codebase
│       ├── produces: Compliance Rule Evaluation Result
│       └── can be: Waived by Waiver
│
Waiver (in .specify/waivers.md)
├── reference: Related Rules
└── status: Immutable (not updated)

Project Planning Reference
├── reads: plan.md
├── reads: tasks.md
├── identifies: Referenced Guides
└── triggers: Compliance Check

Compliance Report
├── aggregates: Multiple Compliance Rule Evaluation Results
├── references: Waivers
└── written to: compliance-report.md
```

---

## State Machines

### Compliance Rule Evaluation Lifecycle

```
Rule Definition (in Guide)
    ↓
Rule Extraction (during compliance check)
    ↓
Rule Evaluation
    ├→ PASS: Requirement satisfied
    ├→ FAIL: Requirement not met
    │   ├→ WAIVED: Corresponding waiver exists
    │   └→ FAILED: No waiver, remains as failure
    └→ ERROR: Rule couldn't be evaluated

Final Status Recorded in Report
```

### Waiver Lifecycle

```
Created
    ↓ (via /waive-requirement)
Immutable Record in .specify/waivers.md
    ↓ (during compliance check)
Referenced by Rule with status "Waived"
    ↓ (in compliance-report.md)
Visible in Audit Trail
```

---

## Validation Rules & Constraints

### Waiver Validation
- `reason`: Required, 1-500 characters, single line
- `timestamp`: Valid ISO-8601, UTC timezone
- `id`: Unique within project, cannot be reused
- No updates allowed; only append new entries

### Rule Validation
- `type`: One of: file_exists, dependency_present, text_includes
- `target`: Valid file path or filename, non-empty
- `condition`: Required for dependency_present and text_includes
- `description`: Non-empty, clear explanation

### Compliance Check Validation
- plan.md or tasks.md must exist in project
- At least one guide must be referenced
- Rules must have valid YAML syntax
- Project must have readable codebase

---

## Data Integrity & Audit Trail

**Waivers Immutability**:
- Stored in version-controlled `.specify/waivers.md`
- Git history provides complete audit trail
- Cannot be modified or deleted (only superseded by new waivers)
- Author captured via git config or manual entry

**Compliance Reports**:
- Generated fresh on each check
- Include timestamp for reproducibility
- Reference specific waiver IDs
- Don't modify older reports (generate new ones)

**Rules Versioning**:
- Rules embedded in guides
- Guides stored in version-controlled directories
- Rule changes tracked via guide versioning
- Reports reference guide version at check time

---

## Performance Considerations

**Rule Evaluation Performance**:
- file_exists: O(1) file system check
- dependency_present: O(n) file parsing (package.json, requirements.txt)
- text_includes: O(m) file content scan (reasonably small files)
- Total for typical project: <30 seconds (from spec requirement)

**Storage**:
- Waivers: O(1) per waiver in markdown file (small size)
- Compliance reports: O(r) where r = number of rules (typically <100)
- Minimal storage footprint

---

## Example Data Flows

### Flow 1: Recording a Waiver

```
User Input: /waive-requirement "Disabling SSL for dev env per ticket #5678"
                ↓
System creates Waiver entity:
{
  id: "W-001",
  reason: "Disabling SSL for dev env per ticket #5678",
  timestamp: "2025-10-21T11:30:00Z"
}
                ↓
System appends to .specify/waivers.md
                ↓
Output: "✓ Waiver W-001 recorded"
                ↓
Developer commits: git add .specify/waivers.md && git commit -m "waiver: dev ssl"
                ↓
Audit trail permanently in git history
```

### Flow 2: Checking Compliance

```
User Input: /check-compliance
                ↓
System reads plan.md/tasks.md
                ↓
Extracts referenced guides: ["backend-patterns.md", "api-design.md"]
                ↓
Locates guides in context/references/SE/
                ↓
For each guide, extracts YAML frontmatter
                ↓
Parses rules array
                ↓
For each rule:
  - Evaluate against codebase → Result
  - Check .specify/waivers.md for matching waivers
  - If waived, mark as "Waived"
  - If failed, mark as "Failed"
                ↓
Generates compliance-report.md with:
  - Pass count, fail count, waive count
  - Detailed results grouped by status
  - Links to waivers where applicable
                ↓
Output: "Report generated at compliance-report.md"
```
