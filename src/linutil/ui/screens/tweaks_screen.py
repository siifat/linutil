"""
System Tweaks Screen

Displays system tweaks and optimizations that can be applied.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, Label, Checkbox
from textual.binding import Binding
from textual.screen import Screen

from linutil.core.config_loader import TweakConfig, TweakDefinition
from linutil.core.executor import PrivilegeHandler, CommandExecutor
from linutil.core.terminal_executor import TerminalExecutor


class TweakCheckbox(Horizontal):
    """Custom checkbox widget for a system tweak."""
    
    def __init__(self, tweak: TweakDefinition):
        super().__init__()
        self.tweak = tweak
        self.checkbox = Checkbox(self.tweak.name, id=f"tweak_{self.tweak.id}")
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield self.checkbox
        yield Label(f" - {self.tweak.description}", classes="tweak-description")


class TweaksScreen(Screen):
    """Screen for browsing and applying system tweaks."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "quit", "Quit"),
        Binding("a", "apply", "Apply Selected"),
        Binding("s", "select_all", "Select All"),
        Binding("n", "select_none", "Select None"),
    ]
    
    def __init__(
        self,
        tweaks_config: TweakConfig,
        privilege_handler: PrivilegeHandler
    ):
        super().__init__()
        self.tweaks_config = tweaks_config
        self.privilege_handler = privilege_handler
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        yield Container(
            Vertical(
                Static(""),
                Label("🔧 System Tweaks & Optimizations", classes="screen-title"),
                Static(""),
                Label(
                    "Select tweaks to apply to your system",
                    classes="subtitle"
                ),
                Static(""),
                
                # Action buttons
                Horizontal(
                    Button("✓ Select All", id="btn-select-all", variant="primary"),
                    Button("✗ Select None", id="btn-select-none", variant="default"),
                    Button("⚡ Apply Selected", id="btn-apply", variant="success"),
                    classes="button-row"
                ),
                Static(""),
                
                # Scrollable tweaks list
                ScrollableContainer(
                    *self._create_tweak_sections(),
                    id="tweaks-container"
                ),
                
                Static(""),
                Horizontal(
                    Button("◀ Back", id="btn-back", variant="default"),
                    classes="button-row"
                ),
                Static(""),
                Label("", id="status-label", classes="status-label"),
                
                id="tweaks-screen-container"
            ),
            id="main-container"
        )
        
        yield Footer()
    
    def _create_tweak_sections(self) -> list[Static | TweakCheckbox]:
        """Create widgets for all tweak sections."""
        widgets = []
        
        if not self.tweaks_config.sections:
            widgets.append(
                Static(
                    "No tweaks available for your distribution yet.",
                    classes="no-tweaks-message"
                )
            )
            return widgets
        
        for section in self.tweaks_config.sections:
            # Section header
            icon = section.get('icon', '🔧')
            name = section.get('name', 'Unknown')
            tweaks = section.get('tweaks', [])
            
            widgets.append(Static(""))
            widgets.append(
                Label(
                    f"{icon} {name} ({len(tweaks)} tweaks)",
                    classes="section-header"
                )
            )
            widgets.append(Static(""))
            
            # Tweaks in this section
            for tweak_data in tweaks:
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
                    section=name,
                )
                
                widgets.append(TweakCheckbox(tweak))
                
                # Show if restart required
                if tweak.requires_restart:
                    widgets.append(
                        Label("  ⚠ Requires restart", classes="restart-warning")
                    )
        
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
        elif button_id == "btn-apply":
            self.action_apply()
    
    def action_select_all(self) -> None:
        """Select all tweak checkboxes."""
        for checkbox in self.query(Checkbox):
            checkbox.value = True
        self.app.notify("All tweaks selected", severity="information")
    
    def action_select_none(self) -> None:
        """Deselect all tweak checkboxes."""
        for checkbox in self.query(Checkbox):
            checkbox.value = False
        self.app.notify("All selections cleared", severity="information")
    
    def action_apply(self) -> None:
        """Apply selected tweaks interactively."""
        # Collect selected tweaks
        selected = []
        
        for tweak_checkbox in self.query(TweakCheckbox):
            if tweak_checkbox.checkbox.value:
                selected.append(tweak_checkbox.tweak)
        
        if not selected:
            self.app.notify(
                "No tweaks selected!",
                severity="warning"
            )
            return
        
        # Prepare commands
        all_commands = []
        requires_restart = False
        
        for tweak in selected:
            # Add comments to separate each tweak
            all_commands.append(f'echo "=== Applying: {tweak.name} ==="')
            
            for cmd_data in tweak.commands:
                command = cmd_data.get('command', '')
                description = cmd_data.get('description', '')
                
                if description:
                    all_commands.append(f'echo "  {description}..."')
                
                all_commands.append(command)
            
            if tweak.requires_restart:
                requires_restart = True
        
        if not all_commands:
            self.app.notify("No commands to execute!", severity="warning")
            return
        
        # Build description
        description = f"Applying {len(selected)} system tweak(s):\n"
        for tweak in selected:
            description += f"  • {tweak.name}\n"
        
        warning = None
        if requires_restart:
            warning = "Some tweaks require a system restart to take effect."
        
        # Run in interactive terminal
        with self.app.suspend():
            executor = TerminalExecutor()
            result = executor.execute_with_confirmation(
                commands=all_commands,
                use_sudo=True,
                description=description,
                warning=warning
            )
        
        # Show result
        if result.success:
            msg = "Tweaks applied successfully!"
            if requires_restart:
                msg += " Please restart your system."
            self.app.notify(msg, severity="information")
        else:
            self.app.notify(
                "Tweak application failed or was cancelled.",
                severity="error"
            )
    

# CSS for the tweaks screen
TWEAKS_SCREEN_CSS = """
#tweaks-screen-container {
    width: 90%;
    max-width: 120;
    height: auto;
    border: solid $accent;
    padding: 2;
}

#tweaks-container {
    height: 30;
    border: solid $primary;
    padding: 1;
    margin: 1 0;
}

.section-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 1 2;
}

.tweak-description {
    color: $text-muted;
    text-style: italic;
}

.restart-warning {
    color: $warning;
    text-style: italic;
    padding: 0 4;
}

.subtitle {
    text-align: center;
    color: $text-muted;
}

.status-label {
    text-align: center;
    color: $warning;
    text-style: bold;
}

.no-tweaks-message {
    text-align: center;
    color: $warning;
    padding: 5;
}

TweakCheckbox {
    height: auto;
    padding: 0 2;
}

TweakCheckbox Checkbox {
    width: auto;
}

TweakCheckbox Label {
    width: 1fr;
}
"""
