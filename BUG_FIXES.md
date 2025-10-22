# Bug Fixes - Interactive Terminal Implementation

## Summary of Changes

Fixed **4 critical bugs** reported during Fedora VM testing by implementing an interactive terminal approach.

## Bugs Fixed

### 1. ✅ Screen Overflow/Not Scrollable
**Problem**: App content was cut off at the bottom of the screen with no scrolling.

**Solution**:
- Added `ScrollableContainer` import to all screens
- Wrapped Update screen content in `ScrollableContainer`
- Apps and Tweaks screens already use `ScrollableContainer`

**Files Modified**:
- `src/linutil/ui/app.py` - Added ScrollableContainer import and usage

---

### 2. ✅ Back and Quit Functions Don't Work  
**Problem**: `Escape` and `Q` keys not responding.

**Solution**:
- Removed blocking `run_worker()` calls that prevented key handling
- Simplified button handlers to not check `is_updating` state
- Keybindings now work immediately since operations run in suspended terminal

**Expected Behavior**:
- `Escape` → Returns to previous screen
- `Q` → Quits the application
- Works from any screen at any time

---

### 3. ✅ **No Password/Interaction Handling (CRITICAL FIX)**
**Problem**: App couldn't handle sudo passwords or yes/no prompts, making it completely non-functional.

**Solution - Interactive Terminal Executor**:

Created `src/linutil/core/terminal_executor.py` with:
- `TerminalExecutor` class that runs commands in the user's actual terminal
- `execute_interactive()` - Runs commands with full stdin/stdout/stderr access
- `execute_with_confirmation()` - Shows commands first, asks user to confirm

Modified all screens to use `app.suspend()`:
```python
with self.app.suspend():
    executor = TerminalExecutor()
    result = executor.execute_with_confirmation(
        commands=['sudo dnf install -y firefox'],
        use_sudo=True,
        description="Installing Firefox"
    )
```

**How It Works**:
1. User clicks "Install" or "Update" in the TUI
2. App suspends (returns to terminal)
3. Shows what will be executed
4. User confirms (Y/N)
5. Commands run with full interaction:
   - User enters sudo password when prompted
   - User sees all real-time output
   - User can answer yes/no prompts
   - User presses Enter when done
6. App resumes, shows success/failure notification

**Files Modified**:
- `src/linutil/core/terminal_executor.py` (NEW)
- `src/linutil/ui/app.py`
- `src/linutil/ui/screens/apps_screen.py`
- `src/linutil/ui/screens/tweaks_screen.py`

---

### 4. ✅ No Verbose Output/Can't See What's Happening
**Problem**: Background workers hid all output, impossible to debug or see progress.

**Solution**:
- Interactive terminal now shows ALL output in real-time
- Users see exactly what commands are running
- Full package manager output visible (download progress, file installation, etc.)
- Easy to debug stuck operations or errors

**Example Output User Sees**:
```
===================================
Installing 3 application(s): Firefox, Git, htop
===================================

The following commands will be executed:

  1. sudo dnf install -y firefox git htop

===================================

Continue? [y/N]: y

===================================
Installing 3 application(s): Firefox, Git, htop
===================================

Last metadata expiration check: 0:15:23 ago on Wed 23 Oct 2025 10:30:45 AM EDT.
Dependencies resolved.
================================================================================
 Package              Architecture    Version           Repository        Size
================================================================================
Installing:
 firefox              x86_64          119.0-1.fc38      updates           195 M
 git                  x86_64          2.41.0-1.fc38     updates           160 k
 htop                 x86_64          3.2.2-1.fc38      fedora            223 k

Transaction Summary
================================================================================
Install  3 Packages

Total download size: 195 M
Installed size: 711 M
Downloading Packages:
(1/3): git-2.41.0-1.fc38.x86_64.rpm              234 kB/s | 160 kB     00:00
(2/3): htop-3.2.2-1.fc38.x86_64.rpm              287 kB/s | 223 kB     00:00
(3/3): firefox-119.0-1.fc38.x86_64.rpm           3.1 MB/s | 195 MB     01:02
--------------------------------------------------------------------------------
Total                                            3.1 MB/s | 195 MB     01:02
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                        1/1
  Installing       : git-2.41.0-1.fc38.x86_64                               1/3
  Installing       : htop-3.2.2-1.fc38.x86_64                               2/3
  Installing       : firefox-119.0-1.fc38.x86_64                            3/3
  Running scriptlet: firefox-119.0-1.fc38.x86_64                            3/3
  Verifying        : firefox-119.0-1.fc38.x86_64                            1/3
  Verifying        : git-2.41.0-1.fc38.x86_64                               2/3
  Verifying        : htop-3.2.2-1.fc38.x86_64                               3/3

Installed:
  firefox-119.0-1.fc38.x86_64
  git-2.41.0-1.fc38.x86_64
  htop-3.2.2-1.fc38.x86_64

Complete!

===================================
Operation completed!
===================================

Press Enter to continue...
```

