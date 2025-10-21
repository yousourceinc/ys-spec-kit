# Tasks: Governance Layer with Automated Compliance Checking and Waiver Process

**Input**: Design documents from `/specs/003-governance-compliance-layer/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions
- Repository root: `/Users/reytianero/code/ys-spec-kit/`
- Source: `src/specify_cli/`
- Tests: `tests/`
- Templates: `.specify/templates/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and governance module structure

- [x] T001 Create governance module directory structure at src/specify_cli/governance/
- [x] T002 Create governance submodule __init__.py files (governance/, governance/rules/)
- [x] T003 [P] Add PyYAML dependency to pyproject.toml (if not present)
- [x] T004 [P] Create test directory structure: tests/unit/governance/, tests/integration/governance/, tests/fixtures/governance/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core rule engine infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement BaseRule abstract class in src/specify_cli/governance/rules/__init__.py
- [x] T006 [P] Implement FileExistsRule class in src/specify_cli/governance/rules/file_rules.py
- [x] T007 [P] Implement DependencyPresentRule class in src/specify_cli/governance/rules/dependency_rules.py
- [x] T008 [P] Implement TextIncludesRule class in src/specify_cli/governance/rules/text_rules.py
- [x] T009 Implement RuleEngine class with rule registration and evaluation in src/specify_cli/governance/rules/engine.py
- [x] T010 Implement RuleParser class for YAML frontmatter extraction in src/specify_cli/governance/rules/parser.py
- [x] T011 Create unit tests for BaseRule in tests/unit/governance/test_base_rule.py
- [x] T012 [P] Create unit tests for FileExistsRule in tests/unit/governance/test_file_rules.py
- [x] T013 [P] Create unit tests for DependencyPresentRule in tests/unit/governance/test_dependency_rules.py
- [x] T014 [P] Create unit tests for TextIncludesRule in tests/unit/governance/test_text_rules.py
- [x] T015 Create unit tests for RuleEngine in tests/unit/governance/test_rule_engine.py
- [x] T016 Create unit tests for RuleParser in tests/unit/governance/test_rule_parser.py
- [x] T017 [P] Create test fixture: sample implementation guide with YAML rules in tests/fixtures/governance/sample_guide.md
- [x] T018 [P] Create test fixture: sample project structure for compliance testing in tests/fixtures/governance/sample_project/

**Checkpoint**: Rule engine foundation complete - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Engineer Creates and Records Compliance Waivers (Priority: P1) 🎯 MVP

**Goal**: Enable engineers to formally record compliance exceptions with reason and timestamp in version-controlled .specify/waivers.md file

**Independent Test**: Execute `/waive-requirement "Test waiver reason"` and verify that .specify/waivers.md is created/appended with structured entry including reason, timestamp, and unique ID

### Implementation for User Story 1

- [x] T019 [US1] Implement WaiverManager class with create_waiver() method in src/specify_cli/governance/waiver.py
- [x] T020 [US1] Implement generate_waiver_id() to auto-increment W-XXX format in src/specify_cli/governance/waiver.py
- [x] T021 [US1] Implement format_waiver_entry() for markdown structure in src/specify_cli/governance/waiver.py
- [x] T022 [US1] Implement append_to_waivers_file() with file creation if needed in src/specify_cli/governance/waiver.py
- [x] T023 [US1] Implement parse_waivers_file() to read existing waivers in src/specify_cli/governance/waiver.py
- [x] T024 [US1] Add waive_requirement CLI command to src/specify_cli/__init__.py using Typer
- [x] T025 [US1] Implement command handler for /waive-requirement with reason validation in src/specify_cli/__init__.py
- [x] T026 [US1] Add Rich formatting for success/error messages in waive_requirement command
- [x] T027 [US1] Add validation for empty/missing reason with clear error message
- [x] T028 [US1] Create unit tests for WaiverManager in tests/unit/governance/test_waiver_manager.py
- [x] T029 [US1] Create integration test for waive_requirement command in tests/integration/governance/test_waive_requirement_command.py
- [x] T030 [US1] Test waiver file creation when .specify/waivers.md doesn't exist
- [x] T031 [US1] Test waiver appending when .specify/waivers.md already exists
- [x] T032 [US1] Test waiver ID auto-increment (W-001, W-002, W-003)
- [x] T033 [US1] Test ISO-8601 timestamp format validation
- [x] T034 [US1] Test error handling for empty reason
- [x] T035 [US1] Add help text and examples for /waive-requirement command

