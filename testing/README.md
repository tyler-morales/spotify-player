# 🧪 Testing Environment

This folder contains all experimental test files for developing new features safely before integrating them into the main application.

## 📁 Test Files Overview

### 🎵 Progress & Display Tests

#### `test_progress_lcd.py`
**Purpose**: Test progress bar display functionality  
**Features**: 
- Time formatting (mm:ss)
- Custom character progress bars (ultra-smooth)
- Smart LCD updates (only when progress changes)
- Works with existing LCD class

**Usage**: `python3 test_progress_lcd.py`  
**What it shows**: Progress bars filling left-to-right with custom block characters

---

#### `test_lcd_characters.py`
**Purpose**: Discover which ASCII characters work on your specific LCD  
**Features**:
- Tests all 256 ASCII characters
- Quick progress bar character testing
- Character range exploration
- Interactive character validation

**Usage**: `python3 test_lcd_characters.py`  
**Use when**: Finding new characters for progress bars or decorative elements

---

#### `test_custom_characters.py`
**Purpose**: Test custom LCD character creation and animation  
**Features**:
- 8 custom character slots
- Progress bar characters (different fill levels)
- Spotify-themed icons (play, pause, music notes)
- Ultra-smooth progress demos

**Usage**: `python3 test_custom_characters.py`  
**What it shows**: Professional-looking progress bars and music symbols

---

### 🎨 Animation Tests

#### `test_double_helix.py` 
**Purpose**: DNA double helix spinning animation  
**Features**:
- 8-phase rotating helix using custom characters
- Mathematical sine wave calculations
- Traveling helix effects
- DNA-themed text backgrounds

**Usage**: `python3 test_double_helix.py`  
**What it shows**: Mesmerizing spinning DNA animation - pure eye candy!

---

#### `test_heart_favorite.py`
**Purpose**: Heart animation for favoriting songs (GPIO button integration)  
**Features**:
- Multiple hearts rising animation (3-8 hearts)
- GPIO pin 17 button monitoring
- Hearts "float above" the display
- Sparkle effects and finale
- Staggered timing for magical effect

**Usage**: `python3 test_heart_favorite.py`  
**What it shows**: Hearts rising from bottom and floating above song info when GPIO 17 pressed

---

## 🚀 Integration Workflow

### 1. Experimentation Phase
- Run tests in this folder to develop and refine features
- Tweak parameters, timing, and visual effects
- Test GPIO integration and LCD compatibility

### 2. Feature Validation
- Ensure test works reliably on your hardware
- Verify GPIO pins and timing are correct
- Test edge cases and error handling

### 3. Integration Ready
- Copy working functions to main application modules
- Update `display_manager.py`, `button_handler.py`, etc.
- Add new display modes to `app_state.py` if needed

## 📋 Test Categories

### Display & Visual
- `test_progress_lcd.py` - Progress bars
- `test_custom_characters.py` - Custom graphics
- `test_lcd_characters.py` - Character discovery

### Animation & Effects  
- `test_double_helix.py` - Spinning animations
- `test_heart_favorite.py` - Interactive heart effects

### Hardware Integration
- `test_heart_favorite.py` - GPIO button integration
- All tests work with your existing LCD setup

## 🔧 Hardware Requirements

**LCD**: 16x2 I2C display at address 0x27  
**GPIO**: Pin 17 for heart/favorite button (configurable)  
**Dependencies**: RPLCD, RPi.GPIO

## 💡 Development Tips

1. **Start with character tests** to find good LCD characters
2. **Use custom character tests** for professional graphics  
3. **Test animations separately** before adding GPIO
4. **Copy working code** to main app when ready
5. **Keep tests updated** as you modify features

## 🎯 Next Steps

When you're happy with a test feature:
1. Run the test thoroughly to ensure stability
2. Copy relevant functions to appropriate main modules
3. Integrate with your existing button/display system
4. Update main app configuration as needed

---

*Happy testing! 🧪 This safe environment lets you experiment without breaking your main Spotify player.*