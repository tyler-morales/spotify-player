#!/usr/bin/env python3
"""
Mock LCD Static Demo
Demonstrates mock LCD functionality without long scrolling animations
"""

import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def static_demo():
    """Demo mock LCD with static displays"""
    print("🖥️  Mock LCD Static Demo")
    print("=" * 40)
    
    # Force use of mock LCD
    os.environ['USE_MOCK_LCD'] = 'true'
    
    from lcd import LCD
    lcd = LCD()
    
    print("\n1. Welcome Screen:")
    lcd.clear()
    lcd.write_line_wave("Welcome :)", 0, speed=0.08)
    lcd.write_line_wave("Starting up...", 1, speed=0.08)
    time.sleep(1)
    
    print("\n2. Now Playing - Short Text:")
    lcd.clear()
    lcd.write_line_wave("Shape of You", 0, speed=0.05)
    lcd.write_line_wave("Ed Sheeran", 1, speed=0.05)
    time.sleep(1)
    
    print("\n3. Clock Display:")
    lcd.clear()
    from datetime import datetime
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%a %b %d")
    lcd.write_line_wave(time_str, 0, speed=0.05)
    lcd.write_line_wave(date_str, 1, speed=0.05)
    time.sleep(1)
    
    print("\n4. Debug Display:")
    lcd.clear()
    lcd.write_line_wave("API: 42 | Ready", 0, speed=0.05)
    lcd.write_line_wave("Mode: clock", 1, speed=0.05)
    time.sleep(1)
    
    print("\n5. No Music Connected:")
    lcd.clear()
    lcd.write_line_wave("No track", 0, speed=0.05)
    lcd.write_line_wave("Connect Spotify", 1, speed=0.05)
    time.sleep(1)
    
    print("\n6. Long Text Preview (first 16 chars):")
    lcd.clear()
    long_title = "Bohemian Rhapsody (Remastered 2011)"
    long_artist = "Queen (Greatest Hits)"
    
    # Show just the initial 16 characters without scrolling
    lcd.lcd.cursor_pos = (0, 0)
    lcd.lcd.write_string(long_title[:16])
    lcd.lcd.cursor_pos = (1, 0)
    lcd.lcd.write_string(long_artist[:16])
    time.sleep(2)
    
    lcd.clear()
    print("\n✅ Static demo completed!")
    print("\n🎯 Mock LCD Features Demonstrated:")
    print("   • ┌─┐ ASCII border characters")
    print("   • │ │ Side borders for 16x2 display")
    print("   • └─┘ Complete border representation")
    print("   • Character-by-character typewriter effect")
    print("   • Real-time console display update")
    print("   • Perfect for development without hardware")

if __name__ == "__main__":
    static_demo()