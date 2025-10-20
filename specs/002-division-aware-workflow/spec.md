# Feature Specification: Division-Aware Workflow

**Feature Branch**: `002-division-aware-workflow`  
**Created**: October 21, 2025  
**Status**: Draft  
**Input**: Division-Aware workflow to provide context-specific guidance by modifying the init command to capture a project's division and updating core AI commands to prioritize relevant divisional guides.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initialize Project with Division Selection (Priority: P1)

A developer starts a new project and wants to ensure that their AI assistant provides guidance specific to their division's standards and best practices. They run the `specify init` command and select their division from a predefined list (Software Engineering, Data Science, Platform Engineering, or other divisions). This division choice is automatically saved to the project configuration, ensuring all subsequent AI interactions are division-aware.

**Why this priority**: This is the foundational feature that enables division-aware guidance throughout the entire workflow. Every subsequent AI interaction depends on knowing the project's division. Without this, the feature cannot function.

**Independent Test**: Fully testable by running `specify init` with the `--division` flag, verifying that `.specify/project.json` is created with the correct division value, and confirming that the default division (SE) is used when the option is not provided.

**Acceptance Scenarios**:

1. **Given** a developer runs `specify init my-project --division DS`, **When** the project is initialized, **Then** `.specify/project.json` is created with `{"division": "DS"}` and the project structure is set up correctly.
2. **Given** a developer runs `specify init my-project` without the `--division` flag, **When** the project is initialized, **Then** `.specify/project.json` is created with the default value `{"division": "SE"}`.
3. **Given** available division options are Software Engineering (SE), Data Science (DS), and Platform Engineering (Platform), **When** a developer uses `--division invalid`, **Then** the command provides an error message listing valid options and prompts the user to select one.
4. **Given** a project is already initialized with a division, **When** the developer checks `.specify/project.json`, **Then** the file is version-controlled and readable by all team members.

---

### User Story 2 - AI Agent Prioritizes Divisional Guides (Priority: P1)

When a developer uses AI commands like `/specify`, `/plan`, or `/tasks` within their project, the AI agent automatically reads the project's division from `.specify/project.json` and prioritizes guides from that division's directory (e.g., `context/references/SE/`, `context/references/DS/`). This ensures the AI provides context-specific recommendations aligned with the team's standards.

**Why this priority**: This is critical for delivering the core value of division-aware guidance. Without this, the division selection has no practical effect. The AI must actively use the division information to provide relevant guidance.

**Independent Test**: Fully testable by initializing a project with a specific division, then triggering an AI command and verifying that the AI references guides from the correct divisional directory in its responses.

**Acceptance Scenarios**:

1. **Given** a project is initialized with `division: SE`, **When** a developer uses the `/specify` command, **Then** the AI agent prominently displays Software Engineering guides from `context/references/SE/` and prioritizes SE-specific patterns and requirements.
2. **Given** a project is initialized with `division: DS`, **When** a developer uses the `/plan` command, **Then** the AI agent references Data Science guides from `context/references/DS/` and provides DS-specific methodology guidance.
3. **Given** a project is initialized with `division: Platform`, **When** a developer uses the `/tasks` command, **Then** the AI agent prioritizes Platform Engineering guides from `context/references/Platform/` and references platform-specific standards.
4. **Given** divisional guides are organized in subdirectories by division, **When** the AI agent generates responses, **Then** it clearly indicates which division's standards it is referencing (e.g., "Following Software Engineering best practices...").

---

### User Story 3 - Division-Aware Guide Search and Discovery (Priority: P2)

When a developer uses guide discovery tools (the in-agent `/guides` command or the `specify guides show <guide-path>` CLI command), search results and guide displays are filtered to prioritize the project's designated division. This helps developers quickly find relevant guides without being overwhelmed by guides from other divisions.

**Why this priority**: This enhances the usability and efficiency of guide discovery but is secondary to the core AI guidance integration. Developers can still manually navigate guides if this feature is not implemented, but having division-aware search makes the experience significantly better.

**Independent Test**: Fully testable by running `specify guides show <guide-path>` with a guide that exists in the division's directory, verifying it displays correctly, and by searching for guides to confirm division-specific results are prioritized.

**Acceptance Scenarios**:

