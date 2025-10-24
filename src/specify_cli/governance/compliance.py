"""
Compliance Checking Module

Provides functionality for discovering guides, evaluating rules, and generating
compliance reports with cross-referencing to waivers.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

from .waiver import WaiverManager, Waiver
from .rules.engine import RuleEngine
from .rules.parser import RuleParser
from .rules import BaseRule
from .metrics import get_metrics_collector
from .caching import GuideCacheManager


class RuleStatus(str, Enum):
    """Status of rule evaluation."""
    PASS = "pass"
    FAIL = "fail"
    WAIVED = "waived"
    ERROR = "error"


@dataclass
class RuleEvaluationResult:
    """Result of evaluating a single rule against codebase."""
    
    rule_id: str
    rule_type: str
    status: RuleStatus
    message: str
    target: str
    guide_id: str
    division: Optional[str] = None
    waiver_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "rule_id": self.rule_id,
            "rule_type": self.rule_type,
            "status": self.status.value,
            "message": self.message,
            "target": self.target,
            "guide_id": self.guide_id,
            "division": self.division,
            "waiver_id": self.waiver_id,
            "timestamp": self.timestamp
        }
    
    def status_emoji(self) -> str:
        """Get emoji for status."""
        status_emojis = {
            RuleStatus.PASS: "✅",
            RuleStatus.FAIL: "❌",
            RuleStatus.WAIVED: "🚫",
            RuleStatus.ERROR: "⚠️"
        }
        return status_emojis.get(self.status, "❓")


class ComplianceChecker:
    """
    Checks code compliance against rules defined in guides.
    
    Evaluates rules, cross-references waivers, and produces aggregated results.
    """
    
    def __init__(self, project_root: Optional[Path] = None, use_cache: bool = True):
        """
        Initialize ComplianceChecker.
        
        Args:
            project_root: Root directory of project (defaults to current directory)
            use_cache: Whether to use guide caching (default: True)
        """
        self.project_root = Path(project_root) if project_root else Path(".")
        self.rule_engine = RuleEngine(str(self.project_root))
        self.rule_parser = RuleParser()
        self.waiver_manager = WaiverManager(project_root=self.project_root)
        self.cache_manager = GuideCacheManager(project_root=self.project_root)
        self.use_cache = use_cache
    
    def run_compliance_check(
        self,
        guides: Optional[List[Path]] = None
    ) -> List[RuleEvaluationResult]:
        """
        Run compliance check against provided guides.
        
        Args:
            guides: List of guide files to check (discovers from plan.md if None)
        
        Returns:
            List of rule evaluation results
        """
        logger.info("Starting compliance check")
        
        # Start metrics collection
        metrics = get_metrics_collector().start_check()
        
        results = []
        
        # If no guides provided, discover them
        if guides is None:
            logger.debug("Discovering guides from project")
            guides = self._discover_guides()
            logger.info(f"Discovered {len(guides)} guides")
        else:
            logger.debug(f"Using {len(guides)} provided guides")
        
        metrics.guides_count = len(guides)
        
        # Load existing waivers
        logger.debug("Loading waivers")
        waivers = self.waiver_manager.list_waivers()
        waiver_map = self._build_waiver_map(waivers)
        logger.debug(f"Loaded {len(waiver_map)} waivers")
        
        # Extract and evaluate rules from each guide
        for guide_path in guides:
            if not guide_path.exists():
                logger.warning(f"Guide file not found: {guide_path}")
                results.append(
                    RuleEvaluationResult(
                        rule_id="discovery-error",
                        rule_type="discovery",
                        status=RuleStatus.ERROR,
                        message=f"Guide file not found: {guide_path}",
                        target=str(guide_path),
                        guide_id=guide_path.stem
                    )
                )
                continue
            
            logger.debug(f"Processing guide: {guide_path}")
            # Extract rules from guide
            try:
                rules_data = self.rule_parser.extract_rules(guide_path)
                guide_id = self._extract_guide_id(guide_path)
                logger.debug(f"Extracted {len(rules_data)} rules from {guide_id}")
                
                for rule_data in rules_data:
                    result = self._evaluate_rule(
                        rule_data,
                        guide_id,
                        waiver_map
                    )
                    results.append(result)
                    logger.debug(f"Rule {result.rule_id}: {result.status.value}")
            
            except Exception as e:
                logger.error(f"Failed to parse guide {guide_path}: {str(e)}")
                results.append(
                    RuleEvaluationResult(
                        rule_id="parse-error",
                        rule_type="parsing",
                        status=RuleStatus.ERROR,
                        message=f"Failed to parse guide: {str(e)}",
                        target=str(guide_path),
                        guide_id=guide_path.stem
                    )
                )
        
        # Finalize metrics
        metrics.rules_count = len(results)
        get_metrics_collector().end_check()
        
        logger.info(f"Compliance check complete: {len(results)} rules evaluated")
        return results
    
    def _discover_guides(self) -> List[Path]:
        """
        Discover guide files from project structure.
        
        Looks for guides in:
        - context/references/ directory
        - Any markdown files with rules in YAML frontmatter
        
        Returns:
            List of discovered guide paths
        """
        logger.debug("Discovering guides in project")
        
        # Check cache first if enabled
        if self.use_cache:
            cached_guides = self.cache_manager.get_guides()
            if cached_guides is not None:
                logger.debug(f"Using cached guides: {len(cached_guides)} guides")
                return cached_guides
        
        guides = []
        
        # Look in context/references/ if it exists
        guides_dir = self.project_root / "context" / "references"
        if guides_dir.exists():
            refs = list(guides_dir.glob("*.md"))
            guides.extend(refs)
            logger.debug(f"Found {len(refs)} guides in context/references/")
        
        # Look for guides in specs/ directory
        specs_dir = self.project_root / "specs"
        if specs_dir.exists():
            specs = list(specs_dir.glob("**/*.md"))
            guides.extend(specs)
            logger.debug(f"Found {len(specs)} guides in specs/")
        
        logger.debug(f"Total guides discovered: {len(guides)}")
        
        # Cache results if enabled
        if self.use_cache and guides:
            self.cache_manager.save_guides(guides)
        
        return guides
    
    def _evaluate_rule(
        self,
        rule_data: Dict[str, Any],
        guide_id: str,
        waiver_map: Dict[str, Waiver]
    ) -> RuleEvaluationResult:
        """
        Evaluate a single rule against the codebase.
        
        Args:
            rule_data: Rule definition from guide
            guide_id: ID of the guide this rule came from
            waiver_map: Map of rule IDs to waivers
        
        Returns:
            RuleEvaluationResult with pass/fail/waived/error status
        """
        rule_id = rule_data.get("id", "unknown")
        rule_type = rule_data.get("type", "unknown")
        
        try:
            # Create rule instance
            rule = self.rule_engine.create_rule(rule_data)
            
            # Evaluate rule
            eval_result = rule.evaluate(self.project_root)
            
            # Determine if rule passed
            rule_passed = eval_result.get("passed", False)
            
            # Check if there's a waiver for this failed rule
            if not rule_passed and rule_id in waiver_map:
                waiver = waiver_map[rule_id]
                return RuleEvaluationResult(
                    rule_id=rule_id,
                    rule_type=rule_type,
                    status=RuleStatus.WAIVED,
                    message=f"🚫 {rule_id} waived by {waiver.waiver_id}",
                    target=eval_result.get("details", ""),
                    guide_id=guide_id,
                    waiver_id=waiver.waiver_id
                )
            
            # Return pass or fail result
            status = RuleStatus.PASS if rule_passed else RuleStatus.FAIL
            return RuleEvaluationResult(
                rule_id=rule_id,
                rule_type=rule_type,
                status=status,
                message=eval_result.get("message", ""),
                target=eval_result.get("details", ""),
                guide_id=guide_id
            )
        
        except Exception as e:
            return RuleEvaluationResult(
                rule_id=rule_id,
                rule_type=rule_type,
                status=RuleStatus.ERROR,
                message=f"Error evaluating rule: {str(e)}",
                target="",
                guide_id=guide_id
            )
    
    def _build_waiver_map(self, waivers: List[Waiver]) -> Dict[str, Waiver]:
        """
        Build a map from rule IDs to waivers.
        
        Args:
            waivers: List of waivers
        
        Returns:
            Map of rule IDs to waivers
        """
        waiver_map = {}
        for waiver in waivers:
            for rule_id in waiver.related_rules:
                waiver_map[rule_id] = waiver
        return waiver_map
    
    def _extract_guide_id(self, guide_path: Path) -> str:
        """Extract guide ID from path (use filename without extension)."""
        return guide_path.stem
