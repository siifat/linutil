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
from textual import events

from linutil.core.config_loader import AppConfig, AppDefinition
from linutil.managers.base_manager import PackageManagerFactory, InstallResult
from linutil.core.executor import PrivilegeHandler, CommandExecutor
from linutil.core.terminal_executor import TerminalExecutor


class AppCheckbox(Horizontal):
    """Custom checkbox widget for an application."""
    
    def __init__(self, app: AppDefinition, package_manager: str):
        super().__init__()
        self.app_def = app  # Renamed from 'app' to avoid conflict with Textual's .app property
        self.package_manager = package_manager
        self.checkbox = Checkbox("", id=f"app_{self.app_def.id}")  # Empty label for checkbox
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield self.checkbox
        yield Vertical(
            Label(f"{self.app_def.name} [{self.app_def.task_list}]", classes="app-name"),
            Label(self.app_def.description, classes="app-description"),
        )
    
    def on_click(self, event: events.Click) -> None:
        """Toggle checkbox when clicking anywhere on the row except the checkbox itself."""
        # Check if the click was on the checkbox widget itself
        if event.widget is self.checkbox:
            # Let the checkbox handle it naturally
            return
        
        # Otherwise, toggle the checkbox
        self.checkbox.toggle()
        event.stop()  # Prevent event bubbling


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
                Label("📦 Application Installer", classes="screen-title"),
                Label(
                    f"Package Manager: {self.package_manager.upper()}",
                    classes="pm-label"
                ),
                
                # Action buttons
                Horizontal(
                    Button("✓ Select All", id="btn-select-all", variant="primary"),
                    Button("✗ Select None", id="btn-select-none", variant="default"),
                    Button("📥 Install Selected", id="btn-install", variant="success"),
                    classes="button-row"
                ),
                
                # Scrollable app list
                ScrollableContainer(
                    *self._create_app_categories(),
                    id="apps-container"
                ),
                
                # Bottom buttons
                Horizontal(
                    Button("◀ Back", id="btn-back", variant="default"),
                    classes="button-row"
                ),
                
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
            
            widgets.append(
                Label(
                    f"{icon} {name} ({len(apps)} apps)",
                    classes="category-header"
                )
            )
            
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
    
    def action_pop_screen(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
    
    def action_install(self) -> None:
        """Install selected applications interactively."""
        # Collect selected apps
        selected = []
        
        for app_checkbox in self.query(AppCheckbox):
            if app_checkbox.checkbox.value:
                selected.append(app_checkbox.app_def)
        
        if not selected:
            self.app.notify(
                "No applications selected!",
                severity="warning"
            )
            return
        
        # Show selection count
        app_names = [app.name for app in selected]
        self.app.notify(
            f"Selected {len(selected)} application(s): {', '.join(app_names[:3])}{'...' if len(app_names) > 3 else ''}",
            severity="information",
            timeout=3
        )
        
        # Prepare installation commands
        commands = []
        packages = []
        
        for app in selected:
            install_info = app.install.get(self.package_manager, {})
            method = install_info.get('method', 'native')
            
            if method == 'native':
                packages.extend(install_info.get('packages', []))
            elif method == 'custom':
                # Custom installation commands
                commands.extend(install_info.get('commands', []))
        
        # Build package install command
        if packages:
            if self.package_manager == 'apt':
                commands.insert(0, f'apt install -y {" ".join(packages)}')
            elif self.package_manager == 'dnf':
                commands.insert(0, f'dnf install -y {" ".join(packages)}')
            elif self.package_manager == 'pacman':
                commands.insert(0, f'pacman -S --noconfirm {" ".join(packages)}')
        
        if not commands:
            self.app.notify("No installation commands to run!", severity="warning")
            return
        
        # Run in interactive terminal
        description = f"Installing {len(selected)} application(s): {', '.join([app.name for app in selected])}"
        
        # Suspend the app and run in terminal
        with self.app.suspend():
            executor = TerminalExecutor()
            result = executor.execute_with_confirmation(
                commands=commands,
                use_sudo=True,
                description=description,
                warning="This will install packages on your system."
            )
        
        # Show result
        if result.success:
            self.app.notify(
                "Installation completed successfully!",
                severity="information"
            )
        else:
            # User cancelled or command failed
            if result.return_code == 130:
                msg = "Installation cancelled (Ctrl+C)"
            else:
                msg = "Installation cancelled or failed"
            self.app.notify(msg, severity="warning")


# CSS for the apps screen
APPS_SCREEN_CSS = """
#apps-screen-container {
    width: 90%;
    max-width: 120;
    height: 100%;
    border: solid $accent;
    padding: 1 2;
}

#apps-container {
    height: 1fr;
    border: solid $primary;
    padding: 1;
    margin: 0;
}

.category-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 0 2;
    margin: 1 0 0 0;
}

AppCheckbox {
    height: auto;
    margin: 0;
    padding: 0 1;
}

AppCheckbox:hover {
    background: $boost;
}

AppCheckbox Vertical {
    margin: 0 0 0 1;
    padding: 0;
    height: auto;
}

AppCheckbox Checkbox {
    padding: 0;
    width: auto;
}

AppCheckbox Label {
    width: 1fr;
    height: auto;
}

.app-name {
    color: $text;
    text-style: bold;
    height: 1;
}

.app-description {
    color: $text-muted;
    text-style: italic;
    height: 1;
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
"""