1. **Given** a project with `division: SE` has guides in both `context/references/SE/` and `context/references/DS/`, **When** a developer searches for guides, **Then** SE guides appear first in the results with DS guides appearing secondarily.
2. **Given** a developer runs `specify guides show backend-patterns.md` in an SE project, **When** the command executes, **Then** it displays the guide from `context/references/SE/backend-patterns.md` if it exists.
3. **Given** a guide path is provided that doesn't exist in the project's division, **When** the command executes, **Then** it searches other divisions and displays the guide if found elsewhere, but with a note indicating it's from a different division.
4. **Given** the `/guides` command is available in the AI agent, **When** a developer uses it in a division-aware project, **Then** it returns division-filtered results prioritizing the project's division.

---

### User Story 4 - Division-Specific Prompts and Instructions (Priority: P2)

The AI command templates for `/specify`, `/plan`, and `/tasks` are updated to include division-specific instructions that guide the AI to prioritize patterns, requirements, and best practices from the project's division. The `/tasks` command specifically requires guide references to come from the project's designated division directory.

**Why this priority**: This ensures consistency and reinforces division awareness in the AI's responses. While the AI can infer division information from the guides directory, explicit instructions in the prompts make the requirement clear and enforceable.

**Independent Test**: Fully testable by examining the AI command prompt templates to verify they include division-specific language, and by testing that the AI refuses to reference guides outside the designated division for the `/tasks` command.

**Acceptance Scenarios**:

1. **Given** the `/specify` prompt is updated with division guidance, **When** an AI agent processes a feature specification for an SE project, **Then** the prompt instructs the AI to reference SE-specific patterns and best practices.
2. **Given** the `/plan` prompt is updated with division guidance, **When** an AI agent generates a development plan for a DS project, **Then** the prompt directs the AI to prioritize Data Science methodologies and tools.
3. **Given** the `/tasks` prompt is updated with division-specific requirements, **When** an AI agent generates tasks for a Platform project, **Then** all "Guide reference" fields in the generated tasks point to guides within `context/references/Platform/`.
4. **Given** a project has multiple divisions' guides available, **When** the `/tasks` command is executed, **Then** guide references must be from the project's configured division, and any references to other divisions are flagged as warnings.

---

### Edge Cases

