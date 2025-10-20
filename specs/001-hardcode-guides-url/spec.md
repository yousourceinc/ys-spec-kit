# Feature Specification: Hardcode Implementation Guides Repository URL

**Feature Branch**: `001-hardcode-guides-url`  
**Created**: 2025-10-20  
**Status**: Draft  
**Input**: User description: "We will hardcode the official URL of our company's implementation guides repository directly into the specify-cli source code. This ensures that every project initialized with our forked tool automatically includes the correct guides without requiring any developer configuration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Initializes New Project with Automatic Guides (Priority: P1)

A developer runs `specify init` to create a new project and the implementation guides are automatically integrated without any configuration needed. The developer doesn't need to know the guides repository URL or set any environment variables.

**Why this priority**: This is the core value proposition - making guides integration transparent and automatic for all developers, eliminating configuration overhead and ensuring consistency across all projects.

**Independent Test**: Can be fully tested by running `specify init my-project --ai claude` and verifying that `context/references/` contains the guides submodule with content from the hardcoded repository URL. Delivers immediate value by ensuring all projects have guides available.

**Acceptance Scenarios**:

1. **Given** a developer has Specify CLI installed and git is available, **When** they run `specify init my-project --ai claude`, **Then** the project is created with guides automatically cloned to `context/references/` from the hardcoded URL
2. **Given** a developer runs `specify init` without setting any environment variables, **When** the initialization completes, **Then** the guides submodule is present and contains the latest implementation guides
3. **Given** guides are already integrated in a project, **When** a developer runs `specify init` again in a different directory, **Then** the guides are cloned fresh without conflicts

---

### User Story 2 - Testing/CI Pipeline Overrides Guides URL (Priority: P2)

A CI/CD pipeline or developer testing environment needs to use a different guides repository (e.g., a staging or test guides repo). They set the `SPECIFY_GUIDES_REPO_URL` environment variable which overrides the hardcoded URL.

**Why this priority**: Essential for testing and CI/CD workflows where different environments need different guide repositories, but secondary to the main use case of automatic integration.

**Independent Test**: Can be tested by setting `export SPECIFY_GUIDES_REPO_URL="git@github.com:test-org/test-guides.git"` and running `specify init`, then verifying the guides come from the override URL, not the hardcoded one. Delivers value by maintaining flexibility for advanced use cases.

**Acceptance Scenarios**:

1. **Given** `SPECIFY_GUIDES_REPO_URL` environment variable is set to a valid git URL, **When** a developer runs `specify init`, **Then** guides are cloned from the environment variable URL instead of the hardcoded URL
2. **Given** the environment variable is set to an empty string, **When** `specify init` runs, **Then** the system falls back to the hardcoded URL
3. **Given** the override URL is invalid or inaccessible, **When** `specify init` runs, **Then** a clear error message indicates the override URL failed and the operation halts

---

### User Story 3 - Developer Updates Guides in Existing Project (Priority: P3)

A developer working on an existing project wants to update their implementation guides to the latest version. They run `specify guides update` which updates the submodule to the latest commit from the configured repository.

**Why this priority**: Important for keeping guides current, but not required for initial project setup. Developers can manually update git submodules if this command isn't available.

**Independent Test**: Can be tested by initializing a project, manually editing guides content to simulate outdated state, running `specify guides update`, and verifying the guides are restored to latest. Delivers value by providing a convenient update mechanism.

**Acceptance Scenarios**:

1. **Given** a project has guides integrated as a submodule, **When** a developer runs `specify guides update`, **Then** the guides submodule is updated to the latest remote commit
2. **Given** the guides repository has new commits, **When** `specify guides update` runs, **Then** the changes are shown and the developer is prompted to commit the submodule update
3. **Given** no git repository exists in the project, **When** `specify guides update` runs, **Then** a clear error explains that guides updates require git

---

### Edge Cases

