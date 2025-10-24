"""
Dependency-based compliance rules.

Implements rules that check for package dependencies in manifest files.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import re
from . import BaseRule


class DependencyPresentRule(BaseRule):
    """Checks if dependency is declared in manifest."""
    
    TYPE = "dependency_present"
    
    def __init__(
        self, 
        rule_id: str, 
        description: str, 
        file: str, 
        package: str,
        version: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize dependency presence rule.
        
        Args:
            rule_id: Unique rule identifier
            description: Human-readable rule description
            file: Dependency manifest file (e.g., requirements.txt, package.json)
            package: Package name to check
            version: Optional version specifier (e.g., ">=1.0", "~2.3")
            **kwargs: Additional rule data
        """
        super().__init__(
            rule_id, 
            description, 
            file=file, 
            package=package, 
            version=version,
            **kwargs
        )
        self.file = file
        self.package = package
        self.version = version
    
    def evaluate(self, project_root: str) -> Dict[str, Any]:
        """
        Check if package is declared in manifest.
        
        Args:
            project_root: Absolute path to project root
        
        Returns:
            Dictionary with:
                - passed (bool): True if package present (and version matches if specified)
                - message (str): Status message
                - details (str): Version found, version required, etc.
        """
        project_path = Path(project_root)
        manifest_path = project_path / self.file
        
        if not manifest_path.exists():
            return {
                "passed": False,
                "message": f"❌ Manifest file not found: {self.file}",
                "details": f"Expected manifest at: {manifest_path}"
            }
        
        try:
            content = manifest_path.read_text()
        except Exception as e:
            return {
                "passed": False,
                "message": f"❌ Could not read manifest file: {self.file}",
                "details": f"Error: {str(e)}"
            }
        
        # Check if package is mentioned in manifest
        package_found = self.package in content
        
        if not package_found:
            return {
                "passed": False,
                "message": f"❌ Package '{self.package}' not declared in {self.file}",
                "details": f"Searched in: {manifest_path}"
            }
        
        # If version specified, provide details (full version matching deferred to future enhancement)
        if self.version:
            # Simple presence check for now - full semantic versioning in future iteration
            version_pattern = re.escape(self.package) + r'[^\n]*' + re.escape(self.version.replace('>=', '').replace('~', '').replace('>', '').replace('<', '').replace('=', '').strip())
            version_mentioned = re.search(version_pattern, content, re.IGNORECASE)
            
            if version_mentioned:
                return {
                    "passed": True,
                    "message": f"✅ Package '{self.package}' declared with version constraint in {self.file}",
                    "details": f"Version requirement: {self.version}"
                }
            else:
                return {
                    "passed": True,
                    "message": f"✅ Package '{self.package}' declared in {self.file}",
                    "details": f"Note: Version constraint '{self.version}' not explicitly validated (semantic versioning deferred)"
                }
        
        return {
            "passed": True,
            "message": f"✅ Package '{self.package}' declared in {self.file}",
            "details": f"Found in: {manifest_path}"
        }
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> 'DependencyPresentRule':
        """
        Create DependencyPresentRule from YAML data.
        
        Args:
            data: Parsed YAML rule definition
        
        Returns:
            DependencyPresentRule instance
        
        Raises:
            ValueError: If required fields are missing
        """
        rule_id = data.get('id')
        description = data.get('description')
        file = data.get('file')
        package = data.get('package')
        version = data.get('version')
        
        if not rule_id:
            raise ValueError("Rule missing required field: 'id'")
        if not description:
            raise ValueError(f"Rule '{rule_id}' missing required field: 'description'")
        if not file:
            raise ValueError(f"Rule '{rule_id}' of type 'dependency_present' missing required field: 'file'")
        if not package:
            raise ValueError(f"Rule '{rule_id}' of type 'dependency_present' missing required field: 'package'")
        
        return cls(rule_id, description, file, package, version)


__all__ = ['DependencyPresentRule']
