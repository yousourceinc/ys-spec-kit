"""
Unit tests for BaseRule abstract class.
"""

import pytest
from specify_cli.governance.rules import BaseRule


class ConcreteRule(BaseRule):
    """Concrete implementation for testing BaseRule."""
    
    TYPE = "test_rule"
    
    def evaluate(self, project_root: str):
        return {
            "passed": True,
            "message": "Test passed",
            "details": "Test details"
        }


def test_base_rule_initialization():
    """Test BaseRule initialization with required fields."""
    rule = ConcreteRule("test-id", "Test description", extra_field="extra_value")
    
    assert rule.id == "test-id"
    assert rule.description == "Test description"
    assert rule.rule_data['extra_field'] == "extra_value"


def test_base_rule_from_yaml_missing_id():
    """Test from_yaml raises ValueError when id is missing."""
    data = {
        'description': 'Test description'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'id'"):
        ConcreteRule.from_yaml(data)


def test_base_rule_from_yaml_missing_description():
    """Test from_yaml raises ValueError when description is missing."""
    data = {
        'id': 'test-rule'
    }
    
    with pytest.raises(ValueError, match="missing required field: 'description'"):
        ConcreteRule.from_yaml(data)


def test_base_rule_evaluate_abstract():
    """Test that BaseRule.evaluate is abstract."""
    # Attempting to instantiate BaseRule directly should fail
    with pytest.raises(TypeError):
        BaseRule("test-id", "Test description")


def test_base_rule_type_constant():
    """Test TYPE constant is defined."""
    assert hasattr(ConcreteRule, 'TYPE')
    assert ConcreteRule.TYPE == "test_rule"
