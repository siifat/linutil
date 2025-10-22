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

### One-Line Installation (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/siifat/linutil/main/install.sh | bash
```

Or using wget:
```bash
wget -qO- https://raw.githubusercontent.com/siifat/linutil/main/install.sh | bash
```

This automatically:
- Checks and installs requirements (Python 3.10+, git, pip)
- Sets up everything in `~/.local/share/linutil`
- Creates a launcher at `~/.local/bin/linutil`
- Adds LinUtil to your PATH

After installation: `source ~/.bashrc && linutil`

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/siifat/linutil.git
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
- Internet connection for package installations

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

## 🔄 Updating

To update LinUtil to the latest version:

```bash
curl -fsSL https://raw.githubusercontent.com/siifat/linutil/main/install.sh | bash
```

Or manually:
```bash
cd ~/.local/share/linutil
git pull && source venv/bin/activate && pip install --upgrade -e .
```

## 🗑️ Uninstalling

```bash
curl -fsSL https://raw.githubusercontent.com/siifat/linutil/main/uninstall.sh | bash
```

## 🎯 Supported Distributions

Currently supported package managers:
- **DNF** (Fedora, RHEL, CentOS, Rocky Linux)
- **APT** (Ubuntu, Debian, Linux Mint, Pop!_OS)
- **Pacman** (Arch Linux, Manjaro, EndeavourOS)
- **Zypper** (openSUSE, SLES)
- **APK** (Alpine Linux)

## 🙏 Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) - An amazing TUI framework
- Inspired by [Chris Titus Tech's LinUtil](https://github.com/ChrisTitusTech/linutil)

---

**Made with ❤️ for the Linux community**