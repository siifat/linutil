# LinUtil UI Preview

## Welcome Screen

```
═══════════════════════════════════════════════════════════════════════════════
  LinUtil - Linux Post-Install Setup                                [H] Help
───────────────────────────────────────────────────────────────────────────────

                    ╔═══════════════════════════════════════════════════╗
                    ║   🐧 LinUtil - Linux Post-Install Setup 🚀       ║
                    ╚═══════════════════════════════════════════════════╝

                         🖥️  Detected: Fedora Linux 40
                         📦 Package Manager: DNF


                    ┌─────────────────────┐  ┌─────────────────────┐
                    │ 📦 Install          │  │ 🔧 System          │
                    │    Applications     │  │    Tweaks          │
                    └─────────────────────┘  └─────────────────────┘

                    ┌─────────────────────┐  ┌─────────────────────┐
                    │ 🔄 Update System    │  │ ❌ Exit            │
                    └─────────────────────┘  └─────────────────────┘


              💡 Tip: Use Ctrl+C to safely exit at any time


         [U] Update  [A] Install Apps  [T] System Tweaks  [Q] Quit
───────────────────────────────────────────────────────────────────────────────
  ESC: Back  Q: Quit                                                     1/1  
═══════════════════════════════════════════════════════════════════════════════
```

## Apps Screen

```
═══════════════════════════════════════════════════════════════════════════════
  LinUtil - Linux Post-Install Setup                                [H] Help
───────────────────────────────────────────────────────────────────────────────

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                      📦 Application Installer                            ║
║                      📦 Package Manager: DNF                             ║
║                                                                           ║
║   ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐          ║
║   │ ✓ Select All │  │ ✗ Select None│  │ 📥 Install Selected│          ║
║   └──────────────┘  └──────────────┘  └────────────────────┘          ║
║                                                                           ║
║   ┌───────────────────────────────────────────────────────────────────┐ ║
║   │                                                                   │ ║
║   │   📦 Browsers                                                     │ ║
║   │                                                                   │ ║
║   │   ☑ Firefox [I]                                                  │ ║
║   │       Fast, private, and secure web browser                      │ ║
║   │                                                                   │ ║
║   │   ☐ Google Chrome [I]                                            │ ║
║   │       Popular web browser from Google                            │ ║
║   │                                                                   │ ║
║   │   ☐ Brave Browser [I]                                            │ ║
║   │       Privacy-focused browser with built-in ad blocking          │ ║
║   │                                                                   │ ║
║   │                                                                   │ ║
║   │   💻 Development                                                  │ ║
║   │                                                                   │ ║
║   │   ☑ Visual Studio Code [I]                                       │ ║
║   │       Powerful code editor from Microsoft                        │ ║
║   │                                                                   │ ║
║   │   ☐ Git [I]                                                      │ ║
║   │       Distributed version control system                         │ ║
║   │                                                                   │ ║
║   │   ☐ Docker [I SI]                                                │ ║
║   │       Container platform for building applications               │ ║
║   │                                                                   │ ║
║   └───────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║   ┌──────────────┐                                                       ║
║   │ ◀ Back       │                                                       ║
║   └──────────────┘                                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

  [I] Install  [A] Select All  [N] Select None  [ESC] Back  [Q] Quit
───────────────────────────────────────────────────────────────────────────────
  ESC: Back  I: Install  Q: Quit                                        2/4  
═══════════════════════════════════════════════════════════════════════════════
```

## Tweaks Screen

```
═══════════════════════════════════════════════════════════════════════════════
  LinUtil - Linux Post-Install Setup                                [H] Help
───────────────────────────────────────────────────────────────────────────────

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                 🔧 System Tweaks & Optimizations                         ║
║                 Select tweaks to apply to your system                    ║
║                                                                           ║
║   ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐          ║
║   │ ✓ Select All │  │ ✗ Select None│  │ ⚡ Apply Selected  │          ║
║   └──────────────┘  └──────────────┘  └────────────────────┘          ║
║                                                                           ║
║   ┌───────────────────────────────────────────────────────────────────┐ ║
║   │                                                                   │ ║
║   │   📦 Package Management                                           │ ║
║   │                                                                   │ ║
║   │   ☑ Enable RPM Fusion [I MP]                                     │ ║
║   │       Enable RPM Fusion Free and Non-Free repositories           │ ║
║   │                                                                   │ ║
║   │   ☑ Install Multimedia Codecs [I MP]                             │ ║
║   │       Install ffmpeg and multimedia codecs                       │ ║
║   │                                                                   │ ║
║   │   ☐ Faster DNF [FM MP]                                           │ ║
║   │       Configure DNF for faster downloads                         │ ║
║   │                                                                   │ ║
║   │                                                                   │ ║
║   │   🔧 System                                                        │ ║
║   │                                                                   │ ║
║   │   ☐ Disable SELinux [FM K]                                       │ ║
║   │       Disable SELinux security (requires restart)                │ ║
║   │       ⚠️ Requires restart                                         │ ║
║   │                                                                   │ ║
║   │   ☐ Enable Firewall [SS SI]                                      │ ║
║   │       Enable and start firewalld service                         │ ║
║   │                                                                   │ ║
║   └───────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║   ┌──────────────┐                                                       ║
║   │ ◀ Back       │                                                       ║
║   └──────────────┘                                                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

  [T] Apply  [A] Select All  [N] Select None  [ESC] Back  [Q] Quit
───────────────────────────────────────────────────────────────────────────────
  ESC: Back  T: Apply  Q: Quit                                          3/4  
═══════════════════════════════════════════════════════════════════════════════
```

