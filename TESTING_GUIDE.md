# 🚀 Quick Start - Testing Bug Fixes

## Prerequisites

You're on your **Fedora 43 VM** with LinUtil already set up.

## Step 1: Activate Virtual Environment

```bash
cd ~/linutil
source venv/bin/activate
```

## Step 2: Pull Latest Changes

If you're using Git:
```bash
git pull
```

Or manually copy the updated files to your VM.

## Step 3: Reinstall

```bash
pip install -e .
```

## Step 4: Run LinUtil

```bash
linutil
```

Or use the test script:
```bash
bash test.sh
```

## What's Different?

### Before (Broken)
- ❌ Couldn't enter sudo password
- ❌ No output visible
- ❌ Escape/Q keys didn't work
- ❌ Screen content cut off

### After (Fixed)
- ✅ **Prompts for password** when needed
- ✅ **Shows all output** in real-time
- ✅ **Keys work immediately**
- ✅ **Content scrolls** properly

## Testing Workflow

### Test 1: Install an Application

1. Launch LinUtil: `linutil`
2. Press `a` (or click "Install Applications")
3. Select an app (e.g., `htop`) with Space
4. Press `i` (or click "Install Selected")
5. **READ** the confirmation screen
6. Type `y` and press Enter
7. **ENTER YOUR PASSWORD** when prompted
8. **WATCH** the installation progress
9. Press Enter when complete
10. You're back in the TUI!

**Expected**: 
- You see DNF downloading packages
- You see installation progress
- You can cancel with Ctrl+C if needed

### Test 2: Apply a Tweak

1. From welcome screen, press `t`
2. Select a tweak (e.g., "Optimize DNF Performance")
3. Press `a` (Apply Selected)
4. Confirm with `y`
5. **ENTER PASSWORD**
6. **WATCH** each command execute
7. Press Enter when done

**Expected**:
- See each tweak command
- See command output
- Confirmation before restart (if needed)

### Test 3: System Update

1. From welcome screen, press `u`
2. Click "Start Update"
3. Confirm with `y`
4. **ENTER PASSWORD**
5. **WATCH** entire update process:
   - dnf check-update
   - dnf upgrade
   - dnf autoremove
6. Press Enter when complete

**Expected**:
- See all package updates
- Download progress bars
- Installation progress
- Full transaction summary

### Test 4: Keybindings

1. From welcome screen, press `a` (Apps)
2. Press `Escape` → Should return to welcome
3. Press `t` (Tweaks)
4. Press `Escape` → Should return to welcome
5. Press `q` → Should quit LinUtil

**Expected**: All keys work immediately, no lag

### Test 5: Scrolling

1. Press `a` (Apps)
2. If many apps listed, use Arrow Up/Down to scroll
3. Screen should scroll smoothly

**Expected**: No content cut off

## Troubleshooting

### "linutil: command not found"
```bash
source venv/bin/activate
pip install -e .
```

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

### Permission denied
Don't run as root! Run as normal user, you'll be prompted for password.

### Stuck at password prompt
If using SSH, make sure you have a real terminal (not redirected). The password prompt needs stdin.

## What Commands Actually Run?

### App Installation (Fedora)
```bash
sudo dnf install -y <package1> <package2> ...
```

### System Update (Fedora)
```bash
sudo dnf check-update || true
sudo dnf upgrade -y
sudo dnf autoremove -y
```

### System Tweaks
Varies by tweak. Examples:
```bash
# Enable RPM Fusion
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

# Install codecs
sudo dnf install -y gstreamer1-plugins-{bad-*,good-*,base} gstreamer1-plugin-openh264

# Optimize DNF
echo 'max_parallel_downloads=10' | sudo tee -a /etc/dnf/dnf.conf
echo 'fastestmirror=True' | sudo tee -a /etc/dnf/dnf.conf
```

## Success Criteria

✅ You can install packages  
✅ You can apply tweaks  
✅ You can update system  
✅ You can see all output  
✅ You can enter passwords  
✅ Keys respond immediately  
✅ Screen scrolls properly  

## Report Issues

If something still doesn't work, please note:
1. What action you took
2. What error message you saw
3. What was expected vs actual behavior
4. Copy/paste the terminal output

---

**Happy Testing!** 🎉

If everything works, LinUtil is production-ready!
