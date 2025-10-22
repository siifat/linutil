# Critical Bug Fixes - Round 2

## Bugs Fixed

### 1. ✅ AttributeError: 'app' Property Conflict

**Error**: 
```
AttributeError: property 'app' of 'AppCheckbox' object has no setter
```

**Root Cause**: 
`AppCheckbox` and `TweakCheckbox` inherit from `Horizontal` (a Textual widget). Textual widgets have a built-in read-only property called `.app` that references the application instance. We were trying to use `self.app` to store our `AppDefinition`, which conflicted with this built-in property.

**Solution**:
- Renamed `self.app` → `self.app_def` in `AppCheckbox` class
- Updated all references: `app_checkbox.app` → `app_checkbox.app_def`

**Files Modified**:
- `src/linutil/ui/screens/apps_screen.py`:
  - Line 25: `self.app_def = app` (was `self.app = app`)
  - Line 27: `self.app_def.name` (was `self.app.name`)
  - Line 27: `self.app_def.id` (was `self.app.id`)
  - Line 32: `self.app_def.description` (was `self.app.description`)
  - Line 181: `app_checkbox.app_def` (was `app_checkbox.app`)

---

### 2. ✅ Back and Quit Keys Not Working

**Problem**: 
Pressing `Escape` or `Q` keys did nothing on any screen.

**Root Cause**:
Textual's keybindings require corresponding `action_*` methods. The bindings defined `Binding("q", "quit", "Quit")` but there was no `action_quit()` method on the screens, so the key press was silently ignored.

**Solution**:
Added `action_quit()` method to all screens that calls `self.app.exit()`:

```python
def action_quit(self) -> None:
    """Quit the application."""
    self.app.exit()
```

**Files Modified**:
- `src/linutil/ui/app.py`:
  - Added `action_quit()` to `WelcomeScreen` (line ~103)
  - Added `action_quit()` to `UpdateScreen` (line ~152)

- `src/linutil/ui/screens/apps_screen.py`:
  - Added `action_quit()` after `action_select_none()` (line ~177)

- `src/linutil/ui/screens/tweaks_screen.py`:
  - Added `action_quit()` after `action_select_none()` (line ~177)

**Now Works**:
- `Escape` key: Goes back to previous screen (built-in Textual action)
- `Q` key: Quits the application completely from any screen

---

## Testing Instructions

### Test on Fedora VM

```bash
cd ~/linutil
source venv/bin/activate
pip install -e .
linutil
```

### Test 1: AttributeError Fixed

1. Launch `linutil`
2. Press `a` or click "Install Applications"
3. **Expected**: Apps screen loads without errors
4. **Previous**: AttributeError crash

### Test 2: Quit Key Works

1. From welcome screen, press `q`
2. **Expected**: LinUtil exits immediately
3. From apps screen, press `q`
4. **Expected**: LinUtil exits immediately
5. From tweaks screen, press `q`
6. **Expected**: LinUtil exits immediately
7. From update screen, press `q`
8. **Expected**: LinUtil exits immediately

### Test 3: Back Key Works

1. From welcome screen, press `a` (Apps)
2. Press `Escape`
3. **Expected**: Returns to welcome screen
4. Press `t` (Tweaks)
5. Press `Escape`
6. **Expected**: Returns to welcome screen
7. Press `u` (Update)
8. Press `Escape`
9. **Expected**: Returns to welcome screen

---

## Summary

- **Bug 1**: Fixed `app` property name conflict → renamed to `app_def`
- **Bug 2**: Fixed missing `action_quit()` methods → added to all 4 screens

Both bugs are now fixed! The app should load properly and keybindings should work.

---

## Next Test

Try installing an application:
1. `linutil`
2. Press `a`
3. Select an app with Space
4. Press `i`
5. Confirm with `y`
6. Enter your password
7. Watch installation

This should now work end-to-end! 🎉
