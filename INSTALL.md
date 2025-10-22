# LinUtil Installation Guide

## 🚀 Quick Install (Recommended)

Install LinUtil with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash
```

Or using wget:

```bash
wget -qO- https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash
```

This will:
- ✅ Check system requirements (Python 3.10+, git, pip)
- ✅ Install missing dependencies automatically
- ✅ Clone the repository to `~/.local/share/linutil`
- ✅ Create a Python virtual environment
- ✅ Install LinUtil and its dependencies
- ✅ Create a launcher script at `~/.local/bin/linutil`
- ✅ Add to your PATH automatically

After installation, run:
```bash
source ~/.bashrc  # or ~/.zshrc if using zsh
linutil
```

## 📋 Manual Installation

If you prefer to install manually:

```bash
# Clone the repository
git clone https://github.com/yourusername/linutil.git
cd linutil

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install LinUtil
pip install -e .

# Run LinUtil
linutil
```

## 🔄 Updating LinUtil

To update to the latest version, simply run the installer again:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash
```

Or manually:

```bash
cd ~/.local/share/linutil
git pull origin main
source venv/bin/activate
pip install --upgrade -e .
```

## 🗑️ Uninstalling LinUtil

To completely remove LinUtil from your system:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/uninstall.sh | bash
```

Or manually:

```bash
rm -rf ~/.local/share/linutil
rm -f ~/.local/bin/linutil
```

## 🔧 Installation Options

### Install for specific distribution

The installer automatically detects your distribution. Supported:
- Fedora / RHEL / CentOS (DNF)
- Ubuntu / Debian / Linux Mint (APT)
- Arch Linux / Manjaro (Pacman)
- openSUSE (Zypper)
- Alpine Linux (APK)

### Install without sudo

If you don't have sudo access, you can still install LinUtil:

```bash
# The installer will skip system dependencies
# Make sure Python 3.10+, git, and pip are already installed
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash
```

### Custom installation directory

```bash
# Set custom install location
export INSTALL_DIR="$HOME/custom/path"
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh | bash
```

## 🐛 Troubleshooting

### Python version too old

If you get a Python version error:

**Fedora/RHEL:**
```bash
sudo dnf install python3.11
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.11 python3.11-venv
```

**Arch:**
```bash
sudo pacman -S python
```

### pip not found

Install pip for your distribution:

**Fedora/RHEL:**
```bash
sudo dnf install python3-pip
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-pip python3-venv
```

**Arch:**
```bash
sudo pacman -S python-pip
```

### LinUtil command not found after installation

Reload your shell configuration:

```bash
source ~/.bashrc  # for bash
source ~/.zshrc   # for zsh
```

Or run directly:
```bash
~/.local/bin/linutil
```

### Permission denied errors

Make sure the install script is executable:

```bash
chmod +x install.sh
./install.sh
```

## 📱 Alternative Installation Methods

### Using Git directly

```bash
git clone https://github.com/yourusername/linutil.git ~/linutil
cd ~/linutil
python3 -m venv venv
source venv/bin/activate
pip install -e .
./venv/bin/python -m linutil.main
```

### Using Python pip (when published)

```bash
pip install --user linutil
linutil
```

### Using distro packages (future)

**Fedora/RHEL (when available):**
```bash
sudo dnf install linutil
```

**Ubuntu/Debian (when available):**
```bash
sudo apt install linutil
```

**Arch AUR (when available):**
```bash
yay -S linutil
```

## 🔐 Security Considerations

The one-line installer:
- ✅ Uses HTTPS to download the script
- ✅ Runs in user space (no system-wide changes without sudo)
- ✅ Creates isolated virtual environment
- ✅ Only modifies `~/.local/share` and `~/.local/bin`
- ✅ Open source - you can review the script before running

To review the installer before running:
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/linutil/main/install.sh
```

## 💡 Post-Installation

After installing LinUtil:

1. **Run it**: `linutil`
2. **Check the README**: Read features and usage guide
3. **Explore**: Browse applications and tweaks
4. **Customize**: Add your own apps/tweaks to YAML files
5. **Update regularly**: Keep LinUtil up to date

## 📞 Getting Help

If you encounter issues:
- Check this guide for common problems
- View the [main README](README.md)
- Open an [issue on GitHub](https://github.com/yourusername/linutil/issues)
- Check existing issues for solutions

---

**Happy Linux setup! 🐧**
