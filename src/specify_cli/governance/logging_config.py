"""
Logging configuration for governance layer.

Provides centralized logging setup for all governance operations.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_governance_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> None:
    """
    Configure logging for governance operations.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional file to write logs to
    """
    # Create logger for governance
    logger = logging.getLogger('specify_cli.governance')
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '[%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def get_governance_logger(name: str) -> logging.Logger:
    """
    Get a logger for the governance module.
    
    Args:
        name: Name of the module
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f'specify_cli.governance.{name}')
