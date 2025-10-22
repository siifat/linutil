# LinUtil - Linux Post-Install Setup Tool

A modern, distro-agnostic TUI (Terminal User Interface) application for streamlining Linux post-installation setup and system management.

![LinUtil Banner](https://img.shields.io/badge/Python-3.14-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

## ✨ Features

- **📦 Application Installer**: Browse and install applications by category with multi-select support
- **🔧 System Tweaks**: Apply system optimizations and tweaks with one click
- **🔄 System Updates**: Interactive system update with real-time output
- **🎯 Distro Detection**: Automatically detects your Linux distribution
- **💻 Interactive Terminal**: Full password prompts and interactive command support
- **🎨 Modern TUI**: Beautiful terminal interface built with Textual
- **💡 Linux Tips**: Learn Linux commands while you work
- **⌨️ Keyboard Shortcuts**: Navigate efficiently with keyboard shortcuts

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/linutil.git
cd linutil

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run LinUtil
linutil
```

### Requirements

- Python 3.10 or higher
- Linux distribution (Fedora, Ubuntu, Debian, Arch, etc.)
- Terminal size: minimum 80x24 characters

## 📖 Usage

### Main Interface

When you launch LinUtil, you'll see the welcome screen with:
- Detected distribution information
- Quick action buttons
- Random Linux tip
- Keyboard shortcuts guide

### Installing Applications

1. Press `a` or click "📦 Install Applications"
2. Browse applications organized by category
3. Click on items to select them (entire row is clickable!)
4. Press `i` or click "📥 Install Selected"
5. Confirm installation and enter your password when prompted

### Applying System Tweaks

1. Press `t` or click "🔧 System Tweaks"
2. Select tweaks you want to apply
3. Press `a` or click "⚡ Apply Selected"
4. Review the commands and confirm

## ⌨️ Keyboard Shortcuts

### Global
- `q` or `Ctrl+C` - Quit application
- `Esc` - Go back to previous screen

### Welcome Screen
- `a` - Install Applications
- `t` - System Tweaks
- `u` - Update System

### Application/Tweaks Screens
- `a` or `s` - Select all items
- `n` - Select none
- `i` or `a` - Install/Apply selected
- Arrow keys - Navigate items
- Mouse hover - Highlights clickable rows

## 🎯 Supported Distributions

Currently supported package managers:
- **DNF** (Fedora, RHEL, CentOS)
- **APT** (Ubuntu, Debian, Linux Mint)
- **Pacman** (Arch Linux, Manjaro)

## 🙏 Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) - An amazing TUI framework
- Inspired by [Chris Titus Tech's LinUtil](https://github.com/ChrisTitusTech/linutil)

---

**Made with ❤️ for the Linux community**