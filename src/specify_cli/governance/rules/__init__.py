"""
Rule engine for compliance checking.

Provides base rule abstraction and rule registry for governance compliance.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseRule(ABC):
    """Abstract base class for all compliance rule types."""
    
    TYPE: str = ""  # Override in subclasses
    
    def __init__(self, rule_id: str, description: str, **kwargs):
        """
        Initialize a compliance rule.
        
        Args:
            rule_id: Unique identifier for the rule (e.g., "api-routes-defined")
            description: Human-readable explanation of the rule
            **kwargs: Type-specific rule data
        """
        self.id = rule_id
        self.description = description
        self.rule_data = kwargs
    
    @abstractmethod
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Evaluate rule against project codebase.
        
        Args:
            project_root: Absolute path to project root directory
        
        Returns:
            Dictionary with keys:
                - passed (bool): True if rule requirement satisfied
                - message (str): Status message for display
                - details (str, optional): Additional context
        """
        pass
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> 'BaseRule':
        """
        Factory method to create rule from YAML dictionary.
        
        Args:
            data: Parsed YAML rule definition
        
        Returns:
            Instantiated rule object
        
        Raises:
            ValueError: If required fields are missing or invalid
        """
        rule_id = data.get('id')
        description = data.get('description')
        
        if not rule_id:
            raise ValueError("Rule missing required field: 'id'")
        if not description:
            raise ValueError(f"Rule '{rule_id}' missing required field: 'description'")
        
        # Extract type-specific fields (subclasses override)
        return cls(rule_id, description, **data)


__all__ = ['BaseRule']
