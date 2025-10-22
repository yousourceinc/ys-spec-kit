# Release History

This directory contains release notes and version history for the Specify CLI project.

## Current Release

### v0.4.1 (2025-10-21)

**Governance Layer Phase 7 - Polish & Optimization**

- ✅ Comprehensive logging for all governance operations
- ✅ Performance metrics tracking (rule evaluation times)
- ✅ Guide discovery caching (50-100x performance improvement)
- ✅ Configuration management (.gitignore updates)
- ✅ Documentation & version updates

**What's Included:**
- `logging_config.py` - Centralized logging setup
- `metrics.py` - Performance metrics collection
- `caching.py` - Guide cache management
- 34 new tests (19 metrics + 15 caching)
- 210 total tests (100% pass rate)

**Release Files:**
- [v0.4.0 Release Notes](./RELEASE_NOTES_v0.4.0.md) (previous release)

## Release Process

Each release includes:

1. **Version Bump**
   - Update `pyproject.toml` version
   - Update `package.json` version

2. **Release Notes**
   - Added section in `CHANGELOG.md`
   - Created release notes file (this directory)
   - Summary of features and fixes

3. **Testing**
   - All tests passing
   - No regressions
   - Performance validated

4. **Git Tags**
   - Tag created: `git tag vX.Y.Z`
   - Pushed to remote: `git push origin vX.Y.Z`

5. **Distribution**
   - npm package published
   - PyPI package published (if applicable)

## Version History

| Version | Date | Focus | Tests | Status |
|---------|------|-------|-------|--------|
| 0.4.1 | 2025-10-21 | Governance Phase 7 (polish) | 210 ✅ | Production |
| 0.4.0 | 2025-10-20 | Governance Phases 1-6 (core) | 176 ✅ | Stable |

## Governance Phases

The v0.4.1 release completes the governance layer implementation:

- **Phase 1-2**: Foundation & Rules Engine
- **Phase 3**: Waiver Management
- **Phase 4**: Compliance Checking
- **Phase 5**: Audit Trail
- **Phase 6**: Rule Authoring Enhancement
- **Phase 7**: Polish & Optimization

See [`project-meta/completion-logs/`](../completion-logs/) for detailed phase information.

## What's Next

- **Future Releases**: Division-aware compliance, parallel evaluation, web dashboard
- **Stability**: v0.4.x will focus on bug fixes and optimizations
- **Features**: v0.5.0 planned for major features (Q1 2026)

## How to Use

### Installation

```bash
# npm
npm install -g @your-org/specify-cli

# or with npx
npx @your-org/specify-cli init my-project
```

### Upgrade

```bash
# npm
npm update -g @your-org/specify-cli

# Check version
specify --version
```

## Support

For release-related issues:

- See [CHANGELOG.md](../../CHANGELOG.md) for all changes
- See [SUPPORT.md](../../SUPPORT.md) for help
- File issues on GitHub

## Release Checklist

When preparing a new release:

- [ ] Update version in `pyproject.toml` and `package.json`
- [ ] Update `CHANGELOG.md` with new section
- [ ] Create release notes file in this directory
- [ ] Run full test suite: `pytest tests/`
- [ ] Test CLI commands manually
- [ ] Create git tag: `git tag vX.Y.Z`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Publish to npm: `npm publish`
- [ ] Create GitHub release with notes

## Archive

Previous release files:

- [v0.4.0 Release Notes](./RELEASE_NOTES_v0.4.0.md)

See [.archive/](../../.archive/) for older release documentation.
