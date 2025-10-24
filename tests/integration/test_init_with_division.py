"""
Integration tests for init command with division support.
"""

import json
import subprocess
import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner

from specify_cli import app


class TestInitWithDivision:
    """Test init command with division parameter."""
    
    def test_init_with_division_ds(self, tmp_path):
        """Test specify init --division DS creates project with DS division."""
        # Use unique project name with timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        project_name = f"test-project-ds-{timestamp}"
        project_path = tmp_path / project_name
        
        # Mock the download_and_extract_template to avoid network calls
        with patch('specify_cli.commands.init.download_and_extract_template') as mock_download, \
             patch('specify_cli.commands.init.ensure_executable_scripts'), \
             patch('specify_cli.commands.init.is_git_repo', return_value=True), \
             patch('specify_cli.commands.init.init_git_repo', return_value=True), \
             patch('specify_cli.commands.init.clone_guides_as_submodule', return_value=True), \
             patch('specify_cli.commands.init.check_tool', return_value=True):
            
            # Configure mock to create the expected directory structure
            def mock_download_func(*args, **kwargs):
                project_path.mkdir(parents=True)
                (project_path / "context").mkdir()
                return project_path
            
            mock_download.side_effect = mock_download_func
            
            # Change to temp directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                
                # Run init command using CliRunner
                runner = CliRunner()
                result = runner.invoke(app, [
                    "init", project_name,
                    "--division", "DS", 
                    "--ai", "copilot", 
                    "--no-git"
                ])
                
                # Should succeed
                assert result.exit_code == 0
            finally:
                os.chdir(original_cwd)
            
            # Check that .specify/project.json was created with correct division
            config_file = project_path / ".specify" / "project.json"
            assert config_file.exists()
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            assert config["division"] == "DS"
    
    def test_init_default_division_se(self, tmp_path):
        """Test specify init without --division defaults to SE."""
        # Use unique project name with timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        project_name = f"test-project-default-{timestamp}"
        project_path = tmp_path / project_name
        
        # Mock the download_and_extract_template to avoid network calls
        with patch('specify_cli.commands.init.download_and_extract_template') as mock_download, \
             patch('specify_cli.commands.init.ensure_executable_scripts'), \
             patch('specify_cli.commands.init.is_git_repo', return_value=True), \
             patch('specify_cli.commands.init.init_git_repo', return_value=True), \
             patch('specify_cli.commands.init.clone_guides_as_submodule', return_value=True), \
             patch('specify_cli.commands.init.check_tool', return_value=True):
            
            # Configure mock to create the expected directory structure
            def mock_download_func(*args, **kwargs):
                project_path.mkdir(parents=True)
                (project_path / "context").mkdir()
                return project_path
            
            mock_download.side_effect = mock_download_func
            
            # Change to temp directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                
                # Run init command without --division using CliRunner
                runner = CliRunner()
                result = runner.invoke(app, [
                    "init", project_name,
                    "--ai", "copilot", 
                    "--no-git"
                ])
                
                # Should succeed
                assert result.exit_code == 0
            finally:
                os.chdir(original_cwd)
            
            # Check that .specify/project.json was created with SE division
            config_file = project_path / ".specify" / "project.json"
            assert config_file.exists()
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            assert config["division"] == "SE"
    
    def test_init_invalid_division_error(self, tmp_path):
        """Test specify init with invalid division shows error."""
        # Use unique project name with timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        project_name = f"test-project-invalid-{timestamp}"
        project_path = tmp_path / project_name
        
        # Mock the download_and_extract_template to avoid network calls
        with patch('specify_cli.commands.init.download_and_extract_template') as mock_download, \
             patch('specify_cli.commands.init.ensure_executable_scripts'), \
             patch('specify_cli.commands.init.is_git_repo', return_value=True), \
             patch('specify_cli.commands.init.init_git_repo', return_value=True), \
             patch('specify_cli.commands.init.clone_guides_as_submodule', return_value=True), \
             patch('specify_cli.commands.init.check_tool', return_value=True):
            
            # Configure mock to create the expected directory structure
            def mock_download_func(*args, **kwargs):
                project_path.mkdir(parents=True)
                (project_path / "context").mkdir()
                return project_path
            
            mock_download.side_effect = mock_download_func
            
            # Change to temp directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                
                # Run init command with invalid division using CliRunner
                runner = CliRunner()
                result = runner.invoke(app, [
                    "init", project_name,
                    "--ai", "copilot", 
                    "--division", "INVALID", 
                    "--no-git"
                ])
                
                # Should fail with error message
                assert result.exit_code != 0
                assert "Invalid division" in result.output
            finally:
                os.chdir(original_cwd)
    
    def test_init_here_option_with_division(self, tmp_path):
        """Test specify init --here with division parameter."""
        # Use unique project name with timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        project_name = f"test-project-here-{timestamp}"
        project_path = tmp_path / project_name
        
        # Create the project directory first
        project_path.mkdir()
        (project_path / "context").mkdir()
        
        # Mock the download_and_extract_template to avoid network calls
        with patch('specify_cli.commands.init.download_and_extract_template') as mock_download, \
             patch('specify_cli.commands.init.ensure_executable_scripts'), \
             patch('specify_cli.commands.init.is_git_repo', return_value=True), \
             patch('specify_cli.commands.init.init_git_repo', return_value=True), \
             patch('specify_cli.commands.init.clone_guides_as_submodule', return_value=True), \
             patch('specify_cli.commands.init.check_tool', return_value=True):
            
            # Configure mock to create the expected directory structure
            def mock_download_func(*args, **kwargs):
                # For --here, the template is extracted into the current directory
                return project_path
            
            mock_download.side_effect = mock_download_func
            
            # Change to project directory for --here
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(project_path)
                
                # Run init command with --here and division using CliRunner
                runner = CliRunner()
                result = runner.invoke(app, [
                    "init", 
                    "--ai", "copilot", 
                    "--division", "Platform", 
                    "--here", 
                    "--no-git",
                    "--force"  # Skip confirmation
                ])
                
                # Should succeed
                assert result.exit_code == 0
                
                # Check that .specify/project.json was created with Platform division
                config_file = project_path / ".specify" / "project.json"
                assert config_file.exists()
            finally:
                os.chdir(original_cwd)
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            assert config["division"] == "Platform"