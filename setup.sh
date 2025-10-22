#!/bin/bash
# Quick Setup Script for LinUtil Development

set -e

echo "╔═══════════════════════════════════════════════════╗"
echo "║      LinUtil - Quick Setup Script                 ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Install development dependencies (optional)
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -r requirements-dev.txt > /dev/null 2>&1
    echo "✓ Development dependencies installed"
fi

# Install package in development mode
echo ""
echo "Installing LinUtil in development mode..."
pip install -e . > /dev/null 2>&1
echo "✓ LinUtil installed"

# Run validation
echo ""
echo "Running validation..."
linutil info
echo ""
linutil validate

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║           Setup Complete! 🎉                      ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "You can now run LinUtil with:"
echo "  linutil              # Launch the TUI"
echo "  linutil info         # Show system info"
echo "  linutil validate     # Validate configs"
echo ""
echo "To deactivate the virtual environment later:"
echo "  deactivate"
echo ""
echo "Happy coding! 🐧"
