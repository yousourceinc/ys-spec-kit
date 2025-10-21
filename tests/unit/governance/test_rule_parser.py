"""
Unit tests for RuleParser.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.parser import RuleParser


def test_rule_parser_parse_frontmatter_valid():
    """Test parsing valid YAML frontmatter."""
    content = """---
title: "Test Guide"
division: "SE"
rules:
  - id: test-rule
    type: file_exists
    path: src/main.py
---

# Guide Content

Some markdown content here.
"""
    
    frontmatter, remaining = RuleParser.parse_frontmatter(content)
    
    assert frontmatter['title'] == "Test Guide"
    assert frontmatter['division'] == "SE"
    assert len(frontmatter['rules']) == 1
    assert "# Guide Content" in remaining


def test_rule_parser_parse_frontmatter_no_frontmatter():
    """Test parsing content without frontmatter."""
    content = "# Guide Content\n\nNo frontmatter here."
    
    frontmatter, remaining = RuleParser.parse_frontmatter(content)
    
    assert frontmatter == {}
    assert remaining == content


def test_rule_parser_parse_frontmatter_malformed_yaml():
    """Test parsing malformed YAML raises ValueError."""
    content = """---
title: "Test Guide
invalid: yaml: syntax
---

# Content
"""
    
    with pytest.raises(ValueError, match="Malformed YAML"):
        RuleParser.parse_frontmatter(content)


def test_rule_parser_parse_frontmatter_not_dict():
    """Test frontmatter that's not a dictionary raises ValueError."""
    content = """---
- item1
- item2
---

# Content
"""
    
    with pytest.raises(ValueError, match="must be a YAML dictionary"):
        RuleParser.parse_frontmatter(content)


def test_rule_parser_extract_rules_valid(tmp_path):
    """Test extracting rules from guide file."""
    guide_content = """---
title: "Backend Guide"
rules:
  - id: api-routes
    type: file_exists
    path: src/api/routes.py
    description: "API routes required"
  - id: tests-present
    type: file_exists
    path: tests/test_api.py
    description: "Tests required"
---

# Backend Implementation Guide
"""
    
    guide_file = tmp_path / "guide.md"
    guide_file.write_text(guide_content)
    
    rules = RuleParser.extract_rules(guide_file)
    
    assert len(rules) == 2
    assert rules[0]['id'] == 'api-routes'
    assert rules[0]['type'] == 'file_exists'
    assert rules[1]['id'] == 'tests-present'


def test_rule_parser_extract_rules_no_rules(tmp_path):
    """Test extracting rules when no rules are present."""
    guide_content = """---
title: "Guide Without Rules"
division: "SE"
---

# Guide Content
"""
    
    guide_file = tmp_path / "guide.md"
    guide_file.write_text(guide_content)
    
    rules = RuleParser.extract_rules(guide_file)
    
    assert rules == []


def test_rule_parser_extract_rules_no_frontmatter(tmp_path):
    """Test extracting rules from guide without frontmatter."""
    guide_content = "# Simple Guide\n\nNo rules here."
    
    guide_file = tmp_path / "guide.md"
    guide_file.write_text(guide_content)
    
    rules = RuleParser.extract_rules(guide_file)
    
    assert rules == []


def test_rule_parser_extract_rules_file_not_found():
    """Test extract_rules raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        RuleParser.extract_rules(Path("/nonexistent/guide.md"))


def test_rule_parser_extract_rules_invalid_rules_type(tmp_path):
    """Test extract_rules raises ValueError when rules is not a list."""
    guide_content = """---
title: "Invalid Guide"
rules: "not a list"
---

# Content
"""
    
    guide_file = tmp_path / "guide.md"
    guide_file.write_text(guide_content)
    
    with pytest.raises(ValueError, match="must be a list"):
        RuleParser.extract_rules(guide_file)


def test_rule_parser_validate_rule_structure_file_exists():
    """Test validating file_exists rule structure."""
    rule = {
        'id': 'test-rule',
        'type': 'file_exists',
        'path': 'src/main.py',
        'description': 'Main file required'
    }
    
    assert RuleParser.validate_rule_structure(rule, 'file_exists') is True


def test_rule_parser_validate_rule_structure_dependency_present():
    """Test validating dependency_present rule structure."""
    rule = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'package': 'requests',
        'description': 'Requests required'
    }
    
    assert RuleParser.validate_rule_structure(rule, 'dependency_present') is True


def test_rule_parser_validate_rule_structure_text_includes():
    """Test validating text_includes rule structure."""
    rule = {
        'id': 'test-rule',
        'type': 'text_includes',
        'file': 'src/config.py',
        'text': 'import React',
        'description': 'React import required'
    }
    
    assert RuleParser.validate_rule_structure(rule, 'text_includes') is True


def test_rule_parser_validate_rule_structure_missing_id():
    """Test validation fails when id is missing."""
    rule = {
        'type': 'file_exists',
        'path': 'test.txt',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'id'"):
        RuleParser.validate_rule_structure(rule, 'file_exists')


def test_rule_parser_validate_rule_structure_missing_description():
    """Test validation fails when description is missing."""
    rule = {
        'id': 'test-rule',
        'type': 'file_exists',
        'path': 'test.txt'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'description'"):
        RuleParser.validate_rule_structure(rule, 'file_exists')


def test_rule_parser_validate_rule_structure_missing_type():
    """Test validation fails when type is missing."""
    rule = {
        'id': 'test-rule',
        'path': 'test.txt',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'type'"):
        RuleParser.validate_rule_structure(rule, 'file_exists')


def test_rule_parser_validate_rule_structure_file_exists_missing_path():
    """Test validation fails for file_exists rule missing path."""
    rule = {
        'id': 'test-rule',
        'type': 'file_exists',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'path'"):
        RuleParser.validate_rule_structure(rule, 'file_exists')


def test_rule_parser_validate_rule_structure_dependency_missing_file():
    """Test validation fails for dependency_present rule missing file."""
    rule = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'package': 'requests',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'file'"):
        RuleParser.validate_rule_structure(rule, 'dependency_present')


def test_rule_parser_validate_rule_structure_dependency_missing_package():
    """Test validation fails for dependency_present rule missing package."""
    rule = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'package'"):
        RuleParser.validate_rule_structure(rule, 'dependency_present')


def test_rule_parser_validate_rule_structure_text_missing_file():
    """Test validation fails for text_includes rule missing file."""
    rule = {
        'id': 'test-rule',
        'type': 'text_includes',
        'text': 'pattern',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'file'"):
        RuleParser.validate_rule_structure(rule, 'text_includes')


def test_rule_parser_validate_rule_structure_text_missing_text():
    """Test validation fails for text_includes rule missing text."""
    rule = {
        'id': 'test-rule',
        'type': 'text_includes',
        'file': 'test.py',
        'description': 'Test'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'text'"):
        RuleParser.validate_rule_structure(rule, 'text_includes')
