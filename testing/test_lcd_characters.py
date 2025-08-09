#!/usr/bin/env python3
"""
LCD Character Test Utility
Tests all ASCII characters to see which ones display properly on your LCD
"""

import time
from lcd import LCD

def test_all_characters():
    """Test all 256 ASCII characters on LCD"""
    print("🔍 Testing all LCD characters...")
    print("Watch your LCD to see which characters display properly!")
    print("Press Ctrl+C to stop early")
    
    lcd = LCD()
    lcd.clear()
    
    good_chars = []
    
    try:
        for i in range(32, 256):  # Skip control characters (0-31)
            char = chr(i)
            
            # Display character info
            lcd.clear()
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(f"Char #{i:03d}")
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(f"'{char}' " + char * 10)  # Show char + repeated
            
            print(f"Testing #{i:03d}: '{char}' - {repr(char)}")
            
            # Ask user if it looks good
            user_input = input("Good? (y/n/s=skip range): ").lower().strip()
            if user_input == 'y':
                good_chars.append((i, char))
            elif user_input == 's':
                skip_to = input("Skip to character number: ")
                try:
                    i = int(skip_to) - 1  # -1 because loop will increment
                except:
                    pass
            
            if len(good_chars) >= 20:  # Stop after finding 20 good chars
                break
                
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    
    lcd.clear()
    lcd.lcd.cursor_pos = (0, 0)
    lcd.lcd.write_string("Test Complete!")
    
    print(f"\n✅ Found {len(good_chars)} good characters:")
    for ascii_code, char in good_chars:
        print(f"   #{ascii_code:03d}: '{char}' - {repr(char)}")
    
    return good_chars

def test_specific_ranges():
    """Test specific promising character ranges"""
    print("🎯 Testing specific character ranges...")
    
    lcd = LCD()
    
    # Test ranges that often have fun characters
    ranges_to_test = [
        (128, 160, "Extended ASCII"),
        (160, 192, "Latin characters"), 
        (192, 224, "Box drawing"),
        (224, 256, "Special symbols")
    ]
    
    for start, end, description in ranges_to_test:
        print(f"\n📍 Testing {description} (#{start}-{end-1}):")
        
        for i in range(start, end):
            try:
                char = chr(i)
                lcd.clear()
                lcd.lcd.cursor_pos = (0, 0)
                lcd.lcd.write_string(f"{description[:8]}")
                lcd.lcd.cursor_pos = (1, 0)
                lcd.lcd.write_string(f"#{i:03d}: '{char}'" + char * 5)
                
                print(f"   #{i:03d}: '{char}'", end=" ")
                time.sleep(0.5)
                
                if i % 8 == 7:  # New line every 8 characters
                    print()
                    
            except Exception as e:
                print(f"   #{i:03d}: ERROR - {e}")
    
    print("\nDone testing ranges!")
    lcd.clear()

def quick_progress_bar_test():
    """Quick test of different character combinations for progress bars"""
    print("🎵 Testing progress bar character combinations...")
    
    lcd = LCD()
    
    # Character pairs to test for progress bars (filled, empty)
    test_pairs = [
        ("*", "-", "Asterisk + Dash"),
        ("+", ".", "Plus + Dot"), 
        ("o", ".", "Lowercase o + Dot"),
        ("O", "o", "Uppercase O + lowercase o"),
        ("X", "-", "X + Dash"),
        ("■", "□", "Filled square + Empty square"),  # Might not work
        ("▓", "░", "Shade blocks"),  # Might not work
        ("|", ".", "Pipe + Dot"),
        (":", ".", "Colon + Dot"),
        ("█", " ", "Block + Space"),  # Might not work
    ]
    
    for filled_char, empty_char, description in test_pairs:
        print(f"\n🧪 Testing: {description}")
        
        try:
            # Test progress bar at 50%
            progress_bar = filled_char * 8 + empty_char * 8
            
            lcd.clear()
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(description[:16])
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(progress_bar)
            
            print(f"   Display: '{progress_bar}'")
            
            response = input("   Good? (y/n): ").lower().strip()
            if response == 'y':
                print(f"   ✅ WINNER: '{filled_char}' + '{empty_char}'")
                return filled_char, empty_char
                
        except Exception as e:
            print(f"   ❌ Error with {description}: {e}")
        
        time.sleep(1)
    
    lcd.clear()
    return None, None

if __name__ == "__main__":
    print("🔤 LCD Character Test Utility")
    print("=" * 40)
    
    choice = input("Choose test:\n1) Test all characters\n2) Test specific ranges\n3) Quick progress bar test\nChoice (1/2/3): ").strip()
    
    try:
        if choice == "1":
            test_all_characters()
        elif choice == "2":
            test_specific_ranges()
        elif choice == "3":
            filled, empty = quick_progress_bar_test()
            if filled and empty:
                print(f"\n🎯 Use these in your progress bar:")
                print(f'   filled = "{filled}" * filled_chars')
                print(f'   empty = "{empty}" * (width - filled_chars)')
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted")
        try:
            lcd = LCD()
            lcd.clear()
        except:
            pass
    except Exception as e:
        print(f"\n❌ Error: {e}")
        try:
            lcd = LCD()
            lcd.clear()
        except:
            pass