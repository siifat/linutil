#!/bin/bash
# Quick test script for LinUtil after bug fixes

echo "========================================="
echo "LinUtil - Quick Test Script"
echo "========================================="
echo ""

# Check if in venv
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Virtual environment not activated!"
    echo ""
    echo "Please run:"
    echo "  source venv/bin/activate"
    echo ""
    exit 1
fi

echo "✓ Virtual environment: $VIRTUAL_ENV"
echo ""

# Reinstall to pick up changes
echo "Reinstalling LinUtil..."
pip install -e . > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ LinUtil reinstalled successfully"
else
    echo "❌ Installation failed!"
    exit 1
fi

echo ""
echo "========================================="
echo "Running LinUtil..."
echo "========================================="
echo ""
echo "Test Checklist:"
echo "  1. Press 'a' to test App Installer"
echo "  2. Press 't' to test System Tweaks"
echo "  3. Press 'u' to test System Update"
echo "  4. Press 'Escape' to test going back"
echo "  5. Press 'q' to test quit"
echo ""
echo "All operations will:"
echo "  ✓ Show you the commands before running"
echo "  ✓ Let you confirm (y/n)"
echo "  ✓ Prompt for your password"
echo "  ✓ Show full verbose output"
echo ""
read -p "Press Enter to launch LinUtil..."

linutil

echo ""
echo "========================================="
echo "Test completed!"
echo "========================================="
