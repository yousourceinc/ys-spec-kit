# Implementation Plan: Governance Layer with Automated Compliance Checking and Waiver Process

**Branch**: `003-governance-compliance-layer` | **Date**: 2025-10-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-governance-compliance-layer/spec.md`

## Summary

Implement a governance layer that transforms Spec Kit from a "guide" to a "guardrail" through automated compliance checking and formal waiver processes. The system enables engineers to record compliance exceptions with auditable trails, developers to verify code against implementation guides, and team leads to review governance practices. The implementation includes two CLI commands (`/waive-requirement` and `/check-compliance`), machine-readable rule engine supporting file_exists/dependency_present/text_includes checks, YAML frontmatter-based rule embedding in guides, and comprehensive reporting with waiver integration.

## Technical Context

**Language/Version**: Python 3.11+ (consistent with existing Specify CLI)  
**Primary Dependencies**: Typer (CLI), Rich (formatting), PyYAML (rule parsing), pathlib (file operations), datetime (timestamps)  
**Storage**: File-based (`.specify/waivers.md`, `compliance-report.md`, YAML in guides)  
**Testing**: pytest (unit tests), subprocess-based integration tests  
**Target Platform**: Linux/macOS/WSL2 (cross-platform)
**Project Type**: Single project (extends existing Specify CLI)  
**Performance Goals**: Waiver recording <10 seconds, compliance check <30 seconds on typical codebase  
**Constraints**: Graceful handling of missing files/guides, clear error messages, immutable audit trail  
**Scale/Scope**: Supports projects with 10k+ lines of code, multiple guides with hundreds of rules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Specification-First ✅
- ✅ Comprehensive feature specification completed with clear requirements
- ✅ Specification approved and ratified with quality checklist completed
- ✅ All user stories and acceptance scenarios defined

### Principle II: Test-Driven Implementation ✅
- ✅ Plan includes unit tests for each component (waiver management, rule engine, compliance checking)
- ✅ Integration tests planned for CLI commands and file operations
- ✅ Test fixtures will validate waiver formatting and rule parsing

### Principle III: CLI and Automation Focus ✅
- ✅ Two new CLI commands: `/waive-requirement` and `/check-compliance`
- ✅ Text-based I/O: plain-text reasons, markdown reports
- ✅ JSON output support planned for automation
- ✅ Immutable audit trail via git-controlled `.specify/waivers.md`

### Principle IV: Integration and Contract Testing ✅
- ✅ File format contracts: waivers.md structure, compliance-report.md schema
- ✅ Rule engine contract: YAML frontmatter parsing from guides
- ✅ Integration with plan.md/tasks.md reference parsing

### Principle V: Observability and Simplicity ✅
- ✅ Simple rule types: file_exists, dependency_present, text_includes (no DSL)
- ✅ Structured error messages for rule failures
- ✅ Clear pass/fail/waive status in reports
- ✅ Timestamps and reasons for all waivers
- ✅ Graceful handling of edge cases (missing files, invalid rules)

### Principle VI: Developer-Centric Experience ✅
- ✅ Intuitive commands: `/waive-requirement` clearly indicates intention
- ✅ Help text for both commands with usage examples
- ✅ Clear error messages guide users on what went wrong and why
- ✅ Audit trail design prioritizes transparency and accountability
- ✅ Report format enables easy review by both developers and leads

**Gate Status**: ✅ PASS - All principles satisfied

## Project Structure

### Documentation (this feature)

```
specs/003-governance-compliance-layer/
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (research and decisions)
├── data-model.md        # Phase 1 output (entities and relationships)
├── quickstart.md        # Phase 1 output (guide for users)
├── contracts/           # Phase 1 output (file format contracts)
│   ├── waivers-schema.md        # Waiver file format contract
│   ├── compliance-report-schema.md  # Report file format contract
│   └── rule-engine-api.md       # Rule engine contract
├── checklists/
│   └── requirements.md   # Specification quality checklist
└── tasks.md             # Phase 2 output (task breakdown for implementation)
```

### Source Code (repository root)

```
src/specify_cli/
├── __init__.py          # Main CLI module (extend with /waive-requirement and /check-compliance)
├── config.py            # Config management (existing - may extend for governance)
└── governance/          # NEW - Governance layer module
    ├── __init__.py
    ├── waiver.py        # Waiver management (create, read, format)
    ├── compliance.py    # Compliance checking (guide parsing, rule evaluation)
    ├── rules/
    │   ├── __init__.py
    │   ├── engine.py    # Rule engine (file_exists, dependency_present, text_includes)
    │   └── parser.py    # YAML frontmatter parser for guides
    └── report.py        # Report generation (compliance-report.md)

tests/
├── unit/
│   ├── test_waiver_management.py        # Waiver creation, formatting, parsing
│   ├── test_rule_engine.py              # Rule evaluation tests
│   ├── test_rule_parser.py              # YAML parsing tests
│   └── test_compliance_report.py        # Report generation tests
├── integration/
│   ├── test_waive_requirement_command.py    # /waive-requirement CLI
│   ├── test_check_compliance_command.py     # /check-compliance CLI
│   └── test_governance_workflow.py          # End-to-end governance workflow
└── fixtures/
    ├── mock_guides/                     # Sample guides with rules
    ├── sample_waivers.md               # Sample waiver file
    └── sample_projects/                # Sample projects for compliance testing
```

**Structure Decision**: Single project extension within existing Specify CLI. Governance components added as a submodule (`governance/`) under `src/specify_cli/` to maintain modularity. Tests follow existing pytest structure with unit, integration, and fixtures directories.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

