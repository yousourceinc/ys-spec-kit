"""
Unit tests for governance metrics module.
"""

import time
import pytest
from pathlib import Path

from specify_cli.governance.metrics import (
    RuleMetrics,
    ComplianceCheckMetrics,
    MetricsCollector,
    get_metrics_collector
)


class TestRuleMetrics:
    """Test RuleMetrics class."""
    
    def test_rule_metrics_initialization(self):
        """Test RuleMetrics initialization."""
        metric = RuleMetrics(rule_id="R-001", rule_type="file_exists")
        assert metric.rule_id == "R-001"
        assert metric.rule_type == "file_exists"
        assert metric.start_time > 0
        assert metric.end_time is None
        assert metric.duration_ms == 0.0
    
    def test_rule_metrics_duration_calculation(self):
        """Test duration calculation."""
        metric = RuleMetrics(rule_id="R-001", rule_type="file_exists")
        time.sleep(0.01)  # Sleep 10ms
        metric.end_time = metric.start_time + 0.01  # Simulate 10ms duration
        assert 8 < metric.duration_ms < 12  # Allow some variance
    
    def test_rule_metrics_to_dict(self):
        """Test conversion to dictionary."""
        metric = RuleMetrics(rule_id="R-001", rule_type="file_exists")
        metric.end_time = metric.start_time + 0.01
        result = metric.to_dict()
        
        assert result['rule_id'] == "R-001"
        assert result['rule_type'] == "file_exists"
        assert 'duration_ms' in result
        assert isinstance(result['duration_ms'], float)


class TestComplianceCheckMetrics:
    """Test ComplianceCheckMetrics class."""
    
    def test_check_metrics_initialization(self):
        """Test ComplianceCheckMetrics initialization."""
        metrics = ComplianceCheckMetrics()
        assert metrics.start_time > 0
        assert metrics.end_time is None
        assert metrics.guides_count == 0
        assert metrics.rules_count == 0
        assert metrics.rule_metrics == []
        assert metrics.total_duration_ms == 0.0
    
    def test_check_metrics_duration(self):
        """Test total duration calculation."""
        metrics = ComplianceCheckMetrics()
        time.sleep(0.01)
        metrics.end_time = metrics.start_time + 0.01
        assert 8 < metrics.total_duration_ms < 12
    
    def test_check_metrics_add_rule_metric(self):
        """Test adding rule metrics."""
        metrics = ComplianceCheckMetrics()
        rule_metric = RuleMetrics(rule_id="R-001", rule_type="file_exists")
        rule_metric.end_time = rule_metric.start_time + 0.001
        
        metrics.add_rule_metric(rule_metric)
        assert len(metrics.rule_metrics) == 1
        assert metrics.rule_metrics[0] == rule_metric
    
    def test_check_metrics_average_duration(self):
        """Test average rule duration calculation."""
        metrics = ComplianceCheckMetrics()
        
        # Add three rules with known durations
        for i in range(3):
            rule_metric = RuleMetrics(
                rule_id=f"R-{i:03d}",
                rule_type="file_exists"
            )
            rule_metric.end_time = rule_metric.start_time + 0.01
            metrics.add_rule_metric(rule_metric)
        
        avg = metrics.avg_rule_duration_ms
        assert 8 < avg < 12
    
    def test_check_metrics_to_dict(self):
        """Test conversion to dictionary."""
        metrics = ComplianceCheckMetrics()
        metrics.guides_count = 2
        metrics.rules_count = 5
        metrics.end_time = metrics.start_time + 0.05
        
        result = metrics.to_dict()
        assert result['guides_count'] == 2
        assert result['rules_count'] == 5
        assert 'total_duration_ms' in result
        assert 'avg_rule_duration_ms' in result
        assert result['rules'] == []
    
    def test_check_metrics_summary(self):
        """Test human-readable summary."""
        metrics = ComplianceCheckMetrics()
        metrics.guides_count = 2
        metrics.rules_count = 5
        metrics.end_time = metrics.start_time + 0.05
        
        summary = metrics.summary()
        assert "Compliance Check Metrics" in summary
        assert "Total Duration" in summary
        assert "Guides: 2" in summary
        assert "Rules Evaluated: 5" in summary


class TestMetricsCollector:
    """Test MetricsCollector class."""
    
    def test_collector_initialization(self):
        """Test MetricsCollector initialization."""
        collector = MetricsCollector()
        assert collector.current_check is None
        assert collector.history == []
    
    def test_start_check(self):
        """Test starting a check."""
        collector = MetricsCollector()
        metrics = collector.start_check()
        
        assert isinstance(metrics, ComplianceCheckMetrics)
        assert collector.current_check == metrics
    
    def test_end_check(self):
        """Test ending a check."""
        collector = MetricsCollector()
        metrics = collector.start_check()
        time.sleep(0.01)
        
        result = collector.end_check()
        
        assert result == metrics
        assert metrics.end_time is not None
        assert collector.current_check is None
        assert len(collector.history) == 1
    
    def test_start_rule_evaluation(self):
        """Test starting rule evaluation."""
        collector = MetricsCollector()
        metric = collector.start_rule_evaluation("R-001", "file_exists")
        
        assert isinstance(metric, RuleMetrics)
        assert metric.rule_id == "R-001"
        assert metric.rule_type == "file_exists"
    
    def test_end_rule_evaluation(self):
        """Test ending rule evaluation."""
        collector = MetricsCollector()
        collector.start_check()
        
        metric = collector.start_rule_evaluation("R-001", "file_exists")
        time.sleep(0.01)
        collector.end_rule_evaluation(metric)
        
        assert metric.end_time is not None
        assert len(collector.current_check.rule_metrics) == 1
    
    def test_get_current_metrics(self):
        """Test getting current metrics."""
        collector = MetricsCollector()
        assert collector.get_current_metrics() is None
        
        metrics = collector.start_check()
        assert collector.get_current_metrics() == metrics
    
    def test_get_history(self):
        """Test getting metrics history."""
        collector = MetricsCollector()
        
        # Run multiple checks
        for i in range(3):
            collector.start_check()
            collector.end_check()
        
        history = collector.get_history()
        assert len(history) == 3
    
    def test_clear_history(self):
        """Test clearing metrics history."""
        collector = MetricsCollector()
        
        collector.start_check()
        collector.end_check()
        assert len(collector.history) == 1
        
        collector.clear_history()
        assert len(collector.history) == 0
    
    def test_metrics_workflow(self):
        """Test complete metrics workflow."""
        collector = MetricsCollector()
        
        # Start check
        metrics = collector.start_check()
        metrics.guides_count = 2
        time.sleep(0.01)
        
        # Add rule metrics
        for i in range(3):
            rule_metric = collector.start_rule_evaluation(
                f"R-{i:03d}",
                "file_exists"
            )
            time.sleep(0.005)
            collector.end_rule_evaluation(rule_metric)
        
        # End check
        result = collector.end_check()
        
        assert result.guides_count == 2
        assert len(result.rule_metrics) == 3
        assert result.total_duration_ms > 15  # At least 15ms total


class TestGlobalMetricsCollector:
    """Test global metrics collector instance."""
    
    def test_get_metrics_collector(self):
        """Test getting global metrics collector."""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()
        
        # Should be the same instance
        assert collector1 is collector2
