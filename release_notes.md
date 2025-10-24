# Spec Kit Templates v0.4.3

## 🎯 What's Changed

### Prompt File Naming Standardization
- **Removed `speckit.*` prefix** from all GitHub Copilot prompt files
- All prompt files now use clean, non-prefixed naming convention:
  - `analyze.prompt.md` (was `speckit.analyze.prompt.md`)
  - `clarify.prompt.md` (was `speckit.clarify.prompt.md`)
  - `implement.prompt.md` (was `speckit.implement.prompt.md`)
  - `plan.prompt.md` (was `speckit.plan.prompt.md`)
  - `specify.prompt.md` (was `speckit.specify.prompt.md`)
  - `tasks.prompt.md` (was `speckit.tasks.prompt.md`)

### Bug Fixes
- Fixed guides repository URL to use correct organization: `yousourcephinc/ys-requirements-list`
- Fixed template download source to use correct repository: `yousourcephinc/ys-spec-kit`

### Governance Commands
All templates now include the full governance layer commands:
- `audit.prompt.md` - Audit governance compliance
- `waive.prompt.md` - Request governance waivers
- `waivers.prompt.md` - View active waivers

## 📦 Template Packages

This release includes templates for all supported AI agents:
- GitHub Copilot
- Claude Code
- Gemini CLI
- Cursor
- Qwen Code
- opencode
- Windsurf
- Codex
- Kilocode
- Auggie (Augment Code)
- Roo Code
- Amazon Q Developer CLI

Each agent has both **bash** (sh) and **PowerShell** (ps) variants.

## 🚀 Installation

```bash
# Initialize a new project with clean prompt naming
specify init my-project --ai copilot

# Or use the --here flag in an existing project
cd my-project
specify init --here --ai copilot
```

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.
