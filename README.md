# Spotify Player LCD Display

A Raspberry Pi project that displays track information, clock, and system debug info on an I2C LCD display, with intelligent GPIO button navigation and interruptible scrolling animations.

## Features

- **Multi-Page Display System**: Three pages accessible via GPIO button cycling

  - **Now Playing Page**: Displays track title and artist with smart scrolling for overflow text
  - **Clock Page**: Shows current time with typewriter animation
  - **Debug Page**: System information including date, uptime, and current time

- **Intelligent Scrolling**:

  - Automatic scrolling for text longer than 16 characters
  - **Interruptible scrolling** - press button during animation to immediately skip to next page
  - Typewriter effect for initial text display

- **Smart GPIO Navigation**:
- 4-button controls: PREV (GPIO17), PLAY (GPIO18), NEXT (GPIO27), CYCLE (GPIO22)
- Debounced inputs with visual feedback
- Hold CYCLE 5s to restart app/service (configurable)

## Hardware Requirements

- Raspberry Pi with GPIO pins
- 16x2 I2C LCD display (PCF8574 controller, default address 0x27)
- 4x momentary push buttons: GPIO 17/18/27/22 to GND (internal pull-downs)

## File Structure

```
├── README.md              # This file
├── learnings.md           # Study topics and learning resources
├── lcd.py                 # LCD control class with animations
├── main.py                # NEW: Main application entrypoint (standard)
├── pages.py               # LEGACY: Deprecated, forwards to main.py
├── buttons.py             # Button testing utility
├── now-playing.py         # Simple now-playing display demo
└── pages/                 # LEGACY: old page modules (kept for reference)
    ├── __init__.py
    ├── clock.py           # Clock page implementation (legacy)
    ├── now_playing.py     # Now playing page implementation (legacy)
    └── debug.py           # System debug information page (legacy)
```

## Key Components

### LCD Class (`lcd.py`)

- **I2C Communication**: Handles PCF8574-based LCD control
- **Typewriter Effect**: `write_line_wave()` creates character-by-character display
- **Interruptible Scrolling**: `scroll_both()` monitors GPIO during animation and can be stopped mid-scroll
- **Display Management**: Smart text handling for overflow content

### Modern App Flow (`main.py`)

- Single-threaded LCD updates with background monitoring for Spotify track changes
- 4-button control (PREV/PLAY/NEXT/CYCLE) with hold-to-restart feature
- Auto-sleep to clock when idle; auto-wake on playback/buttons

### Legacy Page System (`pages.py` + `pages/`)

- Kept only for reference/backward compatibility
- `pages.py` now forwards to `main.py`

## New: Smooth Slide Transition Between Tracks

- Outgoing title/artist slide left out while the new track slides in from the right.
- Works with overflow text: captures the currently visible scrolling window so the slide is seamless.
- After the slide completes, auto-pauses briefly before resuming pendulum scrolling.

Configuration (advanced):

- Transition speed (seconds per frame): `app_state.display_state['transition_speed']` (default `0.06`).
- Feature applies to `now_playing` mode; other modes still use the wave effect.

Testing:

- Run the slide transition tests (headless):
  - `python3 testing/test_slide_transition.py`
- Also see: `testing/test_display.py` and `testing/test_welcome_screen.py` for related display behaviors.

## Usage

### Run the application:

```bash
python3 main.py
```

Note: `pages.py` exists only for backward compatibility and prints a deprecation notice if used.

### Controls:

- **PREV/PLAY/NEXT**: Playback controls
- **CYCLE (short press)**: Cycle display modes (now_playing → clock → debug)
- **CYCLE (hold 5s)**: Restart the application or service (configurable; see REBOOT_FEATURE.md)
- **Ctrl+C**: Exit application cleanly

### Test individual components:

```bash
python3 testing/test_welcome_screen.py   # headless welcome/mode logic
python3 testing/test_reboot_feature.py   # headless hold-to-restart logic
```

## Development Status

✅ Completed Features include the modern `main.py` flow, caching, romanization, and hold-to-restart. Legacy files remain for reference but are no longer the recommended path.
