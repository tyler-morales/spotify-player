#!/usr/bin/env python3
"""
Mock LCD Scrolling Demo
Shows how long text is handled with scrolling
"""

import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def scrolling_demo():
    """Demo mock LCD scrolling for long text"""
    print("🖥️  Mock LCD Scrolling Demo")
    print("=" * 40)
    
    # Force use of mock LCD
    os.environ['USE_MOCK_LCD'] = 'true'
    
    from lcd import LCD
    lcd = LCD()
    
    print("\n📏 Text length demonstration:")
    short_text = "Ed Sheeran"
    long_text = "Bohemian Rhapsody (Remastered 2011)"
    
    print(f"   Short text: '{short_text}' ({len(short_text)} chars) - fits in 16")
    print(f"   Long text:  '{long_text}' ({len(long_text)} chars) - needs scrolling")
    
    print("\n1. Short text (no scrolling needed):")
    lcd.clear()
    lcd.write_line_wave("Now Playing:", 0, speed=0.03)
    lcd.write_line_wave(short_text, 1, speed=0.03)
    time.sleep(1)
    
    print("\n2. Long text - showing first 16 characters:")
    lcd.clear()
    # Show just the first 16 characters to demonstrate truncation
    lcd.lcd.cursor_pos = (0, 0)
    lcd.lcd.write_string(long_text[:16])  # "Bohemian Rhapsod"
    lcd.lcd.cursor_pos = (1, 0)
    lcd.lcd.write_string("Queen")
    time.sleep(2)
    
    print(f"\n   First 16 chars: '{long_text[:16]}'")
    print(f"   Remaining:      '{long_text[16:]}'")
    print("\n   (In real application, this would scroll to show the full text)")
    
    lcd.clear()
    print("\n✅ Mock LCD handles both short and long text appropriately!")
    print("🎯 Long text gets scrolled in real usage to show all content")

if __name__ == "__main__":
    scrolling_demo()