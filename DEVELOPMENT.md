# LinUtil - Development Guide

## Quick Start

### 1. Clone and Setup

```bash
cd linutil

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### 2. Test the Installation

```bash
# Show system information
linutil info

# Validate configuration files
linutil validate

# Launch the TUI (main application)
linutil
```

### 3. Project Structure

```
linutil/
├── src/linutil/          # Main source code
│   ├── core/             # Core functionality
│   │   ├── distro_detector.py    # OS detection
│   │   ├── config_loader.py      # YAML configuration loading
│   │   └── executor.py           # Command execution
│   ├── managers/         # Package manager implementations
│   │   ├── base_manager.py       # Abstract base class
│   │   ├── apt_manager.py        # APT (Ubuntu/Debian)
│   │   └── dnf_manager.py        # DNF (Fedora) - TODO
│   ├── ui/               # Textual UI components
│   │   ├── app.py                # Main application
│   │   └── screens/              # UI screens - TODO
│   └── main.py           # Entry point
├── data/                 # Configuration files (YAML)
│   ├── apps/            # Application definitions
│   │   └── common.yaml
│   └── tweaks/          # System tweaks
│       ├── ubuntu.yaml
│       ├── fedora.yaml
│       └── common.yaml
├── tests/               # Test files - TODO
├── docs/                # Documentation
└── pyproject.toml       # Project configuration
```

## Development Workflow

### Testing Core Components

#### Test Distribution Detection

```bash
# Run the distro detector
python -m linutil.core.distro_detector

# Expected output:
# Detected Distribution: Ubuntu 24.04 LTS (apt)
#   Name: ubuntu
#   Version: 24.04
#   Codename: noble
#   Package Manager: apt
```

#### Test Configuration Loader

```bash
# Run the config loader
python -m linutil.core.config_loader

# Expected output shows loaded apps and tweaks
```

#### Test Command Executor

```bash
# Run the executor tests
python -m linutil.core.executor
```

#### Test APT Manager

```bash
# Run the APT manager tests (requires APT system)
python -m linutil.managers.apt_manager
```

### Running the Application

```bash
# Launch the full TUI
linutil

# Or with Python
python -m linutil
```

## Adding New Features

### Adding a New Distribution

1. **Create app config**: `data/apps/<distro>.yaml`
2. **Create tweak config**: `data/tweaks/<distro>.yaml`
3. **Update distro detector** if needed (usually auto-detected)
4. **Test**: `linutil validate`

Example minimal `data/tweaks/arch.yaml`:

```yaml
version: "1.0"
distro: "arch"
compatible_versions: []

sections:
  - name: "Essential Post-Install"
    icon: "📦"
    tweaks:
      - id: "update-system"
        name: "Update System"
        description: "Update all packages"
        category: "system"
        requires_restart: false
        idempotent: true
        commands:
          - command: "pacman -Syu --noconfirm"
            description: "Updating system"
```

### Adding New Applications

Edit `data/apps/common.yaml` or create distro-specific files:

```yaml
- id: "neovim"
  name: "Neovim"
  description: "Modern Vim-based text editor"
  install:
    apt:
      packages: ["neovim"]
      method: "native"
    dnf:
      packages: ["neovim"]
      method: "native"
    pacman:
      packages: ["neovim"]
      method: "native"
  tags: ["editor", "development"]
```

### Adding New Tweaks

Edit distro-specific tweak files:

```yaml
- id: "my-custom-tweak"
  name: "My Custom Tweak"
  description: "Description of what this does"
  category: "performance"
  requires_restart: false
  idempotent: true
  commands:
    - command: "echo 'my command'"
      description: "Doing something"
  verification:
    check_command: "test -f /path/to/file"
    success_pattern: ""
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type check
mypy src/
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=linutil --cov-report=html

# Run specific test
pytest tests/test_distro_detector.py
```

## Current Status

### ✅ Completed
- [x] Project structure and configuration
- [x] Distribution detection (Ubuntu, Fedora, Debian, Arch, etc.)
- [x] YAML configuration loader with merging
- [x] Command executor with sudo support
- [x] Base package manager abstraction
- [x] APT package manager implementation
- [x] Basic Textual TUI with welcome screen
- [x] CLI with info and validate commands
- [x] Sample YAML configs (Ubuntu, Fedora)

### 🚧 In Progress / TODO
- [ ] DNF package manager implementation
- [ ] Flatpak manager implementation
- [ ] Application installer screen (TUI)
- [ ] Tweaks screen (TUI)
- [ ] System update screen (functional)
- [ ] Progress indicators and real-time feedback
- [ ] Error handling modals
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation

## Troubleshooting

### Import errors

If you see import errors, make sure:
1. Virtual environment is activated
2. Package is installed: `pip install -e .`
3. Dependencies are installed: `pip install -r requirements.txt`

### "Module not found"

```bash
# Reinstall in development mode
pip uninstall linutil
pip install -e .
```

### YAML errors

Use the validate command:
```bash
linutil validate
```

## Next Steps

1. **Implement DNF Manager** - Similar to APT manager
2. **Build App Installer Screen** - Categorized checkboxes for apps
3. **Build Tweaks Screen** - Selectable tweaks with descriptions
4. **Add Progress Indicators** - Real-time feedback during operations
5. **Write Tests** - Unit and integration tests
6. **Package for Distribution** - .deb, .rpm, PyPI

## Resources

- [Textual Documentation](https://textual.textualize.io/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [YAML Specification](https://yaml.org/spec/)

## Questions?

Check the [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design decisions and technical documentation.
