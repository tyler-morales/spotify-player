#!/usr/bin/env python3
"""
Test Custom LCD Characters
Tests creating and displaying custom characters on LCD including progress bars
"""

from RPLCD.i2c import CharLCD
import time

def test_basic_custom_characters():
    """Test basic custom character creation and display"""
    print("🎨 Testing Basic Custom Characters")
    print("=" * 40)
    
    lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
    
    # Define custom characters (8x5 pixel patterns)
    heart = [
        0b00000,
        0b01010,
        0b11111,
        0b11111,
        0b11111,
        0b01110,
        0b00100,
        0b00000
    ]
    
    speaker = [
        0b00100,
        0b01100,
        0b11100,
        0b11111,
        0b11111,
        0b11100,
        0b01100,
        0b00100
    ]
    
    smile = [
        0b00000,
        0b00000,
        0b01010,
        0b00000,
        0b00000,
        0b10001,
        0b01110,
        0b00000
    ]
    
    bell = [
        0b00100,
        0b01110,
        0b01110,
        0b01110,
        0b11111,
        0b00100,
        0b00000,
        0b00100
    ]
    
    star = [
        0b00100,
        0b10101,
        0b01110,
        0b11111,
        0b01110,
        0b10101,
        0b00100,
        0b00000
    ]
    
    # Write custom characters to CGRAM (Character Generator RAM)
    lcd.create_char(0, heart)
    lcd.create_char(1, speaker)
    lcd.create_char(2, smile) 
    # lcd.create_char(3, bell)
    lcd.create_char(3, star)
    
    # Display the custom characters
    lcd.clear()
    lcd.write_string("Custom chars:")
    lcd.cursor_pos = (1, 0)
    lcd.write_string('\x00 \x01 \x02 \x03')  # Show custom chars by their codes
    
    print("✅ Basic custom characters displayed")
    input("Press Enter to continue...")
    
    lcd.close()

