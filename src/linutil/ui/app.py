"""
Main Textual Application

The main TUI application using Textual framework.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, Label
from textual.binding import Binding
from textual.screen import Screen

from linutil.core.distro_detector import detect_distribution, DistroInfo, DistroDetectionError
from linutil.core.config_loader import ConfigLoader, ConfigLoadError
from linutil.core.executor import PrivilegeHandler, CommandExecutor
from linutil.core.terminal_executor import TerminalExecutor
from linutil.managers.base_manager import PackageManagerFactory
from linutil.managers.apt_manager import AptManager
from linutil.managers.dnf_manager import DnfManager
from linutil.ui.screens.apps_screen import AppsScreen, APPS_SCREEN_CSS
from linutil.ui.screens.tweaks_screen import TweaksScreen, TWEAKS_SCREEN_CSS


class WelcomeScreen(Screen):
    """Welcome screen shown on startup."""
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("u", "update", "Update System"),
        Binding("a", "apps", "Install Apps"),
        Binding("t", "tweaks", "System Tweaks"),
    ]
    
    def __init__(self, distro_info: DistroInfo):
        super().__init__()
        self.distro_info = distro_info
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Container(
            Vertical(
                Static(""),
                Static(
                    "╔═══════════════════════════════════════════════════╗",
                    classes="banner"
                ),
                Static(
                    "║      LinUtil - Linux Post-Install Setup          ║",
                    classes="banner"
                ),
                Static(
                    "╚═══════════════════════════════════════════════════╝",
                    classes="banner"
                ),
                Static(""),
                Label(f"Detected: {self.distro_info.pretty_name}", id="distro-info"),
                Label(f"Package Manager: {self.distro_info.package_manager.upper()}", id="pm-info"),
                Static(""),
                Horizontal(
                    Button("📦 Install Applications", id="btn-apps", variant="primary"),
                    Button("🔧 System Tweaks", id="btn-tweaks", variant="primary"),
                    classes="button-row"
                ),
                Horizontal(
                    Button("🔄 Update System", id="btn-update", variant="success"),
                    Button("❌ Exit", id="btn-exit", variant="error"),
                    classes="button-row"
                ),
                Static(""),
                Static("Use arrow keys and Enter to navigate, or press shortcuts", classes="hint"),
                id="welcome-container"
            ),
            id="main-container"
        )
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "btn-exit":
            self.app.exit()
        elif button_id == "btn-update":
            self.action_update()
        elif button_id == "btn-apps":
            self.action_apps()
        elif button_id == "btn-tweaks":
            self.action_tweaks()
    
    def action_update(self) -> None:
        """Handle update action."""
        self.app.push_screen("update")
    
    def action_apps(self) -> None:
        """Handle apps action."""
        self.app.push_screen("apps")
    
    def action_tweaks(self) -> None:
        """Handle tweaks action."""
        self.app.push_screen("tweaks")


class UpdateScreen(Screen):
    """Screen for system updates."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "quit", "Quit"),
    ]
    
    def __init__(self, package_manager: str, privilege_handler: PrivilegeHandler):
        super().__init__()
        self.package_manager = package_manager
        self.privilege_handler = privilege_handler
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield ScrollableContainer(
            Vertical(
                Static(""),
                Label("🔄 System Update", classes="screen-title"),
                Static(""),
                Label("This will update all installed packages on your system."),
                Label(f"Package Manager: {self.package_manager.upper()}", classes="pm-label"),
                Static(""),
                Label("The update will run in an interactive terminal where you can:", classes="info-label"),
                Label("  • See real-time output", classes="info-label"),
                Label("  • Enter your password when prompted", classes="info-label"),
                Label("  • Confirm package installations", classes="info-label"),
                Static(""),
                Button("🔄 Start Update", id="btn-start-update", variant="success"),
                Button("◀ Back", id="btn-back", variant="default"),
                Static(""),
                id="update-container"
            ),
            id="main-container"
        )
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-start-update":
            self.start_update()
    
    def start_update(self) -> None:
        """Start system update interactively."""
        # Build update command based on package manager
        commands = []
        
        if self.package_manager == 'apt':
            commands = [
                'apt update',
                'apt upgrade -y',
                'apt autoremove -y'
            ]
        elif self.package_manager == 'dnf':
            commands = [
                'dnf check-update || true',  # Returns 100 if updates available
                'dnf upgrade -y',
                'dnf autoremove -y'
            ]
        elif self.package_manager == 'pacman':
            commands = [
                'pacman -Syu --noconfirm'
            ]
        else:
            self.app.notify(f"Package manager {self.package_manager} not supported", severity="error")
            return
        
        # Run in interactive terminal
        description = f"System Update ({self.package_manager.upper()})"
        
        with self.app.suspend():
            executor = TerminalExecutor()
            result = executor.execute_with_confirmation(
                commands=commands,
                use_sudo=True,
                description=description,
                warning="This will update all packages on your system."
            )
        
        # Show result
        if result.success:
            self.app.notify(
                "System updated successfully!",
                severity="information"
            )
        else:
            self.app.notify(
                "Update failed or was cancelled.",
                severity="error"
            )


