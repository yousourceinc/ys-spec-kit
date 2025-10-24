# Documentation

This folder contains the documentation source files for ys-spec-kit, built using [DocFX](https://dotnet.github.io/docfx/).

## 📚 Quick Navigation

### For First-Time Users
- [index.md](./index.md) - Main documentation homepage
- [quickstart.md](./quickstart.md) - Quick start guide (5 minutes)
- [guides/governance-quickstart.md](./guides/governance-quickstart.md) - Hands-on governance intro

### For Developers
- [installation.md](./installation.md) - Installation guide
- [guides/governance-overview.md](./guides/governance-overview.md) - Comprehensive architecture
- [guides/compliance-checking.md](./guides/compliance-checking.md) - Compliance verification
- [guides/waiver-management.md](./guides/waiver-management.md) - Recording exceptions
- [guides/rule-authoring.md](./guides/rule-authoring.md) - Creating custom rules

### For Contributors
- [local-development.md](./local-development.md) - Development setup
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines

### For Troubleshooting
- [troubleshooting/common-issues.md](./troubleshooting/common-issues.md) - Common problems
- [troubleshooting/faq.md](./troubleshooting/faq.md) - Frequently asked questions

## 📁 Directory Structure

```
docs/
├── README.md (this file)              # Documentation overview
├── docfx.json                         # DocFX configuration
├── index.md                           # Main homepage
├── toc.yml                            # Table of contents
├── installation.md                    # Installation guide
├── quickstart.md                      # Quick start (5 min)
├── local-development.md               # Development setup
├── guides/                            # Feature guides
│   ├── governance-overview.md         # Architecture & concepts
│   ├── governance-quickstart.md       # 5-minute intro with examples
│   ├── compliance-checking.md         # Deep dive: verification
│   ├── waiver-management.md           # Deep dive: exceptions
│   └── rule-authoring.md              # Deep dive: custom rules
├── api/                               # Technical APIs (coming soon)
│   ├── cli-reference.md               # CLI commands
│   ├── governance-api.md              # API reference
│   └── rule-engine-api.md             # Rule engine API
├── troubleshooting/                   # Troubleshooting
│   ├── common-issues.md               # Known issues & solutions
│   └── faq.md                         # FAQ
└── _site/                             # Generated docs (ignored by git)
```

## Building Locally

To build the documentation locally:

1. Install DocFX:
   ```bash
   dotnet tool install -g docfx
   ```

2. Build the documentation:
   ```bash
   cd docs
   docfx docfx.json --serve
   ```

3. Open your browser to `http://localhost:8080` to view the documentation.

## Documentation Sections

### Guides (`guides/`)
In-depth guides for all governance features and workflows.

| Guide | Purpose | Time |
|-------|---------|------|
| [governance-quickstart.md](./guides/governance-quickstart.md) | Get started with hands-on examples | 5 min |
| [governance-overview.md](./guides/governance-overview.md) | Complete architecture and concepts | 20 min |
| [compliance-checking.md](./guides/compliance-checking.md) | Verify project compliance | 15 min |
| [waiver-management.md](./guides/waiver-management.md) | Record exceptions and waivers | 10 min |
| [rule-authoring.md](./guides/rule-authoring.md) | Create custom compliance rules | 20 min |

### API Reference (`api/`)
Technical API documentation for programmatic integration.

| Reference | Content |
|-----------|---------|
| [cli-reference.md](./api/cli-reference.md) | Command-line interface documentation |
| [governance-api.md](./api/governance-api.md) | Governance module API (WaiverManager, ComplianceChecker) |
| [rule-engine-api.md](./api/rule-engine-api.md) | Rule engine API (RuleEngine, RuleParser) |

### Troubleshooting (`troubleshooting/`)
Solutions for common issues and frequently asked questions.

| Resource | Focus |
|----------|-------|
| [common-issues.md](./troubleshooting/common-issues.md) | Problems and solutions |
| [faq.md](./troubleshooting/faq.md) | Frequently asked questions |

## Learning Paths

### Path 1: Quick Understanding (15 minutes)
1. [Main README](../README.md) - Project overview (5 min)
2. [quickstart.md](./quickstart.md) - Getting started (10 min)

### Path 2: Governance Deep Dive (1-2 hours)
1. [governance-overview.md](./guides/governance-overview.md) - Architecture (30 min)
2. [governance-quickstart.md](./guides/governance-quickstart.md) - Hands-on intro (15 min)
3. [compliance-checking.md](./guides/compliance-checking.md) - Verification (20 min)
4. [waiver-management.md](./guides/waiver-management.md) - Exceptions (15 min)
5. [rule-authoring.md](./guides/rule-authoring.md) - Custom rules (20 min)

### Path 3: Developer Setup (2-3 hours)
1. [installation.md](./installation.md) - Install ys-spec-kit (15 min)
2. [local-development.md](./local-development.md) - Development setup (30 min)
3. [api/cli-reference.md](./api/cli-reference.md) - CLI commands (20 min)
4. [api/governance-api.md](./api/governance-api.md) - Programmatic access (30 min)

### Path 4: Troubleshooting (30 minutes)
1. [troubleshooting/common-issues.md](./troubleshooting/common-issues.md) - Known problems (15 min)
2. [troubleshooting/faq.md](./troubleshooting/faq.md) - Common questions (10 min)

## Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/docs.yml`.

The DocFX configuration is in `docfx.json` and the table of contents is in `toc.yml`.

## Contributing to Documentation

Found an issue or want to improve the docs?

1. Edit the markdown files in this directory
2. Build locally to preview: `docfx docfx.json --serve`
3. Submit a pull request with your improvements

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

**Last Updated**: 2025-10-22  
**Status**: Complete with guides and API references  
**Maintained By**: The ys-spec-kit Team
