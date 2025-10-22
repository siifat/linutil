# Quick Start Guide for Fedora VM

## First Time Setup (Already Done ✓)

You've already run `bash setup.sh`. Great!

## Every Time You Open a New Terminal

The virtual environment needs to be activated in each new terminal session:

```bash
cd ~/linutil
source venv/bin/activate
```

You'll see `(venv)` appear in your prompt when it's active.

## Running LinUtil

Once the virtual environment is activated:

```bash
# Show system information
linutil info

# Validate configuration files
linutil validate

# Launch the TUI application
linutil

# Show version
linutil --version
```

## Testing After the Config Fix

Since I just fixed the data path issue, you need to reinstall:

```bash
cd ~/linutil
source venv/bin/activate
pip install -e .
```

Then test again:

```bash
linutil info
# Should now show:
# ✓ Apps config found
# ✓ Tweaks config found

linutil validate
# Should now show applications and tweaks
```

## Deactivating the Virtual Environment

When you're done:

```bash
deactivate
```

## Troubleshooting

### "linutil: command not found"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Check if installed: `pip list | grep linutil`

### "No such file or directory"
- Make sure you're in the linutil directory: `cd ~/linutil`

### Data files not found
- The fix has been applied
- Reinstall: `pip install -e .`
- Verify path: `python -c "from pathlib import Path; import linutil.core.config_loader as cl; print(Path(cl.__file__).parent.parent.parent.parent / 'data')"`

## Development Workflow

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Make changes to code or YAML files

# 3. If you changed Python code, reinstall
pip install -e .

# 4. Test
linutil validate
linutil

# 5. When done
deactivate
```

## What You Should See Now

After applying the fix and reinstalling:

```bash
linutil validate
```

Should show:
- ✓ Configuration loaded successfully!
- **4 application categories** (Web Browsers, Development Tools, Multimedia, Utilities)
- **10 total applications**
- **4 tweak sections**
- **7 total tweaks** for Fedora

Enjoy! 🎉