**Checkpoint**: Engineers can now record waivers with `/waive-requirement "reason"` - MVP feature complete

---

## Phase 4: User Story 2 - Developer Checks Code Compliance Against Guides (Priority: P1)

**Goal**: Enable developers to verify code against machine-readable rules from implementation guides, generating compliance reports with pass/fail/waived status

**Independent Test**: Execute `/check-compliance` after implementing a feature with known compliance points and verify that a compliance-report.md is generated with accurate pass/fail/waived status for each rule

### Implementation for User Story 2

- [x] T036 [US2] Implement GuideDiscovery class to parse plan.md/tasks.md for guide references in src/specify_cli/governance/discovery.py
- [x] T037 [US2] Implement find_guide_files() to locate guides in context/references/ in src/specify_cli/governance/discovery.py
- [x] T038 [US2] Implement ComplianceChecker class with run_compliance_check() in src/specify_cli/governance/compliance.py
- [x] T039 [US2] Implement evaluate_rules_with_waivers() to cross-reference waivers in src/specify_cli/governance/compliance.py
- [x] T040 [US2] Implement RuleEvaluationResult data class in src/specify_cli/governance/compliance.py
- [x] T041 [US2] Integrate RuleEngine with ComplianceChecker for rule evaluation
- [x] T042 [US2] Integrate RuleParser to extract rules from discovered guides
- [x] T043 [US2] Integrate WaiverManager to load and match waivers to failed rules
- [x] T044 [US2] Implement waiver matching logic: rule_id → waiver_id lookup
- [x] T045 [US2] Implement status determination: pass/fail/waived/error
- [x] T046 [US2] Implement ComplianceReportGenerator class in src/specify_cli/governance/report.py
- [x] T047 [US2] Implement generate_report_header() with timestamp and status in src/specify_cli/governance/report.py
- [x] T048 [US2] Implement generate_summary_section() with pass/fail/waive counts in src/specify_cli/governance/report.py
- [x] T049 [US2] Implement generate_checked_guides_section() in src/specify_cli/governance/report.py
- [x] T050 [US2] Implement generate_passed_rules_section() in src/specify_cli/governance/report.py
- [x] T051 [US2] Implement generate_failed_rules_section() with recommendations in src/specify_cli/governance/report.py
- [x] T052 [US2] Implement generate_waived_rules_section() with waiver references in src/specify_cli/governance/report.py
- [x] T053 [US2] Implement generate_error_rules_section() (optional) in src/specify_cli/governance/report.py
- [x] T054 [US2] Implement write_report_to_file() to generate compliance-report.md in src/specify_cli/governance/report.py
- [x] T055 [US2] Add check_compliance CLI command to src/specify_cli/__init__.py using Typer
- [x] T056 [US2] Implement command handler for /check-compliance in src/specify_cli/__init__.py
- [x] T057 [US2] Add Rich formatting for compliance check progress and results
- [x] T058 [US2] Add error handling for missing plan.md/tasks.md
- [x] T059 [US2] Add error handling for no guides found
- [x] T060 [US2] Add error handling for invalid rule syntax in guides
- [x] T061 [US2] Create unit tests for GuideDiscovery in tests/unit/governance/test_guide_discovery.py
- [x] T062 [US2] Create unit tests for ComplianceChecker in tests/unit/governance/test_compliance_checker.py
- [x] T063 [US2] Create unit tests for ComplianceReportGenerator in tests/unit/governance/test_report_generator.py
- [x] T064 [US2] Create integration test for check_compliance command in tests/integration/governance/test_check_compliance_command.py
- [x] T065 [US2] Test guide discovery from plan.md references
- [x] T066 [US2] Test rule extraction from YAML frontmatter
- [x] T067 [US2] Test rule evaluation: file_exists checks
- [x] T068 [US2] Test rule evaluation: dependency_present checks
- [x] T069 [US2] Test rule evaluation: text_includes checks
- [x] T070 [US2] Test waiver matching: failed rule + waiver = "Waived" status
- [x] T071 [US2] Test report generation: all sections present
- [x] T072 [US2] Test report generation: accurate pass/fail/waive counts
- [x] T073 [US2] Test error handling: guide not found
- [x] T074 [US2] Test error handling: invalid YAML in guide
- [x] T075 [US2] Test error handling: missing plan.md
- [x] T076 [US2] Add help text and examples for /check-compliance command

