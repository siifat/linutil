"""
Base Package Manager Module

Abstract base class for all package managers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Callable, Any
from enum import Enum


class InstallMethod(Enum):
    """Installation method."""
    NATIVE = "native"
    CUSTOM = "custom"
    FLATPAK = "flatpak"


@dataclass
class PackageInfo:
    """Information about a package."""
    
    name: str
    version: str = ""
    description: str = ""
    installed: bool = False
    available: bool = False


@dataclass
class InstallResult:
    """Result of package installation."""
    
    success: bool
    packages_installed: list[str]
    packages_failed: list[str]
    errors: dict[str, str]  # package_name -> error_message
    output: str = ""
    
    @property
    def all_successful(self) -> bool:
        """Check if all packages installed successfully."""
        return self.success and len(self.packages_failed) == 0


class BasePackageManager(ABC):
    """Abstract base class for package managers."""
    
    def __init__(self, package_type: str):
        """
        Initialize package manager.
        
        Args:
            package_type: Type of package manager (apt, dnf, etc.)
        """
        self.package_type = package_type
        self._cache_updated = False
    
    @abstractmethod
    async def update_cache(self) -> bool:
        """
        Update package cache/repository lists.
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def install_packages(
        self,
        packages: list[str],
        on_progress: Optional[Callable[[str], None]] = None
    ) -> InstallResult:
        """
        Install packages using the package manager.
        
        Args:
            packages: List of package names to install
            on_progress: Callback for progress updates
            
        Returns:
            InstallResult with installation details
        """
        pass
    
    @abstractmethod
    async def is_package_installed(self, package: str) -> bool:
        """
        Check if a package is installed.
        
        Args:
            package: Package name
            
        Returns:
            True if installed
        """
        pass
    
    @abstractmethod
    async def search_package(self, query: str) -> list[PackageInfo]:
        """
        Search for packages.
        
        Args:
            query: Search query
            
        Returns:
            List of matching packages
        """
        pass
    
    @abstractmethod
    async def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """
        Get information about a package.
        
        Args:
            package: Package name
            
        Returns:
            PackageInfo or None if not found
        """
        pass
    
    async def upgrade_system(
        self,
        on_progress: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Upgrade all installed packages.
        
        Args:
            on_progress: Callback for progress updates
            
        Returns:
            True if successful
        """
        # Default implementation - subclasses should override
        return False
    
    def parse_output(self, output: str) -> dict[str, Any]:
        """
        Parse package manager output into standardized format.
        
        Args:
            output: Raw output from package manager
            
        Returns:
            Dictionary with parsed information
        """
        # Default implementation - subclasses should override for specific parsing
        return {
            "raw_output": output,
            "progress": None,
            "current_action": ""
        }


class PackageManagerFactory:
    """Factory for creating package manager instances."""
    
    _managers: dict[str, type[BasePackageManager]] = {}
    
    @classmethod
    def register(cls, package_type: str, manager_class: type[BasePackageManager]):
        """
        Register a package manager implementation.
        
        Args:
            package_type: Package manager type (apt, dnf, etc.)
            manager_class: Package manager class
        """
        cls._managers[package_type] = manager_class
    
    @classmethod
    def create(cls, package_type: str, **kwargs) -> Optional[BasePackageManager]:
        """
        Create a package manager instance.
        
        Args:
            package_type: Package manager type
            **kwargs: Additional arguments for the manager
            
        Returns:
            Package manager instance or None if not registered
        """
        manager_class = cls._managers.get(package_type)
        if manager_class:
            return manager_class(**kwargs)
        return None
    
    @classmethod
    def get_available_managers(cls) -> list[str]:
        """Get list of registered package manager types."""
        return list(cls._managers.keys())
