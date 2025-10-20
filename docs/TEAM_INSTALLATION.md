# Team Installation Guide - Specify CLI with OAuth

Quick start guide for team members installing and using Specify CLI with GitHub OAuth authentication.

## Prerequisites

- ✅ Node.js 16+ and npm
- ✅ Python 3.11+
- ✅ Git
- ✅ GitHub account (member of your-org)
- ✅ Web browser (for OAuth)

## Installation

### Option 1: Global Install (Recommended)

```bash
# Install globally via npm
npm install -g @your-org/specify-cli

# Verify installation
specify --version
```

### Option 2: Use via npx (No Installation)

```bash
# Run directly without installing
npx @your-org/specify-cli init my-project
```

### Option 3: Development Install

```bash
# Clone the repository
git clone git@github.com:your-org/ys-spec-kit.git
cd ys-spec-kit

# Install dependencies
npm install

# Install Python CLI
npm run postinstall

# Link for development
npm link

# Verify
specify --version
```

## First-Time Setup

### 1. Get OAuth Credentials

Contact your team admin or check your team's password manager for:

- `SPECIFY_GITHUB_CLIENT_ID`
- `SPECIFY_GITHUB_CLIENT_SECRET`
- `SPECIFY_GITHUB_ORG`

### 2. Configure Environment

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
# GitHub OAuth for Specify CLI
export SPECIFY_GITHUB_CLIENT_ID="Iv1.xxxxxxxxxxxxx"
export SPECIFY_GITHUB_CLIENT_SECRET="your_client_secret_here"
export SPECIFY_GITHUB_ORG="your-org"
```

Reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

### 3. Verify Setup

```bash
# Check environment variables
echo $SPECIFY_GITHUB_CLIENT_ID
# Should output: Iv1.xxxxxxxxxxxxx

# Test authentication
specify init test-project
```

## First Run (One-Click Authentication)

When you run Specify for the first time:

```bash
$ specify init my-project --ai claude

Verifying GitHub authentication...

🔐 Authenticating with GitHub...
Using browser flow

Opening browser for authentication...
```

**What happens next**:

1. ✅ Browser opens automatically to GitHub
2. ✅ GitHub OAuth authorization page appears
3. ✅ You click "Authorize your-org"
4. ✅ Browser shows "Authentication Successful"
5. ✅ Terminal continues with project creation

```bash
✅ Authentication successful!

Creating project: my-project...
✓ Project structure created
✓ Agent commands generated
✓ Context files initialized

Done! Your project is ready.
```

**Token saved**: `~/.specify/oauth_token.json` (persists across sessions)

## Usage

### Initialize New Project

```bash
# Basic usage
specify init my-project --ai claude

# In current directory
specify init . --ai claude
```

**Note**: Implementation guides (if configured) are automatically available after initialization. Use `specify guides` commands to manage them.

### Logout

Clear your authentication:

```bash
specify logout
```

### Check Tools

Verify installed tools:

```bash
specify check
```

### Manage Guides

If implementation guides are configured for your project:

```bash
# Update guides to the latest version
specify guides update

# Search guides by keyword
specify guides search <keyword>

# Display a specific guide  
specify guides show <guide-path>
```

**Note**: Guide repository configuration is set at the binary level during project initialization. To add or change guides, contact your team administrator.

### Get Help

```bash
specify --help
specify init --help
```

## SSH / Headless Environments

If you're working via SSH or without a GUI:

```bash
# Use device flow (manual code entry)
SPECIFY_DEVICE_FLOW=true specify init my-project

# Output:
# Please visit: https://github.com/login/device
# Enter code: WDJB-MJHT
#
# Waiting for authorization...
```

Visit the URL on any device (even your phone) and enter the code.

## Workflow Example

Complete workflow from start to deployment:

```bash
# 1. Install Specify
npm install -g @your-org/specify-cli

# 2. Initialize project
specify init photo-organizer --ai claude

