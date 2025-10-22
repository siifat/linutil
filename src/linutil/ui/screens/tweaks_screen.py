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
        """Apply selected tweaks."""
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
        
        # Update status
        status_label = self.query_one("#status-label", Label)
        status_label.update(f"Preparing to apply {len(selected)} tweak(s)...")
        
        # Apply in background
        self.app.notify(
            f"Applying {len(selected)} tweak(s)...",
            severity="information",
            timeout=5
        )
        
        # Run application
        self.run_worker(
            self._apply_tweaks(selected),
            name="apply_tweaks"
        )
    
    async def _apply_tweaks(self, tweaks: list[TweakDefinition]) -> None:
        """
        Apply tweaks in the background.
        
        Args:
            tweaks: List of tweaks to apply
        """
        status_label = self.query_one("#status-label", Label)
        
        try:
            executor = CommandExecutor(self.privilege_handler)
            
            applied_count = 0
            skipped_count = 0
            failed_count = 0
            requires_restart = False
            
            for i, tweak in enumerate(tweaks):
                status_label.update(
                    f"[{i+1}/{len(tweaks)}] Applying: {tweak.name}..."
                )
                
                # Check if already applied (if verification exists)
                if tweak.verification and tweak.idempotent:
                    check_cmd = tweak.verification.get('check_command', '')
                    success_pattern = tweak.verification.get('success_pattern', '')
                    
                    if check_cmd:
                        check_result = await executor.execute(
                            check_cmd,
                            use_sudo=False
                        )
                        
                        # Check if already applied
                        if success_pattern:
                            import re
                            if re.search(success_pattern, check_result.stdout):
                                status_label.update(
                                    f"⊘ Skipped: {tweak.name} (already applied)"
                                )
                                skipped_count += 1
                                continue
                
                # Apply the tweak (execute all commands)
                all_success = True
                
                for cmd_data in tweak.commands:
                    command = cmd_data.get('command', '')
                    description = cmd_data.get('description', '')
                    
                    if description:
                        status_label.update(f"  {description}...")
                    
                    result = await executor.execute(
                        command,
                        use_sudo=True,
                        timeout=300
                    )
                    
                    if not result.success:
                        status_label.update(
                            f"❌ Failed: {tweak.name} - {result.stderr[:100]}"
                        )
                        failed_count += 1
                        all_success = False
                        break
                
                if all_success:
                    status_label.update(f"✓ Applied: {tweak.name}")
                    applied_count += 1
                    
                    if tweak.requires_restart:
                        requires_restart = True
            
            # Final status
            summary = f"✓ Applied: {applied_count}"
            if skipped_count > 0:
                summary += f", ⊘ Skipped: {skipped_count}"
            if failed_count > 0:
                summary += f", ❌ Failed: {failed_count}"
            
            status_label.update(summary)
            
            # Notify user
            if requires_restart:
                self.app.notify(
                    "⚠ System restart required for some tweaks to take effect!",
                    severity="warning",
                    timeout=10
                )
            
            if failed_count == 0:
                self.app.notify(
                    f"Successfully applied {applied_count} tweak(s)!",
                    severity="information"
                )
            else:
                self.app.notify(
                    f"Completed with {failed_count} error(s)",
                    severity="error"
                )
            
        except Exception as e:
            status_label.update(f"❌ Error: {str(e)}")
            self.app.notify(
                f"Tweak application failed: {str(e)}",
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
