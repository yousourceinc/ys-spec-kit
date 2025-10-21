# Compliance Report Format Contract

**Version**: 1.0  
**File**: `compliance-report.md`  
**Purpose**: Summary of compliance check results with pass/fail/waive status  
**Format**: Markdown with structured sections

## Report Structure

```markdown
# Compliance Report

**Generated**: [ISO-8601 timestamp]
**Project**: [project name]
**Status**: [status emoji + description]

## Summary

- ✅ Passed: [count]
- ❌ Failed: [count]
- 🚫 Waived: [count]
- ⚠️ Errors: [count] (optional)

## Checked Guides

- [guide-name.md] ([division])
- [guide-name.md] ([division])

## Passed Rules ✅

### Rule: [rule description]
- Type: [file_exists|dependency_present|text_includes]
- Target: [file path or filename]
- Status: **PASS** ✅
- Details: [success message]

[Additional passed rules...]

## Failed Rules ❌

### Rule: [rule description]
- Type: [file_exists|dependency_present|text_includes]
- Target: [file path or filename]
- Status: **FAIL** ❌
- Details: [failure details]
- **Recommendation**: [suggested action]

[Additional failed rules...]

## Waived Rules 🚫

### Rule: [rule description]
- Type: [file_exists|dependency_present|text_includes]
- Target: [file path or filename]
- Status: **WAIVED** 🚫
- Waiver: [W-XXX] - "[waiver reason]"
- Timestamp: [ISO-8601 timestamp]

[Additional waived rules...]

## Error Rules ⚠️

(Optional section if errors occurred)

### Rule: [rule description]
- Type: [file_exists|dependency_present|text_includes]
- Status: **ERROR** ⚠️
- Error: [error message]
```

## Header Section

### Generated Timestamp
- Format: ISO-8601 with Z suffix
- Example: `2025-10-21T14:30:00Z`
- Purpose: Shows when report was generated

### Project Name
- Content: Project directory name or configured name
- Purpose: Identifies which project was checked

### Status
- Format: Emoji + brief description
- Examples:
  - `✅ COMPLIANT` (0 failed, 0 errors)
  - `⚠️ PARTIAL` (has failed or waived rules)
  - `❌ NON-COMPLIANT` (has failed rules, no waivers)
  - `🔧 ERRORS` (rule evaluation errors)

## Summary Section

Bullet-point list with counts:

```markdown
## Summary

- ✅ Passed: 5 rules
- ❌ Failed: 2 rules
- 🚫 Waived: 1 rules
- ⚠️ Errors: 0 rules
```

All four counts should be present even if zero.

## Checked Guides Section

List guides that were analyzed:

```markdown
## Checked Guides

- backend-patterns.md (SE)
- api-design.md (SE)
- common-practices.md (Common)
```

Format: `- [guide-name] ([division])`

## Rule Results Sections

Three sections by status: Passed, Failed, Waived (optionally Errors)

### Passed Rules Section ✅

```markdown
## Passed Rules ✅

### Rule: API routes defined
- Type: file_exists
- Target: src/api/routes.py
- Status: **PASS** ✅
- Details: File exists at expected location

### Rule: FastAPI router decorator used
- Type: text_includes
- Target: src/api/routes.py
- Text Pattern: @router.get
- Status: **PASS** ✅
- Details: Pattern found in file (3 occurrences)
```

**Details Field Examples**:
- `"File exists at expected location"`
- `"Pattern found in file (5 occurrences)"`
- `"Dependency declared with version 1.2.3"`

### Failed Rules Section ❌

```markdown
## Failed Rules ❌

### Rule: API tests required
- Type: file_exists
- Target: tests/api/test_routes.py
- Status: **FAIL** ❌
- Details: File not found
- **Recommendation**: Create test file or update rule target path

### Rule: JWT authentication required
- Type: text_includes
- Target: src/auth/auth.py
- Text Pattern: import jwt
- Status: **FAIL** ❌
- Details: Pattern not found in file
- **Recommendation**: Add JWT import or remove JWT requirement from guide
```

**Recommendation Field**: Actionable suggestion for fixing failure

**Details Field Examples**:
- `"File not found at expected path"`
- `"Pattern not found in file"`
- `"Dependency 'axios' not declared in package.json"`

### Waived Rules Section 🚫

```markdown
## Waived Rules 🚫

### Rule: MFA authentication required
- Type: text_includes
- Target: src/auth/mfa.py
- Text Pattern: mfa_enabled=True
- Status: **WAIVED** 🚫
- Waiver: W-001 - "Disabling MFA for internal service accounts as per ticket #1234"
- Timestamp: 2025-10-21T10:30:00Z

### Rule: Rate limiting enforced
- Type: text_includes
- Target: src/middleware/rate_limit.py
- Text Pattern: rate_limiter.check()
- Status: **WAIVED** 🚫
- Waiver: W-002 - "Temporary rate limiting disabled for testing"
- Timestamp: 2025-10-21T11:15:00Z
```

