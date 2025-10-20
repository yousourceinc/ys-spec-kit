# Tasks: Hardcode Implementation Guides Repository URL

**Input**: Design documents from `/specs/001-hardcode-guides-url/`
**Prerequisites**: plan.md ✅, spec.md ✅, quickstart.md ✅

**Tests**: Tests are REQUIRED per Constitution Principle II (Test-Driven Implementation). Implementation already exists; tests will be added retroactively.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/specify_cli/`, `tests/` at repository root
- This is a CLI tool - all paths relative to repository root

---

## Phase 1: Setup (Test Infrastructure)

**Purpose**: Create test directory structure and fixtures for testing guides integration

- [ ] T001 Create test directory structure: `tests/unit/`, `tests/integration/`, `tests/fixtures/`
- [ ] T002 [P] Create mock guides repository fixture in `tests/fixtures/mock_guides_repo/`
- [ ] T003 [P] Set up pytest configuration in `pyproject.toml` or `pytest.ini`
- [ ] T004 [P] Create test helper utilities for git repository operations in `tests/conftest.py`

**Checkpoint**: Test infrastructure ready for writing tests

---

## Phase 2: Foundational (No Blocking Prerequisites)

**Purpose**: N/A - This feature has no foundational blocking tasks. Implementation is a modification to existing code.

**Note**: Since the implementation already exists in `src/specify_cli/__init__.py`, we proceed directly to adding tests and documentation for each user story.

---

## Phase 3: User Story 1 Testing ✅ COMPLETE

**Status**: All 30 tasks completed - User Story 1 MVP fully tested and verified!

**Summary**: Created comprehensive test suite (23 core tests + 7 verification tasks) covering unit, integration, and edge cases. Fixed critical bug in implementation (absolute vs relative paths). All tests passing. User Story 1 ready for MVP validation.

---

## Phase 4: User Story 2 - Testing/CI Pipeline Overrides Guides URL (Priority: P2) ✅ COMPLETE

**Status**: All 12 tasks completed - Environment variable override mechanism fully tested and documented!

**Summary**: Created comprehensive tests for SPECIFY_GUIDES_REPO_URL override functionality. Verified implementation logic and updated all documentation. User Story 2 ready for production use.

### Tests for User Story 2 (REQUIRED - TDD Retroactive)

#### Unit Tests (tests/unit/test_guides_integration.py)

- [x] T035 [P] [US2] Test environment variable override takes precedence over constant in `tests/unit/test_guides_integration.py`
- [x] T036 [P] [US2] Test fallback to hardcoded constant when env var is not set in `tests/unit/test_guides_integration.py`
- [x] T037 [P] [US2] Test empty string environment variable falls back to constant in `tests/unit/test_guides_integration.py`
- [x] T038 [P] [US2] Test whitespace-only environment variable falls back to constant in `tests/unit/test_guides_integration.py`

#### Integration Tests (tests/integration/test_environment_override.py)

- [x] T039 [P] [US2] Test `specify init` with `SPECIFY_GUIDES_REPO_URL` set uses override URL in `tests/integration/test_environment_override.py`
- [x] T040 [P] [US2] Test `specify init` with invalid override URL shows clear error in `tests/integration/test_environment_override.py`
- [x] T041 [P] [US2] Test `specify init` with empty override env var falls back to hardcoded URL in `tests/integration/test_environment_override.py`

### Implementation Verification for User Story 2

**NOTE**: Code already exists - verify it matches specification

- [x] T042 [US2] Verify environment variable check logic: `os.getenv("SPECIFY_GUIDES_REPO_URL", "").strip() or GUIDES_REPO_URL` in `src/specify_cli/__init__.py`
- [x] T043 [US2] Verify override mechanism is documented in code comments in `src/specify_cli/__init__.py`

### Documentation for User Story 2

- [x] T044 [P] [US2] Add `SPECIFY_GUIDES_REPO_URL` to Environment Variables table in `README.md`
- [x] T045 [P] [US2] Document override usage in `docs/TEAM_INSTALLATION.md`
- [x] T046 [P] [US2] Add CI/CD override examples to `quickstart.md` (already exists, verify completeness)

**Checkpoint**: User Story 2 tested and documented - Override mechanism validated!

---

## Phase 5: User Story 3 - Developer Updates Guides in Existing Project (Priority: P3)

**Goal**: Maintain `specify guides update` command to allow developers to update guides to latest version

**Independent Test**: Initialize project, manually edit guides, run `specify guides update`, verify restoration to latest

**Implementation Status**: ✅ Code exists (no changes needed from previous implementation)

### Tests for User Story 3 (REQUIRED - TDD Retroactive)

#### Integration Tests (tests/integration/test_guides_update.py)

- [ ] T047 [P] [US3] Test `specify guides update` updates submodule to latest commit in `tests/integration/test_guides_update.py`
- [ ] T048 [P] [US3] Test `specify guides update` shows changes and prompts for commit in `tests/integration/test_guides_update.py`
- [ ] T049 [P] [US3] Test `specify guides update` shows "already up to date" when no changes in `tests/integration/test_guides_update.py`
- [ ] T050 [P] [US3] Test `specify guides update` fails gracefully when no guides present in `tests/integration/test_guides_update.py`
- [ ] T051 [P] [US3] Test `specify guides update` fails gracefully when not in git repository in `tests/integration/test_guides_update.py`
- [ ] T052 [P] [US3] Test `specify guides update` handles directory exists but not submodule error in `tests/integration/test_guides_update.py`

### Implementation Verification for User Story 3

**NOTE**: Code already exists from previous implementation - verify it still works

- [ ] T053 [US3] Verify `guides update` command exists and is accessible via CLI in `src/specify_cli/__init__.py`
- [ ] T054 [US3] Verify `update_guides()` function uses `git submodule update --remote --merge` in `src/specify_cli/__init__.py`
- [ ] T055 [US3] Verify error handling for missing guides directory in `src/specify_cli/__init__.py`
- [ ] T056 [US3] Verify error handling for non-git repository in `src/specify_cli/__init__.py`

### Documentation for User Story 3

- [ ] T057 [P] [US3] Add `specify guides update` to Commands table in `README.md`
- [ ] T058 [P] [US3] Document update workflow in `docs/TEAM_INSTALLATION.md`
- [ ] T059 [P] [US3] Update `specify guides --help` text with current functionality

**Checkpoint**: User Story 3 tested and documented - Guides update verified!

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation, version management, and release preparation

### Documentation Updates

- [ ] T060 [P] Update `CHANGELOG.md` with v0.4.0 release notes
- [ ] T061 [P] Verify `GUIDES_IMPLEMENTATION_COMPLETE.md` is accurate
- [ ] T062 [P] Update `NEXTSTEPS.md` to mark v0.4.0 as complete
- [ ] T063 [P] Review and finalize `quickstart.md` completeness
- [ ] T064 [P] Add implementation notes to `AGENTS.md` if needed

### Version Management

- [ ] T065 Verify version bump to 0.4.0 in `pyproject.toml`
- [ ] T066 Verify version bump to 0.4.0 in `package.json`
- [ ] T067 Verify all version references are consistent across files

### Testing & Validation

- [ ] T068 Run all unit tests: `pytest tests/unit/ -v`
- [ ] T069 Run all integration tests: `pytest tests/integration/ -v`
- [ ] T070 Run all tests with coverage: `pytest --cov=src/specify_cli tests/`
- [ ] T071 Verify test coverage meets minimum threshold (>80%)
- [ ] T072 Run manual smoke test: `specify init /tmp/test-project --ai claude`
- [ ] T073 Verify guides cloned correctly: `ls /tmp/test-project/context/references/`
- [ ] T074 Test override mechanism: `SPECIFY_GUIDES_REPO_URL=<test-url> specify init /tmp/test-override`

### Code Quality

- [ ] T075 [P] Run linter: `ruff check src/specify_cli/`
- [ ] T076 [P] Run formatter: `ruff format src/specify_cli/`
- [ ] T077 [P] Check for type errors: `mypy src/specify_cli/` (if applicable)
- [ ] T078 Review all error messages for clarity and actionability

### CI/CD & Release

- [ ] T079 Ensure all CI checks pass on branch
- [ ] T080 Create pull request from `001-hardcode-guides-url` to `main`
- [ ] T081 Request code review from team
- [ ] T082 Merge approved PR to `main`
- [ ] T083 Tag release: `git tag v0.4.0`
- [ ] T084 Push tag: `git push origin v0.4.0`
- [ ] T085 Publish to npm: `npm publish`
- [ ] T086 Update pip package distribution

### Communication

- [ ] T087 Announce release to team with upgrade instructions
- [ ] T088 Update internal documentation/wiki if applicable

**Final Checkpoint**: All tests pass, documentation complete, ready for production deployment!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: N/A for this feature
- **User Stories (Phase 3-5)**: Can proceed independently (implementation exists)
  - Tests can be written in parallel across all three stories
  - Verification tasks should follow test completion
  - Documentation can be updated in parallel
- **Polish (Phase 6)**: Depends on all user stories being tested and verified

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - core functionality
- **User Story 2 (P2)**: Depends on US1 conceptually but tests can run in parallel
- **User Story 3 (P3)**: Independent of US1 and US2 - can be tested in parallel

### Within Each User Story

- **Tests**: All tests marked [P] can run in parallel
- **Verification**: Sequential (verify code after tests are written)
- **Documentation**: All docs marked [P] can run in parallel

### Parallel Opportunities

#### Phase 1: Setup
All 4 setup tasks (T001-T004) can run in parallel

#### Phase 3: User Story 1 Tests
All unit tests (T005-T012) can run in parallel
All integration tests (T013-T017) can run in parallel
All edge case tests (T018-T023) can run in parallel

#### Phase 4: User Story 2 Tests
All unit tests (T035-T038) can run in parallel
All integration tests (T039-T041) can run in parallel

#### Phase 5: User Story 3 Tests
All integration tests (T047-T052) can run in parallel

#### Phase 6: Polish
Documentation (T060-T064) can run in parallel
Testing validation (T068-T074) should run sequentially
Code quality (T075-T078) can run in parallel

---

## Parallel Example: User Story 1 Unit Tests

```bash
# Launch all unit tests for User Story 1 together:
pytest tests/unit/test_guides_integration.py::test_clone_guides_with_valid_url &
pytest tests/unit/test_guides_integration.py::test_clone_guides_with_invalid_url &
pytest tests/unit/test_guides_integration.py::test_clone_guides_directory_exists_as_submodule &
pytest tests/unit/test_guides_integration.py::test_clone_guides_directory_exists_not_submodule &
pytest tests/unit/test_guides_integration.py::test_clone_guides_timeout_add &
pytest tests/unit/test_guides_integration.py::test_clone_guides_timeout_update &
pytest tests/unit/test_guides_integration.py::test_clone_guides_network_error &
pytest tests/unit/test_guides_integration.py::test_clone_guides_already_exists_handled &
wait
```

---

## Implementation Strategy

### Retroactive TDD Approach (Implementation Exists)

1. **Phase 1**: Setup test infrastructure (T001-T004)
2. **Phase 3**: Write all User Story 1 tests (T005-T034)
   - Tests should pass immediately (implementation exists)
   - If tests fail, fix implementation to match specification
3. **Phase 4**: Write all User Story 2 tests (T035-T046)
4. **Phase 5**: Write all User Story 3 tests (T047-T059)
5. **Phase 6**: Polish and release (T060-T088)

### MVP Validation (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1 tests and verification
3. **STOP and VALIDATE**: All US1 tests pass
4. Document US1 and prepare for demo
5. Optionally deploy/demo just US1 functionality

### Incremental Delivery

1. US1 tested → MVP ready → Demo/Deploy
2. US2 tested → Override capability validated → Demo/Deploy
3. US3 tested → Update command verified → Demo/Deploy
4. Polish → Production release v0.4.0

### Parallel Team Strategy

With multiple developers:

1. **Developer A**: Write US1 tests (T005-T034)
2. **Developer B**: Write US2 tests (T035-T046)
3. **Developer C**: Write US3 tests (T047-T059)
4. **All together**: Polish phase (T060-T088)

---

## Overall Progress: 46/88 tasks completed (52.3%)

### Phase Status Summary:
- **Phase 1**: Test Infrastructure Setup ✅ COMPLETE (4/4 tasks)
- **Phase 2**: Implementation ✅ COMPLETE (0/0 tasks - code already existed)
- **Phase 3**: User Story 1 Testing ✅ COMPLETE (30/30 tasks)
- **Phase 4**: User Story 2 Testing ✅ COMPLETE (12/12 tasks)
- **Phase 5**: User Story 3 Testing 🔄 PENDING (13/13 tasks)
- **Phase 6**: Polish & Release 🔄 PENDING (29/29 tasks)

### MVP Status: User Stories 1 & 2 Complete ✅
Both core features (automatic guides integration + environment variable override) are fully implemented, tested, and ready for validation. All unit and integration tests passing.

---

## Task Summary

**Total Tasks**: 88
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 0 tasks (N/A)
- Phase 3 (US1): 30 tasks (19 tests + 8 verification + 3 docs)
- Phase 4 (US2): 12 tasks (7 tests + 2 verification + 3 docs)
- Phase 5 (US3): 13 tasks (6 tests + 4 verification + 3 docs)
- Phase 6 (Polish): 29 tasks

**Parallel Opportunities**: 58 tasks marked [P] (66%)

**Test Tasks**: 32 tests (36%)
- Unit tests: 12
- Integration tests: 14
- Edge case tests: 6

**Implementation Note**: Code already exists in `feat/hardcode-guides-url` branch. This task list focuses on adding comprehensive tests retroactively per Constitution Principle II (Test-Driven Implementation), verifying implementation matches specification, and completing documentation for v0.4.0 release.

**MVP Scope**: Phase 1 + Phase 3 (User Story 1) = 34 tasks

**Recommended Execution**: Phases 3-5 (all tests) can run in parallel, then converge on Phase 6 (polish) for final release.
