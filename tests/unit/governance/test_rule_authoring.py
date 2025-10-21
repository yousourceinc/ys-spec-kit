"""
Unit tests for rule authoring and validation enhancements.

Tests the enhanced RuleParser with comprehensive validation, better error messages,
and support for embedded rules in guides.
"""

import pytest
from pathlib import Path
from specify_cli.governance.rules.parser import RuleParser, RuleParseError


class TestRuleValidationEnhanced:
    """Tests for enhanced rule validation with detailed error messages."""
    
    def test_validate_unknown_rule_type(self):
        """Test validation fails for unknown rule type."""
        rule = {
            'id': 'test-rule',
            'type': 'unknown_type',
            'description': 'Test',
        }
        
        with pytest.raises(RuleParseError, match="unknown type"):
            RuleParser.validate_rule_structure(rule)
    
    def test_validate_invalid_field_type_file_exists(self):
        """Test validation fails when field has wrong type."""
        rule = {
            'id': 'test-rule',
            'type': 'file_exists',
            'description': 'Test',
            'path': 123  # Should be string
        }
        
        with pytest.raises(RuleParseError, match="path.*must be a string"):
            RuleParser.validate_rule_structure(rule)
    
    def test_validate_empty_field_path(self):
        """Test validation fails when path is empty string."""
        rule = {
            'id': 'test-rule',
            'type': 'file_exists',
            'description': 'Test',
            'path': ''
        }
        
        with pytest.raises(RuleParseError, match="path.*cannot be empty"):
            RuleParser.validate_rule_structure(rule)
    
    def test_validate_empty_field_package(self):
        """Test validation fails when package is empty string."""
        rule = {
            'id': 'test-rule',
            'type': 'dependency_present',
            'description': 'Test',
            'file': 'requirements.txt',
            'package': ''
        }
        
        with pytest.raises(RuleParseError, match="package.*cannot be empty"):
            RuleParser.validate_rule_structure(rule)
    
    def test_validate_empty_field_text(self):
        """Test validation fails when text is empty string."""
        rule = {
            'id': 'test-rule',
            'type': 'text_includes',
            'description': 'Test',
            'file': 'README.md',
            'text': ''
        }
        
        with pytest.raises(RuleParseError, match="text.*cannot be empty"):
            RuleParser.validate_rule_structure(rule)
    
    def test_validate_with_optional_fields(self):
        """Test validation succeeds with optional fields."""
        rule = {
            'id': 'test-rule',
            'type': 'dependency_present',
            'description': 'Test with optional version',
            'file': 'requirements.txt',
            'package': 'pytest',
            'version': '>=7.0'  # Optional field
        }
        
        assert RuleParser.validate_rule_structure(rule) is True
    
    def test_validate_text_includes_with_case_sensitivity(self):
        """Test text_includes rule with case_sensitive option."""
        rule = {
            'id': 'test-rule',
            'type': 'text_includes',
            'description': 'Case insensitive search',
            'file': 'README.md',
            'text': 'License',
            'case_sensitive': False  # Optional field
        }
        
        assert RuleParser.validate_rule_structure(rule) is True


