"""
Unit tests for compliance checking module.

Tests cover:
- Rule evaluation results
- Compliance checking workflow
- Guide discovery
- Waiver cross-referencing
- Report generation
"""

import pytest
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

from specify_cli.governance.compliance import (
    ComplianceChecker,
    RuleEvaluationResult,
    RuleStatus
)
from specify_cli.governance.report import ComplianceReportGenerator
from specify_cli.governance.waiver import WaiverManager


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_with_guides(temp_project_dir):
    """Create temp project with sample guides."""
    guides_dir = temp_project_dir / "context" / "references"
    guides_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample guide with rules
    guide_content = """---
title: "Backend API Implementation"
division: "SE"
rules:
  - id: api-routes-defined
    type: file_exists
    path: "src/api/routes.py"
    description: "API routes module required"
  
  - id: tests-present
    type: file_exists
    path: "tests/api/test_routes.py"
    description: "API tests required"
---

# Backend API Implementation Guide

Implement API routes with proper testing.
"""
    
    guide_file = guides_dir / "backend-api.md"
    guide_file.write_text(guide_content)
    
    return temp_project_dir


class TestRuleEvaluationResult:
    """Tests for RuleEvaluationResult data class."""
    
    def test_result_initialization(self):
        """Test basic result initialization."""
        result = RuleEvaluationResult(
            rule_id="test-rule",
            rule_type="file_exists",
            status=RuleStatus.PASS,
            message="Test message",
            target="test/file.py",
            guide_id="test-guide"
        )
        assert result.rule_id == "test-rule"
        assert result.status == RuleStatus.PASS
    
    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        result = RuleEvaluationResult(
            rule_id="test-rule",
            rule_type="file_exists",
            status=RuleStatus.FAIL,
            message="Test message",
            target="test/file.py",
            guide_id="test-guide",
            waiver_id="W-001"
        )
        result_dict = result.to_dict()
        assert result_dict["rule_id"] == "test-rule"
        assert result_dict["status"] == "fail"
        assert result_dict["waiver_id"] == "W-001"
    
    def test_result_status_emoji(self):
        """Test status emoji generation."""
        test_cases = [
            (RuleStatus.PASS, "✅"),
            (RuleStatus.FAIL, "❌"),
            (RuleStatus.WAIVED, "🚫"),
            (RuleStatus.ERROR, "⚠️")
        ]
        
        for status, expected_emoji in test_cases:
            result = RuleEvaluationResult(
                rule_id="test",
                rule_type="test",
                status=status,
                message="test",
                target="test",
                guide_id="test"
            )
            assert result.status_emoji() == expected_emoji
    
    def test_result_timestamp_format(self):
        """Test that timestamp is ISO-8601 format."""
        result = RuleEvaluationResult(
            rule_id="test",
            rule_type="test",
            status=RuleStatus.PASS,
            message="test",
            target="test",
            guide_id="test"
        )
        # Verify ISO-8601 format
        assert len(result.timestamp) == 20
        assert "T" in result.timestamp
        assert result.timestamp.endswith("Z")


class TestComplianceChecker:
    """Tests for ComplianceChecker."""
    
    def test_checker_initialization(self, temp_project_dir):
        """Test checker initialization."""
        checker = ComplianceChecker(project_root=temp_project_dir)
        assert checker.project_root == temp_project_dir
        assert checker.rule_engine is not None
        assert checker.rule_parser is not None
    
    def test_discover_guides_empty(self, temp_project_dir):
        """Test guide discovery with no guides."""
        checker = ComplianceChecker(project_root=temp_project_dir)
        guides = checker._discover_guides()
        assert guides == []
    
    def test_discover_guides_in_context(self, temp_with_guides):
        """Test guide discovery finds guides in context/references."""
        checker = ComplianceChecker(project_root=temp_with_guides)
        guides = checker._discover_guides()
        assert len(guides) > 0
        assert any("backend-api.md" in str(g) for g in guides)
    
    def test_build_waiver_map(self, temp_project_dir):
        """Test building waiver map for rule lookup."""
        from specify_cli.governance.waiver import Waiver
        
        waivers = [
            Waiver("W-001", "test", "2025-10-21T10:00:00Z", related_rules=["rule-1", "rule-2"]),
            Waiver("W-002", "test", "2025-10-21T11:00:00Z", related_rules=["rule-3"])
        ]
        
        checker = ComplianceChecker(project_root=temp_project_dir)
        waiver_map = checker._build_waiver_map(waivers)
        
        assert "rule-1" in waiver_map
        assert "rule-2" in waiver_map
        assert "rule-3" in waiver_map
        assert waiver_map["rule-1"].waiver_id == "W-001"
        assert waiver_map["rule-3"].waiver_id == "W-002"
    
    def test_extract_guide_id(self, temp_project_dir):
        """Test extracting guide ID from path."""
        checker = ComplianceChecker(project_root=temp_project_dir)
        guide_path = Path("/path/to/backend-api.md")
        guide_id = checker._extract_guide_id(guide_path)
        assert guide_id == "backend-api"


