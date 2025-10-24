---
description: Create a compliance waiver with full audit trail for rules that require valid exceptions.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

Goal: Create documented compliance waivers for governance rules that cannot or should not be immediately fixed, establishing a transparent audit trail of exceptions with proper justification.

This command wraps the `specify waive-requirement` CLI command and helps you craft well-justified waivers that satisfy organizational governance requirements.

Execution steps:

1. **Understand the waiver request**: Determine:
   - Which rule(s) need waivers (by rule ID)
   - The reason/justification for the exception
   - Whether this is a temporary or permanent waiver
   - Any context from previous `/audit` results

2. **Validate justification**: Before creating a waiver, ensure:
   - There's a legitimate business or technical reason
   - The exception is documented clearly
   - The waiver doesn't violate critical security/compliance requirements
   - Alternative solutions have been considered

3. **Craft the waiver reason**: Help the user write a clear, professional justification that includes:
   - **What**: Which requirement is being waived
   - **Why**: The business/technical reason for the exception
   - **Context**: Relevant ticket numbers, architectural decisions, or constraints
   - **Duration**: Whether temporary (with remediation plan) or permanent
   - **Risk assessment**: Any implications of this exception

4. **Execute the waiver command**:
   ```bash
   # For specific rule(s):
   specify waive-requirement "JUSTIFICATION" --rules RULE-001,RULE-002
   
   # For general waiver (user will specify rules):
   specify waive-requirement "JUSTIFICATION"
   ```

5. **Explain the waiver record**: The waiver will be:
   - Stored in `.specify/waivers.md`
   - Assigned a unique waiver ID (e.g., W-001)
   - Timestamped with ISO 8601 format
   - Include division context (from project.json)
   - Be version-controlled (committed to git)

6. **Verify waiver creation**: After creation:
   - Confirm the waiver was added to waivers.md
   - Show the waiver ID assigned
   - Explain that this will now affect `/audit` results (waived rules won't show as failures)
   - Recommend running `/audit` again to verify the waiver is applied

Example usage:
- `/waive Create waiver for MFA requirement on service account per JIRA-1234`
- `/waive Need exception for test database not using encryption in development environment`

Best practices for waivers:
1. **Be specific**: Reference ticket numbers, decision records, or architectural docs
2. **Include timeline**: Indicate if temporary and when remediation is planned
3. **Assess risk**: Note any security or compliance implications
4. **Get approval**: For sensitive waivers, mention if leadership approval is needed
5. **Link to work**: Reference related tasks, stories, or technical debt items

Warning signs of inappropriate waivers:
- "We don't have time to fix this" (without timeline)
- Waiving security requirements without risk assessment
- Vague justifications without context
- Permanent waivers for known technical debt

Constitution Authority: Waivers should align with the project constitution's governance principles. If a waiver conflicts with core principles, escalate for constitution review rather than creating a waiver.

Output format: 
1. Show the crafted waiver justification for user approval
2. Present the exact command that will be run
3. After execution, display the waiver ID and confirmation
4. Recommend next steps (re-run audit, commit waiver, notify team)

Do NOT auto-approve waivers - always show the user what will be created and get explicit confirmation before executing the command.
