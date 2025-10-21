"""
Unit tests for TextIncludesRule.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.text_rules import TextIncludesRule


def test_text_includes_rule_initialization():
    """Test TextIncludesRule initialization."""
    rule = TextIncludesRule(
        "test-id",
        "Test text pattern",
        "src/config.py",
        "import React",
        case_sensitive=True
    )
    
    assert rule.id == "test-id"
    assert rule.description == "Test text pattern"
    assert rule.file == "src/config.py"
    assert rule.text == "import React"
    assert rule.case_sensitive is True
    assert rule.TYPE == "text_includes"


def test_text_includes_rule_evaluate_pattern_found(tmp_path):
    """Test rule passes when pattern is found."""
    test_file = tmp_path / "config.py"
    test_file.write_text("import React from 'react'\nimport './App.css'\n")
    
    rule = TextIncludesRule("test-id", "Test description", "config.py", "import React")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']
    assert "Pattern found" in result['message']
    assert "1 occurrence" in result['details']


def test_text_includes_rule_evaluate_pattern_not_found(tmp_path):
    """Test rule fails when pattern is not found."""
    test_file = tmp_path / "config.py"
    test_file.write_text("import Vue from 'vue'\n")
    
    rule = TextIncludesRule("test-id", "Test description", "config.py", "import React")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False
    assert "❌" in result['message']
    assert "not found" in result['message']


def test_text_includes_rule_evaluate_file_not_found(tmp_path):
    """Test rule fails when file doesn't exist."""
    rule = TextIncludesRule("test-id", "Test description", "nonexistent.py", "pattern")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False
    assert "❌" in result['message']
    assert "not found" in result['message']


def test_text_includes_rule_evaluate_multiple_occurrences(tmp_path):
    """Test rule counts multiple occurrences."""
    test_file = tmp_path / "routes.py"
    test_file.write_text(
        "@router.get('/users')\n"
        "@router.get('/posts')\n"
        "@router.get('/comments')\n"
    )
    
    rule = TextIncludesRule("test-id", "Test description", "routes.py", "@router.get")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "3 occurrences" in result['details']


def test_text_includes_rule_evaluate_case_insensitive(tmp_path):
    """Test rule with case insensitive search."""
    test_file = tmp_path / "config.py"
    test_file.write_text("IMPORT React FROM 'react'\n")
    
    rule = TextIncludesRule(
        "test-id", 
        "Test description", 
        "config.py", 
        "import react",
        case_sensitive=False
    )
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']


def test_text_includes_rule_evaluate_case_sensitive_fails(tmp_path):
    """Test case sensitive search fails on case mismatch."""
    test_file = tmp_path / "config.py"
    test_file.write_text("IMPORT REACT\n")
    
    rule = TextIncludesRule(
        "test-id",
        "Test description",
        "config.py",
        "import react",
        case_sensitive=True
    )
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False


def test_text_includes_rule_from_yaml():
    """Test creating rule from YAML data."""
    data = {
        'id': 'router-decorator',
        'type': 'text_includes',
        'file': 'src/api/routes.py',
        'text': '@router.get',
        'description': 'Router decorators required',
        'case_sensitive': True
    }
    
    rule = TextIncludesRule.from_yaml(data)
    
    assert rule.id == 'router-decorator'
    assert rule.file == 'src/api/routes.py'
    assert rule.text == '@router.get'
    assert rule.case_sensitive is True


def test_text_includes_rule_from_yaml_default_case_sensitive():
    """Test from_yaml defaults case_sensitive to True."""
    data = {
        'id': 'test-rule',
        'type': 'text_includes',
        'file': 'test.py',
        'text': 'pattern',
        'description': 'Test description'
    }
    
    rule = TextIncludesRule.from_yaml(data)
    assert rule.case_sensitive is True


def test_text_includes_rule_from_yaml_missing_file():
    """Test from_yaml raises ValueError when file is missing."""
    data = {
        'id': 'test-rule',
        'type': 'text_includes',
        'text': 'pattern',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'file'"):
        TextIncludesRule.from_yaml(data)


def test_text_includes_rule_from_yaml_missing_text():
    """Test from_yaml raises ValueError when text is missing."""
    data = {
        'id': 'test-rule',
        'type': 'text_includes',
        'file': 'test.py',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'text'"):
        TextIncludesRule.from_yaml(data)
