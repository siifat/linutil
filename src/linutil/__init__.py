"""
LinUtil - Linux Post-Install Setup Application

A modern, mouse-supported TUI application for automating Linux post-installation tasks.
"""

__version__ = "0.1.0"
__author__ = "LinUtil Contributors"
__license__ = "MIT"

from linutil.core.distro_detector import detect_distribution, DistroInfo
from linutil.core.config_loader import ConfigLoader

__all__ = ["detect_distribution", "DistroInfo", "ConfigLoader", "__version__"]
