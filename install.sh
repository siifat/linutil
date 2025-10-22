#!/bin/bash
# LinUtil - Linux Post-Install Setup Tool
# One-line installer: curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash

set -e

# Colors for output
RC='\033[0m'
RED='\033[31m'
YELLOW='\033[33m'
GREEN='\033[32m'
CYAN='\033[36m'

# Configuration
REPO_URL="https://github.com/yourusername/linutil"
INSTALL_DIR="$HOME/.local/share/linutil"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$INSTALL_DIR/venv"

# Print colored output
print_color() {
    printf "%b%s%b\n" "$1" "$2" "$RC"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect package manager
detect_package_manager() {
    if command_exists apt-get; then
        echo "apt-get"
    elif command_exists dnf; then
        echo "dnf"
    elif command_exists pacman; then
        echo "pacman"
    elif command_exists zypper; then
        echo "zypper"
    elif command_exists apk; then
        echo "apk"
    else
        echo "unknown"
    fi
}

# Check system requirements
check_requirements() {
    print_color "$CYAN" "Checking system requirements..."
    
    # Check Python version
    if ! command_exists python3; then
        print_color "$RED" "Error: Python 3 is not installed"
        print_color "$YELLOW" "Please install Python 3.10 or higher and try again"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    REQUIRED_VERSION="3.10"
    
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
        print_color "$RED" "Error: Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required"
        exit 1
    fi
    
    print_color "$GREEN" "✓ Python $PYTHON_VERSION found"
    
    # Check for git
    if ! command_exists git; then
        print_color "$YELLOW" "Git not found. Attempting to install..."
        install_git
    fi
    
    print_color "$GREEN" "✓ Git found"
    
    # Check for pip
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        print_color "$YELLOW" "pip not found. Attempting to install..."
        install_pip
    fi
    
    print_color "$GREEN" "✓ pip found"
}

# Install git
install_git() {
    PACKAGER=$(detect_package_manager)
    
    case "$PACKAGER" in
        apt-get)
            sudo apt-get update && sudo apt-get install -y git
            ;;
        dnf)
            sudo dnf install -y git
            ;;
        pacman)
            sudo pacman -S --noconfirm git
            ;;
        zypper)
            sudo zypper install -y git
            ;;
        apk)
            sudo apk add git
            ;;
        *)
            print_color "$RED" "Error: Could not install git automatically"
            print_color "$YELLOW" "Please install git manually and try again"
            exit 1
            ;;
    esac
}

# Install pip
install_pip() {
    PACKAGER=$(detect_package_manager)
    
    case "$PACKAGER" in
        apt-get)
            sudo apt-get install -y python3-pip python3-venv
            ;;
        dnf)
            sudo dnf install -y python3-pip
            ;;
        pacman)
            sudo pacman -S --noconfirm python-pip
            ;;
        zypper)
            sudo zypper install -y python3-pip
            ;;
        apk)
            sudo apk add py3-pip
            ;;
        *)
            print_color "$YELLOW" "Installing pip using get-pip.py..."
            curl -sS https://bootstrap.pypa.io/get-pip.py | python3
            ;;
    esac
}

# Check if LinUtil is already installed
check_existing_installation() {
    if [ -d "$INSTALL_DIR" ]; then
        print_color "$YELLOW" "LinUtil is already installed at $INSTALL_DIR"
        printf "Do you want to update it? [Y/n]: "
        read -r response
        if [ "$response" = "n" ] || [ "$response" = "N" ]; then
            print_color "$GREEN" "Installation cancelled"
            exit 0
        fi
        print_color "$CYAN" "Updating existing installation..."
        cd "$INSTALL_DIR"
        git pull origin main
        source "$VENV_DIR/bin/activate"
        pip install --upgrade -e .
        print_color "$GREEN" "✓ LinUtil updated successfully!"
        return 0
    fi
    return 1
}

# Clone repository
clone_repository() {
    print_color "$CYAN" "Cloning LinUtil repository..."
    
    # Create parent directory if it doesn't exist
    mkdir -p "$(dirname "$INSTALL_DIR")"
    
    # Clone the repository
    if ! git clone "$REPO_URL" "$INSTALL_DIR"; then
        print_color "$RED" "Error: Failed to clone repository"
        exit 1
    fi
    
    print_color "$GREEN" "✓ Repository cloned successfully"
}

