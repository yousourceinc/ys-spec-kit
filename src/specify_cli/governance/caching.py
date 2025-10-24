"""
Caching utilities for governance operations.

Provides caching for expensive operations like guide discovery
to optimize performance for large codebases.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GuideCacheManager:
    """Manages caching of guide discovery results."""
    
    CACHE_DIR = Path(".specify/.cache")
    CACHE_FILE = CACHE_DIR / "guides_cache.txt"
    CACHE_EXPIRY_SECONDS = 3600  # 1 hour
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize cache manager.
        
        Args:
            project_root: Root directory of project
        """
        self.project_root = Path(project_root) if project_root else Path(".")
        self.cache_dir = self.project_root / self.CACHE_DIR
        self.cache_file = self.project_root / self.CACHE_FILE
    
    def _get_project_hash(self) -> str:
        """
        Generate hash of project structure for cache validation.
        
        Returns:
            Hash of project state
        """
        # Hash based on key directories that might contain guides
        dirs_to_hash = [
            self.project_root / "specs",
            self.project_root / "context" / "references",
        ]
        
        hash_obj = hashlib.md5()
        for dir_path in dirs_to_hash:
            if dir_path.exists():
                # Hash the list of markdown files
                md_files = sorted(dir_path.glob("**/*.md"))
                for md_file in md_files:
                    # Use relative path and modification time
                    rel_path = md_file.relative_to(self.project_root)
                    mtime = md_file.stat().st_mtime
                    hash_obj.update(f"{rel_path}:{mtime}".encode())
        
        return hash_obj.hexdigest()
    
    def _is_cache_valid(self, cached_hash: str) -> bool:
        """
        Check if cache is valid.
        
        Args:
            cached_hash: Hash from cache file
        
        Returns:
            True if cache is still valid
        """
        if not self.cache_file.exists():
            return False
        
        # Check expiry time
        file_mtime = self.cache_file.stat().st_mtime
        age_seconds = (datetime.now().timestamp() - file_mtime)
        if age_seconds > self.CACHE_EXPIRY_SECONDS:
            logger.debug("Cache expired")
            return False
        
        # Check if project structure changed
        current_hash = self._get_project_hash()
        if current_hash != cached_hash:
            logger.debug("Project structure changed, cache invalid")
            return False
        
        return True
    
    def get_guides(self) -> Optional[List[Path]]:
        """
        Get cached guides if available.
        
        Returns:
            List of guide paths or None if cache invalid
        """
        if not self.cache_file.exists():
            logger.debug("No cache file found")
            return None
        
        try:
            with open(self.cache_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return None
                
                cached_hash = lines[0].strip()
                if not self._is_cache_valid(cached_hash):
                    return None
                
                # Parse cached paths
                guides = []
                for line in lines[1:]:
                    path_str = line.strip()
                    if path_str:
                        guides.append(Path(path_str))
                
                logger.debug(f"Using cached guides: {len(guides)} guides")
                return guides
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            return None
    
    def save_guides(self, guides: List[Path]) -> None:
        """
        Save guides to cache.
        
        Args:
            guides: List of guide paths to cache
        """
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_file, 'w') as f:
                # Write project hash for validation
                project_hash = self._get_project_hash()
                f.write(f"{project_hash}\n")
                
                # Write guide paths
                for guide in guides:
                    f.write(f"{guide}\n")
            
            logger.debug(f"Cached {len(guides)} guides")
        except Exception as e:
            logger.warning(f"Error saving cache: {e}")
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
                logger.debug("Cache cleared")
        except Exception as e:
            logger.warning(f"Error clearing cache: {e}")
    
    @staticmethod
    def get_global_cache_dir() -> Path:
        """
        Get global cache directory path.
        
        Returns:
            Path to global cache directory
        """
        return Path(".specify/.cache")


class RuleEvaluationCache:
    """Caches rule evaluation results."""
    
    CACHE_DIR = Path(".specify/.cache")
    CACHE_FILE = CACHE_DIR / "rule_cache.txt"
    CACHE_EXPIRY_SECONDS = 1800  # 30 minutes
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize rule cache.
        
        Args:
            project_root: Root directory of project
        """
        self.project_root = Path(project_root) if project_root else Path(".")
        self.cache_dir = self.project_root / self.CACHE_DIR
        self.cache_file = self.project_root / self.CACHE_FILE
    
    def get_cached_result(self, rule_id: str, target: str) -> Optional[Dict]:
        """
        Get cached evaluation result.
        
        Args:
            rule_id: Rule identifier
            target: Evaluation target (e.g., file path)
        
        Returns:
            Cached result dict or None
        """
        # Placeholder for rule caching
        # Can be implemented if needed for performance
        return None
    
    def cache_result(self, rule_id: str, target: str, result: Dict) -> None:
        """
        Cache evaluation result.
        
        Args:
            rule_id: Rule identifier
            target: Evaluation target
            result: Result to cache
        """
        # Placeholder for rule caching
        pass
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        try:
            if self.cache_file.exists():
                self.cache_file.unlink()
                logger.debug("Rule cache cleared")
        except Exception as e:
            logger.warning(f"Error clearing rule cache: {e}")
