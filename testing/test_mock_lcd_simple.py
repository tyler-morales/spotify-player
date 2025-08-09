#!/usr/bin/env python3
"""
Simple Mock LCD Demo
Quick demonstration of ASCII-based LCD visualization
"""

import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def simple_demo():
    """Simple demo of mock LCD functionality"""
    print("🖥️  Mock LCD Simple Demo")
    print("=" * 40)
    
    # Force use of mock LCD
    os.environ['USE_MOCK_LCD'] = 'true'
    
    from lcd import LCD
    lcd = LCD()
    
    print("\n1. Basic display:")
    time.sleep(1)
    
    print("\n2. Short text (no scrolling):")
    lcd.clear()
    lcd.write_line_wave("Now Playing:", 0, speed=0.05)
    lcd.write_line_wave("Ed Sheeran", 1, speed=0.05)
    time.sleep(2)
    
    print("\n3. Long text (with scrolling for 3 seconds):")
    lcd.clear()
    long_title = "Bohemian Rhapsody (Remastered 2011)"
    lcd.write_line_wave(long_title, 0, speed=0.03)
    lcd.write_line_wave("Queen", 1, speed=0.03)
    
    # Show scrolling for 3 seconds
    interrupt_flag = False
    def test_interrupt():
        return interrupt_flag
    
    import threading
    def interrupt_after_delay():
        time.sleep(3)
        global interrupt_flag
        interrupt_flag = True
    
    interrupt_thread = threading.Thread(target=interrupt_after_delay, daemon=True)
    interrupt_thread.start()
    
    lcd.display(long_title, "Queen", interrupt_callback=test_interrupt)
    
    print("\n4. Clock display:")
    lcd.clear()
    time.sleep(0.5)
    from datetime import datetime
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%a %b %d")
    
    lcd.write_line_wave(time_str, 0, speed=0.05)
    lcd.write_line_wave(date_str, 1, speed=0.05)
    time.sleep(2)
    
    lcd.clear()
    print("\n✅ Demo completed!")
    print("\n🎯 Mock LCD Features:")
    print("   • ASCII borders using ┌─┐│└┘ characters")
    print("   • 16x2 character display simulation")
    print("   • Typewriter effect for text appearance")
    print("   • Scrolling animation for long text")
    print("   • Console-based visualization for development")

if __name__ == "__main__":
    simple_demo()