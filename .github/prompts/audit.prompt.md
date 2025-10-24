---
description: Run compliance checks against implementation guides to ensure adherence to defined rules and governance standards.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

Goal: Execute compliance audits against your project's implementation guides to verify adherence to governance rules, organizational standards, and best practices defined in the guide repository.

This command wraps the `specify check-compliance` CLI command and helps you interpret compliance reports, identify violations, and determine appropriate remediation strategies.

Execution steps:

1. **Understand the request**: Parse user arguments for:
   - Specific guide paths to check (if provided)
   - Whether to bypass cache (`--no-cache` flag)
   - Any specific areas of concern mentioned

2. **Run compliance check**: Execute the CLI command:
   ```bash
   specify check-compliance [--guides GUIDE_PATHS] [--no-cache]
   ```
   
3. **Parse the compliance report**: The output will include:
   - **Rules discovered**: Total number of rules found in guides
   - **Pass/Fail/Waived counts**: Summary of rule evaluation results
   - **Detailed results**: For each rule:
     - Rule ID and description
     - Pass/Fail/Waived status
     - Reason for failure (if applicable)
     - Associated waivers (if any)
   - **Performance metrics**: Rule evaluation times and total duration

4. **Interpret results**:
   - **PASS**: Rules that are satisfied - acknowledge these
   - **FAIL**: Rules that are violated - these need attention:
     - Explain what the rule requires
     - Identify what's missing or incorrect
     - Suggest remediation options:
       a. Fix the code/configuration to comply
       b. Create a waiver if there's a valid exception
   - **WAIVED**: Rules that have active waivers - note these for transparency

5. **Present findings**: Create a structured summary:
   - Overall compliance score (passed/total rules)
   - Critical violations requiring immediate action
   - Minor violations that can be addressed iteratively
   - Active waivers for context
   - Recommended next steps

6. **Offer remediation guidance**:
   - For each failure, provide specific fix suggestions
   - If a waiver is appropriate, explain how to create one using `/waive`
   - Prioritize fixes based on rule severity and impact

Example usage:
- `/audit` - Check all guides
- `/audit Check authentication and authorization guides only` - Focused audit
- `/audit --no-cache` - Force fresh guide loading

Constitution Authority: Compliance rules in implementation guides are derived from organizational standards and the project constitution. Rule failures should be treated seriously unless a valid waiver exists.

Output format: Present a clear, actionable compliance report with:
- Executive summary (pass/fail/waived counts)
- Detailed findings grouped by status
- Prioritized remediation plan
- Commands to create waivers if needed (reference `/waive` command)

Do NOT modify any files during this command - this is read-only analysis. Remediation happens through separate actions the user explicitly approves.
