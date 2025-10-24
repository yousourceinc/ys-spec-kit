# Governance Quickstart

Get started with Specify CLI's governance layer in **5 minutes**.

## Prerequisites

- Specify CLI installed and initialized
- A project with implementation guides containing rules
- Optional: Git repository for waiver management

## 1. Run Your First Compliance Check (2 min)

```bash
# Check compliance against all discovered guides
specify check-compliance

# With specific guides
specify check-compliance --guides context/references/my-guide.md

# Disable caching (useful for debugging)
specify check-compliance --no-cache
```

**Output**: Generates `compliance-report.md` with results

## 2. Understand the Report (1 min)

```markdown
# Compliance Report
Generated: 2025-10-22T10:30:00Z

## Summary
- ✅ Passed: 5 rules
- ❌ Failed: 2 rules
- ⚠️ Waived: 1 rule
- Total: 8 rules from 2 guides

## Passed Rules
- SE-001: Entry point exists ✅
- SE-002: Type hints present ✅
...

## Failed Rules
- LINT-001: No style violations ❌
  Recommendation: Run formatter
- TEST-002: Test coverage > 80% ❌
  Recommendation: Add unit tests
...
```

## 3. Create Your First Waiver (1 min)

When a failure is acceptable (legacy code, technical debt, etc.):

```bash
# Create a waiver with a clear reason
specify waive-requirement "Legacy system - will refactor in Phase 3"

# Create a waiver for specific rules
specify waive-requirement "Temporary: waiting for dependency update" --rules LINT-001 TEST-002
```

Output: Creates entry in `.specify/waivers.md`

```markdown
## W-001: Legacy system - will refactor in Phase 3
- **Created**: 2025-10-22T10:35:00Z
- **Related Rules**: (all failed rules)
- **Status**: Active
```

## 4. Manage Waivers (1 min)

```bash
# List all waivers
specify waivers list

# List with details
specify waivers list --verbose

# View specific waiver
specify waivers show W-001

# Remove waiver (when issue is fixed)
rm .specify/waivers.md  # then recreate without the waiver
```

## 5. Common Workflows

### Workflow A: Fix Issues and Pass Compliance

```bash
# 1. Run compliance check
specify check-compliance

# 2. Fix failing rules (e.g., add type hints)
# ... make code changes ...

# 3. Re-run to verify
specify check-compliance  # Should show ✅ Passed

# 4. Commit success
git add .
git commit -m "fix: improve code compliance"
```

### Workflow B: Waive Known Issues

```bash
# 1. Run compliance check
specify check-compliance

# 2. Create waiver for known technical debt
specify waive-requirement "Async refactor - scheduled for Q1 2026"

# 3. Review waiver details
specify waivers show W-001

# 4. Commit with waiver
git add .specify/waivers.md compliance-report.md
git commit -m "docs: record waiver for async refactor"
```

### Workflow C: Monitor Compliance Over Time

```bash
# Track compliance progress
for week in {1..4}; do
  echo "Week $week:"
  specify check-compliance
  grep "Summary" compliance-report.md
done

# Identify trends
git log --oneline .specify/waivers.md
```

## Rule Type Examples

### file_exists Rule

Ensure critical files are present:

```yaml
rules:
  - id: "SE-001"
    type: "file_exists"
    path: "src/main.py"
    description: "Ensure main entry point exists"
```

### dependency_present Rule

Check for required packages:

```yaml
rules:
  - id: "LINT-001"
    type: "dependency_present"
    package: "pytest"
    description: "Testing framework required"
```

### text_includes Rule

Validate content in files:

```yaml
rules:
  - id: "TEST-002"
    type: "text_includes"
    target: "README.md"
    text: "## Testing"
    description: "README should document testing"
```

## Tips & Tricks

### 🚀 Speed Up Checks

Caching is enabled by default:

```bash
# First run: scans guides (slower)
specify check-compliance  # ~2-5 seconds

# Subsequent runs: uses cache (faster)
specify check-compliance  # ~100-200ms

# Cache auto-invalidates after 1 hour
# or when project structure changes
```

### 📊 View Metrics

After a compliance check, view performance:

```python
from specify_cli.governance.metrics import MetricsCollector

metrics = MetricsCollector.get_instance()
print(metrics.summary())
# Output: "Checked 2 guides with 8 rules (avg 45ms per rule)"
```

### 🔍 Debug Rule Issues

```bash
# Re-run without cache for fresh evaluation
specify check-compliance --no-cache

# Check specific guide only
specify check-compliance --guides context/references/my-guide.md
```

### 📝 Document Waivers Properly

Good waiver reasons:

```
✅ "Legacy authentication system - will migrate to OAuth in Q1 2026"
✅ "Async refactor pending - blocked on dependency version update"
✅ "Type hints deferred - requires type stubs for external library"
```

Bad waiver reasons:

```
❌ "will fix later"
❌ "temporary"
❌ "todo"
❌ "hack"
```

## Troubleshooting

### "No guides found"

```bash
# Verify guides exist in context/references/
ls -la context/references/

# Check guide discovery
specify check-compliance --guides path/to/guide.md
```

### "Rule failed but shouldn't"

```bash
# Check rule details in guide YAML
cat context/references/my-guide.md | head -50

# Verify file paths in file_exists rules
ls -la path/specified/in/rule

# Check text_includes case sensitivity
grep "exact text" file.md
```

### "Cache seems stale"

```bash
# Force refresh by disabling cache
specify check-compliance --no-cache

# Manual cache clear (if it exists)
rm -rf .specify/.cache/
```

## Next Steps

1. **Learn more**: Read [Governance Overview](./governance-overview.md)
2. **Author rules**: See [Rule Authoring Guide](./rule-authoring.md)
3. **Deep dive**: Check [Compliance Checking](./compliance-checking.md)
4. **Advanced**: Review [Phase 7 Completion](../../project-meta/completion-logs/GOVERNANCE_PHASE_7_COMPLETION.md)

## Command Reference

```bash
# Compliance checking
specify check-compliance [--guides PATHS] [--no-cache]

# Waiver management
specify waive-requirement "Reason" [--rules RULE_IDS]
specify waivers list [--verbose]
specify waivers show W-001

# Help
specify check-compliance --help
specify waive-requirement --help
```

## Common Questions

**Q: When should I create a waiver?**
A: When a rule failure is acceptable and you've decided not to fix it immediately. Always document the reason and plan for resolution.

**Q: Are waivers version-controlled?**
A: Yes! `.specify/waivers.md` should be committed to git so all team members see active waivers.

**Q: Can I share rules across projects?**
A: Yes! Place rules in shared implementation guides and reference them via `SPECIFY_GUIDES_REPO_URL`.

**Q: How often should I run compliance checks?**
A: Best practice: before each commit. CI/CD integration coming in future phases.

## Support

Need help? See:

- [Troubleshooting Guide](../troubleshooting/)
- [FAQ](../troubleshooting/faq.md)
- [Main SUPPORT.md](../../SUPPORT.md)
