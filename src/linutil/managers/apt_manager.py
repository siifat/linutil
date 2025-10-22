"""
APT Package Manager Implementation

Package manager for Debian-based distributions (Ubuntu, Debian, etc.)
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


class AptManager(BasePackageManager):
    """Package manager for APT (Debian/Ubuntu)."""
    
    def __init__(self, executor: Optional[CommandExecutor] = None):
        """
        Initialize APT package manager.
        
        Args:
            executor: Command executor (creates default if None)
        """
        super().__init__(package_type="apt")
        self.executor = executor or CommandExecutor(PrivilegeHandler())
    
    async def update_cache(self) -> bool:
        """Update APT package cache."""
        result = await self.executor.execute(
            "apt update",
            use_sudo=True,
            timeout=300
        )
        
        if result.success:
            self._cache_updated = True
            return True
        return False
    
    async def install_packages(
        self,
        packages: list[str],
        on_progress: Optional[Callable[[str], None]] = None
    ) -> InstallResult:
        """Install packages using APT."""
        # Ensure cache is updated
        if not self._cache_updated:
            if on_progress:
                on_progress("Updating package cache...")
            await self.update_cache()
        
        # Build install command
        packages_str = " ".join(packages)
        command = f"apt install -y {packages_str}"
        
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
        # Use dpkg-query which is faster than dpkg -l
        result = await self.executor.execute(
            f"dpkg-query -W -f='${{Status}}' {package} 2>/dev/null",
            use_sudo=False
        )
        
        return "install ok installed" in result.stdout
    
    async def search_package(self, query: str) -> list[PackageInfo]:
        """Search for packages."""
        result = await self.executor.execute(
            f"apt search {query}",
            use_sudo=False
        )
        
        packages: list[PackageInfo] = []
        
        # Parse apt search output
        # Format: package/suite version architecture
        #   description
        lines = result.stdout.split('\n')
        current_package = None
        
        for line in lines:
            # Package line starts without indentation
            if line and not line.startswith(' '):
                match = re.match(r'^([^/]+)/\S+\s+(\S+)', line)
                if match:
                    name = match.group(1)
                    version = match.group(2)
                    current_package = PackageInfo(
                        name=name,
                        version=version,
                        installed=False,
                        available=True
                    )
                    packages.append(current_package)
            # Description line is indented
            elif current_package and line.startswith('  '):
                current_package.description = line.strip()
        
        return packages
    
    async def get_package_info(self, package: str) -> Optional[PackageInfo]:
        """Get information about a package."""
        result = await self.executor.execute(
            f"apt show {package}",
            use_sudo=False
        )
        
        if not result.success:
            return None
        
        # Parse apt show output
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
            description=info.get('Description', ''),
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
            on_progress("Updating package lists...")
        
        if not await self.update_cache():
            return False
        
        if on_progress:
            on_progress("Upgrading packages...")
        
        # Use full-upgrade to handle dependencies properly
        result = await self.executor.execute(
            "apt full-upgrade -y",
            use_sudo=True,
            timeout=3600,  # 1 hour for system upgrade
            on_output=on_progress
        )
        
        return result.success
    
    def parse_output(self, output: str) -> dict[str, Any]:
        """Parse APT output for progress information."""
        info: dict[str, Any] = {
            "raw_output": output,
            "progress": None,
            "current_action": ""
        }
        
        # Look for progress indicators
        progress_match = re.search(r'Progress:\s*\[(\d+)%\]', output)
        if progress_match:
            info["progress"] = int(progress_match.group(1))
        
        # Determine current action
        if "Reading package lists" in output:
            info["current_action"] = "Reading package lists"
        elif "Building dependency tree" in output:
            info["current_action"] = "Building dependency tree"
        elif "Reading state information" in output:
            info["current_action"] = "Reading state information"
        elif "The following NEW packages will be installed" in output:
            info["current_action"] = "Calculating packages to install"
        elif "Unpacking" in output:
            info["current_action"] = "Unpacking packages"
        elif "Setting up" in output:
            info["current_action"] = "Setting up packages"
        elif "Processing triggers" in output:
            info["current_action"] = "Processing triggers"
        elif "Fetched" in output:
            info["current_action"] = "Downloading packages"
        
        return info
    
    def _extract_error(self, stderr: str, package: str) -> str:
        """Extract error message for a specific package."""
        # Look for common error patterns
        if f"E: Unable to locate package {package}" in stderr:
            return f"Package '{package}' not found in repositories"
        elif "E: Unmet dependencies" in stderr:
            return "Unmet dependencies"
        elif "E: Package" in stderr and "has no installation candidate" in stderr:
            return "No installation candidate available"
        else:
            # Return first error line
            for line in stderr.split('\n'):
                if line.startswith('E:'):
                    return line[3:].strip()
            return "Installation failed"


# Register with factory
PackageManagerFactory.register("apt", AptManager)


if __name__ == "__main__":
    # Test the APT manager
    import asyncio
    
    async def test():
        manager = AptManager()
        
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
