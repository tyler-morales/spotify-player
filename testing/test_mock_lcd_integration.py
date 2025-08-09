#!/usr/bin/env python3
"""
Test Mock LCD Integration with Display Manager
"""

import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_display_manager_integration():
    """Test mock LCD with display manager"""
    print("🧪 Testing Mock LCD + Display Manager Integration")
    print("=" * 50)
    
    # Force use of mock LCD
    os.environ['USE_MOCK_LCD'] = 'true'
    
    # Import display manager components
    import app_state
    from display_manager import get_display_content
    from lcd import LCD
    
    lcd = LCD()
    
    # Test different display modes
    modes_to_test = [
        ('welcome', "Welcome mode"),
        ('clock', "Clock mode"),
        ('debug', "Debug mode"),
        ('now_playing', "Now Playing mode (no track)")
    ]
    
    for mode, description in modes_to_test:
        print(f"\n📺 Testing {description}:")
        
        # Set the display mode
        app_state.set_display_mode(app_state.DISPLAY_MODES.index(mode))
        
        # Get content from display manager
        line1, line2 = get_display_content()
        
        print(f"   Content: '{line1}' | '{line2}'")
        
        # Display with mock LCD
        lcd.clear()
        lcd.write_line_wave(line1, 0, speed=0.03)
        lcd.write_line_wave(line2, 1, speed=0.03)
        time.sleep(1)
    
    print("\n✅ Integration test completed!")
    print("🎯 Mock LCD successfully integrates with existing display system!")

if __name__ == "__main__":
    test_display_manager_integration()