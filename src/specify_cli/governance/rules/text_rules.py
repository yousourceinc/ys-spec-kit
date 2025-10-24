"""
Text pattern compliance rules.

Implements rules that check for text patterns in files.
"""

from pathlib import Path
from typing import Dict, Any
from . import BaseRule


class TextIncludesRule(BaseRule):
    """Checks if text pattern appears in file."""
    
    TYPE = "text_includes"
    
    def __init__(
        self, 
        rule_id: str, 
        description: str, 
        file: str, 
        text: str,
        case_sensitive: bool = True,
        **kwargs
    ):
        """
        Initialize text inclusion rule.
        
        Args:
            rule_id: Unique rule identifier
            description: Human-readable rule description
            file: File path to search
            text: Text pattern to find
            case_sensitive: Whether search is case-sensitive (default: True)
            **kwargs: Additional rule data
        """
        super().__init__(
            rule_id, 
            description, 
            file=file, 
            text=text, 
            case_sensitive=case_sensitive,
            **kwargs
        )
        self.file = file
        self.text = text
        self.case_sensitive = case_sensitive
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if text pattern appears in file.
        
        Args:
            project_root: Absolute path to project root
        
        Returns:
            Dictionary with:
                - passed (bool): True if pattern found
                - message (str): Status message
                - details (str): Number of occurrences, line number (if available)
        """
        project_path = Path(project_root)
        file_path = project_path / self.file
        
        if not file_path.exists():
            return {
                "passed": False,
                "message": f"❌ File not found: {self.file}",
                "details": f"Expected file at: {file_path}"
            }
        
        try:
            content = file_path.read_text()
        except Exception as e:
            return {
                "passed": False,
                "message": f"❌ Could not read file: {self.file}",
                "details": f"Error: {str(e)}"
            }
        
        # Search for text pattern
        search_content = content if self.case_sensitive else content.lower()
        search_text = self.text if self.case_sensitive else self.text.lower()
        
        if search_text in search_content:
            # Count occurrences
            occurrences = search_content.count(search_text)
            return {
                "passed": True,
                "message": f"✅ Pattern found in {self.file}",
                "details": f"Pattern '{self.text}' found ({occurrences} occurrence{'s' if occurrences != 1 else ''})"
            }
        else:
            return {
                "passed": False,
                "message": f"❌ Pattern not found in {self.file}",
                "details": f"Searched for: '{self.text}' (case {'sensitive' if self.case_sensitive else 'insensitive'})"
            }
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> 'TextIncludesRule':
        """
        Create TextIncludesRule from YAML data.
        
        Args:
            data: Parsed YAML rule definition
        
        Returns:
            TextIncludesRule instance
        
        Raises:
            ValueError: If required fields are missing
        """
        rule_id = data.get('id')
        description = data.get('description')
        file = data.get('file')
        text = data.get('text')
        case_sensitive = data.get('case_sensitive', True)  # Default to case-sensitive
        
        if not rule_id:
            raise ValueError("Rule missing required field: 'id'")
        if not description:
            raise ValueError(f"Rule '{rule_id}' missing required field: 'description'")
        if not file:
            raise ValueError(f"Rule '{rule_id}' of type 'text_includes' missing required field: 'file'")
        if not text:
            raise ValueError(f"Rule '{rule_id}' of type 'text_includes' missing required field: 'text'")
        
        return cls(rule_id, description, file, text, case_sensitive)


__all__ = ['TextIncludesRule']
