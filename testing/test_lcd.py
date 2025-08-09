#!/usr/bin/env python3
"""
Test LCD display functionality
"""

import time
from lcd import LCD

def test_lcd():
    """Test LCD wave effect and display cycling"""
    
    print("🖥️  Testing LCD Display...")
    lcd = LCD()
    
    try:
        # Test 1: Wave effect with short text
        print("Test 1: Short text (should show wave effect)")
        lcd.clear()
        lcd.write_line_wave("Short Text", 0, speed=0.1)
        lcd.write_line_wave("Line 2", 1, speed=0.1)
        time.sleep(2)
        
        # Test 2: Wave effect with long text
        print("Test 2: Long text (should show wave effect then scroll)")
        lcd.clear()
        long_title = "This is a very long song title that should scroll"
        long_artist = "Artist with a really long name that overflows"
        
        # Show wave effect first
        lcd.write_line_wave(long_title, 0, speed=0.05)
        lcd.write_line_wave(long_artist, 1, speed=0.05)
        time.sleep(1)
        
        # Then show scrolling for 10 seconds
        print("Scrolling for 10 seconds...")
        
        # Simple interrupt test
        interrupt_flag = False
        def test_interrupt():
            return interrupt_flag
        
        # Create a thread to interrupt after 5 seconds
        import threading
        def interrupt_after_delay():
            time.sleep(5)
            global interrupt_flag
            interrupt_flag = True
            print("🛑 Interrupting scroll...")
        
        interrupt_thread = threading.Thread(target=interrupt_after_delay, daemon=True)
        interrupt_thread.start()
        
        lcd.display(long_title, long_artist, interrupt_callback=test_interrupt)
        
        print("✅ LCD tests completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    finally:
        lcd.clear()
        print("🧹 LCD cleared")

if __name__ == "__main__":
    test_lcd()