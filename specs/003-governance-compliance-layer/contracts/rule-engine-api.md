# Rule Engine API Contract

**Version**: 1.0  
**Module**: `src/specify_cli/governance/rules/`  
**Purpose**: Define machine-readable compliance rules and evaluation engine  
**Format**: Python classes with well-defined interfaces

## Rule Definition Format

### YAML Frontmatter Format (in Implementation Guides)

```yaml
---
title: "Backend API Implementation"
division: "SE"
rules:
  - id: api-routes-defined
    type: file_exists
    path: "src/api/routes.py"
    description: "API routes module must exist"
  
  - id: tests-present
    type: file_exists
    path: "tests/api/test_routes.py"
    description: "API tests must exist"
  
  - id: fastapi-dependency
    type: dependency_present
    file: "requirements.txt"
    package: "fastapi"
    version: ">=0.95"
    description: "FastAPI version 0.95+ required"
  
  - id: router-decorator-used
    type: text_includes
    file: "src/api/routes.py"
    text: "@router.get"
    description: "Must use FastAPI router decorators"
---

# Backend API Implementation Guide

[Content...]
```

## Rule Field Specifications

### Common Fields (All Rules)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique rule identifier (lowercase, hyphens) |
| `type` | string | Yes | Rule type: file_exists, dependency_present, text_includes |
| `description` | string | Yes | Human-readable rule description |

### file_exists Rule

```yaml
- id: routes-file-exists
  type: file_exists
  path: "src/api/routes.py"
  description: "API routes file must exist"
```

**Fields**:
- `path`: File path to check (required)
- Must exist for rule to pass
- Relative paths: relative to project root

### dependency_present Rule

```yaml
- id: fastapi-required
  type: dependency_present
  file: "requirements.txt"
  package: "fastapi"
  version: ">=0.95"
  description: "FastAPI 0.95+ required"
```

**Fields**:
- `file`: Dependency manifest file (required, e.g., requirements.txt, package.json, Gemfile)
- `package`: Package name to check (required)
- `version`: Optional version specifier (e.g., ">=1.0", "~2.3", "exactly 3.4.5")
- Version matching: Follows semantic versioning when specified

### text_includes Rule

```yaml
- id: router-import
  type: text_includes
  file: "src/api/routes.py"
  text: "@router.get"
  description: "Must use FastAPI router decorators"
  case_sensitive: true
```

**Fields**:
- `file`: File path to search (required)
- `text`: Text pattern to find (required)
- `case_sensitive`: Boolean (default: true)
- Pattern matching: Exact string match (not regex in initial version)

## Python API

### BaseRule Class

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseRule(ABC):
    """Abstract base class for all rule types"""
    
    def __init__(self, rule_id: str, description: str, **kwargs):
        self.id = rule_id
        self.description = description
        self.rule_data = kwargs
    
    @abstractmethod
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Evaluate rule against project codebase.
        
        Returns:
            {
                "passed": bool,
                "message": str,
                "details": str (optional)
            }
        """
        pass
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> 'BaseRule':
        """Factory method to create rule from YAML dict"""
        pass
```

### FileExistsRule Class

```python
class FileExistsRule(BaseRule):
    """Checks if a file exists in project"""
    
    TYPE = "file_exists"
    
    def __init__(self, rule_id: str, description: str, path: str):
        super().__init__(rule_id, description, path=path)
        self.path = path
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if file exists at given path.
        
        Returns:
            - passed: True if file exists
            - message: "✅ File exists" or "❌ File not found"
            - details: Full path checked
        """
        pass
```

### DependencyPresentRule Class

```python
class DependencyPresentRule(BaseRule):
    """Checks if dependency is declared in manifest"""
    
    TYPE = "dependency_present"
    
    def __init__(
        self, 
        rule_id: str, 
        description: str, 
        file: str, 
        package: str,
        version: str = None
    ):
        super().__init__(
            rule_id, 
            description, 
            file=file, 
            package=package, 
            version=version
        )
        self.file = file
        self.package = package
        self.version = version
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if package is declared in manifest.
        
        Returns:
            - passed: True if package present (and version matches if specified)
            - message: Status message
            - details: Version found, version required, etc.
        """
        pass
```

### TextIncludesRule Class

```python
class TextIncludesRule(BaseRule):
    """Checks if text pattern appears in file"""
    
    TYPE = "text_includes"
    
    def __init__(
        self, 
        rule_id: str, 
        description: str, 
        file: str, 
        text: str,
        case_sensitive: bool = True
    ):
        super().__init__(
            rule_id, 
            description, 
            file=file, 
            text=text, 
            case_sensitive=case_sensitive
        )
        self.file = file
        self.text = text
        self.case_sensitive = case_sensitive
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if text pattern appears in file.
        
        Returns:
            - passed: True if pattern found
            - message: Status message
            - details: Number of occurrences, line number (if available)
        """
        pass
```

## RuleEngine Class

```python
from typing import List, Tuple

