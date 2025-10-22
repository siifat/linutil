"""
DNF Package Manager Implementation

Package manager for Fedora-based distributions (Fedora, RHEL, CentOS, etc.)
"""

import re
from typing import Optional, Callable, Any

from linutil.managers.base_manager import (
    BasePackageManager,
    PackageInfo,
    InstallResult,
    PackageManagerFactory
)
from linutil.core.executor import CommandExecutor, PrivilegeHandler


class DnfManager(BasePackageManager):
    """Package manager for DNF (Fedora/RHEL)."""
    
    def __init__(self, executor: Optional[CommandExecutor] = None):
        """
        Initialize DNF package manager.
        
        Args:
            executor: Command executor (creates default if None)
        """
        super().__init__(package_type="dnf")
        self.executor = executor or CommandExecutor(PrivilegeHandler())
    
    async def update_cache(self) -> bool:
        """Update DNF package cache."""
        result = await self.executor.execute(
            "dnf check-update",
            use_sudo=True,
            timeout=300
        )
        
        # DNF check-update returns 100 if updates are available, 0 if not
        # So we consider both success
        if result.return_code in [0, 100]:
            self._cache_updated = True
            return True
        return False
    
    async def install_packages(
        self,
        packages: list[str],
        on_progress: Optional[Callable[[str], None]] = None
    ) -> InstallResult:
        """Install packages using DNF."""
        # Ensure cache is updated
        if not self._cache_updated:
            if on_progress:
                on_progress("Updating package cache...")
            await self.update_cache()
        
        # Build install command
        packages_str = " ".join(packages)
        command = f"dnf install -y {packages_str}"
        
        installed: list[str] = []
        failed: list[str] = []
        errors: dict[str, str] = {}
        
        # Execute installation
        result = await self.executor.execute(
            command,
            use_sudo=True,
            timeout=1800,  # 30 minutes for large installations
            on_output=on_progress
        )
        
        if result.success:
            # All packages installed successfully
            installed = packages.copy()
        else:
            # Try to determine which packages failed
            # Check each package individually
            for package in packages:
                is_installed = await self.is_package_installed(package)
                if is_installed:
                    installed.append(package)
                else:
                    failed.append(package)
                    # Try to extract error from output
                    error_msg = self._extract_error(result.stderr, package)
                    errors[package] = error_msg
        
        return InstallResult(
            success=result.success,
            packages_installed=installed,
            packages_failed=failed,
            errors=errors,
            output=result.output
        )
    
    async def is_package_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        # Use rpm -q which is faster than dnf list
        result = await self.executor.execute(
            f"rpm -q {package}",
            use_sudo=False
        )
        
        return result.return_code == 0
    
    async def search_package(self, query: str) -> list[PackageInfo]:
        """Search for packages."""
        result = await self.executor.execute(
            f"dnf search {query}",
            use_sudo=False
        )
        
        packages: list[PackageInfo] = []
        
        # Parse dnf search output
        # Format: name.arch : description
        lines = result.stdout.split('\n')
        in_results = False
        
        for line in lines:
            # Results start after a separator line
            if "=" in line and len(line) > 50:
                in_results = True
                continue
            
            if in_results and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    name_arch = parts[0].strip()
                    description = parts[1].strip()
                    
                    # Extract package name (remove .arch)
                    name = name_arch.split('.')[0] if '.' in name_arch else name_arch
                    
                    packages.append(PackageInfo(
                        name=name,
                        description=description,
                        installed=False,
                        available=True
                    ))
        
        return packages
    
    async def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """Get information about a package."""
        result = await self.executor.execute(
            f"dnf info {package}",
            use_sudo=False
        )
        
        if not result.success:
            return None
        
        # Parse dnf info output
        info: dict[str, str] = {}
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        
        # Check if installed
        is_installed = await self.is_package_installed(package)
        
        return PackageInfo(
            name=package,
            version=info.get('Version', ''),
            description=info.get('Summary', ''),
            installed=is_installed,
            available=True
        )
    
    async def upgrade_system(
        self,
        on_progress: Optional[Callable[[str], None]] = None
    ) -> bool:
        """Upgrade all installed packages."""
        # Update cache first
        if on_progress:
            on_progress("Checking for updates...")
        
        if not await self.update_cache():
            return False
        
        if on_progress:
            on_progress("Upgrading packages...")
        
        # Use upgrade command
        result = await self.executor.execute(
            "dnf upgrade -y",
            use_sudo=True,
            timeout=3600,  # 1 hour for system upgrade
            on_output=on_progress
        )
        
        return result.success
    
    def parse_output(self, output: str) -> dict[str, Any]:
        """Parse DNF output for progress information."""
        info: dict[str, Any] = {
            "raw_output": output,
            "progress": None,
            "current_action": ""
        }
        
        # Determine current action
        if "Downloading Packages:" in output:
            info["current_action"] = "Downloading packages"
        elif "Installing:" in output:
            info["current_action"] = "Installing packages"
        elif "Upgrading:" in output:
            info["current_action"] = "Upgrading packages"
        elif "Running transaction check" in output:
            info["current_action"] = "Checking transaction"
        elif "Running transaction test" in output:
            info["current_action"] = "Testing transaction"
        elif "Running transaction" in output:
            info["current_action"] = "Running transaction"
        elif "Verifying" in output:
            info["current_action"] = "Verifying packages"
        elif "Complete!" in output:
            info["current_action"] = "Complete"
            info["progress"] = 100
        
        # Try to extract progress from download indicators
        # DNF shows: (1/10): package.rpm
        progress_match = re.search(r'\((\d+)/(\d+)\):', output)
        if progress_match:
            current = int(progress_match.group(1))
            total = int(progress_match.group(2))
            if total > 0:
                info["progress"] = int((current / total) * 100)
        
        return info
    
    def _extract_error(self, stderr: str, package: str) -> str:
        """Extract error message for a specific package."""
        # Look for common error patterns
        if f"No match for argument: {package}" in stderr:
            return f"Package '{package}' not found in repositories"
        elif "Error: Unable to find a match" in stderr:
            return f"Package '{package}' not available"
        elif "conflicts with" in stderr:
            return "Package conflicts with installed packages"
        elif "Insufficient space" in stderr:
            return "Insufficient disk space"
        else:
            # Return first error line
            for line in stderr.split('\n'):
                if line.startswith('Error:'):
                    return line[7:].strip()
            return "Installation failed"


# Register with factory
PackageManagerFactory.register("dnf", DnfManager)


if __name__ == "__main__":
    # Test the DNF manager
    import asyncio
    
    async def test():
        manager = DnfManager()
        
        print("Testing package check...")
        is_installed = await manager.is_package_installed("curl")
        print(f"curl installed: {is_installed}")
        
        print("\nTesting package info...")
        info = await manager.get_package_info("htop")
        if info:
            print(f"Package: {info.name}")
            print(f"Version: {info.version}")
            print(f"Installed: {info.installed}")
        
        print("\nTesting search...")
        results = await manager.search_package("python3")
        print(f"Found {len(results)} packages")
        for pkg in results[:5]:
            print(f"  - {pkg.name}: {pkg.description}")
    
    asyncio.run(test())
