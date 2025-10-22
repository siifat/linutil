"""
Configuration Loader Module

Loads and merges YAML configuration files based on detected distribution.
"""

import yaml
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass

from linutil.core.distro_detector import DistroInfo


class ConfigLoadError(Exception):
    """Raised when configuration loading fails."""
    pass


@dataclass
class AppDefinition:
    """Definition of an installable application."""
    
    id: str
    name: str
    description: str
    install: dict[str, Any]
    tags: list[str]
    category: str = ""
    
    def supports_package_manager(self, pm: str) -> bool:
        """Check if this app supports a given package manager."""
        return pm in self.install or "flatpak" in self.install


@dataclass
class TweakDefinition:
    """Definition of a system tweak."""
    
    id: str
    name: str
    description: str
    category: str
    commands: list[dict[str, str]]
    requires_restart: bool = False
    idempotent: bool = True
    dependencies: list[str] = None
    verification: Optional[dict[str, str]] = None
    section: str = ""
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class AppConfig:
    """Application configuration."""
    
    categories: list[dict[str, Any]]
    
    def get_all_apps(self) -> list[AppDefinition]:
        """Get all applications as AppDefinition objects."""
        apps = []
        for category in self.categories:
            cat_name = category.get("name", "")
            for app_data in category.get("applications", []):
                app = AppDefinition(
                    id=app_data["id"],
                    name=app_data["name"],
                    description=app_data["description"],
                    install=app_data["install"],
                    tags=app_data.get("tags", []),
                    category=cat_name,
                )
                apps.append(app)
        return apps


@dataclass
class TweakConfig:
    """Tweak configuration."""
    
    sections: list[dict[str, Any]]
    distro: str = ""
    compatible_versions: list[str] = None
    
    def __post_init__(self):
        if self.compatible_versions is None:
            self.compatible_versions = []
    
    def get_all_tweaks(self) -> list[TweakDefinition]:
        """Get all tweaks as TweakDefinition objects."""
        tweaks = []
        for section in self.sections:
            section_name = section.get("name", "")
            for tweak_data in section.get("tweaks", []):
                tweak = TweakDefinition(
                    id=tweak_data["id"],
                    name=tweak_data["name"],
                    description=tweak_data["description"],
                    category=tweak_data.get("category", ""),
                    commands=tweak_data["commands"],
                    requires_restart=tweak_data.get("requires_restart", False),
                    idempotent=tweak_data.get("idempotent", True),
                    dependencies=tweak_data.get("dependencies", []),
                    verification=tweak_data.get("verification"),
                    section=section_name,
                )
                tweaks.append(tweak)
        return tweaks