class TestComplianceReportGenerator:
    """Tests for ComplianceReportGenerator."""
    
    def test_generator_initialization(self, temp_project_dir):
        """Test generator initialization."""
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        assert generator.project_root == temp_project_dir
    
    def test_generate_report_header(self, temp_project_dir):
        """Test report header generation."""
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        header = generator.generate_report_header("Test Project", "main")
        
        assert "# Compliance Report" in header
        assert "Test Project" in header
        assert "main" in header
        assert "Generated" in header
    
    def test_generate_summary_section_empty(self, temp_project_dir):
        """Test summary generation with no results."""
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        summary = generator.generate_summary_section([])
        
        assert "## Summary" in summary
        assert "NO RULES" in summary
    
    def test_generate_summary_section_all_passed(self, temp_project_dir):
        """Test summary with all rules passed."""
        results = [
            RuleEvaluationResult(
                rule_id=f"rule-{i}",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="test"
            )
            for i in range(3)
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        summary = generator.generate_summary_section(results)
        
        assert "COMPLIANT" in summary
        assert "✅ Passed | 3" in summary
        assert "❌ Failed | 0" in summary
    
    def test_generate_summary_section_with_failures(self, temp_project_dir):
        """Test summary with failures."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="test"
            ),
            RuleEvaluationResult(
                rule_id="rule-2",
                rule_type="file_exists",
                status=RuleStatus.FAIL,
                message="Failed",
                target="test",
                guide_id="test"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        summary = generator.generate_summary_section(results)
        
        assert "PARTIAL" in summary
        assert "❌ Failed | 1" in summary
    
    def test_generate_checked_guides_section(self, temp_project_dir):
        """Test guides section generation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="backend-api"
            ),
            RuleEvaluationResult(
                rule_id="rule-2",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="database-schema"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        section = generator.generate_checked_guides_section(results)
        
        assert "## Guides Checked" in section
        assert "backend-api" in section
        assert "database-schema" in section
    
    def test_generate_passed_rules_section(self, temp_project_dir):
        """Test passed rules section generation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="File found",
                target="src/main.py",
                guide_id="backend"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        section = generator.generate_passed_rules_section(results)
        
        assert "## ✅ Passed Rules" in section
        assert "rule-1" in section
        assert "File found" in section
    
    def test_generate_failed_rules_section(self, temp_project_dir):
        """Test failed rules section generation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.FAIL,
                message="File not found",
                target="src/main.py",
                guide_id="backend"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        section = generator.generate_failed_rules_section(results)
        
        assert "## ❌ Failed Rules" in section
        assert "rule-1" in section
        assert "Recommendation" in section
        assert "waive-requirement" in section
    
    def test_generate_waived_rules_section(self, temp_project_dir):
        """Test waived rules section generation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.WAIVED,
                message="Waived",
                target="src/main.py",
                guide_id="backend",
                waiver_id="W-001"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        section = generator.generate_waived_rules_section(results)
        
        assert "## 🚫 Waived Rules" in section
        assert "rule-1" in section
        assert "W-001" in section
    
    def test_generate_error_rules_section(self, temp_project_dir):
        """Test error rules section generation."""
        results = [
            RuleEvaluationResult(
                rule_id="parse-error",
                rule_type="parsing",
                status=RuleStatus.ERROR,
                message="Failed to parse guide",
                target="backend.md",
                guide_id="backend"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        section = generator.generate_error_rules_section(results)
        
        assert "## ⚠️ Errors" in section
        assert "Failed to parse" in section
    
    def test_generate_report_full(self, temp_project_dir):
        """Test full report generation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="backend"
            ),
            RuleEvaluationResult(
                rule_id="rule-2",
                rule_type="file_exists",
                status=RuleStatus.FAIL,
                message="Failed",
                target="test",
                guide_id="backend"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        report = generator.generate_report(
            results,
            project_name="TestProject",
            branch="develop"
        )
        
        assert "# Compliance Report" in report
        assert "TestProject" in report
        assert "develop" in report
        assert "## Summary" in report
        assert "✅ Passed" in report
        assert "❌ Failed" in report
    
    def test_write_report_to_file(self, temp_project_dir):
        """Test writing report to file."""
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        report_content = "# Test Report\n\nThis is a test."
        
        report_path = generator.write_report_to_file(report_content)
        
        assert report_path.exists()
        assert report_path.read_text() == report_content
    
    def test_generate_and_write_report(self, temp_project_dir):
        """Test generate and write in one operation."""
        results = [
            RuleEvaluationResult(
                rule_id="rule-1",
                rule_type="file_exists",
                status=RuleStatus.PASS,
                message="Passed",
                target="test",
                guide_id="backend"
            )
        ]
        
        generator = ComplianceReportGenerator(project_root=temp_project_dir)
        report_path = generator.generate_and_write_report(
            results,
            project_name="TestProject"
        )
        
        assert report_path.exists()
        content = report_path.read_text()
        assert "TestProject" in content
        assert "## Summary" in content
