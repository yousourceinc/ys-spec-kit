"""
Unit tests for DependencyPresentRule.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.dependency_rules import DependencyPresentRule


def test_dependency_present_rule_initialization():
    """Test DependencyPresentRule initialization."""
    rule = DependencyPresentRule(
        "test-id", 
        "Test dependency", 
        "requirements.txt", 
        "requests",
        version=">=2.28"
    )
    
    assert rule.id == "test-id"
    assert rule.description == "Test dependency"
    assert rule.file == "requirements.txt"
    assert rule.package == "requests"
    assert rule.version == ">=2.28"
    assert rule.TYPE == "dependency_present"


def test_dependency_present_rule_evaluate_package_found(tmp_path):
    """Test rule passes when package is declared."""
    manifest = tmp_path / "requirements.txt"
    manifest.write_text("requests>=2.28.0\npytest>=7.0.0\n")
    
    rule = DependencyPresentRule("test-id", "Test description", "requirements.txt", "requests")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']
    assert "requests" in result['message']


def test_dependency_present_rule_evaluate_package_not_found(tmp_path):
    """Test rule fails when package is not declared."""
    manifest = tmp_path / "requirements.txt"
    manifest.write_text("pytest>=7.0.0\n")
    
    rule = DependencyPresentRule("test-id", "Test description", "requirements.txt", "requests")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False
    assert "❌" in result['message']
    assert "not declared" in result['message']
    assert "requests" in result['message']


def test_dependency_present_rule_evaluate_manifest_not_found(tmp_path):
    """Test rule fails when manifest file doesn't exist."""
    rule = DependencyPresentRule("test-id", "Test description", "requirements.txt", "requests")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False
    assert "❌" in result['message']
    assert "not found" in result['message']


def test_dependency_present_rule_evaluate_with_version(tmp_path):
    """Test rule with version constraint."""
    manifest = tmp_path / "requirements.txt"
    manifest.write_text("requests>=2.28.0\n")
    
    rule = DependencyPresentRule(
        "test-id", 
        "Test description", 
        "requirements.txt", 
        "requests",
        version=">=2.28"
    )
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']


def test_dependency_present_rule_package_json(tmp_path):
    """Test rule with package.json."""
    manifest = tmp_path / "package.json"
    manifest.write_text('{"dependencies": {"axios": "^1.4.0"}}')
    
    rule = DependencyPresentRule("test-id", "Test description", "package.json", "axios")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']


def test_dependency_present_rule_from_yaml():
    """Test creating rule from YAML data."""
    data = {
        'id': 'fastapi-required',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'package': 'fastapi',
        'version': '>=0.95',
        'description': 'FastAPI required'
    }
    
    rule = DependencyPresentRule.from_yaml(data)
    
    assert rule.id == 'fastapi-required'
    assert rule.file == 'requirements.txt'
    assert rule.package == 'fastapi'
    assert rule.version == '>=0.95'


def test_dependency_present_rule_from_yaml_missing_file():
    """Test from_yaml raises ValueError when file is missing."""
    data = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'package': 'requests',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'file'"):
        DependencyPresentRule.from_yaml(data)


def test_dependency_present_rule_from_yaml_missing_package():
    """Test from_yaml raises ValueError when package is missing."""
    data = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'package'"):
        DependencyPresentRule.from_yaml(data)


def test_dependency_present_rule_from_yaml_optional_version():
    """Test from_yaml works without version field."""
    data = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'package': 'requests',
        'description': 'Test description'
    }
    
    rule = DependencyPresentRule.from_yaml(data)
    assert rule.version is None
