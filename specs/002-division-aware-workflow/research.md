# Research: Division-Aware Workflow

**Feature**: Division-Aware Workflow  
**Date**: October 21, 2025  
**Status**: Phase 0 Complete

## Overview

This document consolidates research findings for implementing division-aware functionality in the Specify CLI. The feature builds on the existing guides integration (v0.4.0) by adding division context to project initialization, context scripts, and guide discovery.

## Research Areas

### 1. Project Configuration Storage

**Decision**: Store division in `.specify/project.json` as a simple JSON object

**Rationale**:
- JSON is human-readable and easily editable by developers
- Python stdlib `json` module provides reliable read/write operations
- File is automatically version-controlled (in project root's `.specify/` directory)
- Schema is simple: `{"division": "SE"}` - no complex nested structures needed
- Extensible: additional project metadata can be added later without breaking changes

**Alternatives Considered**:
- **TOML/YAML**: More complex to parse, requires additional dependencies
- **Environment variables**: Not version-controlled, not persistent across sessions
- **Hidden file (`.specify-division`)**: Less discoverable, harder to manage multiple config values
- **SQLite database**: Massive over-engineering for storing a single string value

**Implementation Notes**:
- Use `pathlib.Path` for cross-platform path handling
- Implement atomic writes (write to temp file, then rename) to prevent corruption
- Default to "SE" if file is missing or corrupted (fail gracefully)
- Schema validation: ensure division is a string and matches valid division list

---

### 2. Division Validation and Extensibility

**Decision**: Validate against predefined list from guides repository structure

**Rationale**:
- Divisions are discovered by scanning `context/references/` directory for subdirectories
- This makes the system automatically extensible: add a directory, it's a valid division
- Validation prevents typos and provides clear error messages
- Hardcoded list in CLI is backup if guides directory is not available
- Default divisions: SE, DS, Platform (per spec requirements)

**Alternatives Considered**:
- **Hardcoded enum in CLI**: Inflexible, requires code changes to add divisions
- **No validation**: Allows typos, poor user experience
- **External config file for divisions**: Over-engineering for simple list
- **Regex patterns**: Too permissive, doesn't validate against actual guide structure

**Implementation Notes**:
- Function: `get_valid_divisions(guides_path: Path) -> list[str]`
- Returns sorted list of subdirectories in `context/references/`
- Falls back to `["SE", "DS", "Platform"]` if guides not available
- CLI validation uses this list for `--division` parameter
- Error message format: "Invalid division 'XYZ'. Valid options: SE, DS, Platform"

---

### 3. Context Script Division Awareness

**Decision**: Bash/PowerShell scripts read `.specify/project.json` and filter guides by division

**Rationale**:
- Scripts already read plan.md and generate context files - extending to read project config is natural
- Bash has `jq` for JSON parsing (check availability, fall back to Python if needed)
- PowerShell has native JSON parsing via `ConvertFrom-Json`
- Guide prioritization: division guides listed first, then "Common/" guides, then other divisions
- Maintains backward compatibility: if no project.json, treat all guides equally

**Alternatives Considered**:
- **Python-only context generation**: Would require rewriting bash/PowerShell scripts, breaks existing workflows
- **Pass division as CLI argument**: Not persistent, requires manual specification every time
- **Read from environment variable**: Not version-controlled, inconsistent across team

**Implementation Notes**:
- Bash: Use `jq -r '.division' .specify/project.json 2>/dev/null || echo "SE"`
- PowerShell: `(Get-Content .specify/project.json | ConvertFrom-Json).division`
- Both scripts should handle missing file gracefully (default to "SE")
- Guide filtering logic:
  1. List guides from `context/references/{DIVISION}/`
  2. Then list guides from `context/references/Common/` (if it exists)
  3. Finally list guides from other divisions (marked as "Other division: DS")
- Update agent context file format to include "Division: SE" header

---

### 4. AI Command Template Updates

**Decision**: Update `/specify`, `/plan`, `/tasks` templates with explicit division instructions

**Rationale**:
- AI agents need explicit instructions to prioritize division-specific guides
- Templates already use placeholder syntax for dynamic content
- Division context should be inserted near the top of prompts for visibility
- `/tasks` requires stricter enforcement: guide references must be from project division
- Templates are Markdown files in `templates/commands/` - easy to update

**Alternatives Considered**:
- **Implicit guidance**: Rely on AI to infer division from guide structure - too unreliable
- **Dynamic template generation**: Over-engineering, templates are simple text files
- **Separate templates per division**: Massive duplication, maintenance nightmare

**Implementation Notes**:
- Add section to templates: "## Project Division Context"
- Example text: "This project is configured for the **{DIVISION}** division. Prioritize guides from `context/references/{DIVISION}/` in your responses."
- For `/tasks`: "**REQUIREMENT**: All guide references in the Guide Reference field must point to guides within `context/references/{DIVISION}/`. References to other divisions are not permitted."
- Use `{DIVISION}` placeholder - replaced by context scripts when generating agent files
- Templates remain human-readable and editable

---

### 5. Guide Discovery and Filtering

**Decision**: Implement `specify guides show <guide-path>` CLI command with division-aware search

**Rationale**:
- CLI command provides consistent, scriptable interface for guide access
- Division-aware search: first look in `{DIVISION}/`, then `Common/`, then other divisions
- Rich library already used for CLI formatting - can display guides nicely
- Supports both relative paths (`backend-patterns.md`) and full paths (`SE/backend-patterns.md`)
- `/guides` in-agent command delegates to this CLI command for consistency

**Alternatives Considered**:
- **Separate `/guides` implementation**: Would duplicate logic and create inconsistency
- **Web-based guide browser**: Out of scope, over-engineering for MVP
- **Full-text search engine**: Too complex for current needs, can be added later
- **No CLI command**: Forces developers to navigate file system manually

**Implementation Notes**:
- Command signature: `specify guides show [GUIDE_PATH]`
- If no path provided, show list of available guides (tree view by division)
- Search algorithm:
  1. Try exact match in `{DIVISION}/` directory
  2. Try exact match in `Common/` directory
  3. Try exact match in other divisions (warn if found in different division)
  4. If still not found, try fuzzy search across all divisions
- Display format: guide title, division badge, file path, content preview
- Use Rich's `Markdown` renderer for guide content display
- Performance: cache guide list for session, invalidate on directory changes

---

### 6. Backward Compatibility

**Decision**: Existing projects without `.specify/project.json` default to "SE" division

**Rationale**:
- No breaking changes - all existing functionality continues to work
- "SE" is specified as appropriate default in feature spec
- Context scripts check for file existence before reading
- CLI commands detect missing file and show friendly upgrade prompt
- Developers can add division to existing projects via `specify init --here --division DS`

**Alternatives Considered**:
- **Force migration**: Too disruptive, breaks existing workflows
- **No default**: Requires all projects to have explicit division - breaking change
- **Prompt on first command**: Annoying for users, interrupts workflow
- **Different default per command**: Inconsistent, confusing behavior

**Implementation Notes**:
- Function: `get_project_division(project_root: Path) -> str`
- Returns division from `.specify/project.json` or "SE" if not found
- Log warning if defaulting: "No division configured, using default: SE"
- `specify check` command should detect missing `.specify/project.json` and suggest running `specify init --here --division <DIV>`
- Document upgrade path in CHANGELOG and migration guide

---

### 7. Testing Strategy

**Decision**: Comprehensive unit and integration tests using pytest with fixtures

**Rationale**:
- pytest already configured with markers (unit, integration, edge_case)
- Fixtures provide mock guide structures for consistent test environments
- Integration tests verify end-to-end workflows (init → context update → guide display)
- Unit tests verify individual components (config read/write, division validation)
- Mock file system operations to avoid test pollution

**Test Coverage Plan**:

**Unit Tests** (`tests/unit/test_division_config.py`):
- ✅ Read valid project.json returns correct division
- ✅ Read missing project.json returns default "SE"
- ✅ Read corrupted JSON returns default "SE" and logs error
- ✅ Write division creates valid JSON file
- ✅ Atomic write prevents corruption (test mid-write interruption)
- ✅ Division validation accepts valid divisions
- ✅ Division validation rejects invalid divisions with clear error

**Integration Tests** (`tests/integration/`):
- ✅ `specify init --division DS` creates project with correct division
- ✅ `specify init` without --division defaults to "SE"
- ✅ `specify init --division INVALID` shows error with valid options
- ✅ Context scripts read division and filter guides correctly
- ✅ `specify guides show` prioritizes division guides
- ✅ `specify guides show` falls back to other divisions with warning
- ✅ Update division after initialization works correctly

**Edge Case Tests** (`tests/integration/test_edge_cases.py`):
- ✅ Missing `context/references/` directory
- ✅ Division directory exists but has no guides
- ✅ Special characters in division names (should be rejected)
- ✅ Concurrent access to project.json (locking)
- ✅ Permission errors when creating project.json

**Alternatives Considered**:
- **Manual testing only**: Not repeatable, doesn't catch regressions
- **E2E tests with real guides repo**: Too slow, flaky network dependencies
- **Property-based testing**: Over-engineering for current complexity level

**Implementation Notes**:
- Use `tmp_path` fixture for isolated test file systems
- Mock guide structure in `tests/fixtures/mock_guides/` with SE/, DS/, Platform/ subdirectories
- Use `monkeypatch` for environment variable and function mocking
- Mark slow tests with `@pytest.mark.slow` for optional skipping
- Integration tests should use `subprocess.run()` to invoke CLI as real users would

---

### 8. Performance Considerations

**Decision**: Optimize guide discovery with in-memory caching and lazy loading

**Rationale**:
- Guide list is relatively static (changes only when guides repo updates)
- Reading file system for every command invocation is wasteful
- Cache invalidation can be triggered by directory modification time
- Performance target: <2s for guide display (95th percentile) per spec SC-004

**Alternatives Considered**:
- **No caching**: Every command scans file system, too slow for large guide repos
- **Persistent cache file**: Adds complexity, stale cache management issues
- **Database index**: Over-engineering for file-based guide storage

**Implementation Notes**:
- Cache guide list in memory: `Dict[str, List[Path]]` (division -> guide paths)
- Check `context/references/` modification time before using cache
- Lazy loading: only scan guides when first needed
- Use `pathlib.glob()` for efficient directory traversal
- Benchmark with 100+ guide files to verify <2s target
- Add `--no-cache` flag for debugging

---

## Summary

All research questions from Technical Context have been resolved:

✅ **Configuration storage**: `.specify/project.json` with simple JSON schema  
✅ **Division validation**: Dynamic discovery from guides directory structure  
✅ **Context scripts**: Bash/PowerShell read division and filter guides  
✅ **AI templates**: Explicit division instructions with placeholder replacement  
✅ **Guide discovery**: `specify guides show` CLI command with division-aware search  
✅ **Backward compatibility**: Default to "SE", graceful degradation  
✅ **Testing**: Comprehensive pytest suite with unit/integration/edge case coverage  
✅ **Performance**: In-memory caching, lazy loading, <2s target verified feasible

**Next Phase**: Phase 1 - Design & Contracts (data-model.md, contracts/, quickstart.md)
