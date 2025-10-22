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
        self.checkbox = Checkbox("", id=f"tweak_{self.tweak.id}")  # Empty label for checkbox
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield self.checkbox
        yield Vertical(
            Label(self.tweak.name, classes="tweak-name"),
            Label(self.tweak.description, classes="tweak-description"),
        )
    
    def on_click(self) -> None:
        """Toggle checkbox when clicking anywhere on the row."""
        self.checkbox.toggle()


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
                Label("🔧 System Tweaks & Optimizations", classes="screen-title"),
                Label(
                    "Select tweaks to apply to your system",
                    classes="subtitle"
                ),
                
                # Action buttons
                Horizontal(
                    Button("✓ Select All", id="btn-select-all", variant="primary"),
                    Button("✗ Select None", id="btn-select-none", variant="default"),
                    Button("⚡ Apply Selected", id="btn-apply", variant="success"),
                    classes="button-row"
                ),
                
                # Scrollable tweaks list
                ScrollableContainer(
                    *self._create_tweak_sections(),
                    id="tweaks-container"
                ),
                
                # Bottom buttons
                Horizontal(
                    Button("◀ Back", id="btn-back", variant="default"),
                    classes="button-row"
                ),
                
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
            
            widgets.append(
                Label(
                    f"{icon} {name} ({len(tweaks)} tweaks)",
                    classes="section-header"
                )
            )
            
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
    
    def action_pop_screen(self) -> None:
        """Go back to previous screen."""
        self.app.pop_screen()
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
    
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
        
        # Show selection count
        tweak_names = [tweak.name for tweak in selected]
        self.app.notify(
            f"Selected {len(selected)} tweak(s): {', '.join(tweak_names[:3])}{'...' if len(tweak_names) > 3 else ''}",
            severity="information",
            timeout=3
        )
        
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
            # User cancelled or command failed
            if result.return_code == 130:
                msg = "Tweak application cancelled (Ctrl+C)"
            else:
                msg = "Tweak application cancelled or failed"
            self.app.notify(msg, severity="warning")
    

# CSS for the tweaks screen
TWEAKS_SCREEN_CSS = """
#tweaks-screen-container {
    width: 90%;
    max-width: 120;
    height: 100%;
    border: solid $accent;
    padding: 1 2;
}

#tweaks-container {
    height: 1fr;
    border: solid $primary;
    padding: 1;
    margin: 0;
}

.section-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 0 2;
    margin: 1 0 0 0;
}

TweakCheckbox {
    height: auto;
    margin: 0;
    padding: 0 1;
}

TweakCheckbox:hover {
    background: $boost;
}

TweakCheckbox Vertical {
    margin: 0 0 0 1;
    padding: 0;
    height: auto;
}

TweakCheckbox Checkbox {
    padding: 0;
    width: auto;
}

TweakCheckbox Label {
    width: 1fr;
    height: auto;
}

.tweak-name {
    color: $text;
    text-style: bold;
    height: 1;
}

.tweak-description {
    color: $text-muted;
    text-style: italic;
    height: 1;
}

.restart-warning {
    color: $warning;
    text-style: italic;
    padding: 0 0 0 4;
    margin: 0;
    height: 1;
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
"""