def test_progress_bar_characters():
    """Test custom characters specifically for progress bars"""
    print("📊 Testing Custom Progress Bar Characters")
    print("=" * 40)
    
    lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
    
    # Define progress bar characters - different fill levels
    empty_block = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11111
    ]
    
    quarter_block = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11111,
        0b11111
    ]
    
    half_block = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    three_quarter_block = [
        0b11111,
        0b10001,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    full_block = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    # Music note for fun
    note = [
        0b00100,
        0b00110,
        0b00101,
        0b00101,
        0b00100,
        0b11100,
        0b11100,
        0b00000
    ]
    
    # Create the characters
    lcd.create_char(0, empty_block)      # Empty progress block
    lcd.create_char(1, quarter_block)    # 25% filled
    lcd.create_char(2, half_block)       # 50% filled
    lcd.create_char(3, three_quarter_block) # 75% filled
    lcd.create_char(4, full_block)       # 100% filled
    lcd.create_char(5, note)             # Music note
    
    # Test different progress levels
    progress_tests = [
        (0, "Empty", '\x00' * 16),
        (25, "25%", '\x00' * 12 + '\x01' * 4),
        (50, "50%", '\x00' * 8 + '\x02' * 8),
        (75, "75%", '\x00' * 4 + '\x03' * 12),
        (100, "Full", '\x04' * 16),
    ]
    
    for percent, name, bar in progress_tests:
        lcd.clear()
        lcd.write_string(f"{name} - {percent}%".center(16))
        lcd.cursor_pos = (1, 0)
        lcd.write_string(bar)
        
        print(f"📊 Showing {name} progress bar ({percent}%)")
        time.sleep(2)
    
    # Show music note
    lcd.clear()
    lcd.write_string("Music Mode " + '\x05')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('\x05' * 8 + " Playing!")
    
    print("🎵 Music note test")
    input("Press Enter to continue...")
    
    lcd.close()

def test_spotify_themed_characters():
    """Test Spotify/music themed custom characters"""
    print("🎵 Testing Spotify-Themed Characters")
    print("=" * 40)
    
    lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
    
    # Play button (triangle)
    play_button = [
        0b00000,
        0b01000,
        0b01100,
        0b01110,
        0b01111,
        0b01110,
        0b01100,
        0b01000
    ]
    
    # Pause button (two bars)
    pause_button = [
        0b00000,
        0b01010,
        0b01010,
        0b01010,
        0b01010,
        0b01010,
        0b01010,
        0b00000
    ]
    
    # Next/Skip button
    next_button = [
        0b00000,
        0b01001,
        0b01011,
        0b01111,
        0b01111,
        0b01011,
        0b01001,
        0b00000
    ]
    
    # Volume/Speaker waves
    volume = [
        0b00001,
        0b00011,
        0b00101,
        0b01001,
        0b01001,
        0b00101,
        0b00011,
        0b00001
    ]
    
    # Equalizer bars
    equalizer = [
        0b00000,
        0b10101,
        0b10101,
        0b11111,
        0b01110,
        0b01010,
        0b00100,
        0b00000
    ]
    
    # Musical notes
    double_note = [
        0b00110,
        0b00111,
        0b00101,
        0b00101,
        0b11101,
        0b11100,
        0b11100,
        0b00000
    ]
    
    # Create characters
    lcd.create_char(0, play_button)
    lcd.create_char(1, pause_button)
    lcd.create_char(2, next_button)
    lcd.create_char(3, volume)
    lcd.create_char(4, equalizer)
    lcd.create_char(5, double_note)
    
    # Demo different states
    states = [
        ("Now Playing", '\x00 \x05 Playing \x05 \x03'),
        ("Paused", '\x01 \x05 Paused  \x05 \x03'),
        ("Skipping", '\x02 \x05 Next... \x05 \x03'),
        ("Equalizer", '\x04 \x05 Music \x05 \x04'),
    ]
    
    for title, display in states:
        lcd.clear()
        lcd.write_string(title.center(16))
        lcd.cursor_pos = (1, 0)
        lcd.write_string(display)
        
        print(f"🎶 Showing: {title}")
        time.sleep(2)
    
    input("Press Enter to finish...")
    lcd.close()

def test_progress_with_custom_chars():
    """Test actual progress bar using custom characters"""
    print("⏱️ Testing Progress Bar with Custom Characters")
    print("=" * 40)
    
    lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
    
    # Ultra smooth progress characters (8 levels of fill)
    chars = [
        # Empty
        [0b11111, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11111],
        # 1/8 filled
        [0b11111, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11111, 0b11111],
        # 2/8 filled  
        [0b11111, 0b10001, 0b10001, 0b10001, 0b10001, 0b11111, 0b11111, 0b11111],
        # 3/8 filled
        [0b11111, 0b10001, 0b10001, 0b10001, 0b11111, 0b11111, 0b11111, 0b11111],
        # 4/8 filled
        [0b11111, 0b10001, 0b10001, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
        # 5/8 filled
        [0b11111, 0b10001, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
        # 6/8 filled
        [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
        # Full (just in case)
        [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
    ]
    
    # Create all 8 custom characters
    for i, char_pattern in enumerate(chars):
        lcd.create_char(i, char_pattern)
    
    # Simulate a song progress (4:12 = 252 seconds)
    total_seconds = 252
    
    print("🎵 Simulating song progress with ultra-smooth custom progress bar...")
    print("   Song: 4:12 total duration")
    
    try:
        for current_second in range(0, total_seconds + 1, 5):  # Every 5 seconds
            # Calculate progress
            progress = current_second / total_seconds
            
            # Format time
            current_min = current_second // 60
            current_sec = current_second % 60
            total_min = total_seconds // 60
            total_sec = total_seconds % 60
            
            time_display = f"{current_min}:{current_sec:02d} / {total_min}:{total_sec:02d}".center(16)
            
            # Create progress bar (16 characters wide)
            progress_bar = ""
            for pos in range(16):
                # Calculate what character should be at this position
                position_progress = (pos + 1) / 16
                if progress >= position_progress:
                    # This position should be completely filled
                    progress_bar += '\x06'  # Full character
                elif progress >= (pos / 16):
                    # This position is partially filled
                    partial_progress = (progress - (pos / 16)) * 16
                    char_index = min(int(partial_progress * 8), 7)
                    progress_bar += chr(char_index)
                else:
                    # This position is empty
                    progress_bar += '\x00'  # Empty character
            
            # Update LCD
            lcd.clear()
            lcd.write_string(time_display)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(progress_bar)
            
            print(f"   {current_min}:{current_sec:02d} - {progress*100:.1f}% complete")
            time.sleep(1)
            
            if current_second >= 30:  # Stop after 30 seconds for demo
                break
                
    except KeyboardInterrupt:
        print("\n   Demo stopped by user")
    
    lcd.clear()
    lcd.write_string("Custom Progress")
    lcd.cursor_pos = (1, 0) 
    lcd.write_string("    Complete!")
    
    input("Press Enter to finish...")
    lcd.close()

def main():
    """Main test menu"""
    print("🎨 Custom LCD Character Test Suite")
    print("=" * 50)
    
    tests = [
        ("1", "Basic Custom Characters", test_basic_custom_characters),
        ("2", "Progress Bar Characters", test_progress_bar_characters),
        ("3", "Spotify-Themed Characters", test_spotify_themed_characters),
        ("4", "Ultra-Smooth Progress Demo", test_progress_with_custom_chars),
        ("5", "Run All Tests", None),
    ]
    
    for key, name, func in tests:
        print(f"{key}) {name}")
    
    choice = input("\nChoose test (1-5): ").strip()
    
    try:
        if choice == "5":
            # Run all tests
            for key, name, func in tests[:-1]:  # Exclude "Run All Tests"
                if func:
                    print(f"\n🧪 Running: {name}")
                    func()
        else:
            # Run specific test
            for key, name, func in tests:
                if choice == key and func:
                    func()
                    break
            else:
                print("Invalid choice")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
