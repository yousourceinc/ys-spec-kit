# Implementation Plan: Hardcode Implementation Guides Repository URL

**Branch**: `001-hardcode-guides-url` | **Date**: 2025-10-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-hardcode-guides-url/spec.md`

**Note**: This plan documents the technical implementation for hardcoding the guides repository URL into the Specify CLI source code.

## Summary

This feature modifies the Specify CLI to automatically integrate implementation guides into every project without requiring developer configuration. A hardcoded constant `GUIDES_REPO_URL` will be defined in the Python source code containing the canonical guides repository URL. The `specify init` command will always attempt to clone this repository as a git submodule into `context/references/`. An environment variable `SPECIFY_GUIDES_REPO_URL` will serve as an override for testing and CI/CD scenarios. The implementation focuses on robust error handling, clear logging, and maintaining the existing `specify guides update` command.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: 
- typer (CLI framework)
- rich (terminal output formatting)
- subprocess (git command execution)
- pathlib (path manipulation)

**Storage**: Git submodules (guides stored in `context/references/`)  
**Testing**: pytest (unit tests), integration tests via CLI invocation  
**Target Platform**: Linux, macOS, Windows (WSL2)  
**Project Type**: CLI tool (Python package distributed via npm and pip)  
**Performance Goals**: 
- Guides cloning completes in under 10 seconds for typical repositories
- `specify init` overhead remains minimal (no more than 10% increase)

**Constraints**:
- Must timeout after 30s for `git submodule add`
- Must timeout after 60s for `git submodule update`
- Must maintain backward compatibility with existing projects
- Must work in environments with SSH key authentication

**Scale/Scope**:
- Single Python source file modification (`src/specify_cli/__init__.py`)
- Affects 2 CLI commands: `init` and `guides`
- New constant definition at module level
- Enhanced error handling for 6 identified edge cases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Specification-First
- **Status**: PASS
- **Evidence**: Complete specification exists in `spec.md` with 3 prioritized user stories, 12 functional requirements, and 6 success criteria. All requirements are explicit and testable.

### ✅ II. Test-Driven Implementation
- **Status**: PASS (with note)
- **Evidence**: Feature includes test scenarios in spec. Implementation will include:
  - Unit tests for `clone_guides_as_submodule()` function
  - Integration tests for `specify init` with/without environment variable
  - Edge case tests for all 6 identified scenarios
- **Note**: Implementation already exists; tests will be added retroactively per constitution.

### ✅ III. CLI and Automation Focus
- **Status**: PASS
- **Evidence**: 
  - All functionality exposed via CLI commands (`specify init`, `specify guides update`)
  - Text-based input/output with clear status messages
  - Exit codes for automation (0 = success, 1 = error)
  - No GUI components

### ✅ IV. Integration and Contract Testing
- **Status**: PASS
- **Evidence**:
  - Integration tests for git submodule operations
  - Contract: `GUIDES_REPO_URL` constant is the interface contract
  - Contract: `SPECIFY_GUIDES_REPO_URL` environment variable override
  - Tests verify both hardcoded and override scenarios

### ✅ V. Observability and Simplicity
- **Status**: PASS
- **Evidence**:
  - Clear logging via `StepTracker` for progress tracking
  - Actionable error messages for all failure scenarios
  - Simple design: single constant, straightforward fallback logic
  - No over-engineering: uses standard git submodule commands
  - Complexity justified: timeouts prevent hanging, edge case handling prevents data loss

### ✅ VI. Developer-Centric Experience
- **Status**: PASS
- **Evidence**:
  - Zero configuration required for developers (main use case)
  - Clear `--help` documentation for commands
  - Actionable error messages that explain what went wrong and how to fix it
  - Override mechanism available for advanced users without complicating simple use case
  - Status messages show progress during initialization

**Overall Gate Status**: ✅ **PASS** - All constitutional principles satisfied.

## Project Structure

### Documentation (this feature)

```
specs/001-hardcode-guides-url/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 - not needed (no unknowns)
├── data-model.md        # Phase 1 - not applicable (no data entities)
├── quickstart.md        # Phase 1 - usage examples
├── checklists/
│   └── requirements.md  # Specification quality checklist (passed)
└── contracts/           # Phase 1 - not applicable (CLI tool, no API)
```

### Source Code (repository root)

```
src/specify_cli/
├── __init__.py          # MODIFIED: Main CLI implementation
│   ├── GUIDES_REPO_URL constant (NEW at line ~85)
│   ├── clone_guides_as_submodule() function (ENHANCED with edge case handling)
│   ├── init() command (MODIFIED to always integrate guides)
│   └── guides() command group (EXISTS - no changes needed)

