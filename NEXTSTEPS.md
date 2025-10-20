# Next Steps - Specify CLI Development Roadmap

## Overview

This document outlines the planned features and improvements for Specify CLI based on design discussions and architectural decisions made in our development sessions.

---

## v0.4.0: Implementation Guides Management (HIGH PRIORITY)

### Feature: `specify guides` Commands

**Status**: ✅ PARTIALLY IMPLEMENTED (v0.4.0)

Three developer-centric commands for managing implementation guides:

```bash
specify guides update      # ✅ IMPLEMENTED - Update guides to latest version
specify guides search      # ⏳ PLANNED - Search guides by keyword
specify guides show        # ⏳ PLANNED - Display a specific guide
```

#### Design Decisions

- **Configuration Level**: Guide repository (add/remove) is configured at the **system level** via `SPECIFY_GUIDES_REPO_URL` environment variable
- **Developer Interface**: Only `update`, `search`, and `show` are exposed to developers at runtime
- **Implementation**: Uses git submodules for version control and updates
- **Storage**: Guides stored in `context/references/` directory

#### Implementation Status

**✅ Completed (v0.4.0)**:

1. **Environment Variable**: `SPECIFY_GUIDES_REPO_URL`
   - System-level configuration for guides repository URL
   - Checked during `specify init` command

2. **Automatic Integration** (in `src/specify_cli/__init__.py`):
   - Modified `specify init` to check for `SPECIFY_GUIDES_REPO_URL`
   - Guides automatically cloned as git submodule if variable is set
   - Added `clone_guides_as_submodule()` helper function
   - Robust error handling for invalid/inaccessible repositories

3. **Guides Update Command**:
   - ✅ `specify guides update` - Uses `git submodule update --remote --merge`
   - Checks for git availability and repository status
   - Clear error messages for common issues

4. **Version Bump**:
   - ✅ Updated `pyproject.toml`: 0.3.4 → 0.4.0
   - ✅ Updated `package.json`: 0.3.4 → 0.4.0
   - ✅ Updated `CHANGELOG.md` with v0.4.0 entry

5. **Documentation Updates**:
   - ✅ `README.md` - Added guides reference and environment variable docs
   - ✅ `docs/quickstart.md` - Added guides usage example
   - ✅ `docs/TEAM_INSTALLATION.md` - Added guides management section

**⏳ Remaining Work**:

1. **Search Command** (planned for v0.4.1):
   - Implement file search/indexing for search functionality
   - Support keyword-based search across guide files

2. **Show Command** (planned for v0.4.1):
   - Implement file reading for show functionality
   - Support path-based guide display

#### Example Usage

```bash
# Update guides to latest version from configured repository
specify guides update

# Search for guides related to authentication
specify guides search authentication

# Display specific guide
specify guides show security/jwt-best-practices

# Agent references guides during planning
/plan Following authentication patterns in guides/security
```

#### Related Configuration

During `specify init`, guide repository can be configured at the binary level:
```bash
# Binary-level configuration (not exposed to developers)
# This would be handled during npm package build/distribution
specify init my-project --ai claude  # Guides configured automatically
```

---

## v0.5.0: AI Model Selection (MEDIUM PRIORITY)

### Feature: Enable GPT-5 mini for Clients

**Status**: Planned (NOT YET IMPLEMENTED)  
**Related TODO**: "Enable GPT-5 mini for clients"

Determine where AI models/clients are configured and enable 'GPT-5 mini' as an available/default client option.

#### Implementation Details

1. **Discovery Phase**:
   - Identify where AI agent configurations are stored
   - Check if configuration is in: CLI code, templates, or config files
   - Determine if model selection is per-project or global

2. **Implementation**:
   - Add 'GPT-5 mini' to available models list
   - Update help text and documentation
   - Test model availability across all agents

3. **Documentation Updates**:
   - Update `README.md` - Add GPT-5 mini to supported models
   - Update relevant agent-specific guides
   - Update `CHANGELOG.md`

---

## v0.6.0: Config Management (MEDIUM PRIORITY)

### Feature: `specify config` Commands

**Status**: Planned (NOT YET IMPLEMENTED)

Expose configuration management commands:

```bash
specify config set <key> <value>    # Set configuration value
specify config get <key>            # Get configuration value
specify config list                 # List all configurations
```

#### Purpose

- Allow developers to customize Specify behavior without editing files
- Store user preferences and project settings
- Enable future extensibility

#### Configuration Areas

- Default AI agent selection
- Script type preference (sh vs ps)
- Output format preferences
- Logging levels
- OAuth token refresh intervals

---

## v0.7.0: Advanced Features (LOW PRIORITY)

### Planned Features

1. **Specification Analysis** (`specify analyze`)
   - Cross-artifact consistency checking
   - Coverage analysis
   - Compliance verification against constitution

2. **Compliance Reporting** (`specify compliance`)
   - Generate compliance reports
   - Verify adherence to project constitution
   - Automated gate-checking for implementation

3. **Guides Administration** (Binary-level tools)
   - `specify guides-admin add` - Add new guides repository
   - `specify guides-admin remove` - Remove guides repository
   - `specify guides-admin list` - List configured repositories

---

## Documentation & Process Improvements

### Completed

- ✅ Constitution v1.1.0 ratified with 6 core principles
- ✅ Added Developer-Centric Experience principle
- ✅ OAuth authentication implemented
- ✅ npm distribution ready
- ✅ TEAM_INSTALLATION.md guide created
- ✅ OAUTH_SETUP.md guide created

### In Progress

- 🔄 Implement `specify guides` commands (update, search, show)
- 🔄 Update documentation for guides management

### Pending

- ⏳ Enable GPT-5 mini for clients
- ⏳ Implement `specify config` commands
- ⏳ Create compliance checking framework
- ⏳ Add advanced analysis commands

---

## Architecture Notes

### Guides System

**Binary-level Configuration**:
```
Binary Distribution (npm package) → Includes configured guides repository
                                   → Developer cannot modify at runtime
                                   → Admin/build-time configuration only
```

**Developer-Facing Commands**:
```
specify guides update      → git pull from configured repo
specify guides search      → fs search in context/references/
specify guides show        → fs read from context/references/
```

**Integration with SDD Workflow**:
```
/specify → Reference guides
/plan    → Follow guide patterns
/tasks   → Use guide templates
/implement → Verify against guide requirements
```

### Constitution-Driven Development

All commands and features must adhere to the YS Spec Kit Constitution v1.1.0:

1. **Specification-First** - All changes must start with specs
2. **Test-Driven Implementation** - TDD for all code
3. **CLI and Automation Focus** - CLI-first design
4. **Integration and Contract Testing** - Comprehensive testing
5. **Observability and Simplicity** - Clear logging and YAGNI
6. **Developer-Centric Experience** - User-friendly interfaces

---

## Related Files

- `AGENTS.md` - Agent integration guidelines
- `CHANGELOG.md` - Version history
- `pyproject.toml` - Python package config
- `package.json` - npm package config
- `src/specify_cli/__init__.py` - Main CLI implementation
- `.specify/memory/constitution.md` - Project constitution

---

## Questions & Decisions Pending

- [ ] Should guides include version constraints (e.g., "Use with Python 3.11+")?
- [ ] Should search support advanced queries (regex, fuzzy matching)?
- [ ] Should guides auto-update on `specify init` or require manual update?
- [ ] How should guide conflicts be handled when updating?
- [ ] Should guides include auto-generated API documentation?

---

*Last Updated: 2025-10-20*
*Maintained by: Specification Development Team*