class RuleEngine:
    """Orchestrates rule evaluation"""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.rules: List[BaseRule] = []
    
    def register_rule(self, rule: BaseRule) -> None:
        """Register a rule for evaluation"""
        self.rules.append(rule)
    
    def evaluate_all(self) -> List[Dict[str, Any]]:
        """
        Evaluate all registered rules.
        
        Returns:
            List of evaluation results with rule_id, status, message, details
        """
        pass
    
    @staticmethod
    def create_rule(rule_type: str, **kwargs) -> BaseRule:
        """
        Factory method to create appropriate rule type.
        
        Args:
            rule_type: "file_exists", "dependency_present", or "text_includes"
            **kwargs: Type-specific arguments
        
        Returns:
            Instantiated rule object
        
        Raises:
            ValueError: If rule_type is unknown
        """
        pass
```

## RuleParser Class

```python
from pathlib import Path
import yaml

class RuleParser:
    """Parses YAML frontmatter from guide files"""
    
    @staticmethod
    def extract_rules(guide_file: Path) -> List[Dict[str, Any]]:
        """
        Extract rules from YAML frontmatter of guide file.
        
        Args:
            guide_file: Path to markdown file with YAML frontmatter
        
        Returns:
            List of rule dictionaries
        
        Raises:
            ValueError: If YAML is malformed
            KeyError: If required rule fields missing
        """
        pass
    
    @staticmethod
    def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content.
        
        Args:
            content: Markdown file content
        
        Returns:
            (frontmatter_dict, remaining_content)
        
        Raises:
            ValueError: If frontmatter is malformed
        """
        pass
    
    @staticmethod
    def validate_rule_structure(rule: Dict[str, Any], rule_type: str) -> bool:
        """
        Validate that rule has all required fields for its type.
        
        Args:
            rule: Rule dictionary
            rule_type: Rule type (e.g., "file_exists")
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If required fields missing or invalid
        """
        pass
```

## Evaluation Result Format

Each rule evaluation returns:

```python
{
    "rule_id": "api-routes-defined",
    "rule_type": "file_exists",
    "status": "pass",  # or "fail", "error"
    "message": "✅ File exists at src/api/routes.py",
    "details": {
        "target": "src/api/routes.py",
        "description": "API routes module must exist",
        "guide_id": "backend-patterns.md",
        "division": "SE"
    }
}
```

## Error Handling

### Rule Parsing Errors

```python
class RuleParseError(Exception):
    """Raised when rule YAML is malformed"""
    pass

class MissingRuleFieldError(RuleParseError):
    """Raised when required rule field is missing"""
    pass

class UnknownRuleTypeError(RuleParseError):
    """Raised when rule type is not recognized"""
    pass
```

### Rule Evaluation Errors

```python
class RuleEvaluationError(Exception):
    """Raised when rule can't be evaluated"""
    pass

class FileNotFoundError(RuleEvaluationError):
    """Raised when target file doesn't exist (for file_exists check)"""
    pass

class ManifestParseError(RuleEvaluationError):
    """Raised when dependency manifest can't be parsed"""
    pass
```

### Error Handling Strategy

When rule evaluation fails:
1. Log specific error message
2. Return result with status="error"
3. Include error details in message
4. Continue with next rule (non-blocking)

## Testing Contract

### Unit Tests

```python
def test_file_exists_rule_passes():
    """Rule passes when file exists"""
    pass

def test_file_exists_rule_fails():
    """Rule fails when file doesn't exist"""
    pass

def test_dependency_present_rule_passes():
    """Rule passes when dependency found in manifest"""
    pass

def test_dependency_present_rule_with_version():
    """Rule evaluates version requirements"""
    pass

def test_text_includes_rule_finds_pattern():
    """Rule finds text pattern in file"""
    pass

def test_text_includes_case_sensitivity():
    """Case sensitivity option works correctly"""
    pass

def test_rule_parser_extracts_frontmatter():
    """YAML frontmatter is extracted from guide"""
    pass

def test_rule_parser_handles_malformed_yaml():
    """Malformed YAML raises appropriate error"""
    pass

def test_rule_engine_evaluates_all_rules():
    """Engine evaluates all registered rules"""
    pass
```

### Integration Tests

```python
def test_compliance_check_with_sample_project():
    """Full compliance check against sample project"""
    pass

def test_compliance_check_with_waived_rules():
    """Waived rules are marked correctly"""
    pass
```

## Performance Considerations

### Rule Evaluation Times

- **file_exists**: O(1) filesystem check - ~1ms per rule
- **dependency_present**: O(n) manifest parsing - ~10-100ms depending on manifest size
- **text_includes**: O(m) file content scan - ~5-50ms depending on file size

### Total Expected Time

Typical project (10-20 rules): <1 second  
Large project (50+ rules): <10 seconds  
(From spec requirement: <30 seconds)

### Caching Opportunities

Potential future optimizations:
- Cache parsed manifest files during single check run
- Cache file content to avoid repeated reads
- Track previously checked files to avoid duplicates

## Version Control & Deprecation

### API Stability

- Current version: 1.0
- Breaking changes: New major version required
- Additions: Minor version bump
- Deprecations: 2-version grace period

### Future Extensions

Reserved for future versions:
- Regular expression pattern matching
- Boolean logic conditions (AND, OR, NOT)
- Environment-specific rule variations
- Rule severity levels (critical, warning, info)