---

## Technical Details

### Old Approach (Broken)
```python
# Background worker - NO user interaction
async def _install_apps(self, apps):
    result = await manager.install_packages(packages)
    # User can't enter password
    # User can't see output
    # Keys don't work during execution
```

### New Approach (Fixed)
```python
# Suspend TUI, run in terminal
def action_install(self):
    commands = ['sudo dnf install -y firefox']
    
    with self.app.suspend():  # Exit TUI temporarily
        executor = TerminalExecutor()
        result = executor.execute_with_confirmation(
            commands=commands,
            use_sudo=True,
            description="Installing Firefox"
        )
    # TUI resumes automatically
    self.app.notify("Installation complete!")
```

## Key Benefits

1. **Full Interaction**: Users can enter passwords, answer prompts, press Ctrl+C
2. **Complete Transparency**: Every command and its output is visible
3. **Better UX**: Users see progress bars, download speeds, etc.
4. **Debuggable**: Easy to see where operations fail
5. **Responsive**: Keybindings work because no blocking async operations
6. **Professional**: Matches behavior of standard package manager tools

## Testing Instructions

### Test Password Prompts
```bash
cd ~/linutil
source venv/bin/activate
linutil
```

1. Press `a` → Select an app → Press `i`
2. Confirm installation
3. **Enter your password when prompted**
4. Watch installation progress
5. Press Enter to return to TUI

### Test System Update
1. Press `u`
2. Click "Start Update"
3. Confirm update
4. **Enter password**
5. Watch all packages update
6. Press Enter when done

### Test Tweaks
1. Press `t`
2. Select tweaks → Press `a`
3. Confirm application
4. **Enter password**
5. Watch each tweak apply
6. Press Enter when done

### Test Keybindings
- Press `Escape` from any screen → Should go back
- Press `q` from welcome screen → Should quit
- Keys should work immediately (no lag)

## Files Changed

### New Files
- `src/linutil/core/terminal_executor.py` (170 lines)

### Modified Files
- `src/linutil/ui/app.py`:
  - Added `terminal_executor` import
  - Added `ScrollableContainer` import
  - Simplified `UpdateScreen` (removed async worker)
  - Added `info-label` CSS class
  
- `src/linutil/ui/screens/apps_screen.py`:
  - Added `terminal_executor` import
  - Replaced `_install_apps()` async worker with `action_install()` interactive
  - Removed ~100 lines of async installation code
  
- `src/linutil/ui/screens/tweaks_screen.py`:
  - Added `terminal_executor` import
  - Replaced `_apply_tweaks()` async worker with `action_apply()` interactive
  - Removed ~120 lines of async application code

## Lines of Code

- **Removed**: ~290 lines of complex async worker code
- **Added**: ~200 lines of simple interactive terminal code
- **Net**: -90 lines (simpler and more functional!)

## Migration Notes

The old `CommandExecutor` class (with async/await) is still in the codebase but no longer used by the UI. It could be:
- Kept for future programmatic use
- Removed to simplify the codebase
- Used for CLI commands that don't need interaction

All package manager classes (`AptManager`, `DnfManager`) are also still present but unused. The new approach directly calls package manager CLIs.

---

**Status**: All 4 critical bugs fixed and ready for testing! 🎉
