"""
Linux Command Tips

Random helpful Linux tips displayed to users.
"""

import random

LINUX_TIPS = [
    "Use 'htop' for an interactive process viewer instead of 'top'",
    "Press Ctrl+R to search through your command history",
    "Use 'cd -' to quickly switch to your previous directory",
    "The 'tldr' command shows simplified man pages with examples",
    "Use 'df -h' to check disk space in human-readable format",
    "Ctrl+L clears the terminal (same as typing 'clear')",
    "Use '!!' to repeat your last command",
    "Type 'sudo !!' to run your last command with sudo",
    "Use 'grep -r' to recursively search files in directories",
    "The 'find' command can search by name, type, size, and time",
    "Use 'tmux' or 'screen' to keep sessions alive when disconnected",
    "Press Tab twice to see all available command completions",
    "Use 'man' followed by a command name to read its manual",
    "Ctrl+Z pauses a process, 'bg' resumes it in background",
    "Use 'history' to see your recent commands",
    "The '~' character is shorthand for your home directory",
    "Use 'du -sh *' to see sizes of all items in current directory",
    "Ctrl+A moves cursor to start of line, Ctrl+E to end",
    "Use 'less' instead of 'cat' for viewing large files",
    "The 'which' command shows where a program is installed",
    "Use 'alias' to create shortcuts for long commands",
    "Ctrl+W deletes the word before cursor in terminal",
    "Use 'rsync' instead of 'cp' for better copy operations",
    "The 'tree' command shows directory structure visually",
    "Use 'watch' to run a command repeatedly and see updates",
    "Ctrl+U clears everything before cursor on command line",
    "Use 'apropos' to search man pages for keywords",
    "The 'xargs' command builds commands from standard input",
    "Use 'journalctl -f' to follow system logs in real-time",
    "The 'ncdu' tool provides an interactive disk usage analyzer",
]


def get_random_tip() -> str:
    """Get a random Linux tip."""
    return random.choice(LINUX_TIPS)
