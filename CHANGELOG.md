# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2025-10-21

### Added

- **Governance Layer Phase 7 - Polish & Optimization**
  - **Comprehensive Logging**: Added logging module to all governance operations (waiver creation, compliance checking, rule evaluation)
    - `src/specify_cli/governance/logging_config.py` for centralized setup
    - Structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR)
  - **Performance Metrics**: New metrics module for tracking and reporting performance
    - `src/specify_cli/governance/metrics.py` with RuleMetrics and ComplianceCheckMetrics classes
    - Tracks rule evaluation times, total check duration, and per-rule performance
    - Global metrics collector for aggregating performance data
  - **Guide Discovery Caching**: Optimized for large codebases
    - `src/specify_cli/governance/caching.py` with GuideCacheManager
    - MD5-based project hash for cache validation
    - 1-hour cache expiry with automatic invalidation on project changes
    - Significantly reduces guide discovery time on subsequent checks
  - **Configuration Management**: Updated .gitignore for governance layer
    - Added `compliance-report.md` (ephemeral, not committed)
    - Added `.specify/.cache/` for cache files (not committed)
    - Preserved `.specify/waivers.md` (version-controlled)

### Changed

- **Version Updates**: Updated to v0.4.1 (pyproject.toml, package.json)
- **README.md**: Added comprehensive Governance Layer section with CLI commands and examples
- **ComplianceChecker**: Added optional caching support (enabled by default, can be disabled with `use_cache=False`)

### Technical Details

- **Test Coverage**: Added 34 new tests (19 metrics + 15 caching) for 210 total tests (100% pass rate)
- **Performance**: Compliance checks now include performance metrics reporting
- **Logging**: All governance operations properly logged with contextual information
- **Cache Strategy**: Intelligent cache invalidation based on file timestamps and project structure changes

## [0.4.0] - 2025-10-20

### Added

- **Implementation Guides Integration**: Automatic integration of centrally-defined implementation guides
  - `SPECIFY_GUIDES_REPO_URL` environment variable for system-level guides configuration
  - Guides automatically cloned as git submodule into `context/references/` during `specify init`
  - Robust error handling for invalid or inaccessible guide repositories
- **Guides Management Command**: New `specify guides` CLI command
  - `specify guides update`: Update guides to latest version using `git submodule update --remote`
  - Foundation for future `search` and `show` subcommands
- **Documentation Updates**: Updated README, quickstart, and team installation guides with guides management instructions

### Changed

- Modified `specify init` to check for `SPECIFY_GUIDES_REPO_URL` and clone guides as submodule if set
- Enhanced project initialization flow with guides integration step

### Notes

- Guide repository configuration (add/remove) is handled at binary level, not exposed to developers
- Developers can only update, search (planned), and show (planned) guides
- Guides integration requires git to be available and initialized

## [0.3.4] - 2025-10-17

### Changed

- **CLI branding**: Updated ASCII banner to include "YS" (Yousource) branding
- **Tagline**: Changed to "Yousource Spec Kit - Spec-Driven Development Toolkit"

## [0.3.3] - 2025-10-16

### Fixed

- **Post-install script**: Corrected git repository URL in install-python-cli.js
- **Python CLI installation**: Now properly installs from yousourceinc/ys-spec-kit repository

## [0.3.2] - 2025-10-16

### Changed

- **npm registry**: Explicitly configured publishConfig for public npm registry
- **Package configuration**: Updated repository URL to yousourceinc organization
- **Version**: Bumped to 0.3.2 for npm publication fixes

### Fixed

- **npm publication**: Fixed registry configuration to properly publish to registry.npmjs.org
- **Package metadata**: Corrected repository URL and author information

## [0.3.0] - 2025-10-16

### Added

- **GitHub OAuth authentication**: Browser-based and device flow OAuth for team access control
- **Organization membership verification**: Automatic verification that users are members of authorized GitHub organization
- **npm distribution**: Package now available via npm/npx for easier team distribution
- **Node.js wrapper**: JavaScript wrapper around Python CLI that handles OAuth authentication
- **Logout command**: New `specify logout` command to clear OAuth authentication
- **Secure token storage**: OAuth tokens stored securely in `~/.specify/oauth_token.json` with restrictive file permissions (600)
- **Dual authentication flows**: 
  - Browser flow (default) - automatic browser-based OAuth for GUI environments
  - Device flow - manual code entry for SSH/headless environments