# 3. Open in your AI agent (Claude, Copilot, etc.)
cd photo-organizer
code .  # or cursor, etc.

# 4. Follow SDD workflow in AI agent
/constitution
/specify Build a photo organizer with upload, tagging, and search
/clarify
/plan Following our implementation guides
/tasks
/implement

# 5. Keep guides updated (if configured)
specify guides update

# 6. Commit and deploy
git add .
git commit -m "Initial implementation"
git push
```

## Troubleshooting

### "Command not found: specify"

**Problem**: npm global bin not in PATH

**Solution**:
```bash
# Check npm global bin location
npm config get prefix

# Add to PATH (in ~/.bashrc or ~/.zshrc)
export PATH="$(npm config get prefix)/bin:$PATH"

# Reload
source ~/.bashrc
```

### "OAuth not configured"

**Problem**: Missing environment variables

**Solution**:
```bash
# Verify variables are set
env | grep SPECIFY

# If missing, add to shell profile:
export SPECIFY_GITHUB_CLIENT_ID="..."
export SPECIFY_GITHUB_CLIENT_SECRET="..."
export SPECIFY_GITHUB_ORG="your-org"

# Reload
source ~/.bashrc
```

### "Not a member of required organization"

**Problem**: Not in GitHub organization

**Solution**:
1. Verify you're logged into correct GitHub account in browser
2. Check membership: `https://github.com/orgs/your-org/people`
3. Contact admin if you don't see yourself
4. Ensure org membership is "Public" or click "Make public"

### "Python 3.11+ required"

**Problem**: Python version too old

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.11+ from python.org
# Or use pyenv:
pyenv install 3.11
pyenv global 3.11
```

### "Browser didn't open"

**Problem**: No default browser configured

**Solution**:
1. Copy the URL shown in terminal
2. Paste into any browser manually
3. Complete authorization
4. Return to terminal

### "Port 8888 already in use"

**Problem**: Another app using OAuth port

**Solution**:
```bash
# Use different port
SPECIFY_OAUTH_PORT=9999 specify init my-project
```

### Authentication Issues

**Clear and retry**:
```bash
# Logout and re-authenticate
specify logout
specify init my-project  # Will prompt for auth again
```

## Tips & Best Practices

### Security

- ✅ **Never commit** OAuth secrets to git
- ✅ **Use password manager** for credentials
- ✅ **Logout** when switching machines
- ✅ **Review** authorized apps periodically

### Performance

- ✅ **Token persists**: Only authenticate once per machine
- ✅ **Use npx**: No installation needed for quick tasks
- ✅ **Global install**: Faster for frequent use

### Workflow

- ✅ **Start with constitution**: Define project principles
- ✅ **Use implementation guides**: Reference proven patterns
- ✅ **Check compliance**: Verify spec adherence
- ✅ **Iterate**: Refine specs before implementing

## Getting Help

- **Documentation**: https://github.com/your-org/ys-spec-kit/wiki
- **OAuth Setup**: https://github.com/your-org/ys-spec-kit/blob/main/docs/OAUTH_SETUP.md
- **Issues**: https://github.com/your-org/ys-spec-kit/issues
- **Slack**: #specify-help
- **Email**: devtools@your-org.com

## Quick Reference

```bash
# Installation
npm install -g @your-org/specify-cli

# Authentication
specify init <project>  # Prompts for auth if needed
specify logout          # Clear authentication

# Project Setup
specify init my-project --ai claude
specify init . --here --force

# Tools Check
specify check

# Help
specify --help
specify --version
```

## Next Steps

1. ✅ Install Specify CLI
2. ✅ Configure OAuth credentials
3. ✅ Authenticate with GitHub
4. ✅ Initialize your first project
5. ✅ Follow SDD workflow in AI agent
6. ✅ Check out implementation guides

Welcome to Spec-Driven Development! 🚀
