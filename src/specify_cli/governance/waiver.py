"""
Waiver Management Module

Provides functionality for creating, storing, and retrieving compliance waivers.
Waivers represent formal exceptions to compliance requirements with reason and audit trail.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import re
import logging

logger = logging.getLogger(__name__)


class Waiver:
    """
    Represents a single compliance waiver.
    
    A waiver formally records an exception to a compliance requirement,
    including the reason, timestamp, and unique identifier.
    """
    
    def __init__(
        self,
        waiver_id: str,
        reason: str,
        timestamp: str,
        related_rules: Optional[List[str]] = None,
        created_by: Optional[str] = None
    ):
        """
        Initialize a waiver.
        
        Args:
            waiver_id: Unique identifier in W-XXX format
            reason: Plain-text explanation for the exception
            timestamp: ISO-8601 timestamp
            related_rules: Optional list of rule identifiers
            created_by: Optional author information
        """
        self.waiver_id = waiver_id
        self.reason = reason
        self.timestamp = timestamp
        self.related_rules = related_rules or []
        self.created_by = created_by
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert waiver to dictionary representation."""
        return {
            "id": self.waiver_id,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "related_rules": self.related_rules,
            "created_by": self.created_by
        }
    
    def __repr__(self) -> str:
        return f"Waiver({self.waiver_id}, {self.reason[:30]}...)"


