"""
Task List Indicators Guide

This module provides documentation for the task list indicator system
used in LinUtil, inspired by Chris Titus Tech's LinUtil.
"""

# Task List Indicators
# These indicators help users understand what operations a command will perform
# They appear next to each application/tweak in brackets, e.g., "Firefox [I]"

TASK_INDICATORS = {
    "I": {
        "name": "Installation",
        "description": "Installs packages or software",
        "color": "green",
        "requires_sudo": True,
        "examples": ["Installing Firefox", "Installing development tools"]
    },
    "FM": {
        "name": "File Modification",
        "description": "Modifies system or user configuration files",
        "color": "yellow",
        "requires_sudo": False,  # Depends on file location
        "examples": ["Editing .bashrc", "Modifying config files"]
    },
    "D": {
        "name": "Disk Operations",
        "description": "Performs disk partitioning or modifications",
        "color": "red",
        "requires_sudo": True,
        "examples": ["Partitioning drives", "Formatting disks"]
    },
    "SS": {
        "name": "SystemD Service",
        "description": "Starts, stops, or manages systemd services",
        "color": "blue",
        "requires_sudo": True,
        "examples": ["Enabling Docker service", "Starting firewalld"]
    },
    "K": {
        "name": "Kernel Modifications",
        "description": "Modifies kernel parameters or modules",
        "color": "red",
        "requires_sudo": True,
        "examples": ["Installing kernel modules", "Updating grub"]
    },
    "FI": {
        "name": "Flatpak Installation",
        "description": "Installs applications via Flatpak",
        "color": "cyan",
        "requires_sudo": False,
        "examples": ["Installing Flatpak apps from Flathub"]
    },
    "MP": {
        "name": "Package Manager",
        "description": "Package manager operations (updates, repositories)",
        "color": "green",
        "requires_sudo": True,
        "examples": ["Adding repositories", "Updating package cache"]
    },
    "P*": {
        "name": "Privileged Operation",
        "description": "Requires elevated (root) privileges",
        "color": "red",
        "requires_sudo": True,
        "examples": ["Any operation requiring sudo/root"]
    },
    "SI": {
        "name": "Full System Installation",
        "description": "Complete system installation or major setup",
        "color": "red",
        "requires_sudo": True,
        "examples": ["Installing entire desktop environment"]
    },
    "RP": {
        "name": "Package Removal",
        "description": "Removes packages from the system",
        "color": "yellow",
        "requires_sudo": True,
        "examples": ["Removing unused packages", "Uninstalling software"]
    }
}


def get_task_description(task_code: str) -> str:
    """
    Get the description for a task indicator code.
    
    Args:
        task_code: The task indicator code (e.g., "I", "FM", "D")
        
    Returns:
        Human-readable description of the task
    """
    task_info = TASK_INDICATORS.get(task_code, {})
    return task_info.get("description", "Unknown task")


def get_combined_task_description(task_list: str) -> str:
    """
    Get combined description for multiple task indicators.
    
    Args:
        task_list: Space-separated task codes (e.g., "I FM", "SS MP")
        
    Returns:
        Combined description of all tasks
    """
    tasks = task_list.split()
    descriptions = []
    
    for task in tasks:
        if task in TASK_INDICATORS:
            descriptions.append(TASK_INDICATORS[task]["name"])
    
    return " + ".join(descriptions) if descriptions else "Unknown"


def requires_sudo(task_list: str) -> bool:
    """
    Check if any task in the list requires sudo privileges.
    
    Args:
        task_list: Space-separated task codes
        
    Returns:
        True if any task requires sudo
    """
    tasks = task_list.split()
    return any(
        TASK_INDICATORS.get(task, {}).get("requires_sudo", False)
        for task in tasks
    )


# Example Usage in YAML:
"""
tweaks:
  - id: "install-docker"
    name: "Install Docker"
    description: "Installs Docker container platform"
    task_list: "I SS"  # Installation + SystemD Service
    commands:
      - command: "dnf install -y docker"
      - command: "systemctl enable --now docker"
  
  - id: "optimize-dnf"
    name: "Optimize DNF"
    description: "Improves DNF download speed"
    task_list: "FM MP"  # File Modification + Package Manager
    commands:
      - command: "echo 'max_parallel_downloads=10' >> /etc/dnf/dnf.conf"
"""
