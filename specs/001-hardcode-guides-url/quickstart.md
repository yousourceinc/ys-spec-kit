# Quick Start: Hardcode Guides URL Feature

## For End Users (Developers)

### Basic Usage - No Configuration Required

The simplest use case - guides are automatically integrated:

```bash
# Install Specify CLI
npm install -g @yousourceinc/specify-cli

# Initialize a new project
specify init my-project --ai claude

# Guides are automatically available!
# Check the guides
ls my-project/context/references/
```

**What happened**:
- Guides repository was automatically cloned as a git submodule
- No environment variables needed
- No flags to remember
- Guides are ready to use immediately

### Update Guides

Keep your guides current:

```bash
cd my-project
specify guides update
```

**What this does**:
- Updates the guides submodule to the latest commit
- Shows what changed
- Prompts you to commit the update

### Common Workflows

#### 1. Start a New Feature

```bash
# Guides are already integrated
cd my-project

# Reference guides during development
/specify Build user authentication using guides/security/auth-patterns
```

#### 2. Share Project with Team

```bash
# Clone project
git clone <your-project-url>
cd your-project

# Initialize submodules (includes guides)
git submodule update --init --recursive

# Guides are now available
ls context/references/
```

#### 3. Keep Guides Updated

```bash
# Pull latest guides
specify guides update

# Review changes
git diff context/references

# Commit if satisfied
git add context/references
git commit -m "Update implementation guides"
git push
```

## For Testing/CI Environments

### Override Guides Repository

Use a different guides repository for testing:

```bash
# Set override environment variable
export SPECIFY_GUIDES_REPO_URL="git@github.com:test-org/test-guides.git"

# Initialize project with test guides
specify init test-project --ai claude

# Verify it used test repository
cd test-project
git submodule
```

### CI/CD Pipeline Example

```yaml
# .github/workflows/test.yml
name: Test with Staging Guides

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Specify CLI
        run: npm install -g @yousourceinc/specify-cli
      
      - name: Initialize with staging guides
        env:
          SPECIFY_GUIDES_REPO_URL: git@github.com:your-org/guides-staging.git
        run: specify init test-project --ai claude
      
      - name: Run tests
        run: |
          cd test-project
          npm test
```

## For Maintainers

### Update Hardcoded URL

To change the default guides repository:

```bash
# 1. Edit the constant in source code
vim src/specify_cli/__init__.py

# Find and update:
GUIDES_REPO_URL = "git@github.com:yousourceinc/implementation-guides.git"

# 2. Run tests
pytest tests/

# 3. Commit and release
git commit -am "Update guides repository URL"
git tag v0.4.1
git push origin main --tags

# 4. Publish
npm publish
```

### Test Changes Locally

```bash
# 1. Modify code
vim src/specify_cli/__init__.py

# 2. Install locally
pip install -e .

# 3. Test with temporary directory
specify init /tmp/test-project --ai claude

# 4. Verify guides
ls /tmp/test-project/context/references/

# 5. Cleanup
rm -rf /tmp/test-project
```

### Debug Guides Integration

Enable verbose logging:

```bash
# Run with Python directly to see all output
python -m specify_cli init test-project --ai claude

# Check git submodule status
cd test-project
git submodule status
git submodule foreach git log -1

# Manually update if needed
git submodule update --remote --merge context/references
```

## Troubleshooting

### Problem: Guides not cloning

**Symptoms**: `context/references/` directory is empty or missing

**Causes**:
1. No network connectivity
2. SSH keys not configured
3. No access to guides repository

**Solutions**:
```bash
# Check SSH access to GitHub
ssh -T git@github.com

# Check git configuration
git config --list | grep user

# Manually clone guides
cd your-project
git submodule add git@github.com:yousourceinc/implementation-guides.git context/references
git submodule update --init --recursive
```

### Problem: Permission denied during clone

**Symptoms**: Error message about SSH keys or permissions

**Solution**:
```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to https://github.com/settings/keys

# Test connection
ssh -T git@github.com
```

### Problem: Directory already exists error

**Symptoms**: `Directory context/references/ already exists but is not a submodule`

**Solution**:
```bash
# Backup if needed
mv context/references context/references.backup

# Initialize project again
specify init my-project --ai claude

# Or manually add submodule
cd my-project
git submodule add git@github.com:yousourceinc/implementation-guides.git context/references
```

### Problem: Guides update fails

**Symptoms**: `No implementation guides found in this project`

**Solution**:
```bash
# Check if guides exist
ls -la context/references/

# If missing, add manually
git submodule add git@github.com:yousourceinc/implementation-guides.git context/references
git submodule update --init --recursive

# If exists but not recognized
cd context/references
git remote -v  # Should show guides repository
cd ../..
git submodule update --init --recursive
```

## Performance Tips

### Large Guides Repositories

If guides repository is large:

```bash
# Use shallow clone (faster, less disk space)
git config submodule.context/references.shallow true
git submodule update --init --recursive --depth 1

# Only update when needed, not on every project sync
git config submodule.context/references.update none
```

### Offline Development

If working offline:

```bash
# Clone guides repository separately
git clone git@github.com:yousourceinc/implementation-guides.git ~/guides-cache

# Use cached version when offline
export SPECIFY_GUIDES_REPO_URL="file:///Users/$(whoami)/guides-cache"
specify init offline-project --ai claude
```

## Testing Scenarios

### Test Automatic Integration

```bash
# Clean test
rm -rf /tmp/auto-test
specify init /tmp/auto-test --ai claude
test -d /tmp/auto-test/context/references/ && echo "SUCCESS" || echo "FAILED"
```

### Test Override Mechanism

```bash
# With override
export SPECIFY_GUIDES_REPO_URL="git@github.com:test-org/guides.git"
rm -rf /tmp/override-test
specify init /tmp/override-test --ai claude

# Verify used override URL
cd /tmp/override-test
git config --file .gitmodules --get submodule.context/references.url
```

### Test Update Command

```bash
# Create project
rm -rf /tmp/update-test
specify init /tmp/update-test --ai claude
cd /tmp/update-test

# Make changes to guides (simulate outdated)
cd context/references
git reset --hard HEAD~1
cd ../..

# Update to latest
specify guides update

# Verify updated
cd context/references
git log -1  # Should show latest commit
```

## Related Documentation

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Constitution**: `.specify/memory/constitution.md`
- **Full Guide**: `GUIDES_IMPLEMENTATION_COMPLETE.md`

## Support

If you encounter issues not covered here:

1. Check error message carefully (all errors are actionable)
2. Verify SSH keys are configured
3. Test network connectivity to GitHub
4. Try manual git submodule commands
5. Contact team lead or open an issue

## Changelog

- **2025-10-20**: Initial version for v0.4.0 release
