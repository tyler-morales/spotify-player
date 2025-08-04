# Japanese Text Romanization Feature

## Overview
This feature automatically detects and romanizes Japanese text (hiragana, katakana, and kanji) in Spotify track and artist names for proper display on the HD44780 LCD controller.

## How It Works
- **Automatic Detection**: Detects Japanese characters in track/artist names
- **Romanization**: Converts Japanese text to romaji using the pykakasi library
- **Always On**: When Japanese text is detected, it's automatically romanized (no toggle needed)
- **LCD Compatible**: Ensures all text can be displayed on the 16x2 LCD

## Files Modified/Added

### New Files:
- `japanese_processor.py` - Core Japanese text processing module
- `test_japanese.py` - Test script for Japanese processing
- `test_display_integration.py` - Test script for display integration

### Modified Files:
- `requirements.txt` - Added pykakasi>=2.2.1
- `main.py` - Initialize Japanese processor
- `app_state.py` - Added Japanese processor availability tracking
- `display_manager.py` - Integrated Japanese processing into display content generation

## Installation
1. Install the pykakasi dependency:
   ```bash
   source venv/bin/activate
   pip install pykakasi>=2.2.1
   ```

## Examples
- **Original**: `打上花火` by `DAOKO×米津玄師`
- **Romanized**: `uchiagehanabi` by `DAOKOxyonetsugenshi`

- **Original**: `あいみょん` - `マリーゴールド`
- **Romanized**: `aimyon` - `mariigoorudo`

## Testing
Run the test scripts to verify functionality:
```bash
python test_japanese.py
python test_display_integration.py
```

## Technical Details
- Uses pykakasi library for romanization
- Detects Japanese using Unicode ranges:
  - Hiragana: U+3040-U+309F
  - Katakana: U+30A0-U+30FF
  - Kanji: U+4E00-U+9FAF
- Processing occurs in `display_manager.py` for consistent application
- Graceful fallback when pykakasi is not available
- No performance impact for non-Japanese text