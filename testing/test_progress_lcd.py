#!/usr/bin/env python3
"""
Test Progress Display on Real LCD
Tests progress bar display using the existing LCD class
"""

import time
from lcd import LCD
from RPLCD.i2c import CharLCD

class ProgressDisplay:
    def __init__(self):
        """Initialize using existing LCD class with custom characters"""
        try:
            self.lcd = LCD()  # Use default I2C address 0x27
            self.raw_lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)  # For custom chars
            self.last_progress_bar = ""  # Track last displayed progress bar
            self.custom_chars_loaded = False
            print("✅ LCD initialized for progress testing with custom character support")
        except Exception as e:
            print(f"❌ LCD initialization failed: {e}")
            raise
    
    def setup_custom_progress_characters(self):
        """Setup custom characters for ultra-smooth progress bars"""
        if self.custom_chars_loaded:
            return
            
        # Ultra smooth progress characters (8 levels of horizontal fill - left to right)
        progress_chars = [
            # Empty block (just border)
            [0b11111, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11111],
            # 1/5 filled (1 column)
            [0b11111, 0b11001, 0b11001, 0b11001, 0b11001, 0b11001, 0b11001, 0b11111],
            # 2/5 filled (2 columns)
            [0b11111, 0b11101, 0b11101, 0b11101, 0b11101, 0b11101, 0b11101, 0b11111],
            # 3/5 filled (3 columns)
            [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
            # 4/5 filled (4 columns) - same as full since we only have 3 inner columns in 5x8
            [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
            # Full block
            [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
            # Extra full (same)
            [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
            # Extra full (same)
            [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],
        ]
        
        # Create all 8 custom characters
        for i, char_pattern in enumerate(progress_chars):
            self.raw_lcd.create_char(i, char_pattern)
        
        self.custom_chars_loaded = True
        print("🎨 Custom progress characters loaded!")
    
    def format_time(self, ms):
        """Convert milliseconds to mm:ss format"""
        if ms is None or ms < 0:
            return "0:00"
        
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def create_progress_bar(self, progress_ms, duration_ms, width=16, use_custom_chars=True):
        """Create a 16-character progress bar using custom characters for ultra-smooth display"""
        if not duration_ms or duration_ms <= 0:
            if use_custom_chars:
                return chr(0) * width  # Empty custom blocks
            else:
                return "." * width  # Empty bar fallback
        
        # Calculate progress percentage
        progress = min(progress_ms / duration_ms, 1.0)  # Clamp to 1.0 max
        
        if use_custom_chars and self.custom_chars_loaded:
            # Ultra-smooth custom character progress bar
            progress_bar = ""
            for pos in range(width):
                # Calculate what character should be at this position
                position_start = pos / width
                position_end = (pos + 1) / width
                
                if progress >= position_end:
                    # This position should be completely filled
                    progress_bar += chr(6)  # Full character (index 6)
                elif progress > position_start:
                    # This position is partially filled
                    partial_progress = (progress - position_start) * width
                    char_index = min(int(partial_progress * 8), 7)
                    progress_bar += chr(char_index)
                else:
                    # This position is empty
                    progress_bar += chr(0)  # Empty character (index 0)
            
            return progress_bar
        else:
            # Fallback to character-based progress bar
            filled_chars = int(progress * width)
            filled = "ÿ" * filled_chars  # Reference mark (filled)
            empty = "○" * (width - filled_chars)  # Circle (empty)
            return filled + empty
    
    def display_progress(self, progress_ms, duration_ms, is_playing=True, force_update=False):
        """Display progress on LCD - only updates when progress bar changes"""
        # Format times
        current_time = self.format_time(progress_ms)
        total_time = self.format_time(duration_ms)
        
        # Create time display (centered)
        time_line = f"{current_time} / {total_time}".center(16)
        
        # Create progress bar
        if is_playing:
            progress_bar = self.create_progress_bar(progress_ms, duration_ms)
        else:
            progress_bar = "--PAUSED--      "  # Show paused state
        
        # Only update LCD if progress bar actually changed or forced
        if progress_bar != self.last_progress_bar or force_update:
            # Use raw LCD for custom characters
            self.raw_lcd.clear()
            self.raw_lcd.cursor_pos = (0, 0)
            self.raw_lcd.write_string(time_line)
            self.raw_lcd.cursor_pos = (1, 0)
            self.raw_lcd.write_string(progress_bar)
            
            self.last_progress_bar = progress_bar
            
            print(f"🔄 LCD UPDATED:")
            print(f"   Line 1: '{time_line}'")
            print(f"   Line 2: '{progress_bar}'")
            return True
        else:
            print(f"⏭️  No visual change - LCD not updated (progress: {current_time})")
            return False
    
    def show_no_track(self):
        """Display when no track is playing"""
        line1 = "   No Track    ".center(16)
        if self.custom_chars_loaded:
            line2 = chr(0) * 16  # Empty custom blocks
        else:
            line2 = "----------------"
        
        self.raw_lcd.clear()
        self.raw_lcd.cursor_pos = (0, 0)
        self.raw_lcd.write_string(line1)
        self.raw_lcd.cursor_pos = (1, 0)
        self.raw_lcd.write_string(line2)
        
        print(f"LCD Line 1: '{line1}'")
        print(f"LCD Line 2: '{line2}'")

def test_progress_on_lcd():
    """Test the progress display on real LCD"""
    print("🎵 Testing Progress Display on Real LCD")
    print("="*50)
    
    try:
        # Initialize progress display with real LCD
        progress_display = ProgressDisplay()
        
        # Setup custom progress characters
        print("🎨 Setting up ultra-smooth custom progress characters...")
        progress_display.setup_custom_progress_characters()
        
        # Test scenarios - shorter for LCD testing
        test_cases = [
            {
                'name': 'Beginning of Song',
                'progress_ms': 15000,   # 0:15
                'duration_ms': 180000,  # 3:00
                'is_playing': True
            },
            {
                'name': 'Your Example - 2:34/4:12', 
                'progress_ms': 154000,  # 2:34
                'duration_ms': 252000,  # 4:12
                'is_playing': True
            },
            {
                'name': 'Almost Finished',
                'progress_ms': 165000,  # 2:45
                'duration_ms': 180000,  # 3:00
                'is_playing': True
            },
            {
                'name': 'Paused Song',
                'progress_ms': 154000,  # 2:34
                'duration_ms': 252000,  # 4:12
                'is_playing': False
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📱 Test {i}: {test_case['name']}")
            
            # Display on LCD
            progress_display.display_progress(
                test_case['progress_ms'],
                test_case['duration_ms'],
                test_case['is_playing']
            )
            
            # Show percentage for reference
            if test_case['duration_ms'] > 0:
                percent = (test_case['progress_ms'] / test_case['duration_ms']) * 100
                print(f"Progress: {percent:.1f}%")
            
            # Wait for user to see display
            input("Press Enter to continue to next test...")
        
        # Test "No Track" display
        print(f"\n📱 Test {len(test_cases)+1}: No Track Playing")
        progress_display.show_no_track()
        input("Press Enter to continue to live simulation...")
        
        # Simulate live progress update
        print(f"\n📱 Test {len(test_cases)+2}: Live Progress Simulation")
        print("   Simulating playback progress (10 seconds)...")
        print("   Press Ctrl+C to stop early")
        
        duration_ms = 252000  # 4:12 total
        start_progress = 154000  # Start at 2:34
        
        try:
            for i in range(20):  # 20 seconds of simulation
                current_progress = start_progress + (i * 1000)  # Add 1 second each iteration
                
                # Don't go past the end
                if current_progress >= duration_ms:
                    current_progress = duration_ms - 1000
                
                # Try to update - will only change LCD if progress bar changes
                lcd_updated = progress_display.display_progress(current_progress, duration_ms, True)
                
                # Show percentage
                percent = (current_progress / duration_ms) * 100
                if lcd_updated:
                    print(f"   >> New tick at {percent:.1f}% complete")
                
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n   Simulation stopped by user")
        
        # Clear LCD at end
        progress_display.raw_lcd.clear()
        progress_display.raw_lcd.cursor_pos = (0, 0)
        progress_display.raw_lcd.write_string("Test Complete!")
        progress_display.raw_lcd.cursor_pos = (1, 0)
        progress_display.raw_lcd.write_string("    Success!    ")
        
        print("\n✅ LCD Progress display test completed!")
        print("\n🔧 Ready for integration:")
        print("• Functions work with your LCD class")
        print("• Can add to display_manager.py")
        print("• Need to extract progress_ms + duration_ms from Spotify API")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        test_progress_on_lcd()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        # Clear LCD on exit
        try:
            raw_lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
            raw_lcd.clear()
            raw_lcd.close()
        except:
            pass
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        # Clear LCD on error
        try:
            raw_lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
            raw_lcd.clear()
            raw_lcd.close()
        except:
            pass
