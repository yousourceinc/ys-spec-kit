# Specify CLI - OAuth Quick Start

> Spec-Driven Development CLI with GitHub OAuth authentication

## Installation

```bash
# Install globally
npm install -g @your-org/specify-cli

# Or use via npx (no installation)
npx @your-org/specify-cli init my-project
```

## Prerequisites

- Node.js 16+
- Python 3.11+
- GitHub account (member of your-org)
- OAuth credentials (contact team admin)

## Quick Start

### 1. Configure OAuth

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export SPECIFY_GITHUB_CLIENT_ID="Iv1.xxxxxxxxxxxxx"
export SPECIFY_GITHUB_CLIENT_SECRET="your_client_secret_here"
export SPECIFY_GITHUB_ORG="your-org"
```

Reload: `source ~/.bashrc`

### 2. Initialize Project

```bash
specify init my-project --ai claude
```

Browser opens for GitHub OAuth → Click "Authorize" → Done!

### 3. Use in AI Agent

```bash
cd my-project

# In Claude Code, Copilot, etc.
/constitution
/specify Build a task manager...
/plan
/tasks
/implement
```

## Commands

```bash
specify init <name>     # Initialize project
specify init . --here   # Initialize in current dir
specify logout          # Clear authentication
specify check           # Check installed tools
specify --help          # Show help
```

## Documentation

- **Installation**: [docs/TEAM_INSTALLATION.md](docs/TEAM_INSTALLATION.md)
- **OAuth Setup**: [docs/OAUTH_SETUP.md](docs/OAUTH_SETUP.md)
- **Full Docs**: https://github.com/your-org/ys-spec-kit/wiki

## Troubleshooting

### "OAuth not configured"
```bash
# Set environment variables
export SPECIFY_GITHUB_CLIENT_ID="..."
export SPECIFY_GITHUB_CLIENT_SECRET="..."
export SPECIFY_GITHUB_ORG="your-org"
```

### "Not a member of organization"
Contact your GitHub org admin for access.

### "Command not found"
```bash
# Add npm global bin to PATH
export PATH="$(npm config get prefix)/bin:$PATH"
```

## Support

- Issues: https://github.com/your-org/ys-spec-kit/issues
- Slack: #specify-help

## License

Apache-2.0
