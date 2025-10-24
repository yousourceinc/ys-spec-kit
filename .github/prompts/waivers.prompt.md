---
description: List and view compliance waivers to understand active exceptions and their justifications.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

Goal: View active compliance waivers to understand what governance exceptions exist in the project, their justifications, and their audit trail.

This command wraps the `specify waivers` CLI commands and helps you navigate and understand the waiver registry.

Execution steps:

1. **Determine the operation**: Based on user input:
   - **List all waivers**: Show summary of all active waivers
   - **Show specific waiver**: Display detailed information for a waiver ID
   - **Search/filter**: Help find waivers by keyword, rule ID, or date

2. **Execute the appropriate command**:

   **For listing all waivers:**
   ```bash
   specify waivers list [--verbose]
   ```
   
   **For viewing a specific waiver:**
   ```bash
   specify waivers show W-001
   ```

3. **Present waiver information**: The output includes:
   - **Waiver ID**: Unique identifier (W-XXX format)
   - **Created**: Timestamp when waiver was created
   - **Reason**: Full justification for the exception
   - **Rules**: Which rule IDs this waiver covers
   - **Division**: The development division context
   - **Author**: Who created the waiver (from git)

4. **Interpret waiver status**:
   - **Active waivers**: Currently in effect, will suppress rule failures in `/audit`
   - **Context**: Explain why the waiver exists based on the justification
   - **Coverage**: Which compliance rules are affected

5. **Provide waiver analysis**:
   - Group waivers by type (security, process, technical debt)
   - Highlight temporary waivers that may need follow-up
   - Flag waivers that might be outdated or no longer needed
   - Identify patterns (e.g., multiple waivers for same guide)

6. **Recommend actions** based on findings:
   - **Review old waivers**: Suggest checking if waivers from >6 months ago are still valid
   - **Remediation**: If temporary waivers exist, ask about remediation plans
   - **Consolidation**: If multiple waivers cover similar issues, suggest consolidating
   - **Documentation**: Ensure waivers are properly documented in project docs

Example usage:
- `/waivers` - List all active waivers
- `/waivers Show details for waiver W-003` - View specific waiver
- `/waivers verbose` - Detailed list with full justifications
- `/waivers Search for database waivers` - Find waivers by keyword

Waiver lifecycle management:
1. **Creation**: Via `/waive` command
2. **Active**: Listed in `.specify/waivers.md`, affects `/audit` results
3. **Review**: Periodic review to ensure still valid
4. **Retirement**: When the waived condition is fixed (remove from waivers.md)
5. **Audit**: Waivers are immutable once created (edit = new waiver + removal of old)

Red flags to watch for:
- **Accumulation**: Too many waivers may indicate systemic issues
- **Vague waivers**: Justifications that don't explain the real reason
- **Stale waivers**: Old waivers that may no longer be relevant
- **Pattern of same rule**: Multiple waivers for the same rule across different contexts

Constitution Authority: Waivers are exceptions to governance standards but should align with constitution principles. If waivers consistently conflict with principles, escalate for constitution or standards review.

Output format:
1. **List view**: Table or formatted list showing:
   - Waiver ID | Created | Rules | Brief reason
   
2. **Detail view**: For specific waiver:
   - Full waiver record with all metadata
   - Context about affected rules
   - Related compliance check results
   
3. **Analysis**: When listing multiple waivers:
   - Summary statistics (count, age distribution)
   - Grouping by category or concern area
   - Recommendations for review or action

Do NOT modify the waivers file - this is read-only viewing. To create new waivers, use `/waive`. To retire waivers, help the user manually edit `.specify/waivers.md` after confirming the waived condition is resolved.
