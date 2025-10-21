"""
Rule engine orchestration.

Manages rule registration, evaluation, and provides rule factory.
"""

from typing import List, Dict, Any
from .file_rules import FileExistsRule
from .dependency_rules import DependencyPresentRule
from .text_rules import TextIncludesRule
from . import BaseRule


class RuleEngine:
    """Orchestrates rule evaluation."""
    
    # Registry of rule types
    RULE_TYPES = {
        'file_exists': FileExistsRule,
        'dependency_present': DependencyPresentRule,
        'text_includes': TextIncludesRule,
    }
    
    def __init__(self, project_root: str):
        """
        Initialize rule engine.
        
        Args:
            project_root: Absolute path to project root directory
        """
        self.project_root = project_root
        self.rules: List[BaseRule] = []
    
    def register_rule(self, rule: BaseRule) -> None:
        """
        Register a rule for evaluation.
        
        Args:
            rule: Rule instance to register
        """
        self.rules.append(rule)
    
    def evaluate_all(self) -> List[Dict[str, Any]]:
        """
        Evaluate all registered rules.
        
        Returns:
            List of evaluation results, each containing:
                - rule_id: Rule identifier
                - rule_type: Type of rule
                - passed: Whether rule passed
                - message: Status message
                - details: Additional context
                - description: Rule description
        """
        results = []
        
        for rule in self.rules:
            try:
                evaluation = rule.evaluate(self.project_root)
                results.append({
                    'rule_id': rule.id,
                    'rule_type': rule.TYPE,
                    'description': rule.description,
                    'passed': evaluation['passed'],
                    'message': evaluation['message'],
                    'details': evaluation.get('details', ''),
                })
            except Exception as e:
                # Rule evaluation error - mark as error status
                results.append({
                    'rule_id': rule.id,
                    'rule_type': rule.TYPE,
                    'description': rule.description,
                    'passed': False,
                    'message': f"⚠️ Error evaluating rule",
                    'details': f"Error: {str(e)}",
                    'error': True,
                })
        
        return results
    
    @staticmethod
    def create_rule(rule_type: str, **kwargs) -> BaseRule:
        """
        Factory method to create appropriate rule type.
        
        Args:
            rule_type: "file_exists", "dependency_present", or "text_includes"
            **kwargs: Type-specific arguments (id, description, etc.)
        
        Returns:
            Instantiated rule object
        
        Raises:
            ValueError: If rule_type is unknown
        """
        rule_class = RuleEngine.RULE_TYPES.get(rule_type)
        
        if not rule_class:
            raise ValueError(
                f"Unknown rule type: '{rule_type}'. "
                f"Supported types: {', '.join(RuleEngine.RULE_TYPES.keys())}"
            )
        
        return rule_class.from_yaml(kwargs)


__all__ = ['RuleEngine']