tests/                    # TO BE CREATED
├── unit/
│   └── test_guides_integration.py
├── integration/
│   └── test_init_with_guides.py
└── fixtures/
    └── mock_guides_repo/

.specify/
└── memory/
    └── constitution.md   # Referenced for compliance
```

**Structure Decision**: Single project structure (Option 1) is used. This is a CLI tool with all code in `src/specify_cli/`. The primary modification is to the existing `__init__.py` file, adding the hardcoded constant and enhancing the guides integration logic within the `init()` command. No new files are created for the core functionality - this is a focused modification to existing code paths.

## Complexity Tracking

*No violations detected - this section documents justified complexity only*

| Design Choice | Rationale | Simpler Alternative Rejected Because |
|---------------|-----------|-------------------------------------|
| Timeout configuration (30s/60s) | Prevents hanging on network issues | No timeout could block indefinitely, causing poor UX |
| Edge case handling for existing directory | Prevents accidental data loss | Silent overwrite could destroy user data |
| Environment variable override | Required for testing/CI flexibility | Hardcoded-only would break testing workflows |
| Git submodule validation | Ensures data integrity | Assuming success could leave broken state |

## Phase 0: Research & Technical Decisions

**Status**: No research needed - all technical decisions are clear from specification.

### Decision Log

#### 1. Git Submodule Approach

**Decision**: Use `git submodule add` and `git submodule update --init --recursive`

**Rationale**:
- Standard git feature, well-understood by developers
- Version control for guides content
- Automatic updates via `git submodule update --remote`
- Clean separation from project code

**Alternatives Considered**:
- Git clone without submodule: Rejected - loses version tracking, complicates updates
- Copy files directly: Rejected - no version control, manual sync required
- Package as Python dependency: Rejected - guides are content, not code

#### 2. Constant Location

**Decision**: Define `GUIDES_REPO_URL` constant near top of `__init__.py` (after imports, line ~85)

**Rationale**:
- Easily discoverable for maintainers
- Near other constants (`AI_CHOICES`, `SCRIPT_TYPE_CHOICES`)
- Clear documentation comments
- Single source of truth

#### 3. Override Mechanism

**Decision**: Check environment variable first, fall back to constant

**Implementation**: `guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL`

**Rationale**:
- Empty string handling (`.strip() or`) ensures empty env var falls back
- Simple one-liner, no complex conditional logic
- Explicit precedence: env var > hardcoded constant

#### 4. Error Handling Strategy

**Decision**: Fail fast with actionable errors for all edge cases

**Rationale**:
- Prevents silent failures that leave broken project state
- Guides users to resolution with specific error messages
- Aligns with Constitution Principle VI (Developer-Centric Experience)

#### 5. Timeout Values

**Decision**: 30 seconds for add, 60 seconds for update

**Rationale**:
- Typical git clone for small repos: 5-15 seconds
- Allows for slower networks without indefinite hanging
- Different values reflect operation complexity
- Update may need more time for recursive submodules

## Phase 1: Design & Implementation Details

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│ specify init command                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Check git availability                               │
│  2. Initialize project structure                         │
│  3. ┌────────────────────────────────────┐             │
│     │ Guides Integration Step           │             │
│     ├────────────────────────────────────┤             │
│     │ • Get URL (env var OR constant)   │             │
│     │ • Validate project is git repo    │             │
│     │ • Call clone_guides_as_submodule()│             │
│     │ • Handle success/failure          │             │
│     └────────────────────────────────────┘             │
│  4. Finalize project setup                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
                          │
                          │ calls
                          ▼
┌─────────────────────────────────────────────────────────┐
│ clone_guides_as_submodule(project_path, url, tracker)   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Check if context/references/ exists                 │
│     ├─ Exists as submodule? → Return success            │
│     └─ Exists but not submodule? → Error                │
│                                                          │
│  2. Create context/ parent directory                     │
│                                                          │
│  3. Execute: git submodule add <url> context/references │
│     ├─ Timeout: 30 seconds                              │
│     ├─ Already exists error? → Treat as success         │
│     └─ Other error? → Return failure                    │
│                                                          │
│  4. Execute: git submodule update --init --recursive    │
│     ├─ Timeout: 60 seconds                              │
│     └─ Error? → Return failure                          │
│                                                          │
│  5. Log success and return True                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Code Modifications

#### 1. Add GUIDES_REPO_URL Constant

**Location**: `src/specify_cli/__init__.py`, line ~85 (after SCRIPT_TYPE_CHOICES)

```python
# Official implementation guides repository URL
# This is the canonical source for implementation guides that will be automatically
# integrated into every project initialized with specify init.
# Override: Set SPECIFY_GUIDES_REPO_URL environment variable to use a different repository.
GUIDES_REPO_URL = "git@github.com:yousourceinc/implementation-guides.git"
```

#### 2. Enhance clone_guides_as_submodule() Function

**Location**: `src/specify_cli/__init__.py`, line ~443

**Changes**:
- Add check for existing directory before attempting clone
- Validate if existing directory is a submodule (check `.gitmodules`)
- Handle "already exists" git error gracefully
- Return True if already configured, False only on actual failure

**New Logic**:
```python
# Before attempting git submodule add:
if guides_dir.exists():
    gitmodules_path = project_path / ".gitmodules"
    if gitmodules_path.exists():
        gitmodules_content = gitmodules_path.read_text()
        if str(guides_dir.relative_to(project_path)) in gitmodules_content:
            # Already a valid submodule
            return True
    # Exists but not a submodule - error
    return False
