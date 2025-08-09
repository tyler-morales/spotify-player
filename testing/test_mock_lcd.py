#!/usr/bin/env python3
"""
Test Mock LCD Display functionality
Demonstrates ASCII-based LCD visualization using keyboard characters
"""

import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_mock_lcd_basic():
    """Test basic mock LCD functionality"""
    print("🧪 Testing Mock LCD Basic Functionality...")
    
    # Force use of mock LCD
    os.environ['USE_MOCK_LCD'] = 'true'
    
    from lcd import LCD
    
    lcd = LCD()
    
    print("\n1. Testing clear and basic display...")
    time.sleep(1)
    
    print("\n2. Testing typewriter effect...")
    lcd.clear()
    lcd.write_line_wave("Hello World!", 0, speed=0.1)
    lcd.write_line_wave("Mock LCD Test", 1, speed=0.1)
    time.sleep(2)
    
    print("\n3. Testing long text scrolling...")
    lcd.clear()
    long_title = "This is a very long song title that should scroll back and forth"
    long_artist = "Artist with a really long name that overflows the display"
    
    # Show wave effect first
    lcd.write_line_wave(long_title, 0, speed=0.05)
    lcd.write_line_wave(long_artist, 1, speed=0.05)
    time.sleep(1)
    
    print("\n4. Testing scrolling for 10 seconds...")
    print("⏰ (Will interrupt after 5 seconds to test interrupt functionality)")
    
    # Test interrupt functionality
    interrupt_flag = False
    def test_interrupt():
        return interrupt_flag
    
    # Create a thread to interrupt after 5 seconds
    import threading
    def interrupt_after_delay():
        time.sleep(5)
        global interrupt_flag
        interrupt_flag = True
        print("\n🛑 Interrupting scroll...")
    
    interrupt_thread = threading.Thread(target=interrupt_after_delay, daemon=True)
    interrupt_thread.start()
    
    lcd.display(long_title, long_artist, interrupt_callback=test_interrupt)
    
    print("\n✅ Mock LCD basic tests completed!")

def test_mock_lcd_animations():
    """Test various animations and effects"""
    print("\n🎨 Testing Mock LCD Animations...")
    
    os.environ['USE_MOCK_LCD'] = 'true'
    from lcd import LCD
    
    lcd = LCD()
    
    # Test different content types
    test_cases = [
        ("Short Text", "Line 2"),
        ("Medium length text", "Another medium text"),
        ("This is an extremely long line that will definitely need scrolling", "Short"),
        ("Short", "This is also an extremely long line that needs scrolling as well"),
        ("Both lines are very long and will need scrolling", "This second line is equally long and should scroll too")
    ]
    
    for i, (line1, line2) in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {'Long' if len(line1) > 16 else 'Short'} + {'Long' if len(line2) > 16 else 'Short'}")
        
        lcd.clear()
        time.sleep(0.5)
        
        # Show typewriter effect
        lcd.write_line_wave(line1, 0, speed=0.05)
        lcd.write_line_wave(line2, 1, speed=0.05)
        
        # If either line is long, show scrolling for 3 seconds
        if len(line1) > 16 or len(line2) > 16:
            print("   📜 Scrolling...")
            interrupt_flag = False
            def interrupt_test():
                return interrupt_flag
            
            def stop_after_delay():
                time.sleep(3)
                global interrupt_flag
                interrupt_flag = True
            
            interrupt_thread = threading.Thread(target=stop_after_delay, daemon=True)
            interrupt_thread.start()
            
            lcd.display(line1, line2, interrupt_callback=interrupt_test)
        else:
            time.sleep(2)
    
    print("\n✅ Animation tests completed!")

def test_mock_lcd_real_scenarios():
    """Test scenarios similar to actual Spotify player usage"""
    print("\n🎵 Testing Real Spotify Player Scenarios...")
    
    os.environ['USE_MOCK_LCD'] = 'true'
    from lcd import LCD
    
    lcd = LCD()
    
    # Simulate different display modes
    scenarios = [
        # Welcome message
        ("Welcome :)", "Starting up..."),
        
        # Now playing - short
        ("Shape of You", "Ed Sheeran"),
        
        # Now playing - long title
        ("Bohemian Rhapsody (Remastered 2011)", "Queen"),
        
        # Now playing - long artist
        ("Hotel California", "Eagles (Their Greatest Hits 1971-1975)"),
        
        # Now playing - both long
        ("Stairway to Heaven (Led Zeppelin IV Remaster)", "Led Zeppelin (Rock and Roll Hall of Fame)"),
        
        # Clock display
        ("14:32:45", "Mon Dec 23"),
        
        # Debug display
        ("API: 42 | Playing", "Mode: now_playing"),
        
        # No track
        ("No track", "Connect Spotify")
    ]
    
    for i, (line1, line2) in enumerate(scenarios, 1):
        print(f"\n🎬 Scenario {i}: {line1[:20]}{'...' if len(line1) > 20 else ''}")
        
        lcd.clear()
        time.sleep(0.5)
        
        # Quick typewriter effect (faster for demo)
        lcd.write_line_wave(line1, 0, speed=0.03)
        lcd.write_line_wave(line2, 1, speed=0.03)
        
        # Show scrolling if needed
        if len(line1) > 16 or len(line2) > 16:
            print("   📜 Scrolling demonstration...")
            interrupt_flag = False
            def interrupt_test():
                return interrupt_flag
            
            def stop_after_delay():
                time.sleep(2)  # Shorter for demo
                global interrupt_flag
                interrupt_flag = True
            
            interrupt_thread = threading.Thread(target=stop_after_delay, daemon=True)
            interrupt_thread.start()
            
            lcd.display(line1, line2, interrupt_callback=interrupt_test)
        else:
            time.sleep(1.5)
    
    lcd.clear()
    print("\n✅ Real scenario tests completed!")

if __name__ == "__main__":
    print("🖥️  Mock LCD Display Test Suite")
    print("=" * 50)
    
    # Basic functionality
    test_mock_lcd_basic()
    
    time.sleep(2)
    
    # Animation tests
    test_mock_lcd_animations()
    
    time.sleep(2)
    
    # Real scenario tests
    test_mock_lcd_real_scenarios()
    
    print("\n" + "=" * 50)
    print("🎉 All Mock LCD tests completed successfully!")
    print("🖥️  The ASCII LCD representation uses:")
    print("   ┌─────────────────┐  <- Top border")
    print("   │ 16 char content │  <- Content rows")
    print("   │ 16 char content │")
    print("   └─────────────────┘  <- Bottom border")