- **Environment detection**: Automatically selects appropriate OAuth flow based on environment

### Changed

- **Authentication method**: OAuth flow instead of manual token creation for better security and UX
- **Distribution method**: Now available via npm in addition to pip
- **Version**: Bumped to 0.3.0 per AGENTS.md requirements for changes to `__init__.py`

### Security

- OAuth tokens have minimal permissions (read:org, read:user only)
- CSRF protection via state parameter in OAuth flow
- Local callback server for OAuth (localhost only, port 8888)
- Token files created with restrictive permissions (600)
- No token data sent to external servers (stays on user's machine)

## [LATEST_VERSION] - RELEASE_DATE

### Added

- Support for using `.` as a shorthand for current directory in `specify init .` command, equivalent to `--here` flag but more intuitive for users

## [0.0.17] - 2025-09-22

### Added

- New `/clarify` command template to surface up to 5 targeted clarification questions for an existing spec and persist answers into a Clarifications section in the spec.
- New `/analyze` command template providing a non-destructive cross-artifact discrepancy and alignment report (spec, clarifications, plan, tasks, constitution) inserted after `/tasks` and before `/implement`.
	- Note: Constitution rules are explicitly treated as non-negotiable; any conflict is a CRITICAL finding requiring artifact remediation, not weakening of principles.

## [0.0.16] - 2025-09-22

### Added

- `--force` flag for `init` command to bypass confirmation when using `--here` in a non-empty directory and proceed with merging/overwriting files.

## [0.0.15] - 2025-09-21

### Added

- Support for Roo Code.

## [0.0.14] - 2025-09-21

### Changed

- Error messages are now shown consistently.

## [0.0.13] - 2025-09-21

### Added

- Support for Kilo Code. Thank you [@shahrukhkhan489](https://github.com/shahrukhkhan489) with [#394](https://github.com/github/spec-kit/pull/394).
- Support for Auggie CLI. Thank you [@hungthai1401](https://github.com/hungthai1401) with [#137](https://github.com/github/spec-kit/pull/137).
- Agent folder security notice displayed after project provisioning completion, warning users that some agents may store credentials or auth tokens in their agent folders and recommending adding relevant folders to `.gitignore` to prevent accidental credential leakage.

### Changed

- Warning displayed to ensure that folks are aware that they might need to add their agent folder to `.gitignore`.
- Cleaned up the `check` command output.

## [0.0.12] - 2025-09-21

### Changed

- Added additional context for OpenAI Codex users - they need to set an additional environment variable, as described in [#417](https://github.com/github/spec-kit/issues/417).

## [0.0.11] - 2025-09-20

### Added

- Codex CLI support (thank you [@honjo-hiroaki-gtt](https://github.com/honjo-hiroaki-gtt) for the contribution in [#14](https://github.com/github/spec-kit/pull/14))
- Codex-aware context update tooling (Bash and PowerShell) so feature plans refresh `AGENTS.md` alongside existing assistants without manual edits.

## [0.0.10] - 2025-09-20

### Fixed

- Addressed [#378](https://github.com/github/spec-kit/issues/378) where a GitHub token may be attached to the request when it was empty.

## [0.0.9] - 2025-09-19

### Changed

- Improved agent selector UI with cyan highlighting for agent keys and gray parentheses for full names

## [0.0.8] - 2025-09-19

### Added

- Windsurf IDE support as additional AI assistant option (thank you [@raedkit](https://github.com/raedkit) for the work in [#151](https://github.com/github/spec-kit/pull/151))
- GitHub token support for API requests to handle corporate environments and rate limiting (contributed by [@zryfish](https://github.com/@zryfish) in [#243](https://github.com/github/spec-kit/pull/243))

### Changed

- Updated README with Windsurf examples and GitHub token usage
- Enhanced release workflow to include Windsurf templates

## [0.0.7] - 2025-09-18

### Changed

- Updated command instructions in the CLI.
- Cleaned up the code to not render agent-specific information when it's generic.


## [0.0.6] - 2025-09-17

### Added

- opencode support as additional AI assistant option

## [0.0.5] - 2025-09-17

### Added

- Qwen Code support as additional AI assistant option

## [0.0.4] - 2025-09-14

### Added

- SOCKS proxy support for corporate environments via `httpx[socks]` dependency

### Fixed

N/A

### Changed

N/A
