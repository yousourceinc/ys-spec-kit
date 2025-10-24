"""
File-based compliance rules.

Implements rules that check for file existence in the project.
"""

from pathlib import Path
from typing import Dict, Any
from . import BaseRule


class FileExistsRule(BaseRule):
    """Checks if a file exists in project."""
    
    TYPE = "file_exists"
    
    def __init__(self, rule_id: str, description: str, path: str, **kwargs):
        """
        Initialize file existence rule.
        
        Args:
            rule_id: Unique rule identifier
            description: Human-readable rule description
            path: File path to check (relative to project root)
            **kwargs: Additional rule data
        """
        super().__init__(rule_id, description, path=path, **kwargs)
        self.path = path
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if file exists at given path.
        
        Args:
            project_root: Absolute path to project root
        
        Returns:
            Dictionary with:
                - passed (bool): True if file exists
                - message (str): "✅ File exists" or "❌ File not found"
                - details (str): Full path checked
        """
        project_path = Path(project_root)
        file_path = project_path / self.path
        
        exists = file_path.exists()
        
        return {
            "passed": exists,
            "message": f"✅ File exists at {self.path}" if exists else f"❌ File not found at {self.path}",
            "details": f"Checked path: {file_path}"
        }
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> 'FileExistsRule':
        """
        Create FileExistsRule from YAML data.
        
        Args:
            data: Parsed YAML rule definition
        
        Returns:
            FileExistsRule instance
        
        Raises:
            ValueError: If 'path' field is missing
        """
        rule_id = data.get('id')
        description = data.get('description')
        path = data.get('path')
        
        if not rule_id:
            raise ValueError("Rule missing required field: 'id'")
        if not description:
            raise ValueError(f"Rule '{rule_id}' missing required field: 'description'")
        if not path:
            raise ValueError(f"Rule '{rule_id}' of type 'file_exists' missing required field: 'path'")
        
        return cls(rule_id, description, path)


__all__ = ['FileExistsRule']
