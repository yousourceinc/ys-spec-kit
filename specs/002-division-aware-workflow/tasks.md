# Tasks: Division-Aware Workflow

**Feature**: Division-Aware Workflow  
**Branch**: `002-division-aware-workflow`  
**Input**: Design documents from `/specs/002-division-aware-workflow/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions
- Single project structure: `src/specify_cli/`, `scripts/bash/`, `scripts/powershell/`, `templates/commands/`, `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test fixture setup

- [ ] T001 Create test fixtures directory structure in tests/fixtures/mock_guides/ with SE/, DS/, Platform/ subdirectories
- [ ] T002 [P] Create sample guide files in tests/fixtures/mock_guides/SE/ (backend-patterns.md, api-design.md)
- [ ] T003 [P] Create sample guide files in tests/fixtures/mock_guides/DS/ (data-pipelines.md, ml-models.md)
- [ ] T004 [P] Create sample guide files in tests/fixtures/mock_guides/Platform/ (infrastructure.md, kubernetes.md)
- [ ] T005 [P] Create sample guide files in tests/fixtures/mock_guides/Common/ (git-workflow.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core config module that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create src/specify_cli/config.py module with empty placeholder functions
- [ ] T007 Implement read_project_config(project_root: Path) -> dict in src/specify_cli/config.py per python-config-api.md contract
- [ ] T008 Implement write_project_config(project_root: Path, division: str) -> None in src/specify_cli/config.py with atomic write
- [ ] T009 Implement get_project_division(project_root: Path) -> str convenience function in src/specify_cli/config.py
- [ ] T010 Implement get_valid_divisions(guides_path: Path) -> list[str] in src/specify_cli/config.py with directory scanning
- [ ] T011 Implement validate_division(division: str, guides_path: Path) -> tuple[bool, Optional[str]] in src/specify_cli/config.py
- [ ] T012 Write unit tests in tests/unit/test_division_config.py for read_project_config (valid file, missing file, corrupted JSON)
- [ ] T013 Write unit tests in tests/unit/test_division_config.py for write_project_config (create new, atomic write, preserve existing fields)
- [ ] T014 Write unit tests in tests/unit/test_division_config.py for get_valid_divisions (scan directories, fallback to defaults)
- [ ] T015 Write unit tests in tests/unit/test_division_config.py for validate_division (valid/invalid divisions, error messages)

**Checkpoint**: Foundation ready - config module complete and tested, user story implementation can now begin

---

## Phase 3: User Story 1 - Initialize Project with Division Selection (Priority: P1) 🎯 MVP

**Goal**: Enable developers to initialize projects with a division choice that is stored in `.specify/project.json`

**Independent Test**: Run `specify init test-project --division DS` and verify `.specify/project.json` contains `{"division": "DS"}`. Run without `--division` flag and verify default "SE" is used.

**Acceptance Scenarios from Spec**:
1. `specify init my-project --division DS` creates `.specify/project.json` with `{"division": "DS"}`
2. `specify init my-project` without flag creates `.specify/project.json` with `{"division": "SE"}`
3. `--division invalid` shows error with valid options
4. Config file is version-controlled and readable

### Implementation for User Story 1

- [ ] T016 [US1] Add --division CLI option to init command in src/specify_cli/__init__.py with Typer option definition
- [ ] T017 [US1] Add division validation in init command using validate_division() before project creation in src/specify_cli/__init__.py
- [ ] T018 [US1] Add call to write_project_config() in init command after project structure creation in src/specify_cli/__init__.py
- [ ] T019 [US1] Update init command to use "SE" default when --division not provided in src/specify_cli/__init__.py
- [ ] T020 [US1] Add division parameter to help text and examples in init command docstring in src/specify_cli/__init__.py
- [ ] T021 [US1] Write integration test in tests/integration/test_init_with_division.py for `specify init --division DS` scenario
- [ ] T022 [US1] Write integration test in tests/integration/test_init_with_division.py for `specify init` without division (default SE)
- [ ] T023 [US1] Write integration test in tests/integration/test_init_with_division.py for `specify init --division INVALID` error handling
- [ ] T024 [US1] Write integration test in tests/integration/test_init_with_division.py for `specify init --here --division Platform` on existing project

**Checkpoint**: User Story 1 complete - projects can be initialized with divisions, config file is created and validated

---

## Phase 4: User Story 2 - AI Agent Prioritizes Divisional Guides (Priority: P1)

**Goal**: Context scripts read division from `.specify/project.json` and prioritize guides from that division when generating agent context files

**Independent Test**: Initialize project with division DS, run update-agent-context script, verify agent context file lists DS guides first, then Common, then other divisions

**Acceptance Scenarios from Spec**:
1. Project with `division: SE` → AI references SE guides from `context/references/SE/`
2. Project with `division: DS` → AI references DS guides from `context/references/DS/`
3. Project with `division: Platform` → AI references Platform guides from `context/references/Platform/`
4. AI responses clearly indicate which division's standards are referenced

### Implementation for User Story 2 - Bash Script

- [ ] T025 [P] [US2] Add get_project_division() function to scripts/bash/common.sh per shell-script-api.md (uses jq or Python fallback)
- [ ] T026 [P] [US2] Add list_division_guides() function to scripts/bash/common.sh per shell-script-api.md
- [ ] T027 [P] [US2] Add generate_division_context() function to scripts/bash/common.sh that creates division-aware Markdown
- [ ] T028 [US2] Update scripts/bash/update-agent-context.sh to call get_project_division() and use result in context generation
- [ ] T029 [US2] Update scripts/bash/update-agent-context.sh to call generate_division_context() and insert into agent context files

### Implementation for User Story 2 - PowerShell Script

- [ ] T030 [P] [US2] Add Get-ProjectDivision function to scripts/powershell/common.ps1 per shell-script-api.md
- [ ] T031 [P] [US2] Add Get-DivisionGuides function to scripts/powershell/common.ps1 per shell-script-api.md
- [ ] T032 [P] [US2] Add New-DivisionContext function to scripts/powershell/common.ps1 that creates division-aware Markdown
- [ ] T033 [US2] Update scripts/powershell/update-agent-context.ps1 to call Get-ProjectDivision and use result in context generation
- [ ] T034 [US2] Update scripts/powershell/update-agent-context.ps1 to call New-DivisionContext and insert into agent context files

### Testing for User Story 2

- [ ] T035 [US2] Write integration test in tests/integration/test_context_division.py for bash script reading division and generating context
- [ ] T036 [US2] Write integration test in tests/integration/test_context_division.py for PowerShell script reading division and generating context
- [ ] T037 [US2] Write integration test in tests/integration/test_context_division.py verifying division guides appear first in context files
- [ ] T038 [US2] Write integration test in tests/integration/test_context_division.py for missing .specify/project.json (defaults to SE)

**Checkpoint**: User Story 2 complete - context scripts read division and prioritize guides correctly, agent context files are division-aware

---

## Phase 5: User Story 3 - Division-Aware Guide Search and Discovery (Priority: P2)

**Goal**: Implement `specify guides show <guide-path>` CLI command that prioritizes guides from the project's division

**Independent Test**: Initialize SE project, run `specify guides show backend-patterns.md`, verify it displays SE guide. Run with guide from another division, verify it displays with warning.

**Acceptance Scenarios from Spec**:
1. Project with `division: SE` → SE guides appear first in search results
2. `specify guides show backend-patterns.md` in SE project displays `SE/backend-patterns.md`
3. Guide not in division → searches other divisions with note about different division
4. `/guides` command returns division-filtered results

### Implementation for User Story 3

- [ ] T039 [P] [US3] Implement find_guide(name: str, division: str, guides_path: Path) -> Optional[tuple[Path, str]] in src/specify_cli/config.py
- [ ] T040 [P] [US3] Implement list_guides(division: str, guides_path: Path) -> dict[str, list[Path]] in src/specify_cli/config.py
- [ ] T041 [US3] Add `guides` command group to CLI in src/specify_cli/__init__.py with Typer app
- [ ] T042 [US3] Implement `specify guides show <guide-path>` command in src/specify_cli/__init__.py that calls find_guide()
- [ ] T043 [US3] Add Rich Markdown rendering for guide content display in `guides show` command in src/specify_cli/__init__.py
- [ ] T044 [US3] Add division badge display (showing which division the guide is from) in `guides show` command in src/specify_cli/__init__.py
- [ ] T045 [US3] Add warning message when guide found in different division in `guides show` command in src/specify_cli/__init__.py
- [ ] T046 [US3] Implement `specify guides list` command showing all guides organized by division in src/specify_cli/__init__.py
- [ ] T047 [US3] Write unit tests in tests/unit/test_division_config.py for find_guide (division priority, Common fallback, other divisions)
- [ ] T048 [US3] Write unit tests in tests/unit/test_division_config.py for list_guides (organization by priority)
- [ ] T049 [US3] Write integration test in tests/integration/test_guides_division.py for `specify guides show` with guide in project division
- [ ] T050 [US3] Write integration test in tests/integration/test_guides_division.py for `specify guides show` with guide in different division (warning shown)
- [ ] T051 [US3] Write integration test in tests/integration/test_guides_division.py for `specify guides show` with non-existent guide (error message)
- [ ] T052 [US3] Write integration test in tests/integration/test_guides_division.py for `specify guides list` verifying division priority

**Checkpoint**: User Story 3 complete - developers can discover and view guides with division-aware prioritization

---

## Phase 6: User Story 4 - Division-Specific Prompts and Instructions (Priority: P2)

**Goal**: Update AI command templates to include division-aware instructions that guide AI agents to prioritize division-specific patterns

**Independent Test**: Examine `/specify`, `/plan`, `/tasks` template files and verify they contain division placeholders. Generate agent context and verify division instructions are inserted.

**Acceptance Scenarios from Spec**:
1. `/specify` prompt instructs AI to reference SE-specific patterns for SE projects
2. `/plan` prompt directs AI to prioritize DS methodologies for DS projects
3. `/tasks` prompt requires all guide references come from Platform division for Platform projects
4. Guide references from other divisions are flagged as warnings

### Implementation for User Story 4

- [ ] T053 [P] [US4] Add "## Project Division Context" section to templates/commands/specify.md with {DIVISION} placeholder
- [ ] T054 [P] [US4] Add division-aware instructions to templates/commands/specify.md directing AI to prioritize `context/references/{DIVISION}/` guides
- [ ] T055 [P] [US4] Add "## Project Division Context" section to templates/commands/plan.md with {DIVISION} placeholder
- [ ] T056 [P] [US4] Add division-aware instructions to templates/commands/plan.md directing AI to prioritize division-specific methodologies
- [ ] T057 [P] [US4] Add "## Project Division Context" section to templates/commands/tasks.md with {DIVISION} placeholder
- [ ] T058 [P] [US4] Add strict requirement to templates/commands/tasks.md that all guide references must be from {DIVISION} directory
- [ ] T059 [P] [US4] Add enforcement language to templates/commands/tasks.md flagging references to other divisions as violations
- [ ] T060 [US4] Update scripts/bash/update-agent-context.sh to replace {DIVISION} placeholder with actual division from project config
- [ ] T061 [US4] Update scripts/powershell/update-agent-context.ps1 to replace {DIVISION} placeholder with actual division from project config
- [ ] T062 [US4] Write integration test in tests/integration/test_context_division.py verifying {DIVISION} placeholder replaced in agent context files
- [ ] T063 [US4] Write integration test in tests/integration/test_context_division.py verifying division instructions present in all three command templates

**Checkpoint**: User Story 4 complete - AI command templates are division-aware and enforce division-specific guide references

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, documentation, and edge case handling

- [ ] T064 [P] Update README.md with division-aware workflow documentation and examples
- [ ] T065 [P] Update CHANGELOG.md with v0.5.0 Division-Aware Workflow feature entry
- [ ] T066 [P] Create migration guide in docs/ for existing projects to add division configuration
- [ ] T067 Write edge case test in tests/integration/test_edge_cases.py for missing `context/references/` directory
- [ ] T068 Write edge case test in tests/integration/test_edge_cases.py for division directory with no guide files
- [ ] T069 Write edge case test in tests/integration/test_edge_cases.py for concurrent access to .specify/project.json
- [ ] T070 Write edge case test in tests/integration/test_edge_cases.py for permission errors creating project.json
- [ ] T071 Update `specify check` command in src/specify_cli/__init__.py to detect missing .specify/project.json and suggest fix
- [ ] T072 Add performance benchmarking test in tests/integration/ verifying guide display <2s for 100+ guides
- [ ] T073 Add logging for division operations (validation failures, defaults applied) in src/specify_cli/config.py
- [ ] T074 Run quickstart.md validation by following all examples in specs/002-division-aware-workflow/quickstart.md
- [ ] T075 [P] Code cleanup and refactoring for division-related functions
- [ ] T076 Update pyproject.toml version to 0.5.0 and add feature description

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - creates test fixtures
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3, P1)**: Depends on Foundational (config module) - Can start immediately after Phase 2
- **User Story 2 (Phase 4, P1)**: Depends on Foundational (config module) - Can start immediately after Phase 2, parallel with US1
- **User Story 3 (Phase 5, P2)**: Depends on Foundational (config module) - Can start immediately after Phase 2, parallel with US1/US2
- **User Story 4 (Phase 6, P2)**: Depends on User Story 2 (context scripts) - Must wait for US2 bash/PowerShell updates
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - only needs config module (Phase 2)
- **User Story 2 (P1)**: Independent - only needs config module (Phase 2), can run parallel with US1
- **User Story 3 (P2)**: Independent - only needs config module (Phase 2), can run parallel with US1/US2
- **User Story 4 (P2)**: Depends on User Story 2 - needs context script updates to replace placeholders

