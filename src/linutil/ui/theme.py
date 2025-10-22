"""
Modern UI Theme for LinUtil

Professional color scheme and styling configurations.
"""

# Modern color palette inspired by popular TUI applications
THEME_CSS = """
/* ============================================ */
/*             MODERN THEME - LINUTIL          */
/* ============================================ */

/* Root color definitions */
$background: #0d1117;
$surface: #161b22;
$surface-light: #21262d;
$primary: #58a6ff;
$primary-dim: #1f6feb;
$secondary: #8b949e;
$accent: #79c0ff;
$success: #3fb950;
$warning: #d29922;
$error: #f85149;
$text: #c9d1d9;
$text-muted: #8b949e;
$border: #30363d;
$border-accent: #58a6ff;

/* ============================================ */
/*             GLOBAL STYLES                   */
/* ============================================ */

Screen {
    background: $background;
}

/* ============================================ */
/*             CONTAINERS                      */
/* ============================================ */

#main-container {
    align: center middle;
    width: 100%;
    height: 100%;
    background: $background;
}

Container {
    background: transparent;
}

/* ============================================ */
/*             WELCOME SCREEN                  */
/* ============================================ */

#welcome-container {
    width: 90;
    height: auto;
    background: $surface;
    border: rounded $border-accent;
    padding: 3 4;
}

.banner {
    text-align: center;
    color: $accent;
    text-style: bold;
}

#distro-info {
    text-align: center;
    color: $primary;
    text-style: bold;
    margin: 1 0;
}

#pm-info {
    text-align: center;
    color: $success;
    margin-bottom: 1;
}

/* ============================================ */
/*             BUTTONS                         */
/* ============================================ */

.button-row {
    align: center middle;
    width: 100%;
    height: auto;
    margin: 1 0;
}

.button-row Button {
    margin: 0 1;
    min-width: 20;
}

Button {
    border: tall $border;
    background: $surface-light;
    color: $text;
}

Button:hover {
    background: $primary-dim;
    color: white;
    border: tall $primary;
}

Button:focus {
    background: $primary;
    border: tall $accent;
}

Button.-primary {
    background: $primary-dim;
    border: tall $primary;
    color: white;
    text-style: bold;
}

Button.-primary:hover {
    background: $primary;
    border: tall $accent;
}

Button.-success {
    background: $success;
    border: tall $success;
    color: white;
    text-style: bold;
}

Button.-success:hover {
    background: #4ac359;
    border: tall #56d364;
}

Button.-error {
    background: $error;
    border: tall $error;
    color: white;
    text-style: bold;
}

Button.-error:hover {
    background: #ff6b6b;
    border: tall #ff8787;
}

/* ============================================ */
/*             SCREEN TITLES                   */
/* ============================================ */

.screen-title {
    text-align: center;
    text-style: bold;
    color: $accent;
    margin: 0 0 1 0;
    text-style: bold underline;
}

.pm-label {
    text-align: center;
    color: $success;
    margin: 0 0 1 0;
}

/* ============================================ */
/*             UPDATE SCREEN                   */
/* ============================================ */

#update-container {
    width: 90%;
    max-width: 120;
    height: 100%;
    background: $surface;
    border: rounded $border-accent;
    padding: 2 3;
}

#update-info-container {
    height: 1fr;
    border: rounded $border;
    background: $surface-light;
    padding: 2;
    margin: 1 0;
}

.update-info {
    color: $text;
    margin: 0 0 1 0;
}

.info-item {
    color: $text-muted;
    margin: 0 0 0 4;
}

/* ============================================ */
/*             APPS SCREEN                     */
/* ============================================ */

#apps-container {
    height: 1fr;
    border: rounded $border;
    background: $surface-light;
    padding: 1;
    margin: 1 0;
}

.category-label {
    color: $accent;
    text-style: bold;
    background: $surface;
    padding: 1 2;
    margin: 1 0;
    border: tall $border;
}

#apps-container {
    height: 1fr;
    border: rounded $border;
    background: $surface-light;
    padding: 1;
    margin: 1 0;
}

.category-label {
    color: $accent;
    text-style: bold;
    background: $surface;
    padding: 1 2;
    margin: 1 0;
    border: tall $border;
}

.category-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 0 2;
    margin: 1 0 0 0;
}

.section-header {
    text-style: bold;
    color: $accent;
    background: $surface;
    padding: 0 2;
    margin: 1 0 0 0;
}

.no-apps-message {
    text-align: center;
    color: $warning;
    padding: 5;
}

.no-tweaks-message {
    text-align: center;
    color: $warning;
    padding: 5;
}

.subtitle {
    text-align: center;
    color: $text-muted;
    margin: 0 0 1 0;
}

.restart-warning {
    color: $warning;
    text-style: italic;
    padding: 0 0 0 4;
    margin: 0;
    height: 1;
}

#apps-screen-container {
    width: 90%;
    max-width: 120;
    height: 100%;
    background: $surface;
    border: rounded $border-accent;
    padding: 2 3;
}

.app-checkbox-container {
    background: transparent;
    padding: 1 2;
    margin: 0;
    border: none;
}

.app-checkbox-container:hover {
    background: $surface;
    border: tall $border;
}

.app-name {
    color: $text;
    text-style: bold;
    margin: 0;
}

.app-description {
    color: $text-muted;
    margin: 0 0 0 2;
}

AppCheckbox {
    width: 100%;
    height: auto;
    background: transparent;
    padding: 0 1;
}

AppCheckbox:hover {
    background: $surface;
}

AppCheckbox Checkbox {
    width: auto;
}

AppCheckbox Vertical {
    width: 1fr;
    margin: 0 1;
}

/* ============================================ */
/*             TWEAKS SCREEN                   */
/* ============================================ */

#tweaks-container {
    width: 90%;
    max-width: 120;
    height: 100%;
    background: $surface;
    border: rounded $border-accent;
    padding: 2 3;
}

#tweaks-list-container {
    height: 1fr;
    border: rounded $border;
    background: $surface-light;
    padding: 1;
    margin: 1 0;
}

.tweak-checkbox-container {
    background: transparent;
    padding: 1 2;
    margin: 0;
    border: none;
}

.tweak-checkbox-container:hover {
    background: $surface;
    border: tall $border;
}

.tweak-name {
    color: $text;
    text-style: bold;
    margin: 0;
}

.tweak-description {
    color: $text-muted;
    margin: 0 0 0 2;
}

TweakCheckbox {
    width: 100%;
    height: auto;
    background: transparent;
    padding: 0 1;
}

TweakCheckbox:hover {
    background: $surface;
}

TweakCheckbox Checkbox {
    width: auto;
}

TweakCheckbox Vertical {
    width: 1fr;
    margin: 0 1;
}

/* ============================================ */
/*             CHECKBOXES                      */
/* ============================================ */

Checkbox {
    background: transparent;
    border: none;
    padding: 0;
    width: auto;
}

Checkbox:focus {
    background: $surface;
}

Checkbox > .toggle--label {
    color: $text;
    margin: 0 1;
}

/* ============================================ */
/*             TIPS & HINTS                    */
/* ============================================ */

.tip-text {
    text-align: center;
    color: $warning;
    text-style: italic;
    margin: 1 2;
    background: $surface-light;
    padding: 1;
    border: tall $border;
}

.shortcuts-guide {
    text-align: center;
    color: $text-muted;
    text-style: italic;
    margin: 1 2;
}

.hint {
    text-align: center;
    color: $text-muted;
    text-style: italic;
    margin: 1 0;
}

/* ============================================ */
/*             STATUS MESSAGES                 */
/* ============================================ */

.status-label {
    text-align: center;
    color: $warning;
    text-style: bold;
    padding: 1;
    background: $surface-light;
    border: tall $border;
}

.size-warning {
    text-align: center;
    color: $error;
    text-style: bold;
    padding: 2;
    background: $surface;
    border: rounded $error;
}

.info-label {
    color: $text-muted;
    margin: 0 2;
}

/* ============================================ */
/*             HEADER & FOOTER                 */
/* ============================================ */

Header {
    background: $surface;
    color: $accent;
    border: tall $border;
}

Footer {
    background: $surface;
    color: $text-muted;
    border: tall $border;
}

Footer > .footer--key {
    background: $primary-dim;
    color: white;
}

Footer > .footer--description {
    color: $text;
}

/* ============================================ */
/*             SCROLLBARS                      */
/* ============================================ */

ScrollableContainer:focus {
    border: tall $border-accent;
}

Vertical:focus {
    border: none;
}

Horizontal:focus {
    border: none;
}

/* ============================================ */
/*             LOADING STATES                  */
/* ============================================ */

LoadingIndicator {
    background: $surface;
    color: $primary;
}

/* ============================================ */
/*             ACCESSIBILITY                   */
/* ============================================ */

*:disabled {
    opacity: 0.5;
}

*:focus {
    border: tall $border-accent;
}

Static:focus {
    border: none;
}

Label:focus {
    border: none;
}
"""


# Icon/Symbol sets for different UI elements
ICONS = {
    # Navigation
    "back": "◀",
    "forward": "▶",
    "up": "▲",
    "down": "▼",
    
    # Actions
    "install": "📥",
    "update": "🔄",
    "tweak": "🔧",
    "apps": "📦",
    "settings": "⚙",
    "exit": "❌",
    
    # Status
    "success": "✓",
    "error": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "tip": "💡",
    
    # Selection
    "select_all": "✓",
    "select_none": "✗",
    "checked": "☑",
    "unchecked": "☐",
    
    # Categories
    "browser": "🌐",
    "development": "💻",
    "media": "🎵",
    "office": "📝",
    "gaming": "🎮",
    "utility": "🔧",
    "system": "⚙",
}


def get_icon(name: str) -> str:
    """
    Get an icon by name.
    
    Args:
        name: Icon name
        
    Returns:
        Icon character(s)
    """
    return ICONS.get(name, "•")
