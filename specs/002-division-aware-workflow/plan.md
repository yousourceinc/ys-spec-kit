````markdown
# Implementation Plan: Division-Aware Workflow

**Branch**: `002-division-aware-workflow` | **Date**: October 21, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-division-aware-workflow/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Division-Aware Workflow feature enables Specify CLI to provide context-specific AI guidance based on a project's division (Software Engineering, Data Science, Platform Engineering). This is accomplished by:

1. Adding a `--division` CLI option to `specify init` that stores the division in `.specify/project.json`
2. Updating context scripts (bash/PowerShell) to read the division and prioritize relevant guides from `context/references/<DIVISION>/`
3. Enhancing AI command templates (`/specify`, `/plan`, `/tasks`) with division-aware instructions
4. Implementing division-filtered guide discovery through `/guides` command and `specify guides show`

The technical approach builds on the existing guides integration (v0.4.0) by layering division awareness into the configuration, context delivery, and guide discovery systems without requiring changes to the core CLI architecture.

## Technical Context

**Language/Version**: Python 3.12.8 (>=3.11 required per pyproject.toml)  
**Primary Dependencies**: Typer (CLI), Rich (formatting), httpx (HTTP), platformdirs, readchar  
**Storage**: JSON files (`.specify/project.json`), Git repository structure for guides  
**Testing**: pytest with markers (unit, integration, edge_case, requires_git)  
**Target Platform**: Linux/macOS native, WSL2 on Windows (per constitution)  
**Project Type**: Single project - CLI tool with bash/PowerShell scripts  
**Performance Goals**: <2s guide display response time (95th percentile)  
**Constraints**: Must maintain backward compatibility with existing projects, no breaking changes to CLI API  
**Scale/Scope**: Supports 3+ divisions (SE, DS, Platform + extensible), handles projects with 100+ guides

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **I. Specification-First**: Feature specification complete and validated (16/16 quality checks passing). This plan follows the approved spec.

✅ **II. Test-Driven Implementation**: All functional requirements are testable with clear acceptance scenarios. TDD approach will be enforced during implementation.

✅ **III. CLI and Automation Focus**: Feature extends existing CLI (`specify init --division`, `specify guides show`) and bash/PowerShell scripts. All input/output is text-based with JSON support.

✅ **IV. Integration and Contract Testing**: Integration tests required for CLI commands, context scripts, and guide discovery. Contract tests needed for `.specify/project.json` schema.

✅ **V. Observability and Simplicity**: Feature follows YAGNI principles - division is stored as simple JSON string, no over-engineering. Error handling includes structured logging for division validation and guide discovery failures.

✅ **VI. Developer-Centric Experience**: CLI interface prioritizes clarity (`--division SE` is explicit), error messages provide actionable guidance (invalid division lists valid options), help text comprehensive.

### Additional Constraints Compliance

✅ **Cross-platform**: Bash/PowerShell scripts ensure Linux/macOS/WSL2 support  
✅ **Open-source dependencies**: All dependencies are OSI-approved (Typer, Rich, etc.)  
✅ **Security**: No sensitive data storage, `.specify/project.json` is plain text configuration  
✅ **Code review**: PR workflow with reviews enforced by repository settings

### Workflow Compliance

✅ **Branch naming**: Feature branch `002-division-aware-workflow` follows convention  
✅ **Spec sync**: Plan references approved specification, will maintain sync throughout development  
✅ **Testing requirements**: pytest configured with appropriate markers (unit, integration, edge_case)

**Gate Status**: ✅ ALL GATES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```
specs/002-division-aware-workflow/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 output (to be created by /speckit.plan)
├── data-model.md        # Phase 1 output (to be created by /speckit.plan)
├── quickstart.md        # Phase 1 output (to be created by /speckit.plan)
├── contracts/           # Phase 1 output (to be created by /speckit.plan)
│   └── project-config-schema.json  # .specify/project.json schema
├── checklists/
│   └── requirements.md  # Quality validation (complete - 16/16 passing)
└── tasks.md             # Phase 2 output (created by /speckit.tasks command - NOT /speckit.plan)
```

### Source Code (repository root)

```
# Single project structure (CLI tool)
src/
└── specify_cli/
    ├── __init__.py           # Main CLI entrypoint (modify for --division option)
    └── config.py             # New: Project config read/write utilities

scripts/
├── bash/
│   ├── update-agent-context.sh  # Modify: Read division, prioritize guides
│   ├── common.sh                # Modify: Add division utility functions
│   └── create-new-feature.sh    # No changes (out of scope)
└── powershell/
    ├── update-agent-context.ps1 # Modify: Read division, prioritize guides
    ├── common.ps1               # Modify: Add division utility functions
    └── create-new-feature.ps1   # No changes (out of scope)

templates/
└── commands/
    ├── specify.md        # Modify: Add division-aware instructions
    ├── plan.md           # Modify: Add division-aware instructions
    └── tasks.md          # Modify: Add division-aware + enforcement instructions

tests/
├── unit/
│   └── test_division_config.py  # New: Test config read/write
├── integration/
│   ├── test_init_with_division.py  # New: Test specify init --division
│   ├── test_context_division.py     # New: Test context scripts with division
│   └── test_guides_division.py      # New: Test guide filtering
└── fixtures/
    └── mock_guides/          # New: Mock guide structure for testing
        ├── SE/
        ├── DS/
        └── Platform/

.specify/
└── project.json          # New: Created by specify init with {"division": "..."}
```

**Structure Decision**: Single project structure is appropriate as this is a CLI tool with supporting shell scripts. The feature adds new configuration module (`config.py`) to handle `.specify/project.json` operations, modifies existing scripts to read division and prioritize guides, and updates command templates with division-aware instructions. Test structure follows existing pytest conventions with unit/integration/fixtures organization.

## Complexity Tracking

*No constitutional violations - this section is not needed*

This feature maintains simplicity and follows YAGNI principles:
- Division stored as simple string in JSON (no complex data structures)
- No new dependencies required (uses existing Python stdlib json module)
- Guide prioritization uses straightforward directory filtering
- No over-engineering of extensibility (divisions are simply subdirectories)