### Within Each User Story

- **US1**: CLI changes (T016-T020) before integration tests (T021-T024)
- **US2**: Common function additions (T025-T034) before script updates (T028-T029, T033-T034) before tests (T035-T038)
- **US3**: Config functions (T039-T040) before CLI commands (T041-T046) before tests (T047-T052)
- **US4**: Template updates (T053-T059) before script updates (T060-T061) before tests (T062-T063)

### Parallel Opportunities

**Phase 1 (Setup)**: All test fixture creation tasks (T002-T005) can run in parallel

**Phase 2 (Foundational)**: Unit tests (T012-T015) can run in parallel after implementation (T007-T011)

**Phase 3 (US1)**: Integration tests (T021-T024) can run in parallel after CLI implementation (T016-T020)

**Phase 4 (US2)**: 
- Bash functions (T025-T027) parallel with PowerShell functions (T030-T032)
- Bash script updates (T028-T029) parallel with PowerShell script updates (T033-T034)
- Integration tests (T035-T038) can run in parallel

**Phase 5 (US3)**:
- Config functions (T039-T040) can run in parallel
- CLI commands (T041-T046) can run in parallel after config functions
- Unit tests (T047-T048) can run in parallel
- Integration tests (T049-T052) can run in parallel

**Phase 6 (US4)**:
- All template updates (T053-T059) can run in parallel
- Bash script update (T060) parallel with PowerShell script update (T061)
- Integration tests (T062-T063) can run in parallel