**Checkpoint**: Developers can now run `/check-compliance` to verify code against guides - Core compliance enforcement complete

---

## Phase 5: User Story 3 - Team Lead Reviews Governance Audit Trail (Priority: P2)

**Goal**: Enable team leads to review all recorded waivers with reasons and timestamps, cross-referencing with compliance reports for governance oversight

**Independent Test**: Review .specify/waivers.md structure and format to confirm it contains complete audit trail information (reason, timestamp, clear entries) that enables governance review

### Implementation for User Story 3

- [x] T077 [US3] Enhance format_waiver_entry() to ensure chronological ordering in src/specify_cli/governance/waiver.py
- [x] T078 [US3] Implement list_waivers() method for programmatic access in src/specify_cli/governance/waiver.py
- [x] T079 [US3] Implement get_waiver_by_id() for lookup in src/specify_cli/governance/waiver.py
- [x] T080 [US3] Add optional waiver list command: /waivers list (displays all waivers)
- [x] T081 [US3] Add optional waiver show command: /waivers show W-XXX (displays specific waiver)
- [x] T082 [US3] Add Rich table formatting for waiver list display
- [x] T083 [US3] Enhance compliance report to include clickable waiver references
- [x] T084 [US3] Add waiver statistics to compliance report summary (total waivers, recent waivers)
- [x] T085 [US3] Create integration test for waivers list command in tests/integration/governance/test_waivers_command.py
- [x] T086 [US3] Test chronological ordering of waivers in .specify/waivers.md
- [x] T087 [US3] Test cross-reference between compliance-report.md and waivers.md
- [x] T088 [US3] Test waiver lookup by ID
- [x] T089 [US3] Add documentation for team lead governance review workflow

**Checkpoint**: Team leads can review governance audit trail via .specify/waivers.md and compliance reports


---

## Phase 6: User Story 4 - Enhancement: Guide Authors Embed Compliance Rules (Priority: P3)

**Goal**: Enable guide authors to define machine-readable compliance rules directly in guide YAML frontmatter, ensuring rules are automatically discovered and evaluated

**Independent Test**: Add machine-readable rules to a guide file and verify that `/check-compliance` discovers and evaluates those rules correctly

### Implementation for User Story 4

- [ ] T090 [US4] Enhance RuleParser to validate YAML frontmatter structure in src/specify_cli/governance/rules/parser.py
- [ ] T091 [US4] Implement validate_rule_structure() for each rule type in src/specify_cli/governance/rules/parser.py
- [ ] T092 [US4] Add comprehensive error messages for malformed rules (missing fields, invalid types)
- [ ] T093 [US4] Add rule syntax validation: check required fields per rule type
- [ ] T094 [US4] Implement rule linting: detect common mistakes (wrong field names, invalid paths)
- [ ] T095 [US4] Create guide authoring template with example rules in .specify/templates/guide-template.md
- [ ] T096 [US4] Add division field validation in YAML frontmatter
- [ ] T097 [US4] Test rule parsing: valid YAML with all rule types
- [ ] T098 [US4] Test rule parsing: malformed YAML (syntax errors)
- [ ] T099 [US4] Test rule parsing: missing required fields
- [ ] T100 [US4] Test rule parsing: invalid rule types
- [ ] T101 [US4] Test rule parsing: multiple rules in single guide
- [ ] T102 [US4] Create example implementation guide with embedded rules in tests/fixtures/governance/
- [ ] T103 [US4] Add documentation for guide authors: "How to Embed Compliance Rules"
- [ ] T104 [US4] Add rule authoring best practices documentation