- What happens when `context/references/` directory already exists but is not a git submodule? (System should fail with clear error indicating the directory exists but isn't a valid submodule)
- What happens when the hardcoded guides URL is inaccessible due to network or permission issues? (System should fail with actionable error about network/permissions and suggest checking SSH keys or network connectivity)
- What happens when a developer tries to initialize a project in a non-git repository? (System should skip guides integration or fail gracefully with explanation that guides require git)
- What happens when the guides repository is empty or malformed? (System should complete initialization but log warning about guides content)
- What happens when `specify init` is interrupted during guides cloning? (System should clean up partial state and allow retry)
- What happens when the override environment variable contains invalid URL format? (System should validate URL format and fail with clear error before attempting clone)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a hardcoded constant `GUIDES_REPO_URL` in the Python source code containing the official guides repository URL (e.g., `git@github.com:yousourceinc/implementation-guides.git`)
- **FR-002**: System MUST modify `specify init` command to always attempt guides integration without checking for flags or requiring environment variables
- **FR-003**: System MUST clone the guides repository as a git submodule in the `context/references/` directory during every `specify init` execution
- **FR-004**: System MUST check for `SPECIFY_GUIDES_REPO_URL` environment variable first, and use it as an override if present, otherwise fall back to the hardcoded `GUIDES_REPO_URL` constant
- **FR-005**: System MUST validate that the target project is a git repository before attempting to add the guides submodule
- **FR-006**: System MUST fail with a clear, actionable error if `context/references/` exists but is not a valid git repository
- **FR-007**: System MUST fail with a clear, actionable error if the guides repository cannot be cloned due to network issues, permission errors, or invalid URLs
- **FR-008**: System MUST initialize and update the guides submodule automatically using `git submodule update --init --recursive`
- **FR-009**: System MUST detect if the guides directory already exists as a valid submodule and skip re-cloning in that case
- **FR-010**: System MUST preserve the `specify guides update` command to allow developers to update guides to the latest version post-initialization
- **FR-011**: System MUST log clear status messages during guides integration showing progress and completion
- **FR-012**: System MUST timeout after 30 seconds for `git submodule add` operations and 60 seconds for `git submodule update` operations to prevent hanging

### Non-Functional Requirements

- **NFR-001**: The hardcoded URL constant must be easily discoverable in the source code for maintainers (e.g., near the top of the file with clear comments)
- **NFR-002**: Error messages must be actionable, telling users exactly what went wrong and how to fix it
- **NFR-003**: The guides integration step must not significantly increase `specify init` execution time (target: under 10 seconds for typical repositories)
- **NFR-004**: The solution must maintain backward compatibility with existing projects that were initialized before this feature

### Key Entities

- **GUIDES_REPO_URL**: Hardcoded Python constant containing the canonical guides repository URL
- **Guides Submodule**: Git submodule located at `context/references/` containing implementation guides
- **SPECIFY_GUIDES_REPO_URL**: Environment variable that serves as an optional override for the hardcoded URL
- **Project Repository**: The git repository created by `specify init` that will contain the guides submodule

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of projects initialized with `specify init` automatically receive implementation guides without developer configuration (measured by checking for `context/references/` submodule presence)
- **SC-002**: Developers can initialize a project with guides in under 10 seconds on average (excluding initial git repository initialization)
- **SC-003**: Override mechanism works correctly in 100% of test cases when `SPECIFY_GUIDES_REPO_URL` is set (verified through automated testing)
- **SC-004**: Error messages are clear and actionable in all failure scenarios (measured through user testing feedback)
- **SC-005**: Zero configuration required from developers to get guides integration (no environment variables, no flags, no manual steps)
- **SC-006**: `specify guides update` successfully updates guides to latest version in 100% of test cases where submodule exists

## Assumptions

1. **Git Availability**: We assume git is available in the developer's environment since Specify CLI requires git for branch management
2. **SSH Key Setup**: We assume developers have SSH keys configured for GitHub access (required for git@github.com URLs)
3. **Guides Repository Access**: We assume all developers using the forked Specify CLI have read access to the hardcoded guides repository
4. **Network Connectivity**: We assume developers have network access to GitHub during project initialization
5. **Single Guides Repository**: We assume one canonical guides repository is sufficient for all projects (override available for special cases)

## Dependencies

- **Git**: Required for submodule operations
- **Network Access**: Required to clone guides repository from GitHub
- **GitHub SSH Access**: Required for git@ protocol URLs (or HTTPS if URL uses that format)
- **Existing Guides Repository**: The hardcoded URL must point to a valid, accessible git repository

## Out of Scope

- Multiple guides repositories per project (only one guides submodule is supported)
- GUI for managing guides configuration (remains CLI-only)
- Automatic guides version pinning or rollback (developers must use git submodule commands manually)
- Guides content validation or linting (guides are cloned as-is)
- Local/offline guides installation (requires network access to clone)
- Guides search or show commands (planned for v0.4.1, not part of this feature)

## Related Documentation

- Implementation Guides Integration: `GUIDES_IMPLEMENTATION_COMPLETE.md`
- Development Roadmap: `NEXTSTEPS.md` (v0.4.0 section)
- Agent Instructions: `AGENTS.md` (guides integration section)
- Changelog: `CHANGELOG.md` (v0.4.0 entry)

