# 📌 LinUtil Quick Reference Card

## 🚀 Installation & Setup

```bash
cd ~/linutil
source venv/bin/activate    # Every new terminal session
pip install -e .             # After code changes
```

## 🎮 Running LinUtil

```bash
linutil                      # Launch TUI
linutil info                 # Show system info
linutil validate             # Check configs
linutil --version            # Show version
```

## ⌨️ Keyboard Shortcuts

### Welcome Screen
- `a` → Application Installer
- `t` → System Tweaks
- `u` → Update System
- `q` → Quit

### Application Installer
- `a` → Select All
- `n` → Select None
- `i` → Install Selected
- `Space` → Toggle checkbox
- `Escape` → Back

### System Tweaks
- `s` → Select All
- `n` → Select None
- `a` → Apply Selected
- `Space` → Toggle checkbox
- `Escape` → Back

### System Update
- `Escape` → Back
- `q` → Quit

## 📁 File Structure

```
linutil/
├── src/linutil/
│   ├── core/           → Detection, config, execution
│   ├── managers/       → APT, DNF package managers
│   ├── ui/             → TUI screens
│   └── main.py         → CLI entry
├── data/
│   ├── apps/           → App definitions
│   └── tweaks/         → Tweak definitions
└── docs/               → Documentation
```

## 📝 Adding New Content

### Add Application (data/apps/common.yaml)
```yaml
- id: "my-app"
  name: "My Application"
  description: "What it does"
  install:
    apt:
      packages: ["my-app"]
      method: "native"
    dnf:
      packages: ["my-app"]
      method: "native"
  tags: ["category"]
```

### Add Tweak (data/tweaks/fedora.yaml)
```yaml
- id: "my-tweak"
  name: "My Tweak"
  description: "What it does"
  category: "performance"
  requires_restart: false
  idempotent: true
  commands:
    - command: "my-command"
      description: "Doing something"
  verification:
    check_command: "test -f /path"
    success_pattern: ""
```

## 🧪 Testing Commands

```bash
# Test distro detection
python -m linutil.core.distro_detector

# Test config loading
python -m linutil.core.config_loader

# Test command execution
python -m linutil.core.executor

# Test APT manager (Ubuntu)
python -m linutil.managers.apt_manager

# Test DNF manager (Fedora)
python -m linutil.managers.dnf_manager

# Validate all configs
linutil validate
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found` | `source venv/bin/activate` |
| Import errors | `pip install -e .` |
| No apps showing | Check `data/` directory exists |
| No tweaks for distro | Create `data/tweaks/<distro>.yaml` |
| Permission denied | Run as regular user (sudo when needed) |

## 📦 What's Included

### Applications (10)
- Firefox, Chromium (browsers)
- Git, Python 3, VS Code (dev)
- VLC, GIMP (multimedia)
- htop, curl, wget (utilities)

### Fedora Tweaks (7)
- Enable RPM Fusion
- Install codecs
- Optimize DNF
- Development tools
- System optimizations

### Ubuntu Tweaks (6)
- Restricted extras
- Partner repo
- Build essential
- Swappiness optimization
- GNOME Tweaks

## 🎯 Common Workflows

### First-Time Fedora Setup
1. `linutil` → Apps → Select: Git, Python, htop → Install
2. Tweaks → Select: RPM Fusion, Codecs, DNF Opt → Apply
3. Update → Start Update

### First-Time Ubuntu Setup
1. `linutil` → Apps → Select apps → Install
2. Tweaks → Select: Restricted Extras, Build Essential → Apply
3. Update → Start Update

## 📊 Status Indicators

- ✓ → Success
- ❌ → Failed
- ⊘ → Skipped (already applied)
- ⚠ → Warning

## 🔗 Documentation

- `ARCHITECTURE.md` → Technical design
- `README.md` → User guide
- `DEVELOPMENT.md` → Developer guide
- `UPDATE_GUIDE.md` → Latest features
- `FINAL_SUMMARY.md` → Complete overview

## 💡 Pro Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Reinstall after code changes**: `pip install -e .`
3. **Test with validate**: `linutil validate`
4. **Check logs**: Look at terminal output for errors
5. **Start small**: Test with one app/tweak first

## 🚀 Next Steps

1. ✅ Test on Fedora VM
2. ✅ Try installing apps
3. ✅ Try applying tweaks
4. ✅ Try system update
5. ⭐ Add your own apps/tweaks
6. ⭐ Package for distribution
7. ⭐ Share with community

---

**Quick Help**: `linutil --help` or press `?` in any screen