**Checkpoint**: Guide authors can embed compliance rules in YAML frontmatter with validation and helpful error messages

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T105 [P] Add comprehensive logging for all governance operations (waiver creation, compliance checking, rule evaluation)
- [ ] T106 [P] Add performance metrics tracking: rule evaluation times, total check duration
- [ ] T107 [P] Optimize rule evaluation for large codebases (caching, parallel evaluation if needed)
- [ ] T108 [P] Add .gitignore entry for compliance-report.md (reports are ephemeral, not committed)
- [ ] T109 [P] Ensure .specify/waivers.md is NOT in .gitignore (waivers must be committed)
- [ ] T110 Add division-awareness: respect project division from .specify/project.json
- [ ] T111 Add guide prioritization: check division-specific guides first
- [ ] T112 [P] Update README.md with governance layer documentation
- [ ] T113 [P] Update CHANGELOG.md with v0.4.1 governance layer features
- [ ] T114 [P] Update pyproject.toml version: 0.4.0 → 0.4.1
- [ ] T115 [P] Update package.json version: 0.4.0 → 0.4.1
- [ ] T116 Create quickstart guide for governance layer in docs/governance-quickstart.md
- [ ] T117 Add CLI help text improvements for all governance commands
- [ ] T118 Add example guides with embedded rules to templates/
- [ ] T119 [P] Code cleanup: remove debug prints, add docstrings
- [ ] T120 [P] Refactor: extract common report formatting to helper functions
- [ ] T121 Run full test suite: pytest tests/
- [ ] T122 Validate against constitution principles (Spec-First, TDD, CLI Focus, etc.)
- [ ] T123 Performance validation: compliance check completes in <30 seconds
- [ ] T124 Edge case testing: missing files, corrupted waivers, invalid YAML
- [ ] T125 Security review: ensure waivers.md permissions are appropriate (mode 644)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1) can start after Foundational
  - User Story 2 (P1) can start after Foundational (requires User Story 1 complete for waiver integration)
  - User Story 3 (P2) can start after User Stories 1 & 2 complete (enhances existing features)
  - User Story 4 (P3) can start after Foundational (independent of other stories, enhances rule authoring)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories (waiver creation is standalone)
- **User Story 2 (P1)**: Depends on User Story 1 (needs waiver reading for waived rule status)
- **User Story 3 (P2)**: Depends on User Stories 1 & 2 (enhances waiver review and reporting)
- **User Story 4 (P3)**: Can start after Foundational - Independent (focuses on guide authoring, not runtime features)

### Within Each User Story

**User Story 1 (Waivers)**:
1. WaiverManager class implementation (T019-T023)
2. CLI command integration (T024-T027)
3. Unit tests (T028)
4. Integration tests (T029-T034)
5. Documentation (T035)

**User Story 2 (Compliance Checking)**:
1. Discovery and evaluation components (T036-T045) - can run in parallel
2. Report generation (T046-T054)
3. CLI command integration (T055-T060)
4. Unit tests (T061-T063) - can run in parallel
5. Integration tests (T064-T076)

**User Story 3 (Audit Trail)**:
1. Waiver listing enhancements (T077-T084)
2. Integration tests (T085-T088)
3. Documentation (T089)

**User Story 4 (Rule Authoring)**:
1. Parser validation enhancements (T090-T094)
2. Templates and documentation (T095-T096)
3. Tests (T097-T102)
4. Documentation (T103-T104)

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks marked [P] can run in parallel
- T003 (PyYAML dependency)
- T004 (Test directories)

**Phase 2 (Foundational)**: 
- Rule class implementations (T006, T007, T008) can run in parallel
- Rule unit tests (T012, T013, T014) can run in parallel
- Test fixtures (T017, T018) can run in parallel

**Phase 3 (User Story 1)**: All tasks sequential (small, focused implementation)

**Phase 4 (User Story 2)**:
- Discovery, evaluation, report components can be developed in parallel (T036-T054)
- Unit tests (T061, T062, T063) can run in parallel

**Phase 7 (Polish)**: Most documentation and cleanup tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch rule implementations in parallel:
Developer A: "Implement FileExistsRule in src/specify_cli/governance/rules/file_rules.py"
Developer B: "Implement DependencyPresentRule in src/specify_cli/governance/rules/dependency_rules.py"
Developer C: "Implement TextIncludesRule in src/specify_cli/governance/rules/text_rules.py"

# Launch unit tests in parallel (after implementations complete):
Developer A: "Create unit tests for FileExistsRule in tests/unit/governance/test_file_rules.py"
Developer B: "Create unit tests for DependencyPresentRule in tests/unit/governance/test_dependency_rules.py"
Developer C: "Create unit tests for TextIncludesRule in tests/unit/governance/test_text_rules.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Waiver creation) → Test independently
4. Complete Phase 4: User Story 2 (Compliance checking) → Test independently
5. **STOP and VALIDATE**: Test waiver + compliance workflow end-to-end
6. Deploy/demo v0.4.1-rc1

### Incremental Delivery