class TestMultipleRulesExtraction:
    """Tests for extracting multiple rules from a single guide."""
    
    def test_extract_multiple_rules_from_guide(self, tmp_path):
        """Test extracting multiple different rule types from one guide."""
        guide_content = """---
title: "Multi-Rule Guide"
division: "SE"
rules:
  - id: file-check
    type: file_exists
    path: src/main.py
    description: "Main file required"
  
  - id: dep-check
    type: dependency_present
    file: requirements.txt
    package: pytest
    version: ">=7.0"
    description: "Testing framework required"
  
  - id: text-check
    type: text_includes
    file: README.md
    text: "License"
    case_sensitive: false
    description: "License in README"
---

# Multi-Rule Guide
"""
        
        guide_file = tmp_path / "guide.md"
        guide_file.write_text(guide_content)
        
        rules = RuleParser.extract_rules(guide_file)
        
        assert len(rules) == 3
        assert rules[0]['id'] == 'file-check'
        assert rules[1]['id'] == 'dep-check'
        assert rules[2]['id'] == 'text-check'
        assert rules[1]['version'] == '>=7.0'
        assert rules[2]['case_sensitive'] is False
    
    def test_extract_rules_validates_all_rules(self, tmp_path):
        """Test that extraction validates all rules and reports errors."""
        guide_content = """---
title: "Invalid Multi-Rule Guide"
division: "SE"
rules:
  - id: valid-rule
    type: file_exists
    path: src/main.py
    description: "Valid rule"
  
  - id: invalid-rule
    type: file_exists
    description: "Missing path field"
---

# Multi-Rule Guide
"""
        
        guide_file = tmp_path / "guide.md"
        guide_file.write_text(guide_content)
        
        with pytest.raises(RuleParseError, match="Error in rule 'invalid-rule'"):
            RuleParser.extract_rules(guide_file)
    
    def test_extract_rules_from_complex_guide(self, tmp_path):
        """Test extracting rules from a realistic, complex guide."""
        guide_content = """---
title: "Python Backend Standards"
division: "SE"
description: "Standards for Python backend implementation"

rules:
  - id: python-main-module
    type: file_exists
    description: "Main module must exist"
    path: "src/main.py"
  
  - id: pytest-required
    type: dependency_present
    description: "pytest required for testing"
    file: "requirements.txt"
    package: "pytest"
  
  - id: tests-directory
    type: file_exists
    description: "Tests must be organized"
    path: "tests/"
  
  - id: readme-has-setup
    type: text_includes
    description: "README must have setup"
    file: "README.md"
    text: "Setup"
    case_sensitive: false
  
  - id: license-header
    type: text_includes
    description: "License in source"
    file: "src/main.py"
    text: "Copyright"
    case_sensitive: false
---

# Python Backend Standards

Standard compliance guide for Python backends.
"""
        
        guide_file = tmp_path / "guide.md"
        guide_file.write_text(guide_content)
        
        rules = RuleParser.extract_rules(guide_file)
        
        assert len(rules) == 5
        assert all(rule.get('id') for rule in rules)
        assert all(rule.get('description') for rule in rules)
        assert all(rule.get('type') for rule in rules)


class TestRuleParsingEdgeCases:
    """Tests for edge cases in rule parsing."""
    
    def test_rule_with_special_characters_in_path(self, tmp_path):
        """Test rule with special characters in path."""
        rule = {
            'id': 'special-path',
            'type': 'file_exists',
            'description': 'File with special chars',
            'path': 'src/my-module_v2.0/file[test].py'
        }
        
        assert RuleParser.validate_rule_structure(rule) is True
    
    def test_rule_with_unicode_in_description(self, tmp_path):
        """Test rule with unicode characters."""
        rule = {
            'id': 'unicode-rule',
            'type': 'file_exists',
            'description': 'Unicode description: 你好世界 🚀',
            'path': 'src/main.py'
        }
        
        assert RuleParser.validate_rule_structure(rule) is True
    
    def test_rule_with_multiline_description(self):
        """Test rule with multiline description."""
        rule = {
            'id': 'multiline-rule',
            'type': 'file_exists',
            'description': '''Multiline description
spanning multiple lines
with details about the rule''',
            'path': 'src/main.py'
        }
        
        assert RuleParser.validate_rule_structure(rule) is True
    
    def test_extract_rules_with_null_values(self, tmp_path):
        """Test handling of null values in rules."""
        guide_content = """---
title: "Guide with nulls"
division: "SE"
rules:
  - id: test-rule
    type: file_exists
    path: src/main.py
    description: "Test"
    optional_field: null
---

# Guide
"""
        
        guide_file = tmp_path / "guide.md"
        guide_file.write_text(guide_content)
        
        rules = RuleParser.extract_rules(guide_file)
        assert len(rules) == 1
        assert rules[0]['optional_field'] is None


