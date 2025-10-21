"""
Compliance Report Generation Module

Generates markdown compliance reports from rule evaluation results.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Set
from collections import defaultdict

from .compliance import RuleEvaluationResult, RuleStatus


class ComplianceReportGenerator:
    """
    Generates formatted compliance reports from evaluation results.
    
    Creates comprehensive markdown reports with:
    - Summary statistics (pass/fail/waived counts)
    - Per-guide results
    - Detailed rule-by-rule status
    - Waiver cross-references
    """
    
    REPORT_FILE = Path("compliance-report.md")
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize report generator.
        
        Args:
            project_root: Root directory of project (defaults to current directory)
        """
        self.project_root = Path(project_root) if project_root else Path(".")
        self.report_file = self.project_root / self.REPORT_FILE
    
    def generate_report(
        self,
        results: List[RuleEvaluationResult],
        project_name: Optional[str] = None,
        branch: Optional[str] = None
    ) -> str:
        """
        Generate a formatted compliance report.
        
        Args:
            results: List of rule evaluation results
            project_name: Optional project name (defaults to directory name)
            branch: Optional git branch name
        
        Returns:
            Formatted markdown report as string
        """
        if project_name is None:
            project_name = self.project_root.name
        
        report = ""
        
        # Header and metadata
        report += self.generate_report_header(project_name, branch)
        
        # Summary statistics
        report += self.generate_summary_section(results)
        
        # Guides checked
        report += self.generate_checked_guides_section(results)
        
        # Detailed results grouped by status
        report += self.generate_passed_rules_section(results)
        report += self.generate_failed_rules_section(results)
        report += self.generate_waived_rules_section(results)
        report += self.generate_error_rules_section(results)
        
        return report
    
    def generate_report_header(
        self,
        project_name: str,
        branch: Optional[str] = None
    ) -> str:
        """
        Generate report header with metadata.
        
        Args:
            project_name: Name of project
            branch: Optional git branch
        
        Returns:
            Formatted header section
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        header = "# Compliance Report\n\n"
        header += f"**Project**: {project_name}\n"
        if branch:
            header += f"**Branch**: {branch}\n"
        header += f"**Generated**: {timestamp}\n\n"
        
        return header
    
    def generate_summary_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate summary statistics section.
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted summary section
        """
        pass_count = sum(1 for r in results if r.status == RuleStatus.PASS)
        fail_count = sum(1 for r in results if r.status == RuleStatus.FAIL)
        waived_count = sum(1 for r in results if r.status == RuleStatus.WAIVED)
        error_count = sum(1 for r in results if r.status == RuleStatus.ERROR)
        total = len(results)
        
        # Determine overall status
        if fail_count > 0:
            overall_status = "⚠️ PARTIAL (failures found)"
        elif error_count > 0:
            overall_status = "⚠️ PARTIAL (errors encountered)"
        elif total == 0:
            overall_status = "❓ NO RULES (no guides found)"
        else:
            overall_status = f"✅ COMPLIANT ({pass_count} passed)"
        
        summary = "## Summary\n\n"
        summary += f"**Overall Status**: {overall_status}\n\n"
        summary += f"| Metric | Count |\n"
        summary += f"|--------|-------|\n"
        summary += f"| Total Rules | {total} |\n"
        summary += f"| ✅ Passed | {pass_count} |\n"
        summary += f"| ❌ Failed | {fail_count} |\n"
        summary += f"| 🚫 Waived | {waived_count} |\n"
        summary += f"| ⚠️ Errors | {error_count} |\n\n"
        
        return summary
    
    def generate_checked_guides_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate section listing guides that were checked.
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted guides section
        """
        guide_ids = set(r.guide_id for r in results if r.status != RuleStatus.ERROR or r.rule_type == "discovery")
        
        if not guide_ids:
            return ""
        
        section = "## Guides Checked\n\n"
        for guide_id in sorted(guide_ids):
            section += f"- {guide_id}\n"
        section += "\n"
        
        return section
    
    def generate_passed_rules_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate section for passed rules.
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted passed rules section
        """
        passed = [r for r in results if r.status == RuleStatus.PASS]
        
        if not passed:
            return ""
        
        section = "## ✅ Passed Rules\n\n"
        for result in sorted(passed, key=lambda r: r.rule_id):
            section += f"- **{result.rule_id}** ({result.guide_id})\n"
            section += f"  - Message: {result.message}\n"
        section += "\n"
        
        return section
    
    def generate_failed_rules_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate section for failed rules with recommendations.
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted failed rules section
        """
        failed = [r for r in results if r.status == RuleStatus.FAIL]
        
        if not failed:
            return ""
        
        section = "## ❌ Failed Rules\n\n"
        for result in sorted(failed, key=lambda r: r.rule_id):
            section += f"- **{result.rule_id}** ({result.guide_id})\n"
            section += f"  - Type: {result.rule_type}\n"
            section += f"  - Message: {result.message}\n"
            section += f"  - Details: {result.target}\n"
            section += f"\n  **Recommendation**: Review the implementation guide for {result.guide_id} "
            section += f"to understand the requirement for {result.rule_id}.\n"
            section += f"  Alternatively, create a waiver if this failure is intentional: "
            section += f"`specify waive-requirement \"<reason>\"`\n\n"
        
        return section
    
    def generate_waived_rules_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate section for waived rules.
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted waived rules section
        """
        waived = [r for r in results if r.status == RuleStatus.WAIVED]
        
        if not waived:
            return ""
        
        section = "## 🚫 Waived Rules\n\n"
        for result in sorted(waived, key=lambda r: r.rule_id):
            section += f"- **{result.rule_id}** (waiver: {result.waiver_id})\n"
            section += f"  - Guide: {result.guide_id}\n"
            section += f"  - Status: {result.message}\n"
        section += "\n"
        
        return section
    
    def generate_error_rules_section(
        self,
        results: List[RuleEvaluationResult]
    ) -> str:
        """
        Generate section for errors (optional).
        
        Args:
            results: Rule evaluation results
        
        Returns:
            Formatted errors section
        """
        errors = [r for r in results if r.status == RuleStatus.ERROR]
        
        if not errors:
            return ""
        
        section = "## ⚠️ Errors\n\n"
        for result in sorted(errors, key=lambda r: r.rule_id):
            section += f"- **{result.rule_type.upper()}**: {result.message}\n"
        section += "\n"
        
        return section
    
    def write_report_to_file(
        self,
        report_content: str
    ) -> Path:
        """
        Write compliance report to file.
        
        Args:
            report_content: Formatted report content
        
        Returns:
            Path to written report file
        """
        self.report_file.write_text(report_content)
        return self.report_file
    
    def generate_and_write_report(
        self,
        results: List[RuleEvaluationResult],
        project_name: Optional[str] = None,
        branch: Optional[str] = None
    ) -> Path:
        """
        Generate and write compliance report in one operation.
        
        Args:
            results: Rule evaluation results
            project_name: Optional project name
            branch: Optional git branch
        
        Returns:
            Path to written report file
        """
        report_content = self.generate_report(
            results,
            project_name=project_name,
            branch=branch
        )
        return self.write_report_to_file(report_content)
