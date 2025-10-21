"""
Unit tests for governance caching module.
"""

import time
from pathlib import Path
import pytest
import tempfile
import shutil

from specify_cli.governance.caching import (
    GuideCacheManager,
    RuleEvaluationCache
)


class TestGuideCacheManager:
    """Test GuideCacheManager class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project structure."""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        
        # Create necessary directories
        specs_dir = project_root / "specs"
        specs_dir.mkdir(exist_ok=True)
        
        context_dir = project_root / "context" / "references"
        context_dir.mkdir(parents=True, exist_ok=True)
        
        cache_dir = project_root / ".specify" / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create some markdown files
        (specs_dir / "backend.md").write_text("# Backend Guide")
        (context_dir / "architecture.md").write_text("# Architecture")
        
        yield project_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_cache_manager_initialization(self, temp_project):
        """Test cache manager initialization."""
        manager = GuideCacheManager(temp_project)
        assert manager.project_root == temp_project
        assert manager.cache_dir == temp_project / ".specify" / ".cache"
    
    def test_get_project_hash(self, temp_project):
        """Test project hash generation."""
        manager = GuideCacheManager(temp_project)
        hash1 = manager._get_project_hash()
        
        # Hash should be consistent
        hash2 = manager._get_project_hash()
        assert hash1 == hash2
        
        # Hash should change when files are added
        (temp_project / "specs" / "frontend.md").write_text("# Frontend")
        hash3 = manager._get_project_hash()
        assert hash1 != hash3
    
    def test_save_and_get_guides(self, temp_project):
        """Test saving and retrieving guides from cache."""
        manager = GuideCacheManager(temp_project)
        
        guides = [
            temp_project / "specs" / "backend.md",
            temp_project / "context" / "references" / "architecture.md"
        ]
        
        # Save guides
        manager.save_guides(guides)
        assert manager.cache_file.exists()
        
        # Retrieve guides
        cached = manager.get_guides()
        assert cached is not None
        assert len(cached) == 2
    
    def test_cache_invalid_after_modification(self, temp_project):
        """Test cache invalidation after project modification."""
        manager = GuideCacheManager(temp_project)
        
        guides = [temp_project / "specs" / "backend.md"]
        manager.save_guides(guides)
        
        # Cache should be valid
        cached = manager.get_guides()
        assert cached is not None
        
        # Modify a guide file
        time.sleep(0.1)
        (temp_project / "specs" / "backend.md").write_text("# Backend Guide Modified")
        
        # Cache should be invalid now
        cached = manager.get_guides()
        assert cached is None
    
    def test_cache_expiry(self, temp_project):
        """Test cache expiry based on time."""
        manager = GuideCacheManager(temp_project)
        
        # Set very short expiry for testing
        original_expiry = manager.CACHE_EXPIRY_SECONDS
        manager.CACHE_EXPIRY_SECONDS = 1
        
        try:
            guides = [temp_project / "specs" / "backend.md"]
            manager.save_guides(guides)
            
            # Cache should be valid immediately
            cached = manager.get_guides()
            assert cached is not None
            
            # Wait for expiry
            time.sleep(1.1)
            
            # Cache should be expired
            cached = manager.get_guides()
            assert cached is None
        finally:
            manager.CACHE_EXPIRY_SECONDS = original_expiry
    
    def test_clear_cache(self, temp_project):
        """Test clearing cache."""
        manager = GuideCacheManager(temp_project)
        
        guides = [temp_project / "specs" / "backend.md"]
        manager.save_guides(guides)
        assert manager.cache_file.exists()
        
        manager.clear_cache()
        assert not manager.cache_file.exists()
    
    def test_get_global_cache_dir(self):
        """Test getting global cache directory."""
        cache_dir = GuideCacheManager.get_global_cache_dir()
        assert cache_dir == Path(".specify/.cache")
    
    def test_cache_no_guides(self, temp_project):
        """Test cache behavior when no guides found."""
        # Create empty project
        empty_project = Path(tempfile.mkdtemp())
        empty_project.joinpath(".specify/.cache").mkdir(parents=True, exist_ok=True)
        
        try:
            manager = GuideCacheManager(empty_project)
            
            # Don't save guides - cache should return None (no cache file)
            cached = manager.get_guides()
            assert cached is None
        finally:
            shutil.rmtree(empty_project)


class TestRuleEvaluationCache:
    """Test RuleEvaluationCache class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project structure."""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        cache_dir = project_root / ".specify" / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        yield project_root
        
        shutil.rmtree(temp_dir)
    
    def test_rule_cache_initialization(self, temp_project):
        """Test rule cache initialization."""
        cache = RuleEvaluationCache(temp_project)
        assert cache.project_root == temp_project
    
    def test_get_cached_result_placeholder(self, temp_project):
        """Test get_cached_result placeholder."""
        cache = RuleEvaluationCache(temp_project)
        result = cache.get_cached_result("R-001", "test-file.md")
        assert result is None  # Placeholder returns None
    
    def test_cache_result_placeholder(self, temp_project):
        """Test cache_result placeholder."""
        cache = RuleEvaluationCache(temp_project)
        # Should not raise
        cache.cache_result("R-001", "test-file.md", {"status": "pass"})
    
    def test_clear_cache(self, temp_project):
        """Test clearing rule cache."""
        cache = RuleEvaluationCache(temp_project)
        # Create dummy cache file
        cache.cache_file.write_text("dummy")
        
        cache.clear_cache()
        assert not cache.cache_file.exists()
    
    def test_clear_nonexistent_cache(self, temp_project):
        """Test clearing cache when file doesn't exist."""
        cache = RuleEvaluationCache(temp_project)
        # Should not raise
        cache.clear_cache()
        assert not cache.cache_file.exists()


class TestCachingIntegration:
    """Integration tests for caching."""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project with guides."""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        
        # Create directories
        specs_dir = project_root / "specs" / "feature"
        specs_dir.mkdir(parents=True)
        
        context_dir = project_root / "context" / "references"
        context_dir.mkdir(parents=True)
        
        cache_dir = project_root / ".specify" / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create guides
        (specs_dir / "backend.md").write_text("# Backend")
        (specs_dir / "frontend.md").write_text("# Frontend")
        (context_dir / "standards.md").write_text("# Standards")
        
        yield project_root
        
        shutil.rmtree(temp_dir)
    
    def test_cache_multiple_guides(self, temp_project):
        """Test caching multiple guides."""
        manager = GuideCacheManager(temp_project)
        
        guides1 = [
            temp_project / "specs" / "feature" / "backend.md",
            temp_project / "specs" / "feature" / "frontend.md",
            temp_project / "context" / "references" / "standards.md"
        ]
        
        # Cache them
        manager.save_guides(guides1)
        
        # Get from cache
        guides2 = manager.get_guides()
        assert guides2 is not None
        assert len(guides2) == 3
    
    def test_cache_preserves_guide_order(self, temp_project):
        """Test that cache preserves guide order."""
        manager = GuideCacheManager(temp_project)
        
        guides1 = sorted([
            temp_project / "specs" / "feature" / "backend.md",
            temp_project / "context" / "references" / "standards.md"
        ])
        
        manager.save_guides(guides1)
        guides2 = manager.get_guides()
        
        assert guides1 == guides2
