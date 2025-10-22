"""
Distribution Detection Module

Detects the Linux distribution, version, and package manager.
"""

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


class DistroDetectionError(Exception):
    """Raised when distribution detection fails."""
    pass


@dataclass
class DistroInfo:
    """Information about the detected Linux distribution."""
    
    name: str  # e.g., "ubuntu", "fedora", "arch"
    version: str  # e.g., "24.04", "40"
    codename: str  # e.g., "noble", "jammy"
    pretty_name: str  # e.g., "Ubuntu 24.04 LTS"
    package_manager: str  # e.g., "apt", "dnf", "pacman"
    id_like: list[str]  # e.g., ["debian"], ["rhel", "fedora"]
    
    def __str__(self) -> str:
        return f"{self.pretty_name} ({self.package_manager})"
    
    def is_debian_based(self) -> bool:
        """Check if this is a Debian-based distribution."""
        return self.name in ["ubuntu", "debian"] or "debian" in self.id_like
    
    def is_fedora_based(self) -> bool:
        """Check if this is a Fedora-based distribution."""
        return self.name in ["fedora", "rhel", "centos"] or "fedora" in self.id_like
    
    def is_arch_based(self) -> bool:
        """Check if this is an Arch-based distribution."""
        return self.name in ["arch", "manjaro"] or "arch" in self.id_like


def parse_os_release(file_path: Path = Path("/etc/os-release")) -> dict[str, str]:
    """
    Parse /etc/os-release file.
    
    Args:
        file_path: Path to os-release file
        
    Returns:
        Dictionary of key-value pairs from os-release
        
    Raises:
        FileNotFoundError: If os-release file doesn't exist
    """
    os_release = {}
    
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                    
                if "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes from value
                    value = value.strip('"').strip("'")
                    os_release[key] = value
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {file_path}")
    
    return os_release


def determine_package_manager(distro_name: str, id_like: list[str]) -> str:
    """
    Determine the package manager based on distribution.
    
    Args:
        distro_name: The distribution ID
        id_like: List of similar distribution IDs
        
    Returns:
        Package manager name (apt, dnf, pacman, etc.)
        
    Raises:
        DistroDetectionError: If package manager cannot be determined
    """
    # Direct mapping for known distributions
    package_manager_map = {
        "ubuntu": "apt",
        "debian": "apt",
        "linuxmint": "apt",
        "pop": "apt",
        "fedora": "dnf",
        "rhel": "dnf",
        "centos": "dnf",
        "rocky": "dnf",
        "almalinux": "dnf",
        "arch": "pacman",
        "manjaro": "pacman",
        "endeavouros": "pacman",
        "opensuse": "zypper",
        "opensuse-tumbleweed": "zypper",
        "opensuse-leap": "zypper",
    }
    
    # Check direct match
    if distro_name in package_manager_map:
        return package_manager_map[distro_name]
    
    # Check ID_LIKE for derived distributions
    for similar_id in id_like:
        if similar_id in package_manager_map:
            return package_manager_map[similar_id]
    
    # Final attempt: check which package manager is installed
    for pm_name, pm_command in [("apt", "apt"), ("dnf", "dnf"), ("pacman", "pacman"), ("zypper", "zypper")]:
        if shutil.which(pm_command):
            return pm_name
    
    raise DistroDetectionError(
        f"Could not determine package manager for distribution: {distro_name}"
    )


def detect_distribution() -> DistroInfo:
    """
    Detect the current Linux distribution.
    
    Returns:
        DistroInfo object with distribution details
        
    Raises:
        DistroDetectionError: If distribution cannot be detected
    """
    try:
        # Try modern /etc/os-release first (freedesktop.org standard)
        os_release_path = Path("/etc/os-release")
        if not os_release_path.exists():
            # Fallback to /usr/lib/os-release
            os_release_path = Path("/usr/lib/os-release")
        
        if os_release_path.exists():
            os_release = parse_os_release(os_release_path)
            
            distro_name = os_release.get("ID", "").lower()
            version = os_release.get("VERSION_ID", "")
            codename = os_release.get("VERSION_CODENAME", "")
            pretty_name = os_release.get("PRETTY_NAME", distro_name)
            id_like_str = os_release.get("ID_LIKE", "")
            id_like = [x.strip() for x in id_like_str.split()] if id_like_str else []
            
            if not distro_name:
                raise DistroDetectionError("Could not determine distribution ID")
            
            # Determine package manager
            package_manager = determine_package_manager(distro_name, id_like)
            
            return DistroInfo(
                name=distro_name,
                version=version,
                codename=codename,
                pretty_name=pretty_name,
                package_manager=package_manager,
                id_like=id_like,
            )
        
        # Fallback to lsb_release command
        elif shutil.which("lsb_release"):
            return _detect_via_lsb_release()
        
        else:
            raise DistroDetectionError(
                "Could not find /etc/os-release or lsb_release command"
            )
            
    except Exception as e:
        if isinstance(e, DistroDetectionError):
            raise
        raise DistroDetectionError(f"Error detecting distribution: {e}")


def _detect_via_lsb_release() -> DistroInfo:
    """
    Fallback method using lsb_release command.
    
    Returns:
        DistroInfo object
        
    Raises:
        DistroDetectionError: If lsb_release fails
    """
    try:
        result = subprocess.run(
            ["lsb_release", "-a"],
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout
        
        # Parse lsb_release output
        distro_id = ""
        version = ""
        codename = ""
        description = ""
        
        for line in output.split("\n"):
            if "Distributor ID:" in line:
                distro_id = line.split(":", 1)[1].strip().lower()
            elif "Release:" in line:
                version = line.split(":", 1)[1].strip()
            elif "Codename:" in line:
                codename = line.split(":", 1)[1].strip()
            elif "Description:" in line:
                description = line.split(":", 1)[1].strip()
        
        if not distro_id:
            raise DistroDetectionError("lsb_release did not provide distribution ID")
        
        package_manager = determine_package_manager(distro_id, [])
        
        return DistroInfo(
            name=distro_id,
            version=version,
            codename=codename,
            pretty_name=description or distro_id,
            package_manager=package_manager,
            id_like=[],
        )
        
    except subprocess.CalledProcessError as e:
        raise DistroDetectionError(f"lsb_release command failed: {e}")


# Convenience function for testing
def get_distro_name() -> str:
    """
    Get just the distribution name.
    
    Returns:
        Distribution name (e.g., "ubuntu", "fedora")
    """
    return detect_distribution().name


if __name__ == "__main__":
    # Test the detection
    try:
        distro = detect_distribution()
        print(f"Detected Distribution: {distro}")
        print(f"  Name: {distro.name}")
        print(f"  Version: {distro.version}")
        print(f"  Codename: {distro.codename}")
        print(f"  Package Manager: {distro.package_manager}")
        print(f"  ID Like: {distro.id_like}")
    except DistroDetectionError as e:
        print(f"Error: {e}")
