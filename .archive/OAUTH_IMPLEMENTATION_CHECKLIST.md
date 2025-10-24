# OAuth Implementation Checklist

## ✅ Implementation Complete

All code has been implemented. Now you need to configure GitHub OAuth.

## Your Next Steps

### 1. Create GitHub OAuth App (5 minutes)

1. Go to your GitHub organization settings:
   - URL: `https://github.com/organizations/YOUR-ORG/settings/applications`
   - Or: Your Org → Settings → Developer settings → OAuth Apps

2. Click "New OAuth App"

3. Fill in the form:
   ```
   Application name: YourOrg Specify CLI
   Homepage URL: https://github.com/your-org/ys-spec-kit
   Application description: OAuth authentication for Specify CLI
   Authorization callback URL: http://localhost:8888/callback
   ```

4. Check "Enable Device Flow"

5. Click "Register application"

6. **Save these credentials securely**:
   - Client ID: `Iv1.xxxxxxxxxxxxx`
   - Client Secret: Click "Generate a new client secret" and copy it

### 2. Test Locally (2 minutes)

```bash
# Navigate to your repo
cd /Users/reytianero/code/ys-spec-kit

# Install Node.js dependencies
npm install

# Set environment variables (replace with your values)
export SPECIFY_GITHUB_CLIENT_ID="Iv1.xxxxxxxxxxxxx"
export SPECIFY_GITHUB_CLIENT_SECRET="your_client_secret_here"
export SPECIFY_GITHUB_ORG="your-org"

# Test OAuth authentication
node src/auth/github-oauth.js test

# Should open browser and authenticate
```

### 3. Test Full Flow (2 minutes)

```bash
# Make bin/specify.js executable
chmod +x bin/specify.js

# Test specify command
./bin/specify.js init test-project --ai claude

# Should:
# 1. Authenticate via OAuth (browser opens)
# 2. Create project structure
# 3. Success!
```

### 4. Publish to npm (3 minutes)

```bash
# Update package.json with your org name
# Change @your-org/specify-cli to @YOUR-ACTUAL-ORG/specify-cli

# Login to npm
npm login

# Publish (or use GitHub Packages)
npm publish --access public
```

### 5. Team Distribution

Share with your team:

1. **OAuth Credentials** (via password manager):
   - Client ID
   - Client Secret
   - Organization name

2. **Installation Instructions**:
   ```bash
   npm install -g @your-org/specify-cli
   ```

3. **Documentation**:
   - [docs/OAUTH_SETUP.md](docs/OAUTH_SETUP.md)
   - [docs/TEAM_INSTALLATION.md](docs/TEAM_INSTALLATION.md)

## Files Created/Modified

### New Files
- ✅ `src/auth/github-oauth.js` - OAuth authentication module
- ✅ `bin/specify.js` - Node.js wrapper
- ✅ `package.json` - npm package configuration
- ✅ `scripts/install-python-cli.js` - Post-install script
- ✅ `docs/OAUTH_SETUP.md` - OAuth setup guide
- ✅ `docs/TEAM_INSTALLATION.md` - Team installation guide
- ✅ `NPM_README.md` - npm package README

### Modified Files
- ✅ `src/specify_cli/__init__.py` - Added `logout()` command
- ✅ `pyproject.toml` - Version bumped to 0.3.0
- ✅ `CHANGELOG.md` - Added 0.3.0 release notes

## How It Works

### For Team Members

1. **Install**: `npm install -g @your-org/specify-cli`
2. **Configure**: Set OAuth environment variables
3. **Run**: `specify init my-project`
4. **Authenticate**: Browser opens → Click "Authorize" → Done!
5. **Token saved**: `~/.specify/oauth_token.json` (persists)

### Authentication Flows

**Browser Flow (Default)**:
- Works on local machines with GUI
- Automatic browser-based OAuth
- One-click authorization

**Device Flow (SSH/Headless)**:
```bash
SPECIFY_DEVICE_FLOW=true specify init my-project
# Shows code to enter on GitHub
```

### Security Features

- ✅ OAuth with minimal permissions (read:org, read:user)
- ✅ CSRF protection via state parameter
- ✅ Secure token storage (file permissions 600)
- ✅ Organization membership verification
- ✅ Local callback server (localhost only)
- ✅ No token data sent to external servers

## Testing Checklist

Before distributing to team:

- [ ] OAuth app created on GitHub
- [ ] Browser flow works (opens browser, authenticates)
- [ ] Device flow works (shows code, accepts authorization)
- [ ] Organization membership verified
- [ ] Token persists across sessions
- [ ] Logout command works
- [ ] npm package published
- [ ] Documentation complete

## Troubleshooting

### "OAuth not configured"
```bash
# Set environment variables
export SPECIFY_GITHUB_CLIENT_ID="..."
export SPECIFY_GITHUB_CLIENT_SECRET="..."
export SPECIFY_GITHUB_ORG="..."
```

### "Module not found: @octokit/rest"
```bash
# Install dependencies
npm install
```

### "Port 8888 already in use"
```bash
# Use different port
SPECIFY_OAUTH_PORT=9999 specify init my-project
```

## Support

- Documentation: `docs/` folder
- Issues: GitHub Issues
- Questions: Create discussion on GitHub

## Summary

You now have:
- ✅ OAuth authentication (browser + device flow)
- ✅ npm distribution via package.json
- ✅ Organization access control
- ✅ Secure token management
- ✅ Complete documentation
- ✅ Version 0.3.0 released per AGENTS.md

**Next**: Set up GitHub OAuth app and test!
