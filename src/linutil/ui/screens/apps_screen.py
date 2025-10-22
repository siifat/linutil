"""
Application Installer Screen

Displays categorized applications with multi-select checkboxes.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, Label, Checkbox
from textual.binding import Binding
from textual.screen import Screen
from textual.message import Message

from linutil.core.config_loader import AppConfig, AppDefinition
from linutil.managers.base_manager import PackageManagerFactory, InstallResult
from linutil.core.executor import PrivilegeHandler, CommandExecutor


class AppCheckbox(Horizontal):
    """Custom checkbox widget for an application."""
    
    def __init__(self, app: AppDefinition, package_manager: str):
        super().__init__()
        self.app = app
        self.package_manager = package_manager
        self.checkbox = Checkbox(self.app.name, id=f"app_{self.app.id}")
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield self.checkbox
        yield Label(f" - {self.app.description}", classes="app-description")


class AppsScreen(Screen):
    """Screen for browsing and installing applications."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "quit", "Quit"),
        Binding("i", "install", "Install Selected"),
        Binding("a", "select_all", "Select All"),
        Binding("n", "select_none", "Select None"),
    ]
    
    def __init__(
        self,
        apps_config: AppConfig,
        package_manager: str,
        privilege_handler: PrivilegeHandler
    ):
        super().__init__()
        self.apps_config = apps_config
        self.package_manager = package_manager
        self.privilege_handler = privilege_handler
        self.selected_apps: list[AppDefinition] = []
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        yield Container(
            Vertical(
                Static(""),
                Label("📦 Application Installer", classes="screen-title"),
                Static(""),
                Label(
                    f"Package Manager: {self.package_manager.upper()}",
                    classes="pm-label"
                ),
                Static(""),
                
                # Action buttons
                Horizontal(
                    Button("✓ Select All", id="btn-select-all", variant="primary"),
                    Button("✗ Select None", id="btn-select-none", variant="default"),
                    Button("📥 Install Selected", id="btn-install", variant="success"),
                    classes="button-row"
                ),
                Static(""),
                
                # Scrollable app list
                ScrollableContainer(
                    *self._create_app_categories(),
                    id="apps-container"
                ),
                
                Static(""),
                Horizontal(
                    Button("◀ Back", id="btn-back", variant="default"),
                    classes="button-row"
                ),
                Static(""),
                Label("", id="status-label", classes="status-label"),
                
                id="apps-screen-container"
            ),
            id="main-container"
        )
        
        yield Footer()
    
    def _create_app_categories(self) -> list[Static | AppCheckbox]:
        """Create widgets for all app categories."""
        widgets = []
        
        if not self.apps_config.categories:
            widgets.append(
                Static(
                    "No applications available for your distribution yet.",
                    classes="no-apps-message"
                )
            )
            return widgets
        
        for category in self.apps_config.categories:
            # Category header
            icon = category.get('icon', '📦')
            name = category.get('name', 'Unknown')
            apps = category.get('applications', [])
            
            widgets.append(Static(""))
            widgets.append(
                Label(
                    f"{icon} {name} ({len(apps)} apps)",
                    classes="category-header"
                )
            )
            widgets.append(Static(""))
            
            # Apps in this category
            for app_data in apps:
                app = AppDefinition(
                    id=app_data["id"],
                    name=app_data["name"],
                    description=app_data["description"],
                    install=app_data["install"],
                    tags=app_data.get("tags", []),
                    category=name,
                )
                
                # Only show apps that support this package manager or flatpak
                if (self.package_manager in app.install or 
                    "flatpak" in app.install):
                    widgets.append(AppCheckbox(app, self.package_manager))
        
        return widgets
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "btn-back":
            self.app.pop_screen()
        elif button_id == "btn-select-all":
            self.action_select_all()
        elif button_id == "btn-select-none":
            self.action_select_none()
        elif button_id == "btn-install":
            self.action_install()
    
    def action_select_all(self) -> None:
        """Select all application checkboxes."""
        for checkbox in self.query(Checkbox):
            checkbox.value = True
        self.app.notify("All applications selected", severity="information")
    
    def action_select_none(self) -> None:
        """Deselect all application checkboxes."""
        for checkbox in self.query(Checkbox):
            checkbox.value = False
        self.app.notify("All selections cleared", severity="information")
    
    def action_install(self) -> None:
        """Install selected applications."""
        # Collect selected apps
        selected = []
        
        for app_checkbox in self.query(AppCheckbox):
            if app_checkbox.checkbox.value:
                selected.append(app_checkbox.app)
        
        if not selected:
            self.app.notify(
                "No applications selected!",
                severity="warning"
            )
            return
        
        # Update status
        status_label = self.query_one("#status-label", Label)
        status_label.update(f"Preparing to install {len(selected)} application(s)...")
        
        # Install in background
        self.app.notify(
            f"Installing {len(selected)} application(s)...",
            severity="information",
            timeout=5
        )
        
        # Run installation
        self.run_worker(
            self._install_apps(selected),
            name="install_apps"
        )
    
    async def _install_apps(self, apps: list[AppDefinition]) -> None:
        """
        Install applications in the background.
        
        Args:
            apps: List of applications to install
        """
        status_label = self.query_one("#status-label", Label)
        
        try:
            # Create package manager
            executor = CommandExecutor(self.privilege_handler)
            pm_factory = PackageManagerFactory
            
            # Import managers to register them
            from linutil.managers.apt_manager import AptManager
            from linutil.managers.dnf_manager import DnfManager
            
            manager = pm_factory.create(self.package_manager, executor=executor)
            
            if not manager:
                status_label.update(f"Error: Package manager {self.package_manager} not available")
                self.app.notify(
                    f"Package manager {self.package_manager} not supported",
                    severity="error"
                )
                return
            
            # Group apps by installation method
            native_packages = []
            custom_apps = []
            
            for app in apps:
                install_info = app.install.get(self.package_manager, {})
                method = install_info.get('method', 'native')
                
                if method == 'native':
                    native_packages.extend(install_info.get('packages', []))
                elif method == 'custom':
                    custom_apps.append(app)
            
            # Install native packages
            if native_packages:
                status_label.update(
                    f"Installing {len(native_packages)} package(s)..."
                )
                
                def progress_callback(msg: str):
                    status_label.update(msg)
                
                result = await manager.install_packages(
                    native_packages,
                    on_progress=progress_callback
                )
                
                if result.success:
                    status_label.update(
                        f"✓ Successfully installed {len(result.packages_installed)} package(s)!"
                    )
                    self.app.notify(
                        f"Successfully installed {len(result.packages_installed)} packages",
                        severity="information"
                    )
                else:
                    error_msg = f"Installed {len(result.packages_installed)}, Failed: {len(result.packages_failed)}"
                    status_label.update(f"⚠ {error_msg}")
                    
                    # Show detailed errors
                    if result.errors:
                        error_details = "\n".join([
                            f"• {pkg}: {err}" 
                            for pkg, err in result.errors.items()
                        ])
                        self.app.notify(
                            f"Installation errors:\n{error_details}",
                            severity="error",
                            timeout=10
                        )
            
            # TODO: Install custom apps (for future implementation)
            if custom_apps:
                status_label.update(
                    f"Note: {len(custom_apps)} app(s) require custom installation (not yet implemented)"
                )
            
        except Exception as e:
            status_label.update(f"❌ Error: {str(e)}")
            self.app.notify(
                f"Installation failed: {str(e)}",
                severity="error"
            )


# CSS for the apps screen
APPS_SCREEN_CSS = """
#apps-screen-container {
    width: 90%;
    max-width: 120;
    height: auto;
    border: solid $accent;
    padding: 2;
}

#apps-container {
    height: 30;
    border: solid $primary;
    padding: 1;
    margin: 1 0;
}

.category-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 1 2;
}

.app-description {
    color: $text-muted;
    text-style: italic;
}

.pm-label {
    text-align: center;
    color: $success;
}

.status-label {
    text-align: center;
    color: $warning;
    text-style: bold;
}

.no-apps-message {
    text-align: center;
    color: $warning;
    padding: 5;
}

AppCheckbox {
    height: auto;
    padding: 0 2;
}

AppCheckbox Checkbox {
    width: auto;
}

AppCheckbox Label {
    width: 1fr;
}
"""