class ConfigLoader:
    """Loads and manages configuration files."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Path to configuration directory (defaults to package data/)
        """
        if config_dir is None:
            # Default to package's data directory
            # From src/linutil/core/config_loader.py -> go up to project root
            package_root = Path(__file__).parent.parent.parent.parent
            self.config_dir = package_root / "data"
        else:
            self.config_dir = Path(config_dir)
        
        self.apps_dir = self.config_dir / "apps"
        self.tweaks_dir = self.config_dir / "tweaks"
    
    def load_yaml(self, file_path: Path) -> dict[str, Any]:
        """
        Load a YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Parsed YAML data
            
        Raises:
            ConfigLoadError: If file cannot be loaded
        """
        try:
            if not file_path.exists():
                return {}
            
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
                
        except yaml.YAMLError as e:
            raise ConfigLoadError(f"Error parsing YAML file {file_path}: {e}")
        except Exception as e:
            raise ConfigLoadError(f"Error loading {file_path}: {e}")
    
    def merge_app_configs(
        self,
        common_apps: dict[str, Any],
        distro_apps: dict[str, Any],
        distro_info: DistroInfo
    ) -> AppConfig:
        """
        Merge common and distro-specific app configurations.
        Filters out apps that don't support the current package manager.
        
        Args:
            common_apps: Common app configuration
            distro_apps: Distro-specific app configuration
            distro_info: Distribution information
            
        Returns:
            Merged AppConfig
        """
        package_manager = distro_info.package_manager
        merged_categories: dict[str, dict[str, Any]] = {}
        
        # Process common apps
        for category in common_apps.get("categories", []):
            cat_name = category["name"]
            merged_categories[cat_name] = {
                "name": cat_name,
                "icon": category.get("icon", "📦"),
                "applications": []
            }
            
            for app in category.get("applications", []):
                # Check if app supports this package manager or flatpak
                install_methods = app.get("install", {})
                if package_manager in install_methods or "flatpak" in install_methods:
                    merged_categories[cat_name]["applications"].append(app)
        
        # Merge distro-specific apps
        for category in distro_apps.get("categories", []):
            cat_name = category["name"]
            
            if cat_name not in merged_categories:
                merged_categories[cat_name] = {
                    "name": cat_name,
                    "icon": category.get("icon", "📦"),
                    "applications": []
                }
            
            for app in category.get("applications", []):
                install_methods = app.get("install", {})
                if package_manager in install_methods or "flatpak" in install_methods:
                    # Check for duplicates by ID
                    existing_ids = [
                        a["id"] for a in merged_categories[cat_name]["applications"]
                    ]
                    if app["id"] not in existing_ids:
                        merged_categories[cat_name]["applications"].append(app)
        
        # Filter out empty categories
        filtered_categories = [
            cat for cat in merged_categories.values() 
            if cat["applications"]
        ]
        
        return AppConfig(categories=filtered_categories)
    
    def merge_tweak_configs(
        self,
        common_tweaks: dict[str, Any],
        distro_tweaks: dict[str, Any]
    ) -> TweakConfig:
        """
        Merge common and distro-specific tweak configurations.
        
        Args:
            common_tweaks: Common tweak configuration
            distro_tweaks: Distro-specific tweak configuration
            
        Returns:
            Merged TweakConfig
        """
        merged_sections: dict[str, dict[str, Any]] = {}
        
        # Process distro-specific tweaks first (higher priority)
        for section in distro_tweaks.get("sections", []):
            section_name = section["name"]
            merged_sections[section_name] = {
                "name": section_name,
                "icon": section.get("icon", "🔧"),
                "tweaks": section.get("tweaks", []).copy()
            }
        
        # Add common tweaks
        for section in common_tweaks.get("sections", []):
            section_name = section["name"]
            
            if section_name not in merged_sections:
                merged_sections[section_name] = {
                    "name": section_name,
                    "icon": section.get("icon", "🔧"),
                    "tweaks": []
                }
            
            # Add tweaks that don't already exist
            existing_ids = [
                t["id"] for t in merged_sections[section_name]["tweaks"]
            ]
            for tweak in section.get("tweaks", []):
                if tweak["id"] not in existing_ids:
                    merged_sections[section_name]["tweaks"].append(tweak)
        
        # Filter out empty sections
        filtered_sections = [
            sec for sec in merged_sections.values()
            if sec["tweaks"]
        ]
        
        return TweakConfig(
            sections=filtered_sections,
            distro=distro_tweaks.get("distro", ""),
            compatible_versions=distro_tweaks.get("compatible_versions", [])
        )
    
    def load_configurations(self, distro_info: DistroInfo) -> dict[str, Any]:
        """
        Load and merge all configurations based on detected distribution.
        
        Args:
            distro_info: Distribution information
            
        Returns:
            Dictionary with 'apps' and 'tweaks' configurations
            
        Raises:
            ConfigLoadError: If configurations cannot be loaded
        """
        try:
            distro_name = distro_info.name
            
            # Load common apps
            common_apps_file = self.apps_dir / "common.yaml"
            common_apps = self.load_yaml(common_apps_file)
            
            # Load distro-specific apps
            distro_apps_file = self.apps_dir / f"{distro_name}.yaml"
            distro_apps = self.load_yaml(distro_apps_file)
            
            # Merge app configs
            merged_apps = self.merge_app_configs(common_apps, distro_apps, distro_info)
            
            # Load distro-specific tweaks
            tweaks_file = self.tweaks_dir / f"{distro_name}.yaml"
            distro_tweaks = self.load_yaml(tweaks_file)
            
            # Load common tweaks
            common_tweaks_file = self.tweaks_dir / "common.yaml"
            common_tweaks = self.load_yaml(common_tweaks_file)
            
            # Merge tweak configs
            merged_tweaks = self.merge_tweak_configs(common_tweaks, distro_tweaks)
            
            # Validate version compatibility
            if merged_tweaks.compatible_versions and distro_info.version:
                if distro_info.version not in merged_tweaks.compatible_versions:
                    # Log warning but don't fail
                    pass
            
            return {
                "apps": merged_apps,
                "tweaks": merged_tweaks,
                "distro_info": distro_info
            }
            
        except Exception as e:
            if isinstance(e, ConfigLoadError):
                raise
            raise ConfigLoadError(f"Failed to load configurations: {e}")


if __name__ == "__main__":
    # Test the config loader
    from linutil.core.distro_detector import detect_distribution
    
    try:
        distro = detect_distribution()
        print(f"Testing config loader for: {distro.pretty_name}")
        
        loader = ConfigLoader()
        config = loader.load_configurations(distro)
        
        apps = config["apps"]
        tweaks = config["tweaks"]
        
        print(f"\nFound {len(apps.categories)} app categories:")
        for cat in apps.categories:
            print(f"  - {cat['name']}: {len(cat['applications'])} apps")
        
        print(f"\nFound {len(tweaks.sections)} tweak sections:")
        for sec in tweaks.sections:
            print(f"  - {sec['name']}: {len(sec['tweaks'])} tweaks")
            
    except Exception as e:
        print(f"Error: {e}")
