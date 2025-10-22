#!/bin/bash
# LinUtil - Quick uninstaller

set -e

RC='\033[0m'
RED='\033[31m'
GREEN='\033[32m'
CYAN='\033[36m'

INSTALL_DIR="$HOME/.local/share/linutil"
BIN_DIR="$HOME/.local/bin"

print_color() {
    printf "%b%s%b\n" "$1" "$2" "$RC"
}

echo ""
print_color "$CYAN" "╔═══════════════════════════════════════════╗"
print_color "$CYAN" "║     LinUtil Uninstaller                   ║"
print_color "$CYAN" "╚═══════════════════════════════════════════╝"
echo ""

if [ ! -d "$INSTALL_DIR" ]; then
    print_color "$RED" "LinUtil is not installed"
    exit 1
fi

print_color "$CYAN" "This will remove LinUtil from your system."
printf "Are you sure? [y/N]: "
read -r response

if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
    print_color "$GREEN" "Uninstall cancelled"
    exit 0
fi

print_color "$CYAN" "Removing LinUtil..."

# Remove installation directory
rm -rf "$INSTALL_DIR"
print_color "$GREEN" "✓ Removed $INSTALL_DIR"

# Remove launcher script
if [ -f "$BIN_DIR/linutil" ]; then
    rm -f "$BIN_DIR/linutil"
    print_color "$GREEN" "✓ Removed $BIN_DIR/linutil"
fi

echo ""
print_color "$GREEN" "LinUtil has been uninstalled successfully!"
print_color "$CYAN" "Note: PATH entries in your shell config were not removed."
print_color "$CYAN" "You can manually remove the line from ~/.bashrc or ~/.zshrc:"
print_color "$CYAN" "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
