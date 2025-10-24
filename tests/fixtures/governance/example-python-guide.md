---
title: "Python Backend Implementation Guide"
division: "SE"
description: "Standards for Python backend development"

rules:
  - id: python-main-module
    type: file_exists
    description: "Main module must exist at src/main.py"
    path: "src/main.py"
    division: "SE"

  - id: pytest-required
    type: dependency_present
    description: "pytest must be installed for testing"
    file: "requirements.txt"
    package: "pytest"
    division: "SE"

  - id: pytest-installed
    type: dependency_present
    description: "pytest must be in dev requirements"
    file: "requirements-dev.txt"
    package: "pytest"
    version: ">=7.0"
    division: "SE"

  - id: license-header
    type: text_includes
    description: "License header must appear in main module"
    file: "src/main.py"
    text: "Copyright"
    case_sensitive: false
    division: "SE"

  - id: readme-exists
    type: file_exists
    description: "README.md must document the backend"
    path: "README.md"
    division: "SE"

  - id: readme-has-setup
    type: text_includes
    description: "README must include setup instructions"
    file: "README.md"
    text: "Setup"
    case_sensitive: false
    division: "SE"

  - id: tests-directory
    type: file_exists
    description: "Tests must be organized in tests directory"
    path: "tests/"
    division: "SE"

  - id: config-file
    type: file_exists
    description: "Configuration file must exist"
    path: "config.yaml"
    division: "SE"
---

# Python Backend Implementation Guide

This guide defines standards and compliance rules for Python backend projects.

## Overview

All Python backend projects must comply with these standards:

1. **Project Structure**: Standard directory layout with src/, tests/, and configuration
2. **Testing**: Comprehensive test coverage with pytest
3. **Documentation**: Clear README with setup instructions
4. **Configuration**: Centralized configuration management
5. **Dependencies**: Declared in requirements.txt and requirements-dev.txt
6. **Licensing**: Proper license headers in code

## Project Structure

Your Python backend project should follow this structure:

```
project-root/
├── src/
│   └── main.py              # Main entry point (required)
├── tests/                   # Test directory (required)
│   └── test_main.py
├── config.yaml              # Configuration file (required)
├── README.md                # Documentation (required)
├── requirements.txt         # Dependencies
├── requirements-dev.txt     # Development dependencies
└── .gitignore
```

### Required Files

- **src/main.py**: Main entry point (rule: `python-main-module`)
- **README.md**: Project documentation (rule: `readme-exists`)
- **config.yaml**: Configuration file (rule: `config-file`)
- **tests/**: Test directory (rule: `tests-directory`)

## Dependencies

### Runtime Dependencies

List all runtime dependencies in `requirements.txt`:

```
Flask==2.3.0
SQLAlchemy==2.0.0
python-dotenv==1.0.0
```

**Compliance Rule**: `pytest-required`

### Development Dependencies

List all development dependencies in `requirements-dev.txt`:

```
pytest>=7.0
pytest-cov>=4.0
black==23.0.0
pylint==2.17.0
```

**Compliance Rules**: `pytest-installed`

## Main Module

The main module (`src/main.py`) must include:

1. **License header** (rule: `license-header`)
2. **Clear entry point**
3. **Documentation**

Example:

```python
"""
Copyright 2025 Your Organization
Licensed under MIT License
"""

def main():
    """Main entry point for backend service."""
    print("Backend service started")

if __name__ == "__main__":
    main()
```

## Testing

All Python backends must use **pytest** for testing.

**Compliance Rules**:
- `pytest-required`: Pytest must be in runtime dependencies
- `pytest-installed`: Pytest must be in dev dependencies

Create tests in the `tests/` directory:

```python
# tests/test_main.py
import pytest
from src.main import main

def test_main_runs():
    """Test that main function can be called."""
    main()  # Should not raise
```

Run tests:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

## Configuration

Use a `config.yaml` file for configuration:

```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  name: myproject

api:
  host: 0.0.0.0
  port: 8000
  debug: false

logging:
  level: INFO
  format: json
```

**Compliance Rule**: `config-file`

## README Documentation

Your README.md must include:

1. **Project description**
2. **Setup instructions** (rule: `readme-has-setup`)
3. **Usage examples**
4. **Testing instructions**
5. **Contributing guidelines**

Example structure:

```markdown
# My Python Backend

Brief project description.

## Setup

Follow these steps to set up the project:

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Running the Project

```bash
python src/main.py
```

## Testing

```bash
pytest tests/ -v
```

## Contributing

...
```

**Compliance Rules**:
- `readme-exists`: README must exist
- `readme-has-setup`: README must include setup instructions

## Compliance Verification

Verify your project satisfies all compliance rules:

```bash
# Run compliance check
specify check-compliance

# View waivers if any rules are intentionally violated
specify waivers list

# View specific waiver
specify waivers show W-001
```

## Rule Reference

| Rule ID | Type | Requirement |
|---------|------|-------------|
| `python-main-module` | file_exists | Main module at src/main.py |
| `pytest-required` | dependency_present | pytest in requirements.txt |
| `pytest-installed` | dependency_present | pytest in requirements-dev.txt |
| `license-header` | text_includes | License header in src/main.py |
| `readme-exists` | file_exists | README.md exists |
| `readme-has-setup` | text_includes | README includes setup instructions |
| `tests-directory` | file_exists | tests/ directory exists |
| `config-file` | file_exists | config.yaml exists |

## Exceptions

If your project cannot meet a requirement, document the exception:

```bash
specify waive-requirement "Our project uses environment variables for config, not config.yaml"
```

This records the exception in `.specify/waivers.md` for team lead review.

## Further Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Best Practices](https://pep8.org/)
- [Governance Layer Guide](https://github.com/yousourceinc/ys-spec-kit)
