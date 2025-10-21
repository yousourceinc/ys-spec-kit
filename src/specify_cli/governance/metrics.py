"""
Performance metrics tracking for governance operations.

Tracks timing and metrics for compliance checking, rule evaluation,
and related governance operations.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class RuleMetrics:
    """Metrics for a single rule evaluation."""
    rule_id: str
    rule_type: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'rule_id': self.rule_id,
            'rule_type': self.rule_type,
            'duration_ms': round(self.duration_ms, 2)
        }


@dataclass
class ComplianceCheckMetrics:
    """Metrics for a complete compliance check."""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    guides_count: int = 0
    rules_count: int = 0
    rule_metrics: List[RuleMetrics] = field(default_factory=list)
    
    @property
    def total_duration_ms(self) -> float:
        """Get total duration in milliseconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000
    
    @property
    def avg_rule_duration_ms(self) -> float:
        """Get average rule evaluation time in milliseconds."""
        if not self.rule_metrics:
            return 0.0
        total = sum(m.duration_ms for m in self.rule_metrics)
        return total / len(self.rule_metrics)
    
    def add_rule_metric(self, metric: RuleMetrics) -> None:
        """Add rule metrics."""
        self.rule_metrics.append(metric)
        logger.debug(f"Rule metric: {metric.rule_id} took {metric.duration_ms:.2f}ms")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'total_duration_ms': round(self.total_duration_ms, 2),
            'guides_count': self.guides_count,
            'rules_count': self.rules_count,
            'avg_rule_duration_ms': round(self.avg_rule_duration_ms, 2),
            'rules': [m.to_dict() for m in self.rule_metrics]
        }
    
    def summary(self) -> str:
        """Get human-readable summary."""
        return (
            f"Compliance Check Metrics:\n"
            f"  Total Duration: {self.total_duration_ms:.2f}ms\n"
            f"  Guides: {self.guides_count}\n"
            f"  Rules Evaluated: {self.rules_count}\n"
            f"  Avg Rule Time: {self.avg_rule_duration_ms:.2f}ms"
        )


class MetricsCollector:
    """Collects and manages performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.current_check: Optional[ComplianceCheckMetrics] = None
        self.history: List[ComplianceCheckMetrics] = []
    
    def start_check(self) -> ComplianceCheckMetrics:
        """Start a new compliance check."""
        logger.debug("Starting metrics collection for compliance check")
        self.current_check = ComplianceCheckMetrics()
        return self.current_check
    
    def end_check(self) -> Optional[ComplianceCheckMetrics]:
        """End current compliance check."""
        if self.current_check is None:
            return None
        
        self.current_check.end_time = time.time()
        logger.info(self.current_check.summary())
        self.history.append(self.current_check)
        result = self.current_check
        self.current_check = None
        return result
    
    def start_rule_evaluation(self, rule_id: str, rule_type: str) -> RuleMetrics:
        """Start rule evaluation timing."""
        metric = RuleMetrics(rule_id=rule_id, rule_type=rule_type)
        return metric
    
    def end_rule_evaluation(self, metric: RuleMetrics) -> None:
        """End rule evaluation timing."""
        metric.end_time = time.time()
        if self.current_check is not None:
            self.current_check.add_rule_metric(metric)
    
    def get_current_metrics(self) -> Optional[ComplianceCheckMetrics]:
        """Get current metrics."""
        return self.current_check
    
    def get_history(self) -> List[ComplianceCheckMetrics]:
        """Get historical metrics."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear metrics history."""
        self.history.clear()


# Global metrics collector instance
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance."""
    return _metrics_collector
