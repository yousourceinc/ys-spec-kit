"""
Unit tests for RuleEngine.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.engine import RuleEngine
from specify_cli.governance.rules.file_rules import FileExistsRule
from specify_cli.governance.rules.dependency_rules import DependencyPresentRule
from specify_cli.governance.rules.text_rules import TextIncludesRule


def test_rule_engine_initialization(tmp_path):
    """Test RuleEngine initialization."""
    engine = RuleEngine(str(tmp_path))
    
    assert engine.project_root == str(tmp_path)
    assert engine.rules == []


def test_rule_engine_register_rule(tmp_path):
    """Test registering rules."""
    engine = RuleEngine(str(tmp_path))
    rule1 = FileExistsRule("test-1", "Test 1", "file.txt")
    rule2 = FileExistsRule("test-2", "Test 2", "file2.txt")
    
    engine.register_rule(rule1)
    engine.register_rule(rule2)
    
    assert len(engine.rules) == 2
    assert engine.rules[0] == rule1
    assert engine.rules[1] == rule2


def test_rule_engine_evaluate_all_empty(tmp_path):
    """Test evaluate_all with no rules."""
    engine = RuleEngine(str(tmp_path))
    results = engine.evaluate_all()
    
    assert results == []


def test_rule_engine_evaluate_all_passing_rules(tmp_path):
    """Test evaluate_all with passing rules."""
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    
    engine = RuleEngine(str(tmp_path))
    rule = FileExistsRule("test-rule", "Test file exists", "test.txt")
    engine.register_rule(rule)
    
    results = engine.evaluate_all()
    
    assert len(results) == 1
    assert results[0]['rule_id'] == 'test-rule'
    assert results[0]['rule_type'] == 'file_exists'
    assert results[0]['passed'] is True
    assert '✅' in results[0]['message']


def test_rule_engine_evaluate_all_failing_rules(tmp_path):
    """Test evaluate_all with failing rules."""
    engine = RuleEngine(str(tmp_path))
    rule = FileExistsRule("test-rule", "Test file exists", "nonexistent.txt")
    engine.register_rule(rule)
    
    results = engine.evaluate_all()
    
    assert len(results) == 1
    assert results[0]['rule_id'] == 'test-rule'
    assert results[0]['passed'] is False
    assert '❌' in results[0]['message']


def test_rule_engine_evaluate_all_mixed_results(tmp_path):
    """Test evaluate_all with mix of passing and failing rules."""
    # Create one test file
    test_file = tmp_path / "exists.txt"
    test_file.write_text("content")
    
    engine = RuleEngine(str(tmp_path))
    rule1 = FileExistsRule("rule-1", "Existing file", "exists.txt")
    rule2 = FileExistsRule("rule-2", "Missing file", "missing.txt")
    engine.register_rule(rule1)
    engine.register_rule(rule2)
    
    results = engine.evaluate_all()
    
    assert len(results) == 2
    assert results[0]['passed'] is True
    assert results[1]['passed'] is False


def test_rule_engine_evaluate_all_error_handling(tmp_path):
    """Test evaluate_all handles evaluation errors gracefully."""
    engine = RuleEngine(str(tmp_path))
    
    # Create a rule that will raise an error during evaluation
    class BrokenRule(FileExistsRule):
        def evaluate(self, project_root):
            raise RuntimeError("Intentional test error")
    
    rule = BrokenRule("broken-rule", "Broken rule", "test.txt")
    engine.register_rule(rule)
    
    results = engine.evaluate_all()
    
    assert len(results) == 1
    assert results[0]['rule_id'] == 'broken-rule'
    assert results[0]['passed'] is False
    assert '⚠️' in results[0]['message']
    assert 'error' in results[0]
    assert results[0]['error'] is True


def test_rule_engine_create_rule_file_exists():
    """Test creating file_exists rule via factory."""
    rule_data = {
        'id': 'test-rule',
        'type': 'file_exists',
        'path': 'src/main.py',
        'description': 'Main file exists'
    }
    
    rule = RuleEngine.create_rule('file_exists', **rule_data)
    
    assert isinstance(rule, FileExistsRule)
    assert rule.id == 'test-rule'
    assert rule.path == 'src/main.py'


def test_rule_engine_create_rule_dependency_present():
    """Test creating dependency_present rule via factory."""
    rule_data = {
        'id': 'test-rule',
        'type': 'dependency_present',
        'file': 'requirements.txt',
        'package': 'requests',
        'description': 'Requests dependency'
    }
    
    rule = RuleEngine.create_rule('dependency_present', **rule_data)
    
    assert isinstance(rule, DependencyPresentRule)
    assert rule.id == 'test-rule'
    assert rule.package == 'requests'


def test_rule_engine_create_rule_text_includes():
    """Test creating text_includes rule via factory."""
    rule_data = {
        'id': 'test-rule',
        'type': 'text_includes',
        'file': 'src/config.py',
        'text': 'import React',
        'description': 'React import'
    }
    
    rule = RuleEngine.create_rule('text_includes', **rule_data)
    
    assert isinstance(rule, TextIncludesRule)
    assert rule.id == 'test-rule'
    assert rule.text == 'import React'


def test_rule_engine_create_rule_unknown_type():
    """Test create_rule raises ValueError for unknown type."""
    with pytest.raises(ValueError, match="Unknown rule type: 'invalid_type'"):
        RuleEngine.create_rule('invalid_type', id='test', description='test')


def test_rule_engine_rule_types_registry():
    """Test RULE_TYPES registry contains all rule types."""
    assert 'file_exists' in RuleEngine.RULE_TYPES
    assert 'dependency_present' in RuleEngine.RULE_TYPES
    assert 'text_includes' in RuleEngine.RULE_TYPES
    assert RuleEngine.RULE_TYPES['file_exists'] == FileExistsRule
    assert RuleEngine.RULE_TYPES['dependency_present'] == DependencyPresentRule
    assert RuleEngine.RULE_TYPES['text_includes'] == TextIncludesRule
