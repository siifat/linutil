"""
Keyboard Shortcuts Display

Dynamic keyboard shortcuts guide shown at the bottom of screens.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Shortcut:
    """A keyboard shortcut with description and keys."""
    description: str
    keys: List[str]
    
    def format(self) -> str:
        """Format the shortcut for display."""
        keys_str = "/".join(self.keys)
        return f"[{keys_str}] {self.description}"


class ShortcutGuide:
    """Manages keyboard shortcuts for different contexts."""
    
    @staticmethod
    def welcome_screen() -> List[Shortcut]:
        """Shortcuts for the welcome screen."""
        return [
            Shortcut("Quit", ["q", "Ctrl-C"]),
            Shortcut("Install Apps", ["a"]),
            Shortcut("System Tweaks", ["t"]),
            Shortcut("Update System", ["u"]),
        ]
    
    @staticmethod
    def apps_screen() -> List[Shortcut]:
        """Shortcuts for the apps screen."""
        return [
            Shortcut("Quit", ["q", "Ctrl-C"]),
            Shortcut("Back", ["Esc"]),
            Shortcut("Select All", ["a"]),
            Shortcut("Select None", ["n"]),
            Shortcut("Install", ["i"]),
        ]
    
    @staticmethod
    def tweaks_screen() -> List[Shortcut]:
        """Shortcuts for the tweaks screen."""
        return [
            Shortcut("Quit", ["q", "Ctrl-C"]),
            Shortcut("Back", ["Esc"]),
            Shortcut("Select All", ["s"]),
            Shortcut("Select None", ["n"]),
            Shortcut("Apply", ["a"]),
        ]
    
    @staticmethod
    def update_screen() -> List[Shortcut]:
        """Shortcuts for the update screen."""
        return [
            Shortcut("Quit", ["q", "Ctrl-C"]),
            Shortcut("Back", ["Esc"]),
            Shortcut("Start Update", ["Enter"]),
        ]
    
    @staticmethod
    def format_shortcuts(shortcuts: List[Shortcut], max_width: int = 80) -> str:
        """
        Format shortcuts for display with wrapping.
        
        Args:
            shortcuts: List of shortcuts to format
            max_width: Maximum width of output line
            
        Returns:
            Formatted string with shortcuts
        """
        formatted = []
        current_line = []
        current_length = 0
        
        for shortcut in shortcuts:
            formatted_shortcut = shortcut.format()
            shortcut_length = len(formatted_shortcut)
            
            # Check if adding this shortcut would exceed max width
            if current_line and current_length + shortcut_length + 3 > max_width:
                # Start a new line
                formatted.append("  ".join(current_line))
                current_line = [formatted_shortcut]
                current_length = shortcut_length
            else:
                current_line.append(formatted_shortcut)
                current_length += shortcut_length + 3  # +3 for separator
        
        # Add the last line
        if current_line:
            formatted.append("  ".join(current_line))
        
        return "\n".join(formatted)
