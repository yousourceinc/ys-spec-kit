"""
YAML rule parser.

Extracts and parses compliance rules from guide YAML frontmatter.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import re
import yaml


class RuleParseError(Exception):
    """Exception raised for rule parsing and validation errors."""
    pass


class RuleParser:
    """Parses YAML frontmatter from guide files."""
    
    # Define required and optional fields for each rule type
    RULE_TYPE_SCHEMAS = {
        'file_exists': {
            'required': ['id', 'type', 'description', 'path'],
            'optional': ['division']
        },
        'dependency_present': {
            'required': ['id', 'type', 'description', 'file', 'package'],
            'optional': ['version', 'division']
        },
        'text_includes': {
            'required': ['id', 'type', 'description', 'file', 'text'],
            'optional': ['case_sensitive', 'division']
        }
    }
    
    @staticmethod
    def extract_rules(guide_file: Path) -> List[Dict[str, Any]]:
        """
        Extract rules from YAML frontmatter of guide file.
        
        Args:
            guide_file: Path to markdown file with YAML frontmatter
        
        Returns:
            List of rule dictionaries
        
        Raises:
            RuleParseError: If rules cannot be extracted or are invalid
            FileNotFoundError: If guide file does not exist
        """
        if not guide_file.exists():
            raise FileNotFoundError(f"Guide file not found: {guide_file}")
        
        content = guide_file.read_text()
        frontmatter, _ = RuleParser.parse_frontmatter(content)
        
        if not frontmatter:
            return []  # No frontmatter, no rules
        
        rules = frontmatter.get('rules', [])
        
        if not isinstance(rules, list):
            raise RuleParseError(
                f"Invalid 'rules' field: expected list, got {type(rules).__name__}. "
                f"Ensure rules are defined as a YAML list:\nrules:\n  - id: rule-1\n    ..."
            )
        
        # Validate each rule
        for idx, rule in enumerate(rules):
            if not isinstance(rule, dict):
                raise RuleParseError(
                    f"Invalid rule at index {idx}: expected dict, got {type(rule).__name__}. "
                    f"Each rule must be a YAML object."
                )
            
            rule_type = rule.get('type')
            try:
                RuleParser.validate_rule_structure(rule, rule_type)
            except RuleParseError as e:
                # Add context about which rule failed
                rule_id = rule.get('id', f'<rule at index {idx}>')
                raise RuleParseError(f"Error in rule '{rule_id}': {str(e)}")
        
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
            RuleParseError: If frontmatter is malformed
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
            raise RuleParseError(
                f"Malformed YAML in frontmatter: {str(e)}\n"
                f"Ensure your frontmatter follows YAML syntax:\n"
                f"---\nkey: value\nrules:\n  - id: rule-1\n---"
            )
        
        if frontmatter is None:
            # Empty frontmatter
            return {}, remaining_content
        
        if not isinstance(frontmatter, dict):
            raise RuleParseError(
                f"Invalid frontmatter: expected YAML mapping (key: value pairs), "
                f"got {type(frontmatter).__name__}. "
                f"Frontmatter must be a YAML dictionary."
            )
        
        return frontmatter, remaining_content
    
    @staticmethod
    def validate_rule_structure(rule: Dict[str, Any], rule_type: Optional[str] = None) -> bool:
        """
        Validate that rule has all required fields for its type.
        
        Args:
            rule: Rule dictionary
            rule_type: Rule type (e.g., "file_exists"). If None, extracted from rule['type']
        
        Returns:
            True if valid
        
        Raises:
            RuleParseError: If required fields missing or invalid
        """
        if not isinstance(rule, dict):
            raise RuleParseError(f"Expected rule to be a dictionary, got {type(rule).__name__}")
        
        # Get rule type if not provided
        if rule_type is None:
            rule_type = rule.get('type')
        
        rule_id = rule.get('id', '<unknown>')
        
        # Validate common required fields
        if 'id' not in rule:
            raise RuleParseError("Missing required field 'id'. Every rule must have a unique identifier.")
        
        if 'type' not in rule:
            raise RuleParseError(
                f"Rule '{rule_id}' missing required field 'type'. "
                f"Supported types: {', '.join(RuleParser.RULE_TYPE_SCHEMAS.keys())}"
            )
        
        if 'description' not in rule:
            raise RuleParseError(
                f"Rule '{rule_id}' missing required field 'description'. "
                f"Provide a clear description of what this rule checks."
            )
        
        # Validate rule type is known
        if rule_type not in RuleParser.RULE_TYPE_SCHEMAS:
            valid_types = ', '.join(RuleParser.RULE_TYPE_SCHEMAS.keys())
            raise RuleParseError(
                f"Rule '{rule_id}' has unknown type '{rule_type}'. "
                f"Supported types: {valid_types}"
            )
        
        # Get schema for this rule type
        schema = RuleParser.RULE_TYPE_SCHEMAS[rule_type]
        
        # Check required fields for this type
        for required_field in schema['required']:
            if required_field not in rule:
                raise RuleParseError(
                    f"Rule '{rule_id}' of type '{rule_type}' missing required field '{required_field}'. "
                    f"Required fields: {', '.join(schema['required'])}"
                )
        
        # Type-specific validation
        if rule_type == 'file_exists':
            RuleParser._validate_file_exists_rule(rule, rule_id)
        elif rule_type == 'dependency_present':
            RuleParser._validate_dependency_present_rule(rule, rule_id)
        elif rule_type == 'text_includes':
            RuleParser._validate_text_includes_rule(rule, rule_id)
        
        return True
    
    @staticmethod
    def _validate_file_exists_rule(rule: Dict[str, Any], rule_id: str) -> None:
        """Validate file_exists rule."""
        path = rule.get('path')
        if not isinstance(path, str):
            raise RuleParseError(
                f"Rule '{rule_id}': 'path' must be a string, got {type(path).__name__}. "
                f"Example: path: 'src/main.py'"
            )
        if not path.strip():
            raise RuleParseError(f"Rule '{rule_id}': 'path' cannot be empty")
    
    @staticmethod
    def _validate_dependency_present_rule(rule: Dict[str, Any], rule_id: str) -> None:
        """Validate dependency_present rule."""
        file_path = rule.get('file')
        if not isinstance(file_path, str):
            raise RuleParseError(
                f"Rule '{rule_id}': 'file' must be a string, got {type(file_path).__name__}. "
                f"Example: file: 'package.json'"
            )
        if not file_path.strip():
            raise RuleParseError(f"Rule '{rule_id}': 'file' cannot be empty")
        
        package = rule.get('package')
        if not isinstance(package, str):
            raise RuleParseError(
                f"Rule '{rule_id}': 'package' must be a string, got {type(package).__name__}. "
                f"Example: package: 'express'"
            )
        if not package.strip():
            raise RuleParseError(f"Rule '{rule_id}': 'package' cannot be empty")
    
    @staticmethod
    def _validate_text_includes_rule(rule: Dict[str, Any], rule_id: str) -> None:
        """Validate text_includes rule."""
        file_path = rule.get('file')
        if not isinstance(file_path, str):
            raise RuleParseError(
                f"Rule '{rule_id}': 'file' must be a string, got {type(file_path).__name__}. "
                f"Example: file: 'README.md'"
            )
        if not file_path.strip():
            raise RuleParseError(f"Rule '{rule_id}': 'file' cannot be empty")
        
        text = rule.get('text')
        if not isinstance(text, str):
            raise RuleParseError(
                f"Rule '{rule_id}': 'text' must be a string, got {type(text).__name__}. "
                f"Example: text: 'License:'"
            )
        if not text.strip():
            raise RuleParseError(f"Rule '{rule_id}': 'text' cannot be empty")


__all__ = ['RuleParser', 'RuleParseError']
