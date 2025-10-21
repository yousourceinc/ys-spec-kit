---
title: "{{ GUIDE_TITLE }}"
division: "{{ DIVISION }}"
description: "Implementation guide for {{ GUIDE_TITLE }}"

# Compliance rules for this guide
# These rules are automatically discovered and evaluated by the governance layer
# Each rule defines a compliance requirement that projects must satisfy

rules:
  # Example 1: File existence rule
  # This rule ensures a specific file exists in the project
  - id: main-entry-point
    type: file_exists
    description: "Main entry point file must exist"
    path: "src/main.py"
    # Optional: division: "{{ DIVISION }}"
  
  # Example 2: Dependency presence rule
  # This rule ensures a specific package is declared in a manifest file
  - id: testing-framework
    type: dependency_present
    description: "Testing framework must be installed"
    file: "requirements.txt"
    package: "pytest"
    # Optional: version: ">=6.0"  # Can specify minimum version
    # Optional: division: "{{ DIVISION }}"
  
  # Example 3: Text inclusion rule
  # This rule ensures specific text appears in a file (e.g., licenses, imports, config)
  - id: license-header
    type: text_includes
    description: "License header must be present in main files"
    file: "src/main.py"
    text: "# Copyright"
    # Optional: case_sensitive: false  # Default is true
    # Optional: division: "{{ DIVISION }}"
---

# {{ GUIDE_TITLE }}

## Overview

This guide describes the implementation requirements for {{ GUIDE_TITLE }}.

### Key Requirements

1. **{{ REQUIREMENT_1 }}**
   - Detail about requirement 1
   - Related rule: `main-entry-point`

2. **{{ REQUIREMENT_2 }}**
   - Detail about requirement 2
   - Related rule: `testing-framework`

3. **{{ REQUIREMENT_3 }}**
   - Detail about requirement 3
   - Related rule: `license-header`

## Implementation Steps

### Step 1: Setup

Follow these steps to set up {{ GUIDE_TITLE }}:

```bash
# Example setup commands
mkdir -p src
touch src/main.py
```

### Step 2: Configuration

Configure {{ GUIDE_TITLE }}:

```python
# src/main.py
# Copyright 2025 - Your Organization
# Licensed under MIT License

def main():
    """Main entry point."""
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

### Step 3: Testing

Add tests to verify compliance:

```bash
# Install testing dependencies
pip install pytest

# Run tests
pytest tests/
```

## Verification

Verify that your implementation satisfies all compliance rules:

```bash
specify check-compliance
```

This will:
1. Discover all rules from implementation guides
2. Evaluate your project against each rule
3. Generate a compliance report (`compliance-report.md`)
4. Display pass/fail/waived status for each rule

## Troubleshooting

### Rule Not Found

If you get "Rule not found" errors:

1. Ensure the file specified in the rule exists
2. Check file paths are relative to project root
3. Verify the pattern/text matches exactly (check case sensitivity)

### Rule Validation Errors

If you get validation errors when defining rules:

1. Ensure all required fields are present
2. Check field types (e.g., `path` must be a string, not a list)
3. Use the error message to identify the specific issue
4. Refer to the rule schema at the top of this guide

## Best Practices

When defining compliance rules:

1. **Be specific**: Rules should target specific, measurable requirements
2. **Document motivation**: Include why each rule exists
3. **Keep related rules**: Group related rules in the same guide
4. **Use clear IDs**: Rule IDs should be descriptive (`testing-framework` not `test`)
5. **Validate early**: Run `specify check-compliance` frequently during development
6. **Record exceptions**: Use `specify waive-requirement` if a rule failure is intentional

## Rule Types Reference

### file_exists
Ensures a specific file exists in the project.
```yaml
- id: my-rule
  type: file_exists
  description: "Description of what must exist"
  path: "path/to/file.ext"
```

### dependency_present
Ensures a package is declared in a package manifest file.
```yaml
- id: my-rule
  type: dependency_present
  description: "Description of required dependency"
  file: "package.json"  # or requirements.txt, go.mod, etc.
  package: "package-name"
  version: ">=1.0"  # Optional
```

### text_includes
Ensures specific text appears in a file.
```yaml
- id: my-rule
  type: text_includes
  description: "Description of required text"
  file: "path/to/file.txt"
  text: "required text pattern"
  case_sensitive: true  # Optional, default is true
```

## Further Reading

- [Compliance Rule Syntax Guide](https://github.com/yousourceinc/ys-spec-kit/docs/rule-syntax.md)
- [Governance Layer Documentation](https://github.com/yousourceinc/ys-spec-kit/docs/governance-layer.md)
- [Waiver Management](https://github.com/yousourceinc/ys-spec-kit/docs/waivers.md)
