#!/usr/bin/env python3
"""
Test display functionality - both clock and scrolling
"""

import time
from lcd import LCD

def test_scrolling():
    """Test pendulum scrolling with long text"""
    print("🧪 Testing Pendulum Scrolling...")
    
    lcd = LCD()
    
    # Simulate the display state like main.py
    display_state = {
        'content_line1': '',
        'content_line2': '',
        'scroll_pos1': 0,
        'scroll_pos2': 0,
        'scroll_dir1': 1,
        'scroll_dir2': 1,
        'pause_until1': 0,
        'pause_until2': 0,
        'last_update': 0,
        'wave_complete': False
    }
    
    # Test with long text
    long_line1 = "This is a very long song title that should scroll back and forth"
    long_line2 = "Artist name that is also quite long and needs scrolling"
    
    print(f"Line 1 ({len(long_line1)} chars): {long_line1}")
    print(f"Line 2 ({len(long_line2)} chars): {long_line2}")
    
    try:
        lcd.clear()
        
        # Show wave effect first
        print("Phase 1: Wave effect...")
        for i in range(17):  # 0 to 16 characters
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(long_line1[:i].ljust(16))
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(long_line2[:i].ljust(16))
            time.sleep(0.1)
        
        print("Phase 2: Pendulum scrolling for 20 seconds...")
        scroll_pos1 = 0
        scroll_pos2 = 0
        scroll_dir1 = 1
        scroll_dir2 = 1
        pause_until1 = 0
        pause_until2 = 0
        
        width = 16
        scroll_speed = 0.3
        pause_time = 2.0
        start_time = time.time()
        last_update = time.time()
        
        while time.time() - start_time < 20:  # Run for 20 seconds
            now = time.time()
            
            if now - last_update >= scroll_speed:
                # Line 1 scrolling
                if len(long_line1) > width:
                    if pause_until1 <= now:
                        # Use same boundary fix as main.py
                        max_pos = len(long_line1) - width
                        pos = max(0, min(scroll_pos1, max_pos))
                        segment = long_line1[pos:pos + width]
                        lcd.lcd.cursor_pos = (0, 0)
                        lcd.lcd.write_string(segment.ljust(width))
                        
                        print(f"Line 1: pos={pos}, scroll_pos={scroll_pos1}, dir={scroll_dir1}, segment='{segment}'")
                        
                        # Check boundaries BEFORE moving position
                        if scroll_pos1 >= max_pos and scroll_dir1 == 1:
                            scroll_dir1 = -1
                            pause_until1 = now + pause_time
                            print(f"🔄 Line 1 reached end (pos={pos}), reversing")
                        elif scroll_pos1 <= 0 and scroll_dir1 == -1:
                            scroll_dir1 = 1
                            pause_until1 = now + pause_time
                            print(f"🔄 Line 1 reached start (pos={pos}), reversing")
                        else:
                            # Only move if not pausing
                            scroll_pos1 += scroll_dir1
                
                # Line 2 scrolling
                if len(long_line2) > width:
                    if pause_until2 <= now:
                        pos = max(0, min(scroll_pos2, len(long_line2) - width))
                        segment = long_line2[pos:pos + width]
                        lcd.lcd.cursor_pos = (1, 0)
                        lcd.lcd.write_string(segment.ljust(width))
                        
                        scroll_pos2 += scroll_dir2
                        
                        max_pos = len(long_line2) - width
                        if scroll_pos2 >= max_pos and scroll_dir2 == 1:
                            scroll_dir2 = -1
                            pause_until2 = now + pause_time
                            print("🔄 Line 2 reached end, reversing")
                        elif scroll_pos2 <= 0 and scroll_dir2 == -1:
                            scroll_dir2 = 1
                            pause_until2 = now + pause_time
                            print("🔄 Line 2 reached start, reversing")
                
                last_update = now
            
            time.sleep(0.05)
        
        print("✅ Scrolling test completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test stopped")
    finally:
        lcd.clear()

def test_clock():
    """Test clock display without constant wave effect"""
    print("🕒 Testing Clock Display...")
    
    lcd = LCD()
    
    try:
        from datetime import datetime
        
        # Show initial wave effect
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%a %b %d")
        
        print(f"Initial: '{time_str}' | '{date_str}'")
        
        # Wave effect
        lcd.clear()
        for i in range(17):
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(time_str[:i].ljust(16))
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(date_str[:i].ljust(16))
            time.sleep(0.1)
        
        print("Now updating time every second without wave effect...")
        
        # Update time without wave effect
        for _ in range(10):  # 10 seconds
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%a %b %d")
            
            # Direct update without wave
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(time_str.ljust(16))
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(date_str.ljust(16))
            
            print(f"Updated: {time_str}")
            time.sleep(1)
        
        print("✅ Clock test completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test stopped")
    finally:
        lcd.clear()

if __name__ == "__main__":
    print("🧪 Display Testing Suite")
    print("1. Testing scrolling...")
    test_scrolling()
    
    time.sleep(2)
    
    print("\n2. Testing clock...")
    test_clock()
    
    print("\n✅ All tests completed!")