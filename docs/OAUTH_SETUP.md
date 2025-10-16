# GitHub OAuth Setup for Specify CLI

This guide explains how to set up GitHub OAuth authentication for your forked Specify CLI.

## Prerequisites

- GitHub organization account
- Admin access to your GitHub organization
- Node.js 16+ installed

## Step 1: Create GitHub OAuth App

1. **Navigate to OAuth Apps settings**
   - Go to: `https://github.com/organizations/YOUR-ORG/settings/applications`
   - Or: Your Organization → Settings → Developer settings → OAuth Apps

2. **Click "New OAuth App"**

3. **Configure the application**:
   ```
   Application name: YourOrg Specify CLI
   Homepage URL: https://github.com/your-org/ys-spec-kit
   Application description: OAuth authentication for Specify CLI
   Authorization callback URL: http://localhost:8888/callback
   ```

4. **Enable Device Flow**:
   - Check the box: "Enable Device Flow"
   - This allows authentication in SSH/headless environments

5. **Create the app**

6. **Note your credentials**:
   - **Client ID**: `Iv1.xxxxxxxxxxxxx` (visible)
   - **Client Secret**: Click "Generate a new client secret" and save it securely

## Step 2: Configure Environment Variables

Team members need to configure these environment variables:

### Option 1: Set in Shell Profile (Recommended)

Add to `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
# GitHub OAuth for Specify CLI
export SPECIFY_GITHUB_CLIENT_ID="Iv1.xxxxxxxxxxxxx"
export SPECIFY_GITHUB_CLIENT_SECRET="your_client_secret_here"
export SPECIFY_GITHUB_ORG="your-org"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: Set Per-Session

```bash
export SPECIFY_GITHUB_CLIENT_ID="Iv1.xxxxxxxxxxxxx"
export SPECIFY_GITHUB_CLIENT_SECRET="your_client_secret_here"
export SPECIFY_GITHUB_ORG="your-org"
```

### Option 3: Environment File

Create `.env` file in your project:

```bash
SPECIFY_GITHUB_CLIENT_ID=Iv1.xxxxxxxxxxxxx
SPECIFY_GITHUB_CLIENT_SECRET=your_client_secret_here
SPECIFY_GITHUB_ORG=your-org
```

Load with:
```bash
export $(cat .env | xargs)
```

**⚠️ Security Warning**: Never commit `.env` files with secrets to git!

## Step 3: Distribute to Team

### Option A: Secure Credential Sharing

1. **Store credentials in team password manager** (1Password, LastPass, etc.)
   - Store Client ID and Client Secret
   - Share with authorized team members only

2. **Provide setup instructions** to team:
   ```bash
   # Add to your shell profile
   export SPECIFY_GITHUB_CLIENT_ID="<from password manager>"
   export SPECIFY_GITHUB_CLIENT_SECRET="<from password manager>"
   export SPECIFY_GITHUB_ORG="your-org"
   ```

### Option B: Internal Documentation

Create internal wiki/docs with:
- OAuth app details
- Environment variable setup instructions
- Troubleshooting guide

## Step 4: Install Specify CLI

Team members can install via npm:

```bash
# Install globally
npm install -g @your-org/specify-cli

# Or use via npx (no installation)
npx @your-org/specify-cli init my-project
```

## Step 5: Test Authentication

Test the OAuth setup:

```bash
# Test authentication
node src/auth/github-oauth.js test

# Should output:
# 🔐 Authenticating with GitHub...
# Using browser flow
# Opening browser for authentication...
# ✅ Authentication successful!
```

## Authentication Flows

### Browser Flow (Default)

For local development with GUI:

1. Run any specify command: `specify init my-project`
2. Browser opens automatically to GitHub OAuth page
3. Click "Authorize [your-org]"
4. Redirected back to success page
5. Terminal continues with command

**Ports Used**: `localhost:8888` (configurable via `SPECIFY_OAUTH_PORT`)

### Device Flow (SSH/Headless)

For remote servers or SSH sessions:

```bash
# Force device flow
SPECIFY_DEVICE_FLOW=true specify init my-project

# Shows:
# Please visit: https://github.com/login/device
# Enter code: WDJB-MJHT
```

Visit the URL on any device and enter the code.

## Security Best Practices

### For Administrators

1. **Rotate secrets regularly**
   - Regenerate client secret every 90 days
   - Update team documentation

2. **Monitor OAuth app usage**
   - Review authorized users in GitHub settings
   - Revoke access for departed team members

3. **Use organization-wide OAuth app**
   - Ensures automatic access control
   - Centralizes audit logs

4. **Limit OAuth permissions**
   - Only request `read:org` and `read:user`
   - Never request write access

### For Team Members

1. **Protect your environment variables**
   - Don't commit `.env` files
   - Use secure storage (password managers)
   - Don't share secrets in chat/email

2. **Logout when done**
   ```bash
   specify logout
   ```

3. **Token storage location**
   - Tokens saved to: `~/.specify/oauth_token.json`
   - File permissions: `600` (owner read/write only)

## Troubleshooting

### "OAuth not configured" Error

**Problem**: Missing environment variables

**Solution**:
```bash
# Verify variables are set
echo $SPECIFY_GITHUB_CLIENT_ID
echo $SPECIFY_GITHUB_CLIENT_SECRET
echo $SPECIFY_GITHUB_ORG

# If empty, add to shell profile and reload
```

### "Not a member of required organization" Error

**Problem**: User not in GitHub organization

**Solution**:
1. Verify membership: `https://github.com/orgs/your-org/people`
2. Ensure membership is "Public" or OAuth app has org access
3. Contact GitHub admin to add user

### "Port 8888 already in use" Error

**Problem**: Another service using OAuth callback port

**Solution**:
```bash
# Use custom port
SPECIFY_OAUTH_PORT=9999 specify init my-project
```

### "Browser didn't open" Error

**Problem**: No default browser or headless environment

**Solution**:
1. Copy the URL from terminal output
2. Open in any browser manually
3. Or use device flow: `SPECIFY_DEVICE_FLOW=true specify init`

### "Authentication timeout" Error

**Problem**: OAuth flow took too long (5 minute limit)

**Solution**:
1. Complete authorization faster
2. Check network connectivity
3. Try device flow if browser issues

## Advanced Configuration

### Custom Callback URL

For corporate firewalls or proxies:

```bash
# Use custom port
export SPECIFY_OAUTH_PORT=3000

# OAuth app callback URL must match
# http://localhost:3000/callback
```

### Bypass Authentication (Development Only)

For testing without OAuth:

```bash
# Skip OAuth (only for help/version commands)
specify --help
specify --version
```

### Multiple Organizations

If working with multiple orgs:

```bash
# Project A
export SPECIFY_GITHUB_ORG="org-a"
cd project-a && specify init

# Project B  
export SPECIFY_GITHUB_ORG="org-b"
cd project-b && specify init
```

## Support

- **Documentation**: https://github.com/your-org/ys-spec-kit/wiki
- **Issues**: https://github.com/your-org/ys-spec-kit/issues
- **OAuth Setup**: https://github.com/your-org/ys-spec-kit/blob/main/docs/OAUTH_SETUP.md

## Reference

- [GitHub OAuth Apps Documentation](https://docs.github.com/en/apps/oauth-apps)
- [GitHub OAuth Device Flow](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#device-flow)
- [Specify CLI README](../README.md)
