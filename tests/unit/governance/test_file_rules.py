"""
Unit tests for FileExistsRule.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.file_rules import FileExistsRule


def test_file_exists_rule_initialization():
    """Test FileExistsRule initialization."""
    rule = FileExistsRule("test-id", "Test file exists", "src/main.py")
    
    assert rule.id == "test-id"
    assert rule.description == "Test file exists"
    assert rule.path == "src/main.py"
    assert rule.TYPE == "file_exists"


def test_file_exists_rule_evaluate_file_exists(tmp_path):
    """Test rule passes when file exists."""
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    
    rule = FileExistsRule("test-id", "Test description", "test.txt")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']
    assert "test.txt" in result['message']
    assert "Checked path:" in result['details']


def test_file_exists_rule_evaluate_file_missing(tmp_path):
    """Test rule fails when file doesn't exist."""
    rule = FileExistsRule("test-id", "Test description", "nonexistent.txt")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is False
    assert "❌" in result['message']
    assert "not found" in result['message']
    assert "nonexistent.txt" in result['message']


def test_file_exists_rule_evaluate_nested_path(tmp_path):
    """Test rule with nested file path."""
    # Create nested structure
    nested_dir = tmp_path / "src" / "components"
    nested_dir.mkdir(parents=True)
    test_file = nested_dir / "app.py"
    test_file.write_text("content")
    
    rule = FileExistsRule("test-id", "Test description", "src/components/app.py")
    result = rule.evaluate(str(tmp_path))
    
    assert result['passed'] is True
    assert "✅" in result['message']


def test_file_exists_rule_from_yaml():
    """Test creating rule from YAML data."""
    data = {
        'id': 'api-routes',
        'type': 'file_exists',
        'path': 'src/api/routes.py',
        'description': 'API routes must exist'
    }
    
    rule = FileExistsRule.from_yaml(data)
    
    assert rule.id == 'api-routes'
    assert rule.path == 'src/api/routes.py'
    assert rule.description == 'API routes must exist'


def test_file_exists_rule_from_yaml_missing_path():
    """Test from_yaml raises ValueError when path is missing."""
    data = {
        'id': 'test-rule',
        'type': 'file_exists',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'path'"):
        FileExistsRule.from_yaml(data)


def test_file_exists_rule_from_yaml_missing_id():
    """Test from_yaml raises ValueError when id is missing."""
    data = {
        'type': 'file_exists',
        'path': 'test.txt',
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'id'"):
        FileExistsRule.from_yaml(data)


def test_file_exists_rule_from_yaml_missing_description():
    """Test from_yaml raises ValueError when description is missing."""
    data = {
        'id': 'test-rule',
        'type': 'file_exists',
        'path': 'test.txt'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'description'"):
        FileExistsRule.from_yaml(data)