## Update Screen

```
═══════════════════════════════════════════════════════════════════════════════
  LinUtil - Linux Post-Install Setup                                [H] Help
───────────────────────────────────────────────────────────────────────────────

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                           🔄 System Update                               ║
║                         📦 Package Manager: DNF                          ║
║                                                                           ║
║   ┌───────────────────────────────────────────────────────────────────┐ ║
║   │                                                                   │ ║
║   │   This will update all installed packages on your system.        │ ║
║   │                                                                   │ ║
║   │   The update will run in an interactive terminal where you can:  │ ║
║   │                                                                   │ ║
║   │       ✓ See real-time output                                     │ ║
║   │       ✓ Enter your password when prompted                        │ ║
║   │       ✓ Confirm package installations                            │ ║
║   │                                                                   │ ║
║   └───────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║                                                                           ║
║                      ┌─────────────────────┐                            ║
║                      │ 🔄 Start Update     │                            ║
║                      └─────────────────────┘                            ║
║                                                                           ║
║                                                                           ║
║                      ┌─────────────────────┐                            ║
║                      │ ◀ Back              │                            ║
║                      └─────────────────────┘                            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


  [ESC] Back  [Q] Quit
───────────────────────────────────────────────────────────────────────────────
  ESC: Back  Q: Quit                                                     4/4  
═══════════════════════════════════════════════════════════════════════════════
```

## Color Legend

### Text Colors
- **Bright White** (#c9d1d9): Primary content, titles
- **Muted Gray** (#8b949e): Descriptions, secondary info
- **Cyan/Blue** (#58a6ff, #79c0ff): Interactive elements, highlights
- **Green** (#3fb950): Success states, confirmations
- **Orange** (#d29922): Warnings, tips
- **Red** (#f85149): Errors, exit buttons

### Background Colors
- **Deep Dark** (#0d1117): Screen background
- **Dark Gray** (#161b22): Container backgrounds
- **Light Gray** (#21262d): Elevated surfaces, scrollable areas

### Borders
- **Default** (#30363d): Standard borders, separators
- **Accent** (#58a6ff): Focused elements, primary containers

## Key Features

### Visual Hierarchy
1. **Screen Title**: Large, centered, accented
2. **Sub-info**: Muted, below title
3. **Action Buttons**: Prominent, colorful
4. **Content Area**: Scrollable, bordered
5. **Back Button**: Bottom left, consistent

### Interactive Elements
- ✅ **Hover Effects**: Subtle background change
- ✅ **Focus Indicators**: Accent-colored borders
- ✅ **Selection States**: Checked/unchecked symbols
- ✅ **Button Variants**: Color-coded by action type

### Accessibility
- ✅ High contrast ratios (WCAG AA)
- ✅ Clear visual feedback
- ✅ Keyboard navigation
- ✅ Screen reader friendly

### Consistency
- ✅ Same layout structure across screens
- ✅ Consistent icon usage
- ✅ Unified color scheme
- ✅ Predictable button placement

## Terminal Size Requirements

**Minimum**: 80 columns × 24 rows
**Recommended**: 100+ columns × 30+ rows

If terminal is too small, a warning screen is displayed:

```
═══════════════════════════════════════════════════════════════════════════════

                         ⚠️ Terminal Size Too Small

                         Current: 70x20
                         Minimum Required: 80x24

              Please resize your terminal and restart the application.

═══════════════════════════════════════════════════════════════════════════════
```

## Screenshots

For actual screenshots on Linux, run:
```bash
linutil
# Then use your terminal's screenshot feature
```

Or record a demo:
```bash
asciinema rec linutil-demo.cast
linutil
# Use the app
exit
asciinema play linutil-demo.cast
```

---

**Preview Version**: 1.0
**Generated**: October 23, 2025
**Based On**: Textual Framework + GitHub Dark Theme