1. Setup + Foundational → Foundation ready (rule engine works)
2. Add User Story 1 → Test independently → MVP waiver feature (can record exceptions)
3. Add User Story 2 → Test independently → MVP compliance checking (can verify code)
4. **RELEASE v0.4.1**: Core governance features complete
5. Add User Story 3 → Enhance audit trail review
6. Add User Story 4 → Enhance guide authoring experience
7. **RELEASE v0.4.2**: Enhanced governance with better UX

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (critical path)
2. Once Foundational is done:
   - Developer A: User Story 1 (Waivers)
   - Developer B: User Story 4 (Rule authoring - independent)
3. After User Story 1 completes:
   - Developer A: User Story 2 (Compliance - needs waivers)
   - Developer B: Continues User Story 4
4. After User Stories 1 & 2 complete:
   - Developer A or B: User Story 3 (Audit trail enhancements)
5. Polish phase: All developers collaborate

---

## Performance Targets

From spec.md Success Criteria:

- **SC-001**: Waiver recording: <10 seconds → Target tasks: T019-T027
- **SC-002**: Compliance check: <30 seconds → Target tasks: T036-T060 (validate in T123)
- **File operations**: Use pathlib for cross-platform compatibility
- **Rule evaluation**: O(1) for file_exists, O(n) for dependency_present, O(m) for text_includes
- **Caching**: Consider caching parsed manifests during single check run (T107)

---

## Testing Strategy

### Unit Tests (20+ tests planned)

- BaseRule abstract class validation (T011)
- FileExistsRule: file present/absent (T012)
- DependencyPresentRule: package present/version matching (T013)
- TextIncludesRule: text found/not found, case sensitivity (T014)
- RuleEngine: rule registration, evaluation orchestration (T015)
- RuleParser: YAML extraction, validation (T016)
- WaiverManager: creation, parsing, ID generation (T028)
- GuideDiscovery: plan.md parsing, guide location (T061)
- ComplianceChecker: rule evaluation with waivers (T062)
- ComplianceReportGenerator: report sections, formatting (T063)

### Integration Tests (10+ tests planned)

- `/waive-requirement` command: file creation, appending (T029-T034)
- `/check-compliance` command: full workflow (T064-T076)
- `/waivers list` command (T085-T088)
- End-to-end governance workflow (T089)

### Edge Cases

From spec.md Edge Cases section:

- Missing .specify/waivers.md → Create on first waiver (T030)
- No guides referenced in plan.md → Clear error message (T059)
- Invalid rule syntax in guide → Skip rule, log error (T060, T098-T100)
- Corrupted waivers.md → Attempt to parse valid entries (T124)
- Waiver exists but rule removed → Waiver remains valid (T087)
- Multiple rules fail, no waivers → All marked "Failed" (T072)

---

## Constitution Compliance

### Principle I: Specification-First ✅
- Comprehensive spec.md with user stories → Complete
- All contracts defined → Complete (waivers, report, rule engine)
- Data model documented → Complete

### Principle II: Test-Driven Implementation ✅
- Unit tests planned for each component (T011-T016, T028, T061-T063)
- Integration tests for CLI commands (T029-T034, T064-T076, T085-T088)
- Edge case tests (T124)

### Principle III: CLI and Automation Focus ✅
- Two CLI commands: `/waive-requirement`, `/check-compliance`
- Text-based I/O: markdown files
- Structured output: compliance-report.md

### Principle IV: Integration and Contract Testing ✅
- Waivers file contract (waivers-schema.md)
- Compliance report contract (compliance-report-schema.md)
- Rule engine contract (rule-engine-api.md)
- Integration tests validate contracts (T064-T076)

### Principle V: Observability and Simplicity ✅
- Simple rule types: file_exists, dependency_present, text_includes
- Clear error messages (T027, T058-T060, T092)
- Structured logging (T105)

### Principle VI: Developer-Centric Experience ✅
- Intuitive commands: `/waive-requirement`, `/check-compliance`
- Help text and examples (T035, T076)
- Clear error messages guide users (T027, T092)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- Foundation (Phase 2) MUST complete before any user story work
- User Story 2 requires User Story 1 complete (waiver integration)
- Commit after each task or logical group
- Stop at each checkpoint to validate story independently
- Performance validation at T123: ensure <30 second compliance check
- Edge case testing at T124: validate all spec.md edge cases
