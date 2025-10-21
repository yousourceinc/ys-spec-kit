# Quickstart: Division-Aware Workflow

**Feature**: Division-Aware Workflow  
**Target Audience**: Developers using Specify CLI  
**Time to Complete**: 5 minutes

## What You'll Learn

- How to initialize a project with a division
- How AI agents use division context to provide relevant guidance
- How to discover and view division-specific guides
- How to change a project's division

## Prerequisites

- Specify CLI v0.5.0 or later installed
- Implementation guides repository cloned (automatically handled by `specify init`)
- Basic familiarity with Specify CLI commands

## Quick Start

### 1. Initialize Project with Division

Create a new project and specify its division:

```bash
# Software Engineering project (default)
specify init my-backend-service --division SE

# Data Science project
specify init ml-pipeline --division DS

# Platform Engineering project
specify init k8s-operator --division Platform
```

**What happens**:
- Project directory created with `.specify/` structure
- `.specify/project.json` created with your division choice
- Implementation guides cloned to `context/references/`
- AI agent context files configured with division awareness

### 2. Verify Division Configuration

Check your project's division:

```bash
cat .specify/project.json
```

Expected output:
```json
{
  "division": "DS"
}
```

### 3. Use AI Commands with Division Context

AI commands automatically prioritize your division's guides:

**Example: Create a specification**
```bash
# In your project directory
/specify Create a data processing pipeline that validates input schemas
```

**What the AI sees**:
```markdown
## Project Division

**Division**: DS
**Guide Priority**: Guides from `context/references/DS/` should be prioritized.

## Available Guides (DS Division)

- context/references/DS/data-pipelines.md
- context/references/DS/data-validation.md
- context/references/DS/ml-model-standards.md
```

The AI will reference DS-specific guides like `data-pipelines.md` and `data-validation.md` rather than generic patterns.

### 4. Discover Division Guides

List available guides for your division:

```bash
# Show all guides (prioritizes your division)
specify guides show

# View specific guide
specify guides show data-pipelines.md
```

**Output example**:
```
📚 Guide: Data Processing Pipelines
Division: DS
Path: context/references/DS/data-pipelines.md

# Data Processing Pipelines

This guide covers best practices for building data processing
pipelines in Data Science projects...
```

### 5. Search Across Divisions

Find guides from other divisions:

```bash
# Searches your division first, then others
specify guides show backend-patterns.md
```

If the guide is from another division:
```
⚠️  Guide found in different division

📚 Guide: Backend Patterns
Division: SE (not your division: DS)
Path: context/references/SE/backend-patterns.md

# Backend Patterns

This guide is for Software Engineering projects...
```

## Common Workflows

### Initialize Existing Project with Division

Add division to an existing project:

```bash
# In your existing project directory
specify init --here --division Platform
```

This creates `.specify/project.json` without reinitializing the entire project.

### Change Project Division

Update your project's division:

```bash
# Edit the config file
echo '{"division": "SE"}' > .specify/project.json

# Or use your favorite editor
code .specify/project.json

# Verify the change
specify check
```

### Update Agent Context After Division Change

After changing division, update AI agent context files:

```bash
# Bash/zsh
bash scripts/bash/update-agent-context.sh

# PowerShell
pwsh scripts/powershell/update-agent-context.ps1
```

The agent context files (`.claude/`, `.github/`, etc.) will be updated with your new division's guides.

## Division-Specific Examples

### Software Engineering (SE)

**Typical guides**:
- `backend-patterns.md` - Backend architecture patterns
- `api-design.md` - RESTful API design standards
- `testing-strategy.md` - Unit, integration, e2e testing approaches
- `frontend-components.md` - UI component architecture

**Use cases**:
- Web applications
- Mobile apps
- APIs and microservices
- Full-stack projects

### Data Science (DS)

**Typical guides**:
- `data-pipelines.md` - ETL and data processing patterns
- `ml-models.md` - Model training and evaluation standards
- `notebooks.md` - Jupyter notebook best practices
- `feature-engineering.md` - Feature creation and selection

**Use cases**:
- Machine learning projects
- Data analysis pipelines
- Research notebooks
- Model training workflows

### Platform Engineering (Platform)

**Typical guides**:
- `infrastructure.md` - Infrastructure as Code patterns
- `kubernetes.md` - Kubernetes deployment standards
- `monitoring.md` - Observability and alerting setup
- `ci-cd.md` - Deployment pipeline configuration

**Use cases**:
- Infrastructure projects
- DevOps tooling
- Cloud automation
- Container orchestration

## Troubleshooting

### Division Not Found Error

**Error**: `Invalid division 'XYZ'. Valid options: SE, DS, Platform`

**Solution**: Use one of the valid division identifiers listed in the error message.

### No Guides Available

**Issue**: AI doesn't reference any guides

**Possible causes**:
1. Guides repository not cloned: `ls context/references/` should show division directories
2. Division directory empty: `ls context/references/SE/` should show `.md` files
3. Agent context not updated: Run `update-agent-context.sh` to refresh

**Solution**:
```bash
# Re-clone guides repository
rm -rf context/
specify init --here --division SE

# Or manually update context
bash scripts/bash/update-agent-context.sh
```

### Missing `.specify/project.json`

**Issue**: Division defaults to SE unexpectedly

**Solution**: File might have been deleted or not created. Recreate it:
```bash
specify init --here --division DS
```

### Division Not Respected by AI

**Issue**: AI references guides from wrong division

**Possible causes**:
1. Agent context files outdated
2. AI agent not reading context correctly
3. Manual additions to agent files override division context

**Solution**:
```bash
# Regenerate agent context
bash scripts/bash/update-agent-context.sh

# Check agent context file
cat .github/prompts/speckit.specify.prompt.md | grep "Project Division"
```

## Next Steps

- **Read your division's guides**: Browse `context/references/{YOUR_DIVISION}/`
- **Create a specification**: Use `/specify` command to test division-aware guidance
- **Plan a feature**: Use `/plan` command to see division-specific design patterns
- **Generate tasks**: Use `/tasks` command (enforces division guide references)

## Advanced Usage

### Custom Division Validation

Check which divisions are available:

```bash
ls context/references/
```

Any subdirectory is a valid division. To add a new division, create a directory in the guides repository:

```bash
mkdir context/references/Mobile
# Add guides...
```

### CI/CD Integration

Validate division in CI:

```bash
# In your CI script
division=$(jq -r '.division' .specify/project.json)
if [ -z "$division" ]; then
    echo "Error: Division not configured"
    exit 1
fi
echo "Project division: $division"
```

### Team Standardization

Enforce division consistency across team:

```bash
# In pre-commit hook
division=$(jq -r '.division' .specify/project.json)
if [ "$division" != "DS" ]; then
    echo "Error: This repository requires DS division"
    exit 1
fi
```

## Summary

✅ **Initialize**: `specify init --division <DIV>`  
✅ **Verify**: `cat .specify/project.json`  
✅ **Use AI**: `/specify`, `/plan`, `/tasks` automatically use division context  
✅ **Discover**: `specify guides show` to find division guides  
✅ **Update**: Edit `.specify/project.json` and run `update-agent-context.sh`

Division-aware workflow ensures AI guidance is relevant to your project type, reducing noise and improving recommendation quality.

---

**Questions?** Check the [full specification](./spec.md) or run `specify check` to verify your setup.