**Phase 7 (Polish)**:
- Documentation tasks (T064-T066) can run in parallel
- Edge case tests (T067-T070) can run in parallel

---

## Parallel Example: User Story 2

```bash
# Bash and PowerShell work can happen in parallel:
Developer A: T025-T029 (Bash script updates)
Developer B: T030-T034 (PowerShell script updates)

# Within bash work:
T025, T026, T027 can be developed in parallel (different functions in common.sh)

# Within PowerShell work:
T030, T031, T032 can be developed in parallel (different functions in common.ps1)

# All integration tests can run in parallel:
T035, T036, T037, T038 (different test files/scenarios)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only - Both P1)

1. **Complete Phase 1**: Setup (test fixtures) - ~1 hour
2. **Complete Phase 2**: Foundational (config module + unit tests) - ~4 hours
3. **Complete Phase 3**: User Story 1 (init command + integration tests) - ~3 hours
4. **Complete Phase 4**: User Story 2 (context scripts + integration tests) - ~4 hours
5. **STOP and VALIDATE**: Test US1 + US2 together - projects can be initialized with divisions, AI gets division-aware context
6. **Deploy/demo if ready**: Core division-aware workflow is functional

**MVP Delivers**:
- ✅ Initialize projects with division selection
- ✅ AI agents receive division-prioritized guides
- ✅ Backward compatibility (defaults to SE)
- ✅ Context scripts work on Linux/macOS/WSL2

### Full Feature (Add User Stories 3 & 4)

1. Continue from MVP
2. **Complete Phase 5**: User Story 3 (guide discovery CLI) - ~4 hours
3. **Complete Phase 6**: User Story 4 (template updates) - ~2 hours (depends on US2)
4. **Complete Phase 7**: Polish (docs, edge cases, benchmarks) - ~3 hours
5. **Total**: ~21 hours for complete feature

### Parallel Team Strategy

With 2 developers after Foundational phase:

**Sprint 1 (MVP)**:
- Developer A: User Story 1 (Phase 3) - 3 hours
- Developer B: User Story 2 bash (T025-T029) - 2 hours
- Developer B: User Story 2 PowerShell (T030-T034) - 2 hours
- Developer B: User Story 2 tests (T035-T038) - 1 hour
- **Result**: MVP complete in ~3 hours (parallel)

**Sprint 2 (Full Feature)**:
- Developer A: User Story 3 (Phase 5) - 4 hours
- Developer B: User Story 4 (Phase 6) - 2 hours, then helps with US3
- Both: Polish (Phase 7) - 3 hours
- **Result**: Full feature in ~7 hours (parallel)

**Total with 2 devs**: ~10 hours (vs 21 hours sequential)

---

## Success Criteria Mapping

Each user story maps to success criteria from spec.md:

**User Story 1** → SC-001, SC-006:
- ✅ SC-001: Division correctly stored in .specify/project.json
- ✅ SC-006: Error handling provides clear messages (90%+ target)

**User Story 2** → SC-002, SC-007:
- ✅ SC-002: AI receives division-specific guidance (100% consistency)
- ✅ SC-007: All AI command templates updated with division instructions

**User Story 3** → SC-003, SC-004:
- ✅ SC-003: Guide search filtered by division (95%+ in top 50%)
- ✅ SC-004: Guide display <2s response time (95th percentile)

**User Story 4** → SC-008:
- ✅ SC-008: /tasks enforces 100% guide references from division

**All Stories** → SC-005, SC-009, SC-010:
- ✅ SC-005: Division can be changed after initialization
- ✅ SC-009: Teams report improved alignment (80%+ satisfaction)
- ✅ SC-010: Documentation includes clear instructions

---

## Notes

- All tasks follow TDD approach where applicable (tests before implementation)
- [P] tasks can run in parallel (different files, no dependencies within phase)
- [Story] labels enable tracking which user story each task serves
- Each user story is independently testable and deliverable
- Config module (Phase 2) is foundational - blocks all user stories
- User Story 4 depends on User Story 2 (needs context script updates)
- User Stories 1, 2, 3 can run in parallel after Phase 2
- Commit after each task or logical group
- Validate each user story independently before moving to next priority
- MVP = US1 + US2 (both P1) delivers core division-aware workflow
- Full feature = All 4 user stories delivers complete vision
