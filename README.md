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
  - Single button on GPIO pin 17 cycles through all pages
  - Immediate response when scrolling is interrupted
  - Proper debouncing to prevent accidental triggers
  - Visual feedback during interactions

## Hardware Requirements

- Raspberry Pi with GPIO pins
- 16x2 I2C LCD display (PCF8574 controller, default address 0x27)
- Push button connected to GPIO pin 17 (with pull-down resistor)

## File Structure

```
├── README.md              # This file
├── learnings.md           # Study topics and learning resources
├── lcd.py                 # LCD control class with animations
├── pages.py               # Main application - page switching logic
├── buttons.py             # Button testing utility
├── now-playing.py         # Simple now-playing display demo
└── pages/
    ├── __init__.py
    ├── clock.py           # Clock page implementation
    ├── now_playing.py     # Now playing page implementation
    └── debug.py           # System debug information page
```

## Key Components

### LCD Class (`lcd.py`)
- **I2C Communication**: Handles PCF8574-based LCD control
- **Typewriter Effect**: `write_line_wave()` creates character-by-character display
- **Interruptible Scrolling**: `scroll_both()` monitors GPIO during animation and can be stopped mid-scroll
- **Display Management**: Smart text handling for overflow content

### Page System (`pages.py`)
- **Page Cycling**: ClockPage → NowPlayingPage → DebugPage → repeat
- **Interrupt Handling**: Detects when scrolling is interrupted vs. normal completion
- **GPIO Monitoring**: Responsive button detection with proper debouncing
- **State Management**: Clean transitions between pages with LCD clearing

### Page Modules (`pages/`)
- **`clock.py`**: Real-time clock display with formatted time
- **`now_playing.py`**: Track information with interruptible scrolling for long titles
- **`debug.py`**: System stats using `/proc/uptime` and standard Python libraries

## Usage

### Run the main application:
```bash
python3 pages.py
```

### Controls:
- **Press button once**: Cycle to next page
- **Press button during scrolling**: Immediately skip to next page
- **Ctrl+C**: Exit application cleanly

### Test individual components:
```bash
python3 buttons.py          # Test button detection
python3 now-playing.py      # Test basic LCD display
```

## Technical Implementation

### Interruptible Scrolling Algorithm
1. Display starts with typewriter effect
2. If text > 16 chars, begin scrolling animation
3. **Every scroll frame**: Check GPIO pin state
4. **Button pressed**: Immediately return from scroll function
5. **Main loop**: Detect early return and handle page transition

### Page Flow Logic
```
Display Page → Check if interrupted → Handle transition → Next page
     ↓              ↓                      ↓
Scrolling      Button pressed?     Immediate switch
continues      ↓           ↓              ↓
     ↓        Yes         No        Wait for button
Complete      ↓           ↓              ↓
     ↓    Interrupt   Normal wait    Page cycle
Wait for      ↓           ↓              ↓
button    Page switch  Page switch   Page switch
```

## Development Status

✅ **Completed Features:**
- Multi-page navigation system
- Interruptible scrolling animations
- GPIO button handling with debouncing
- System debug information display
- Clean page transitions

🚧 **Next Phase:**
- Spotify API integration
- Real-time track information
- Dynamic content updates
- Enhanced UI interactions