**Waiver Field**: Reference to waiver with reason

**Timestamp Field**: When waiver was created

### Errors Section ⚠️ (Optional)

```markdown
## Error Rules ⚠️

### Rule: Database configuration
- Type: dependency_present
- Target: requirements.txt
- Package: postgresql
- Status: **ERROR** ⚠️
- Error: "requirements.txt file not found or malformed"

### Rule: ESLint configuration
- Type: file_exists
- Target: .eslintrc.json
- Status: **ERROR** ⚠️
- Error: "Invalid rule definition in guide: missing 'path' field"
```

**Error Field**: Details about why rule couldn't be evaluated

## Example Complete Report

```markdown
# Compliance Report

**Generated**: 2025-10-21T14:30:00Z  
**Project**: photo-organizer  
**Status**: ⚠️ PARTIAL

## Summary

- ✅ Passed: 3 rules
- ❌ Failed: 1 rules
- 🚫 Waived: 1 rules
- ⚠️ Errors: 0 rules

## Checked Guides

- backend-patterns.md (SE)
- api-design.md (SE)
- common-practices.md (Common)

## Passed Rules ✅

### Rule: API routes module exists
- Type: file_exists
- Target: src/api/routes.py
- Status: **PASS** ✅
- Details: File exists at expected location

### Rule: FastAPI router decorators used
- Type: text_includes
- Target: src/api/routes.py
- Text Pattern: @router.get
- Status: **PASS** ✅
- Details: Pattern found in file (5 occurrences)

### Rule: Git workflow implemented
- Type: file_exists
- Target: .github/workflows/ci.yml
- Status: **PASS** ✅
- Details: File exists at expected location

## Failed Rules ❌

### Rule: Comprehensive test coverage
- Type: file_exists
- Target: tests/api/test_routes.py
- Status: **FAIL** ❌
- Details: File not found
- **Recommendation**: Create comprehensive test file for API routes module

## Waived Rules 🚫

### Rule: MFA authentication enforcement
- Type: text_includes
- Target: src/auth/auth.py
- Text Pattern: mfa_required = True
- Status: **WAIVED** 🚫
- Waiver: W-001 - "Disabling MFA for internal service accounts per security review"
- Timestamp: 2025-10-21T10:30:00Z
```

## Format Validation

### Required Sections
- Report header (Generated, Project, Status)
- Summary (counts for all rule types)
- Checked Guides

### Optional Sections
- Passed Rules (only if any passed)
- Failed Rules (only if any failed)
- Waived Rules (only if any waived)
- Errors (only if any errors)

### Field Requirements by Status

**PASS**:
- Type, Target, Status, Details (required)
- Text Pattern (if applicable: text_includes)

**FAIL**:
- Type, Target, Status, Details, Recommendation (required)
- Text Pattern (if applicable: text_includes)

**WAIVED**:
- Type, Target, Status, Waiver, Timestamp (required)
- Text Pattern (if applicable: text_includes)

**ERROR**:
- Type, Target, Status, Error (required)

## Parsing Rules

### Section Detection
1. Sections start with `##` (markdown h2)
2. Subsections start with `###` (markdown h3) for individual rules
3. Fields are bullet points with `- **key**: value` format

### Field Extraction
```
Type: Extract from line `^\s*-\s*\*\*Type\*\*:\s*(.+)$`
Target: Extract from line `^\s*-\s*\*\*Target\*\*:\s*(.+)$`
Status: Extract from line `^\s*-\s*\*\*Status\*\*:\s*(.+)$`
Details: Extract from line `^\s*-\s*\*\*Details\*\*:\s*(.+)$`
Recommendation: Extract from line `^\s*-\s*\*\*Recommendation\*\*:\s*(.+)$`
```

## Version Control Integration

### Report Generation
- Generated fresh on each `/check-compliance` run
- Not committed to git (add to .gitignore)
- Timestamp allows comparison of historical checks (via ls -la or similar)

### Integration with Waivers
- Report links back to waivers.md entries
- Waiver IDs (W-001, W-002) are stable, reportable
- Enables cross-repository analysis

## Emojis and Status Indicators

| Emoji | Status | Meaning |
|-------|--------|---------|
| ✅ | PASS | Requirement satisfied |
| ❌ | FAIL | Requirement not met |
| 🚫 | WAIVED | Failed but waived via exception |
| ⚠️ | ERROR | Rule couldn't be evaluated |
| ✅ | COMPLIANT | All rules passed (overall) |
| ⚠️ | PARTIAL | Some rules failed/waived (overall) |
| ❌ | NON-COMPLIANT | Failed rules without waivers (overall) |

## Future Extensibility

Report format is designed for extension:
- New rule types can add new field types
- New sections can be added without breaking existing parsers
- Field ordering is flexible; parsers extract by name

Possible future sections:
- `Performance Metrics` (rule evaluation times)
- `Rule Statistics` (most common failures)
- `Trend Analysis` (comparison with previous runs)