class WaiverManager:
    """
    Manages creation, storage, and retrieval of compliance waivers.
    
    Waivers are stored in `.specify/waivers.md` as a markdown file with
    structured entries for easy review and audit tracking.
    """
    
    WAIVERS_FILE = Path(".specify/waivers.md")
    WAIVERS_DIR = Path(".specify")
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize WaiverManager.
        
        Args:
            project_root: Root directory of project (defaults to current directory)
        """
        self.project_root = Path(project_root) if project_root else Path(".")
        self.waivers_file = self.project_root / self.WAIVERS_FILE
        self.waivers_dir = self.project_root / self.WAIVERS_DIR
    
    @staticmethod
    def generate_waiver_id(existing_waivers: List[Waiver]) -> str:
        """
        Generate next auto-incremented waiver ID in W-XXX format.
        
        Args:
            existing_waivers: List of existing waivers
        
        Returns:
            Next waiver ID (e.g., "W-001", "W-002")
        """
        if not existing_waivers:
            return "W-001"
        
        # Extract numeric part and find max
        max_num = 0
        for waiver in existing_waivers:
            match = re.match(r'W-(\d+)', waiver.waiver_id)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
        
        return f"W-{max_num + 1:03d}"
    
    @staticmethod
    def format_waiver_entry(
        waiver_id: str,
        reason: str,
        timestamp: str,
        related_rules: Optional[List[str]] = None,
        created_by: Optional[str] = None
    ) -> str:
        """
        Format a waiver as markdown for storage.
        
        Args:
            waiver_id: Unique waiver identifier
            reason: Reason for the waiver
            timestamp: ISO-8601 timestamp
            related_rules: Optional list of related rule IDs
            created_by: Optional author information
        
        Returns:
            Formatted markdown string for the waiver entry
        """
        entry = f"\n## Waiver: {waiver_id}\n"
        entry += f"- **Reason**: {reason}\n"
        entry += f"- **Timestamp**: {timestamp}\n"
        
        if created_by:
            entry += f"- **Created By**: {created_by}\n"
        
        if related_rules:
            rules_str = ", ".join(related_rules)
            entry += f"- **Related Rules**: [{rules_str}]\n"
        
        return entry
    
    def create_waiver(
        self,
        reason: str,
        related_rules: Optional[List[str]] = None,
        created_by: Optional[str] = None
    ) -> Waiver:
        """
        Create a new waiver and append it to the waivers file.
        
        Args:
            reason: Plain-text explanation for the exception
            related_rules: Optional list of rule identifiers
            created_by: Optional author information
        
        Returns:
            Created Waiver instance
        
        Raises:
            ValueError: If reason is empty or invalid
        """
        if not reason or not reason.strip():
            logger.warning("Attempt to create waiver with empty reason")
            raise ValueError("Waiver reason cannot be empty")
        
        if len(reason) > 500:
            logger.warning("Attempt to create waiver with reason exceeding 500 chars")
            raise ValueError("Waiver reason cannot exceed 500 characters")
        
        # Generate timestamp in ISO-8601 format
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Read existing waivers to generate next ID
        existing_waivers = self.parse_waivers_file()
        waiver_id = self.generate_waiver_id(existing_waivers)
        
        logger.debug(f"Generating new waiver ID: {waiver_id}")
        
        # Create waiver instance
        waiver = Waiver(
            waiver_id=waiver_id,
            reason=reason.strip(),
            timestamp=timestamp,
            related_rules=related_rules,
            created_by=created_by
        )
        
        # Append to file
        self.append_to_waivers_file(waiver)
        
        logger.info(f"Created waiver {waiver_id} for rules: {related_rules or 'N/A'}")
        return waiver
    
    def append_to_waivers_file(self, waiver: Waiver) -> None:
        """
        Append a waiver to the waivers file, creating it if necessary.
        
        Args:
            waiver: Waiver to append
        """
        # Create .specify directory if needed
        self.waivers_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Waivers directory ready: {self.waivers_dir}")
        
        # Create or update file
        if not self.waivers_file.exists():
            logger.debug(f"Creating new waivers file: {self.waivers_file}")
            # Create new file with header
            header = "# Compliance Waivers\n\n"
            header += "Formal exceptions to compliance requirements.\n"
            header += "All entries are immutable and timestamped for audit trail purposes.\n"
            self.waivers_file.write_text(header)
        
        # Format and append waiver
        entry = self.format_waiver_entry(
            waiver.waiver_id,
            waiver.reason,
            waiver.timestamp,
            waiver.related_rules,
            waiver.created_by
        )
        
        with open(self.waivers_file, 'a') as f:
            f.write(entry)
        logger.debug(f"Appended waiver {waiver.waiver_id} to {self.waivers_file}")
    
    def parse_waivers_file(self) -> List[Waiver]:
        """
        Parse existing waivers from .specify/waivers.md file.
        
        Returns:
            List of Waiver instances (empty if file doesn't exist)
        """
        if not self.waivers_file.exists():
            logger.debug(f"Waivers file does not exist: {self.waivers_file}")
            return []
        
        logger.debug(f"Parsing waivers file: {self.waivers_file}")
        content = self.waivers_file.read_text()
        waivers = []
        
        # Split by waiver sections (## Waiver: W-XXX)
        pattern = r'## Waiver: (W-\d+)\n((?:.*?\n)*?)(?=## Waiver:|$)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            waiver_id = match.group(1)
            waiver_section = match.group(2)
            
            # Parse fields from waiver section
            reason_match = re.search(r'- \*\*Reason\*\*: (.+?)(?:\n|$)', waiver_section)
            timestamp_match = re.search(r'- \*\*Timestamp\*\*: (.+?)(?:\n|$)', waiver_section)
            created_by_match = re.search(r'- \*\*Created By\*\*: (.+?)(?:\n|$)', waiver_section)
            rules_match = re.search(r'- \*\*Related Rules\*\*: \[(.+?)\]', waiver_section)
            
            if reason_match and timestamp_match:
                reason = reason_match.group(1)
                timestamp = timestamp_match.group(1)
                created_by = created_by_match.group(1) if created_by_match else None
                related_rules = [
                    r.strip() for r in rules_match.group(1).split(',')
                ] if rules_match else None
                
                waiver = Waiver(
                    waiver_id=waiver_id,
                    reason=reason,
                    timestamp=timestamp,
                    related_rules=related_rules,
                    created_by=created_by
                )
                waivers.append(waiver)
                logger.debug(f"Parsed waiver {waiver_id}")
        
        logger.debug(f"Parsed {len(waivers)} waivers from file")
        return waivers
    
    def get_waiver_by_id(self, waiver_id: str) -> Optional[Waiver]:
        """
        Retrieve a specific waiver by ID.
        
        Args:
            waiver_id: Waiver identifier to look up
        
        Returns:
            Waiver instance if found, None otherwise
        """
        logger.debug(f"Looking up waiver: {waiver_id}")
        waivers = self.parse_waivers_file()
        for waiver in waivers:
            if waiver.waiver_id == waiver_id:
                logger.debug(f"Found waiver: {waiver_id}")
                return waiver
        logger.warning(f"Waiver not found: {waiver_id}")
        return None
    
    def list_waivers(self) -> List[Waiver]:
        """
        Get all waivers in chronological order.
        
        Returns:
            List of all waivers in file order (chronological)
        """
        return self.parse_waivers_file()