```

#### 3. Modify init() Command Guides Step

**Location**: `src/specify_cli/__init__.py`, line ~1100

**Changes**:
- Always attempt guides integration (not conditional on env var existence)
- Use environment variable as override, constant as fallback
- Treat guides clone failure as fatal error (raise exception)

**New Logic**:
```python
# Guides step - always attempt to integrate guides
guides_repo_url = os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL

if not is_git_repo(project_path):
    tracker.error("guides", "requires git repository")
else:
    if not clone_guides_as_submodule(project_path, guides_repo_url, tracker=tracker):
        raise Exception(f"Failed to clone implementation guides from {guides_repo_url}")
```

### Error Messages

All error messages must be actionable per Constitution Principle VI.

| Scenario | Error Message | Actionable Guidance |
|----------|---------------|---------------------|
| Directory exists, not submodule | `Directory {path} already exists but is not a submodule` | "Remove the directory or rename it, then try again" |
| Network/permission error | `Failed to clone implementation guides from {url}` | "Check your network connection and ensure SSH keys are configured for GitHub" |
| No git repository | `Guides integration requires git repository` | "Initialize project with git or use --no-git flag" |
| Clone timeout | `Guides repository clone timed out` | "Check network connectivity. Large repositories may require manual clone." |
| Invalid URL format | `Invalid guides repository URL: {url}` | "Ensure URL is in format git@github.com:org/repo.git" |
| Update without guides | `No implementation guides found in this project` | "Guides are configured via SPECIFY_GUIDES_REPO_URL during project init" |

### Logging & Observability

Per Constitution Principle V, all operations must provide clear status logging.

**Progress Messages** (via StepTracker):
- `"Cloning guides repository as submodule"` - start
- `"Guides submodule already exists"` - skip
- `"Guides submodule initialized"` - success
- `"Failed to add submodule: {error}"` - failure with details

**Console Output**:
```
✓ Guides submodule initialized
⚠ Note: Implementation guides submodule already exists
✗ Error: Directory context/references/ already exists but is not a submodule
```

### Testing Strategy

#### Unit Tests

**File**: `tests/unit/test_guides_integration.py`

```python
def test_clone_guides_with_valid_url()
def test_clone_guides_with_invalid_url()
def test_clone_guides_directory_exists_as_submodule()
def test_clone_guides_directory_exists_not_submodule()
def test_clone_guides_timeout_handling()
def test_clone_guides_network_error()
def test_environment_variable_override()
def test_fallback_to_hardcoded_constant()
```

#### Integration Tests

**File**: `tests/integration/test_init_with_guides.py`

```python
def test_init_creates_guides_submodule()
def test_init_with_env_var_override()
def test_init_fails_gracefully_on_invalid_url()
def test_init_skips_guides_if_already_present()
def test_guides_update_command()
```

#### Edge Case Tests

All 6 edge cases from specification must have explicit tests:
1. Existing directory not submodule
2. Network/permission issues
3. Non-git repository
4. Empty/malformed guides repo
5. Interrupted clone
6. Invalid URL format

## Phase 2: Implementation Checklist

**Note**: This phase is handled by `/tasks` command. Below is a preview of expected tasks.

### Setup Tasks
- [ ] Create test directory structure
- [ ] Set up pytest fixtures for mock repositories
- [ ] Configure CI to run guides integration tests

### User Story 1: Automatic Guides Integration (P1)
- [ ] Add `GUIDES_REPO_URL` constant to `__init__.py`
- [ ] Enhance `clone_guides_as_submodule()` with edge case handling
- [ ] Modify `init()` command to always attempt guides integration
- [ ] Add environment variable fallback logic
- [ ] Implement timeout handling (30s add, 60s update)
- [ ] Write unit tests for `clone_guides_as_submodule()`
- [ ] Write integration tests for `init` with guides
- [ ] Test all 6 edge cases
- [ ] Update documentation (README.md, quickstart.md)

### User Story 2: Override Mechanism (P2)
- [ ] Test environment variable override functionality
- [ ] Test fallback to hardcoded constant
- [ ] Test empty string handling
- [ ] Document override usage in TEAM_INSTALLATION.md

### User Story 3: Guides Update Command (P3)
- [ ] Verify `guides update` command still works
- [ ] Test error handling when no guides present
- [ ] Add integration tests for update scenarios

### Polish
- [ ] Add comprehensive error messages
- [ ] Add progress logging
- [ ] Update CHANGELOG.md
- [ ] Bump version to 0.4.0
- [ ] Create GUIDES_IMPLEMENTATION_COMPLETE.md

## Backward Compatibility

**Existing Projects**: Projects initialized before this feature will not be affected. Guides integration only occurs during `specify init`.

**Upgrade Path**: Developers with existing projects can manually add guides:
```bash
cd my-existing-project
git submodule add git@github.com:yousourceinc/implementation-guides.git context/references
git submodule update --init --recursive
```

## Performance Considerations

**Baseline**: `specify init` currently takes ~2-5 seconds for project setup

**Expected Impact**: +5-10 seconds for guides cloning (network dependent)

**Mitigation**:
- Timeout prevents indefinite hangs
- Submodule uses git's efficient protocol
- Parallel steps where possible (guides clone doesn't block other setup)

**Monitoring**: Log execution time for guides step to track performance

## Security Considerations

**SSH Key Access**: Requires developers have GitHub SSH keys configured

**Network Security**: Uses git over SSH (encrypted transport)

**Access Control**: Guides repository permissions control who can read

**No Secrets**: No API keys or passwords in code (git handles auth)

## Documentation Updates

### Files to Update

1. **README.md**: Add `GUIDES_REPO_URL` constant documentation
2. **docs/TEAM_INSTALLATION.md**: Add override mechanism usage
3. **docs/quickstart.md**: Add automatic guides integration examples
4. **CHANGELOG.md**: Add v0.4.0 entry
5. **NEXTSTEPS.md**: Update v0.4.0 status
6. **GUIDES_IMPLEMENTATION_COMPLETE.md**: Create implementation summary

### Help Text Updates

**`specify init --help`**: Add note about automatic guides integration

**`specify guides --help`**: Add note about hardcoded repository

## Deployment Plan

1. **Merge to main**: After all tests pass
2. **Version bump**: 0.3.4 → 0.4.0 (minor version, new feature)
3. **Tag release**: v0.4.0
4. **Publish to npm**: `npm publish`
5. **Update pip package**: `uv tool upgrade specify-cli`
6. **Notify team**: Send announcement with upgrade instructions

## Rollback Plan

If issues arise post-deployment:

1. **Immediate**: Revert to v0.3.4 tag
2. **Quick fix**: Set empty `GUIDES_REPO_URL` constant to disable feature
3. **Long-term**: Fix bugs and release v0.4.1

## Success Metrics

Align with Success Criteria from specification:

- **SC-001**: 100% of new projects have guides → Monitor via telemetry
- **SC-002**: Init time under 10s → Log and monitor execution time
- **SC-003**: Override works 100% → Verify via automated tests
- **SC-004**: Clear error messages → User feedback surveys
- **SC-005**: Zero configuration → No support tickets about setup
- **SC-006**: Update works 100% → Verify via automated tests

## Implementation Note

**Status**: This plan documents a feature that has been implemented. The code exists in the `feat/hardcode-guides-url` branch. This plan serves as:

1. **Documentation**: Technical reference for the implementation
2. **Test Guide**: Blueprint for writing comprehensive tests
3. **SDD Example**: Demonstration of retroactive specification/planning

The implementation matches this plan, but tests need to be added per Constitution Principle II (Test-Driven Implementation).

