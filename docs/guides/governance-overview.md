# Governance Layer Overview

The Specify CLI includes a comprehensive **governance layer** for managing compliance, waivers, and rule validation across your project. This document provides an overview of governance concepts and capabilities.

## Quick Links

- [Governance Quickstart](./governance-quickstart.md) - Get started in 5 minutes
- [Compliance Checking](./compliance-checking.md) - Verify code against rules
- [Waiver Management](./waiver-management.md) - Create and manage exceptions
- [Rule Authoring](./rule-authoring.md) - Define compliance rules

## What is Governance?

Governance in the Specify CLI context means:

1. **Compliance**: Automated verification that code meets defined requirements
2. **Waivers**: Formal exceptions with audit trail for approved deviations
3. **Rules**: Machine-readable compliance checks embedded in implementation guides
4. **Reporting**: Clear compliance status and remediation recommendations

## Core Concepts

### Rules

**Rules** are machine-readable compliance checks defined in YAML frontmatter within implementation guides. Three rule types are supported:

- **`file_exists`**: Verify required files are present
- **`dependency_present`**: Check for required dependencies
- **`text_includes`**: Validate text content in files

### Compliance Reports

**Compliance Reports** document the status of all rules against your code:

- ✅ **Passed**: Rule requirements met
- ❌ **Failed**: Rule requirements not met
- ⚠️ **Waived**: Rule intentionally bypassed with exception
- ⏸️ **Error**: Rule could not be evaluated

### Waivers

**Waivers** are formal exceptions to compliance rules:

- Version-controlled in `.specify/waivers.md`
- Immutable audit trail with timestamps
- Division-aware tracking
- Automatic matching with failed rules

## Architecture

The governance layer consists of five integrated components:

```
┌─────────────────────────────────────────────────────┐
│              Governance Layer Stack                  │
├─────────────────────────────────────────────────────┤
│  API Layer (ComplianceChecker, WaiverManager)       │
├─────────────────────────────────────────────────────┤
│  Rule Engine (RuleEngine, RuleParser)               │
├─────────────────────────────────────────────────────┤
│  Cross-Cutting Concerns (Logging, Metrics, Cache)   │
├─────────────────────────────────────────────────────┤
│  Data Persistence (Waivers, Reports, Project files) │
└─────────────────────────────────────────────────────┘
```

### Core Modules

- **`waiver.py`**: Waiver creation, storage, and retrieval
- **`compliance.py`**: Compliance checking and evaluation
- **`report.py`**: Report generation and formatting
- **`rules/engine.py`**: Rule registration and execution
- **`logging_config.py`**: Centralized logging setup
- **`metrics.py`**: Performance tracking and reporting
- **`caching.py`**: Guide discovery optimization

## Key Features

### 🚀 Performance

- **Caching**: 50-100x faster on subsequent checks
- **Metrics**: Track rule evaluation times
- **Lazy Loading**: Only evaluate necessary guides

### 📋 Audit Trail

- **Immutable Waivers**: Every exception recorded
- **Timestamps**: ISO-8601 format for compliance
- **Traceability**: Full history of decisions

### 🔍 Transparency

- **Detailed Reports**: Clear pass/fail/waived status
- **Recommendations**: Actionable remediation guidance
- **Logging**: Comprehensive operation logging

### 🛡️ Security

- **Version Control**: Waivers in git for review
- **Division Awareness**: Role-based compliance
- **Validation**: Input checking and sanitization

## Division Awareness

Governance rules can be division-specific:

```yaml
rules:
  - id: "PYTHON-001"
    type: "file_exists"
    path: "src/main.py"
    division: "SE"  # Software Engineering only
```

This enables different compliance requirements for different teams.

## Getting Started

### 1. Initialize a Project

```bash
specify init my-project --ai claude
```

The project includes `.specify/` directory for governance artifacts.

### 2. Run Your First Compliance Check

```bash
specify check-compliance
```

This discovers and evaluates all rules from your implementation guides.

### 3. Create a Waiver (if needed)

```bash
specify waive-requirement "Legacy system exception" --rules PYTHON-001
```

### 4. View Reports

```bash
cat compliance-report.md
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `specify check-compliance` | Evaluate all rules and generate report |
| `specify waive-requirement "reason"` | Create a new waiver |
| `specify waivers list` | List all active waivers |
| `specify waivers show W-001` | View specific waiver details |

## Best Practices

### ✅ DO

- **Regular Checks**: Run compliance checks before commits
- **Clear Reasons**: Provide detailed waiver reasons
- **Rule Validation**: Test rules during guide authoring
- **Review Waivers**: Regularly review active waivers
- **Version Control**: Commit `.specify/waivers.md` with code

### ❌ DON'T

- **Ignore Failures**: Address compliance issues promptly
- **Vague Waivers**: Avoid "temporary" or "hack" reasons
- **Stale Waivers**: Remove waivers when issues are fixed
- **Skip Documentation**: Always document rule changes
- **Commit Reports**: `.specify/compliance-report.md` is ephemeral

## Architecture Details

See [Phase 7 Completion Summary](../../project-meta/completion-logs/GOVERNANCE_PHASE_7_COMPLETION.md) for detailed implementation information.

## Next Steps

1. Read the [Governance Quickstart](./governance-quickstart.md) for hands-on examples
2. Learn about [Compliance Checking](./compliance-checking.md)
3. Master [Rule Authoring](./rule-authoring.md)
4. Explore [Waiver Management](./waiver-management.md)

## Support

For issues or questions about governance:

- Check [Troubleshooting](../troubleshooting/) section
- Review [FAQ](../troubleshooting/faq.md)
- See [SUPPORT.md](../../SUPPORT.md) for contact information
