# LinUtil Color Palette Reference

## Base Colors

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Background Colors                              │
│  ─────────────────                              │
│  $background    #0d1117  ███████  Base         │
│  $surface       #161b22  ███████  Cards        │
│  $surface-light #21262d  ███████  Elevated     │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  Primary Colors                                 │
│  ──────────────                                 │
│  $primary       #58a6ff  ███████  Main Blue    │
│  $primary-dim   #1f6feb  ███████  Darker Blue  │
│  $secondary     #8b949e  ███████  Gray         │
│  $accent        #79c0ff  ███████  Highlight    │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  Semantic Colors                                │
│  ───────────────                                │
│  $success       #3fb950  ███████  Green        │
│  $warning       #d29922  ███████  Orange       │
│  $error         #f85149  ███████  Red          │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  Text Colors                                    │
│  ───────────                                    │
│  $text          #c9d1d9  ███████  Primary Text │
│  $text-muted    #8b949e  ███████  Muted Text   │
│                                                 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│  Border Colors                                  │
│  ─────────────                                  │
│  $border        #30363d  ███████  Default      │
│  $border-accent #58a6ff  ███████  Highlighted  │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Usage Examples

### Welcome Screen
```
╔═══════════════════════════════════════════════════╗
║   🐧 LinUtil - Linux Post-Install Setup 🚀       ║  ← $accent
╚═══════════════════════════════════════════════════╝

🖥️  Detected: Fedora Linux 40                         ← $primary
📦 Package Manager: DNF                               ← $success

┌─────────────────┐ ┌─────────────────┐
│ 📦 Install Apps │ │ 🔧 System Tweaks│             ← $primary-dim
└─────────────────┘ └─────────────────┘

┌─────────────────┐ ┌─────────────────┐
│ 🔄 Update System│ │ ❌ Exit         │             ← $success / $error
└─────────────────┘ └─────────────────┘

💡 Tip: Use 'j' and 'k' to navigate...               ← $warning
```

### Apps Screen
```
┌─────────────────────────────────────────────────┐
│                                                 │ ← $surface
│  📦 Application Installer                       │ ← $accent
│  📦 Package Manager: DNF                        │ ← $success
│                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │✓ Select  │ │✗ Select  │ │📥 Install│       │
│  │  All     │ │  None    │ │ Selected │       │
│  └──────────┘ └──────────┘ └──────────┘       │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │ ← $surface-light
│  │  📦 Browsers                              │ │ ← $accent
│  │                                           │ │
│  │  ☑ Firefox [I]                           │ │ ← $text
│  │     Fast, private web browser            │ │ ← $text-muted
│  │                                           │ │
│  │  ☐ Chrome [I]                            │ │
│  │     Google web browser                   │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌──────────┐                                  │
│  │◀ Back    │                                  │
│  └──────────┘                                  │
└─────────────────────────────────────────────────┘
```

### Button States

```
Default State:
┌─────────────┐
│  Button     │  background: $surface-light
└─────────────┘  border: $border

Hover State:
┌─────────────┐
│  Button     │  background: $primary-dim
└─────────────┘  border: $primary

Focus State:
┌═════════════┐
║  Button     ║  background: $primary
╚═════════════╝  border: $accent (thick)

Primary Variant:
┌─────────────┐
│  Button     │  background: $primary-dim
└─────────────┘  border: $primary
                 text-style: bold

Success Variant:
┌─────────────┐
│  Button     │  background: $success
└─────────────┘  border: $success
                 text-style: bold

Error Variant:
┌─────────────┐
│  Button     │  background: $error
└─────────────┘  border: $error
                 text-style: bold
```

### Checkbox States

```
Unchecked:
☐ Application Name [I]                    ← $text (bold)
    Description text here                 ← $text-muted (italic)

Checked:
☑ Application Name [I]                    ← $text (bold)
    Description text here                 ← $text-muted (italic)

Hover (entire row):
┌─────────────────────────────────────────┐
│ ☐ Application Name [I]                  │ ← $surface background
│     Description text here               │ ← $border
└─────────────────────────────────────────┘
```

### Containers

```
Main Container (Screen Level):
┌─────────────────────────────────────────┐
│                                         │ ← background: $background
│   ┌─────────────────────────────────┐  │
│   │                                 │  │ ← background: $surface
│   │                                 │  │    border: rounded $border-accent
│   │   ┌─────────────────────────┐  │  │
│   │   │                         │  │  │ ← background: $surface-light
│   │   │                         │  │  │    border: rounded $border
│   │   │   Content Here          │  │  │
│   │   │                         │  │  │
│   │   └─────────────────────────┘  │  │
│   │                                 │  │
│   └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

## Color Combinations

### High Contrast (WCAG AA)
✅ $text on $background (ratio: 12.63:1)
✅ $text on $surface (ratio: 11.82:1)
✅ $primary on $background (ratio: 8.37:1)
✅ $success on $background (ratio: 7.24:1)

### Color Harmony
- **Triadic**: Primary ($primary), Success ($success), Warning ($warning)
- **Analogous**: Primary ($primary), Accent ($accent), Secondary ($secondary)
- **Complementary**: Primary ($primary), Error ($error)

## Accessibility Guidelines

### Do's ✅
- Use $text for important content
- Use $text-muted for secondary info
- Use semantic colors ($success, $warning, $error) consistently
- Provide clear focus indicators with $border-accent
- Maintain 3:1 contrast ratio for UI components

### Don'ts ❌
- Don't use $text-muted for critical information
- Don't mix border styles (use rounded consistently)
- Don't use colors alone to convey information
- Don't place $secondary text on $surface (low contrast)

## Dark Theme Best Practices

1. **Depth Through Elevation**
   - Base: $background
   - Level 1: $surface
   - Level 2: $surface-light

2. **Color Temperature**
   - Cool tones for interactive elements (blues)
   - Warm tones for warnings/actions (oranges, greens)

3. **Text Hierarchy**
   - Headers: $accent + bold
   - Body: $text
   - Metadata: $text-muted + italic

4. **Interactive Feedback**
   - Default: subtle borders
   - Hover: brighter background
   - Focus: accent border
   - Active: primary color

## Inspiration Sources

- **GitHub Dark Theme**: Primary color palette
- **VS Code Dark+**: Border and surface colors
- **Dracula Theme**: Color harmony inspiration
- **Material Design**: Elevation system

## Terminal Testing

Test your terminal with this command:
```bash
echo -e "\033[38;2;88;166;255m■\033[0m Primary ($primary)"
echo -e "\033[38;2;63;251;80m■\033[0m Success ($success)"
echo -e "\033[38;2;210;153;34m■\033[0m Warning ($warning)"
echo -e "\033[38;2;248;81;73m■\033[0m Error ($error)"
echo -e "\033[38;2;201;209;217m■\033[0m Text ($text)"
echo -e "\033[38;2;139;148;158m■\033[0m Muted ($text-muted)"
```

If you see colored blocks, your terminal supports the color palette!

---

**Color Palette Version**: 1.0
**Last Updated**: October 23, 2025
**Based On**: GitHub Dark Theme
