# Waivers File Format Contract

**Version**: 1.0  
**File**: `.specify/waivers.md`  
**Purpose**: Immutable, version-controlled audit trail of compliance exceptions  
**Format**: Markdown with structured entries

## File Structure

```markdown
# Compliance Waivers

[Sequential waiver entries below]

## Waiver: W-001
- **Reason**: [Plain-text reason, max 500 chars]
- **Timestamp**: [ISO-8601 format: YYYY-MM-DDTHH:MM:SSZ]
- **Related Rules**: [Optional comma-separated rule IDs]

## Waiver: W-002
- **Reason**: [...]
- **Timestamp**: [...]
```

## Format Specifications

### File Header
```markdown
# Compliance Waivers

This file maintains an immutable, version-controlled audit trail of 
compliance exceptions granted for this project.
```

(Optional header explaining the file's purpose)

### Entry Structure

Each waiver is a markdown section level 2 (`##`) with:

- **Section Heading**: `## Waiver: W-XXX` (W-001, W-002, W-003, etc.)
- **Reason**: Bullet point with `**Reason**: [text]`
- **Timestamp**: Bullet point with `**Timestamp**: [ISO-8601]`
- **Related Rules**: Optional bullet point with `**Related Rules**: [ids]`

### Field Specifications

#### Waiver ID (W-XXX)
- Format: `W-` followed by zero-padded 3-digit number
- Auto-incrementing: W-001, W-002, W-003, etc.
- Uniqueness: No duplicate IDs in same file
- Pattern: `/^W-\d{3}$/`

#### Reason
- Content: Plain-text explanation
- Max length: 500 characters
- Requirements: Non-empty, single line (no line breaks)
- Purpose: Explains why exception was necessary

#### Timestamp
- Format: ISO-8601 with Z suffix (UTC timezone)
- Example: `2025-10-21T14:30:00Z`
- Pattern: `/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/`
- Requirement: Must be valid datetime

#### Related Rules (Optional)
- Format: Comma-separated list of rule IDs
- Example: `api-routes-defined, tests-present`
- Purpose: Cross-reference which rules this waiver affects
- If absent: Waiver applies generally (no specific rule link)

## Example Valid Waivers File

```markdown
# Compliance Waivers

This file maintains an immutable, version-controlled audit trail of compliance exceptions.

## Waiver: W-001
- **Reason**: Disabling MFA for internal service accounts as per security review ticket #1234
- **Timestamp**: 2025-10-21T10:30:00Z
- **Related Rules**: auth-mfa-enabled

## Waiver: W-002
- **Reason**: Temporary SSL bypass for development environment only
- **Timestamp**: 2025-10-21T11:15:00Z

## Waiver: W-003
- **Reason**: Legacy authentication method required for third-party integration per contract
- **Timestamp**: 2025-10-21T14:45:00Z
- **Related Rules**: modern-auth-required, oauth2-implementation
```

## Parsing Rules

### Entry Detection
1. Look for lines matching `^## Waiver: W-\d{3}$`
2. Each section spans until next section or EOF
3. Collect all bullet points (`- **key**: value`) in section

### Field Extraction
1. Extract reason from line matching `^\s*-\s*\*\*Reason\*\*:\s*(.+)$`
2. Extract timestamp from line matching `^\s*-\s*\*\*Timestamp\*\*:\s*(.+)$`
3. Extract related rules from line matching `^\s*-\s*\*\*Related Rules\*\*:\s*(.+)$` (optional)

### Validation
- Waiver ID must exist and be unique
- Reason must be non-empty (after trim)
- Timestamp must be valid ISO-8601
- Timestamp must not be in future

## Version Control Integration

### Immutability Enforcement
- File is appended-only; entries never modified or deleted
- Git history provides complete audit trail
- Each waiver addition appears as separate commit

### Author Tracking
- Git commit author/committer identifies who created waiver
- Timestamp in waiver is independent of commit time
- Both provide auditability

### Example Git History
```
commit abc123 - Author: engineer@company.com - "waiver: disable mfa"
commit def456 - Author: engineer@company.com - "waiver: ssl bypass"
```

## Error Handling

### Parsing Errors
- Malformed ID: Skip entry, log warning
- Missing required field: Skip entry, log error
- Invalid timestamp: Skip entry, log error
- Duplicate ID: Log warning, use first occurrence

### Usage by Compliance Checker
1. Read waivers file if exists
2. Parse all valid entries
3. Create lookup: rule_id → waiver_id for cross-referencing
4. If rule failed + waiver exists → mark as "Waived"
5. If rule failed + no waiver → mark as "Failed"

## Future Extensibility

Current format is extensible:
- New optional bullet points can be added (e.g., `**Duration**: temporary`)
- New fields won't break existing parsers
- Backward compatible with current format

Reserved for future use:
- `**Duration**: [permanent|temporary]`
- `**Reviewer**: [email]`
- `**Expiration**: [date]`