class LinUtilApp(App):
    """Main LinUtil application."""
    
    CSS = """
    #main-container {
        align: center middle;
        width: 100%;
        height: 100%;
    }
    
    #welcome-container {
        width: 80;
        height: auto;
        border: solid $accent;
        padding: 2;
    }
    
    #update-container {
        width: 80;
        height: auto;
        border: solid $accent;
        padding: 2;
    }
    
    .banner {
        text-align: center;
        color: $accent;
    }
    
    .screen-title {
        text-align: center;
        text-style: bold;
        color: $accent;
    }
    
    #distro-info, #pm-info {
        text-align: center;
        margin-bottom: 1;
    }
    
    .pm-label {
        text-align: center;
        color: $success;
        margin: 1;
    }
    
    .button-row {
        align: center middle;
        width: 100%;
        height: auto;
        margin: 1;
    }
    
    .button-row Button {
        margin: 0 1;
    }
    
    .hint {
        text-align: center;
        color: $text-muted;
        text-style: italic;
    }
    
    .info-label {
        color: $text-muted;
        margin: 0 2;
    }
    
    .status-label {
        text-align: center;
        color: $warning;
        text-style: bold;
        min-height: 3;
    }
    """ + APPS_SCREEN_CSS + TWEAKS_SCREEN_CSS
    
    TITLE = "LinUtil - Linux Post-Install Setup"
    
    def __init__(
        self,
        distro_info: DistroInfo,
        config: dict,
        privilege_handler: PrivilegeHandler
    ):
        """
        Initialize the application.
        
        Args:
            distro_info: Distribution information
            config: Configuration dictionary
            privilege_handler: Privilege handler
        """
        super().__init__()
        self.distro_info = distro_info
        self.config = config
        self.privilege_handler = privilege_handler
    
    def on_mount(self) -> None:
        """Called when app is mounted."""
        # Install screens
        self.install_screen(WelcomeScreen(self.distro_info), name="welcome")
        self.install_screen(
            UpdateScreen(self.distro_info.package_manager, self.privilege_handler),
            name="update"
        )
        self.install_screen(
            AppsScreen(
                self.config["apps"],
                self.distro_info.package_manager,
                self.privilege_handler
            ),
            name="apps"
        )
        self.install_screen(
            TweaksScreen(self.config["tweaks"], self.privilege_handler),
            name="tweaks"
        )
        
        # Show welcome screen
        self.push_screen("welcome")


def create_app() -> LinUtilApp:
    """
    Create and configure the application.
    
    Returns:
        Configured LinUtilApp instance
        
    Raises:
        DistroDetectionError: If distribution cannot be detected
        ConfigLoadError: If configuration cannot be loaded
    """
    # Detect distribution
    distro_info = detect_distribution()
    
    # Load configuration
    config_loader = ConfigLoader()
    config = config_loader.load_configurations(distro_info)
    
    # Create privilege handler
    privilege_handler = PrivilegeHandler()
    
    # Create and return app
    return LinUtilApp(
        distro_info=distro_info,
        config=config,
        privilege_handler=privilege_handler
    )


if __name__ == "__main__":
    try:
        app = create_app()
        app.run()
    except (DistroDetectionError, ConfigLoadError) as e:
        print(f"Error: {e}")
        exit(1)