# Create virtual environment
create_virtualenv() {
    print_color "$CYAN" "Creating virtual environment..."
    
    cd "$INSTALL_DIR"
    
    if ! python3 -m venv "$VENV_DIR"; then
        print_color "$RED" "Error: Failed to create virtual environment"
        exit 1
    fi
    
    print_color "$GREEN" "✓ Virtual environment created"
}

# Install LinUtil
install_linutil() {
    print_color "$CYAN" "Installing LinUtil..."
    
    cd "$INSTALL_DIR"
    source "$VENV_DIR/bin/activate"
    
    if ! pip install --upgrade pip; then
        print_color "$YELLOW" "Warning: Failed to upgrade pip"
    fi
    
    if ! pip install -e .; then
        print_color "$RED" "Error: Failed to install LinUtil"
        exit 1
    fi
    
    print_color "$GREEN" "✓ LinUtil installed successfully"
}

# Create launcher script
create_launcher() {
    print_color "$CYAN" "Creating launcher script..."
    
    mkdir -p "$BIN_DIR"
    
    cat > "$BIN_DIR/linutil" << 'EOF'
#!/bin/bash
# LinUtil launcher script

INSTALL_DIR="$HOME/.local/share/linutil"
VENV_DIR="$INSTALL_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: LinUtil is not properly installed"
    echo "Please run the installer again"
    exit 1
fi

source "$VENV_DIR/bin/activate"
python -m linutil.main "$@"
EOF
    
    chmod +x "$BIN_DIR/linutil"
    
    print_color "$GREEN" "✓ Launcher created at $BIN_DIR/linutil"
}

# Add to PATH
add_to_path() {
    # Check if BIN_DIR is already in PATH
    if [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
        return 0
    fi
    
    print_color "$CYAN" "Adding LinUtil to PATH..."
    
    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    
    case "$SHELL_NAME" in
        bash)
            RC_FILE="$HOME/.bashrc"
            ;;
        zsh)
            RC_FILE="$HOME/.zshrc"
            ;;
        fish)
            RC_FILE="$HOME/.config/fish/config.fish"
            ;;
        *)
            RC_FILE="$HOME/.profile"
            ;;
    esac
    
    # Add PATH export to rc file
    if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$RC_FILE" 2>/dev/null; then
        echo "" >> "$RC_FILE"
        echo "# Added by LinUtil installer" >> "$RC_FILE"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC_FILE"
        print_color "$GREEN" "✓ Added to PATH in $RC_FILE"
        print_color "$YELLOW" "Please run: source $RC_FILE"
        print_color "$YELLOW" "Or restart your terminal"
    fi
}

# Print success message
print_success() {
    echo ""
    print_color "$GREEN" "╔═══════════════════════════════════════════╗"
    print_color "$GREEN" "║   LinUtil installed successfully! 🎉    ║"
    print_color "$GREEN" "╚═══════════════════════════════════════════╝"
    echo ""
    print_color "$CYAN" "To run LinUtil, use one of these commands:"
    print_color "$YELLOW" "  1. source ~/.bashrc && linutil"
    print_color "$YELLOW" "  2. $BIN_DIR/linutil"
    print_color "$YELLOW" "  3. $VENV_DIR/bin/python -m linutil.main"
    echo ""
    print_color "$CYAN" "To update LinUtil in the future, run:"
    print_color "$YELLOW" "  curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash"
    echo ""
    print_color "$CYAN" "To uninstall LinUtil, run:"
    print_color "$YELLOW" "  rm -rf $INSTALL_DIR"
    print_color "$YELLOW" "  rm -f $BIN_DIR/linutil"
    echo ""
}

# Main installation process
main() {
    echo ""
    print_color "$CYAN" "╔═══════════════════════════════════════════╗"
    print_color "$CYAN" "║     LinUtil Installation Script          ║"
    print_color "$CYAN" "║  Linux Post-Install Setup Tool           ║"
    print_color "$CYAN" "╚═══════════════════════════════════════════╝"
    echo ""
    
    # Check if running on Linux
    if [ "$(uname)" != "Linux" ]; then
        print_color "$RED" "Error: LinUtil only supports Linux"
        exit 1
    fi
    
    # Check for existing installation
    if check_existing_installation; then
        print_success
        exit 0
    fi
    
    # Check system requirements
    check_requirements
    
    # Clone repository
    clone_repository
    
    # Create virtual environment
    create_virtualenv
    
    # Install LinUtil
    install_linutil
    
    # Create launcher script
    create_launcher
    
    # Add to PATH
    add_to_path
    
    # Print success message
    print_success
}

# Run main function
main