- What happens when a project is initialized without guides configured or when the `context/references/` directory doesn't exist? (The system should function gracefully, allowing division selection but noting that guides are not available.)
- How does the system behave if `.specify/project.json` is deleted or corrupted? (The system should either default to SE or prompt the user to reconfigure the division.)
- What if a developer changes their project's division after initialization? (The system should allow updating `.specify/project.json` through a new command or configuration interface, and the change should take effect immediately in subsequent AI interactions.)
- What if a division name contains special characters or spaces? (Only predefined division names (SE, DS, Platform) should be allowed; invalid inputs should be rejected with clear error messages.)
- How does the system handle requests for guides from non-existent divisions? (The system should return an error indicating the division is not recognized and list valid options.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST add a `--division` CLI option to the `specify init` command that accepts predefined division values (SE, DS, Platform, and any additional divisions defined in the guides repository structure).
- **FR-002**: System MUST default the `--division` option to "SE" (Software Engineering) when the option is not provided during project initialization.
- **FR-003**: System MUST create and store the project division in a version-controlled file `.specify/project.json` in the format `{"division": "<DIVISION_NAME>"}` during project initialization.
- **FR-004**: System MUST validate that the division value provided is from the predefined list of valid divisions; if invalid, it MUST display an error message listing valid options and prompt the user to select one.
- **FR-005**: System MUST read `.specify/project.json` to determine the project's division and make this information available to AI context scripts and command templates.
- **FR-006**: Context scripts (update-agent-context.sh and update-agent-context.ps1) MUST read the project's division from `.specify/project.json` and prominently display guides from the project's designated division directory (e.g., `context/references/SE/`) to the AI agent.
- **FR-007**: AI command templates for `/specify`, `/plan`, and `/tasks` MUST be updated to include instructions that direct AI agents to prioritize patterns, requirements, and best practices from the project's designated division subdirectory within the guides.
- **FR-008**: The `/tasks` command template MUST require that all guide references point to guides within the project's designated division directory; references to guides outside the division MUST be flagged or rejected.
- **FR-009**: System MUST implement or enhance the `/guides` command (in-agent discovery tool) to filter and prioritize search results, showing guides from the project's division first, followed by guides from other divisions.
- **FR-010**: System MUST implement the `specify guides show <guide-path>` CLI command to display a specific guide file, prioritizing guides from the project's division when multiple matches exist.
- **FR-011**: System MUST handle cases where `.specify/project.json` is missing or corrupted by either using a sensible default (SE) or prompting the user to reconfigure the division.
- **FR-012**: System MUST allow developers to update the project's division after initialization through a configuration command or by directly editing `.specify/project.json`, with the change taking effect immediately in subsequent AI interactions.

### Key Entities

- **Project Configuration (.specify/project.json)**: A version-controlled JSON file that stores the project's metadata, including the selected division. Structure: `{"division": "<DIVISION_NAME>"}`. This file is created during project initialization and can be updated by developers.
- **Division**: A category that organizes guides and standards relevant to specific types of projects (e.g., Software Engineering, Data Science, Platform Engineering). Each division has a corresponding subdirectory in `context/references/<DIVISION>/`.
- **Divisional Guides Directory**: A subdirectory within `context/references/` that contains guides, patterns, and best practices specific to a division (e.g., `context/references/SE/`, `context/references/DS/`, `context/references/Platform/`).
- **AI Command Template**: A prompt or instruction set used by AI agents when executing commands like `/specify`, `/plan`, or `/tasks`. These templates are updated to include division-aware instructions.
- **Context Script**: A bash or PowerShell script (update-agent-context.sh or update-agent-context.ps1) that prepares and delivers context information to AI agents. This script is enhanced to read the project's division and prioritize relevant guides.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can initialize a project with a specific division using `specify init <project-name> --division <DIVISION>` and the division is correctly stored in `.specify/project.json`.
- **SC-002**: AI agents receive division-specific guidance with 100% consistency; every AI response references guides and standards from the project's designated division first.
- **SC-003**: Guide search results are filtered by division; guides from the project's division appear in the top 50% of results in at least 95% of search queries.
- **SC-004**: Developers can discover and display divisional guides using `specify guides show <guide-path>` with a response time under 2 seconds in 95% of cases.
- **SC-005**: Project division can be changed after initialization through configuration interface or file editing, with the change taking effect immediately in the next AI interaction.
- **SC-006**: Error handling for invalid divisions or missing `.specify/project.json` provides clear, actionable messages to developers at least 90% of the time.
- **SC-007**: All AI command templates (`/specify`, `/plan`, `/tasks`) are updated to include division-aware instructions, with no template missing this guidance.
- **SC-008**: The `/tasks` command enforces that 100% of guide references come from the project's designated division, with violations flagged in the output.
- **SC-009**: Development teams using division-aware workflows report improved alignment with divisional standards, with at least 80% of teams confirming enhanced relevance of AI guidance within the first month.
- **SC-010**: System documentation includes clear instructions for developers on how to initialize projects with divisions and how to interpret division-specific guidance from AI agents.

## Assumptions

- **Division Structure Exists**: The guides repository (`context/references/`) is organized with subdirectories for each division (SE, DS, Platform, etc.). If a division doesn't have a corresponding directory, the system treats guides from that division as unavailable.
- **Default Division is Appropriate**: Software Engineering (SE) is a reasonable default for most projects. Projects that require a different division must explicitly select it during initialization.
- **`.specify/project.json` is Reliable**: The file is created correctly during initialization, version-controlled, and not subject to manual corruption. Developers are assumed to have basic JSON editing knowledge if they manually modify this file.
- **AI Agents Can Access Division Context**: AI command templates and context scripts are designed such that AI agents can reliably read and understand division information provided to them. The AI agent integrations (Copilot, Claude, etc.) are capable of interpreting and acting on division-specific instructions.
- **Guide Organization by Division is Feasible**: The guides repository can be effectively organized into divisional subdirectories without significant refactoring. Guides can be tagged or categorized by division to support this organization.
- **Version Control Compatibility**: `.specify/project.json` can be safely version-controlled without conflicts, as division selection is typically a one-time choice during project initialization and rarely changes.
- **Backward Compatibility**: Existing projects without `.specify/project.json` continue to work with a sensible default (SE) or with a graceful upgrade prompt.

---

**Status**: Ready for Clarification and Planning  
**Next Step**: Run `/speckit.clarify` to refine requirements or proceed directly to `/speckit.plan` for detailed task breakdown.

