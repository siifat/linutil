"""
Main Entry Point

Command-line interface for LinUtil application.
"""

import sys
import click
from pathlib import Path

from linutil import __version__
from linutil.core.distro_detector import detect_distribution, DistroDetectionError
from linutil.core.config_loader import ConfigLoader, ConfigLoadError
from linutil.ui.app import create_app


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.pass_context
def cli(ctx, version):
    """
    LinUtil - Linux Post-Install Setup Application
    
    A modern, user-friendly tool for automating Linux post-installation tasks.
    """
    if version:
        click.echo(f"LinUtil version {__version__}")
        ctx.exit(0)
    
    if ctx.invoked_subcommand is None:
        # No subcommand, launch the TUI
        launch_tui()


@cli.command()
def info():
    """Show system information and detected distribution."""
    try:
        click.echo("Detecting system information...")
        distro = detect_distribution()
        
        click.echo("\n" + "="*50)
        click.echo("System Information")
        click.echo("="*50)
        click.echo(f"Distribution:      {distro.pretty_name}")
        click.echo(f"Name:              {distro.name}")
        click.echo(f"Version:           {distro.version}")
        click.echo(f"Codename:          {distro.codename}")
        click.echo(f"Package Manager:   {distro.package_manager.upper()}")
        if distro.id_like:
            click.echo(f"Based on:          {', '.join(distro.id_like)}")
        click.echo("="*50)
        
        # Check what configs are available
        config_loader = ConfigLoader()
        click.echo("\nChecking available configurations...")
        
        apps_file = config_loader.apps_dir / f"{distro.name}.yaml"
        tweaks_file = config_loader.tweaks_dir / f"{distro.name}.yaml"
        
        if apps_file.exists():
            click.echo(f"✓ Apps config found:   {apps_file}")
        else:
            click.echo(f"✗ Apps config missing: {apps_file}")
        
        if tweaks_file.exists():
            click.echo(f"✓ Tweaks config found: {tweaks_file}")
        else:
            click.echo(f"✗ Tweaks config missing: {tweaks_file}")
        
        # Common configs
        common_apps = config_loader.apps_dir / "common.yaml"
        common_tweaks = config_loader.tweaks_dir / "common.yaml"
        
        if common_apps.exists():
            click.echo(f"✓ Common apps:         {common_apps}")
        if common_tweaks.exists():
            click.echo(f"✓ Common tweaks:       {common_tweaks}")
        
    except DistroDetectionError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config-dir', type=click.Path(exists=True), help='Custom configuration directory')
def validate(config_dir):
    """Validate configuration files."""
    try:
        click.echo("Validating configuration files...")
        
        distro = detect_distribution()
        click.echo(f"Detected: {distro.pretty_name}")
        
        config_loader = ConfigLoader(Path(config_dir) if config_dir else None)
        config = config_loader.load_configurations(distro)
        
        apps = config["apps"]
        tweaks = config["tweaks"]
        
        click.echo(f"\n✓ Configuration loaded successfully!")
        click.echo(f"  - {len(apps.categories)} application categories")
        
        total_apps = sum(len(cat['applications']) for cat in apps.categories)
        click.echo(f"  - {total_apps} total applications")
        
        click.echo(f"  - {len(tweaks.sections)} tweak sections")
        
        total_tweaks = sum(len(sec['tweaks']) for sec in tweaks.sections)
        click.echo(f"  - {total_tweaks} total tweaks")
        
        # Show categories
        click.echo("\nApplication Categories:")
        for cat in apps.categories:
            icon = cat.get('icon', '📦')
            click.echo(f"  {icon} {cat['name']}: {len(cat['applications'])} apps")
        
        click.echo("\nTweak Sections:")
        for sec in tweaks.sections:
            icon = sec.get('icon', '🔧')
            click.echo(f"  {icon} {sec['name']}: {len(sec['tweaks'])} tweaks")
        
    except DistroDetectionError as e:
        click.echo(f"Error detecting distribution: {e}", err=True)
        sys.exit(1)
    except ConfigLoadError as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


def launch_tui():
    """Launch the Textual TUI application."""
    try:
        app = create_app()
        app.run()
    except DistroDetectionError as e:
        click.echo(f"Error: Could not detect your Linux distribution.", err=True)
        click.echo(f"Details: {e}", err=True)
        click.echo("\nLinUtil may not support your distribution yet.", err=True)
        click.echo("Supported distributions: Ubuntu, Fedora, Debian, Arch", err=True)
        sys.exit(1)
    except ConfigLoadError as e:
        click.echo(f"Error: Could not load configuration files.", err=True)
        click.echo(f"Details: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nExiting...")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
