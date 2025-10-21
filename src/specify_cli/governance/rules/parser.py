"""
YAML rule parser.

Extracts and parses compliance rules from guide YAML frontmatter.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
import yaml


class RuleParser:
    """Parses YAML frontmatter from guide files."""
    
    @staticmethod
    def extract_rules(guide_file: Path) -> List[Dict[str, Any]]:
        """
        Extract rules from YAML frontmatter of guide file.
        
        Args:
            guide_file: Path to markdown file with YAML frontmatter
        
        Returns:
            List of rule dictionaries
        
        Raises:
            ValueError: If YAML is malformed
            KeyError: If required rule fields missing
        """
        if not guide_file.exists():
            raise FileNotFoundError(f"Guide file not found: {guide_file}")
        
        content = guide_file.read_text()
        frontmatter, _ = RuleParser.parse_frontmatter(content)
        
        if not frontmatter:
            return []  # No frontmatter, no rules
        
        rules = frontmatter.get('rules', [])
        
        if not isinstance(rules, list):
            raise ValueError(f"'rules' in frontmatter must be a list, got {type(rules).__name__}")
        
        return rules
    
    @staticmethod
    def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content.
        
        Args:
            content: Markdown file content
        
        Returns:
            Tuple of (frontmatter_dict, remaining_content)
        
        Raises:
            ValueError: If frontmatter is malformed
        """
        # Match YAML frontmatter: ---\n...\n---
        frontmatter_pattern = re.compile(
            r'^---\s*\n(.*?)\n---\s*\n',
            re.DOTALL | re.MULTILINE
        )
        
        match = frontmatter_pattern.match(content)
        
        if not match:
            return {}, content  # No frontmatter
        
        yaml_content = match.group(1)
        remaining_content = content[match.end():]
        
        try:
            frontmatter = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Malformed YAML in frontmatter: {str(e)}")
        
        if not isinstance(frontmatter, dict):
            raise ValueError(f"Frontmatter must be a YAML dictionary, got {type(frontmatter).__name__}")
        
        return frontmatter, remaining_content
    
    @staticmethod
    def validate_rule_structure(rule: Dict[str, Any], rule_type: str) -> bool:
        """
        Validate that rule has all required fields for its type.
        
        Args:
            rule: Rule dictionary
            rule_type: Rule type (e.g., "file_exists")
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If required fields missing or invalid
        """
        # Common required fields
        if 'id' not in rule:
            raise ValueError("Rule missing required field: 'id'")
        if 'description' not in rule:
            raise ValueError(f"Rule '{rule['id']}' missing required field: 'description'")
        if 'type' not in rule:
            raise ValueError(f"Rule '{rule['id']}' missing required field: 'type'")
        
        # Type-specific required fields
        if rule_type == 'file_exists':
            if 'path' not in rule:
                raise ValueError(f"Rule '{rule['id']}' of type 'file_exists' missing required field: 'path'")
        
        elif rule_type == 'dependency_present':
            if 'file' not in rule:
                raise ValueError(f"Rule '{rule['id']}' of type 'dependency_present' missing required field: 'file'")
            if 'package' not in rule:
                raise ValueError(f"Rule '{rule['id']}' of type 'dependency_present' missing required field: 'package'")
        
        elif rule_type == 'text_includes':
            if 'file' not in rule:
                raise ValueError(f"Rule '{rule['id']}' of type 'text_includes' missing required field: 'file'")
            if 'text' not in rule:
                raise ValueError(f"Rule '{rule['id']}' of type 'text_includes' missing required field: 'text'")
        
        return True


__all__ = ['RuleParser']