class TestRuleErrorMessages:
    """Tests for quality and usefulness of error messages."""
    
    def test_error_message_includes_rule_id(self):
        """Test that error messages include the rule ID for context."""
        rule = {
            'id': 'my-important-rule',
            'type': 'file_exists',
            'description': 'Test'
        }
        
        try:
            RuleParser.validate_rule_structure(rule)
            assert False, "Should have raised"
        except RuleParseError as e:
            assert 'my-important-rule' in str(e)
    
    def test_error_message_suggests_fix(self):
        """Test that error messages provide guidance on fixing issues."""
        rule = {
            'id': 'test',
            'type': 'invalid_type',
            'description': 'Test'
        }
        
        try:
            RuleParser.validate_rule_structure(rule)
            assert False, "Should have raised"
        except RuleParseError as e:
            error_msg = str(e)
            # Should mention valid types
            assert 'file_exists' in error_msg or 'Supported types' in error_msg
    
    def test_error_message_lists_required_fields(self):
        """Test that error messages include required fields for rule type."""
        rule = {
            'id': 'test',
            'type': 'dependency_present',
            'description': 'Test'
        }
        
        try:
            RuleParser.validate_rule_structure(rule)
            assert False, "Should have raised"
        except RuleParseError as e:
            # Should mention required fields
            assert 'Required fields' in str(e) or 'file' in str(e) or 'package' in str(e)


class TestRuleSyntaxValidation:
    """Tests for comprehensive rule syntax validation."""
    
    def test_rule_id_validation(self):
        """Test that rule IDs are required."""
        rule = {
            'type': 'file_exists',
            'path': 'test.txt',
            'description': 'Test'
        }
        
        with pytest.raises(RuleParseError, match="'id'"):
            RuleParser.validate_rule_structure(rule)
    
    def test_rule_type_validation(self):
        """Test that rule type is required and must be known."""
        rule = {
            'id': 'test',
            'path': 'test.txt',
            'description': 'Test'
        }
        
        with pytest.raises(RuleParseError, match="'type'"):
            RuleParser.validate_rule_structure(rule)
    
    def test_rule_description_validation(self):
        """Test that description is required."""
        rule = {
            'id': 'test',
            'type': 'file_exists',
            'path': 'test.txt'
        }
        
        with pytest.raises(RuleParseError, match="'description'"):
            RuleParser.validate_rule_structure(rule)
    
    def test_all_rule_types_supported(self):
        """Test that all documented rule types are supported."""
        valid_types = ['file_exists', 'dependency_present', 'text_includes']
        
        for rule_type in valid_types:
            if rule_type == 'file_exists':
                rule = {
                    'id': f'test-{rule_type}',
                    'type': rule_type,
                    'description': 'Test',
                    'path': 'test.txt'
                }
            elif rule_type == 'dependency_present':
                rule = {
                    'id': f'test-{rule_type}',
                    'type': rule_type,
                    'description': 'Test',
                    'file': 'requirements.txt',
                    'package': 'pytest'
                }
            elif rule_type == 'text_includes':
                rule = {
                    'id': f'test-{rule_type}',
                    'type': rule_type,
                    'description': 'Test',
                    'file': 'test.txt',
                    'text': 'pattern'
                }
            
            assert RuleParser.validate_rule_structure(rule) is True


class TestDivisionAwareness:
    """Tests for division field support in rules."""
    
    def test_rule_with_division_field(self):
        """Test that rules support optional division field."""
        rule = {
            'id': 'test-rule',
            'type': 'file_exists',
            'path': 'src/main.py',
            'description': 'Test',
            'division': 'SE'  # Optional field
        }
        
        assert RuleParser.validate_rule_structure(rule) is True
    
    def test_extract_rules_with_division(self, tmp_path):
        """Test extracting rules that specify division."""
        guide_content = """---
title: "SE Division Guide"
division: "SE"
rules:
  - id: se-rule-1
    type: file_exists
    path: src/main.py
    description: "SE specific rule"
    division: "SE"
  
  - id: se-rule-2
    type: file_exists
    path: docs/guide.md
    description: "SE documentation rule"
    division: "SE"
---

# SE Division Guide
"""
        
        guide_file = tmp_path / "guide.md"
        guide_file.write_text(guide_content)
        
        rules = RuleParser.extract_rules(guide_file)
        
        assert len(rules) == 2
        assert all(rule.get('division') == 'SE' for rule in rules)

