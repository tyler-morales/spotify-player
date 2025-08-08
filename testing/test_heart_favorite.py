#!/usr/bin/env python3
"""
Heart Favorite Animation Test
Animates a heart rising from bottom to top when GPIO pin 17 is pressed (favorite song)
"""

from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import threading

class HeartFavoriteDisplay:
    def __init__(self, heart_button_pin=17):
        """Initialize LCD and GPIO for heart favorite animation"""
        try:
            self.lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
            self.heart_button_pin = heart_button_pin
            self.heart_chars_loaded = False
            self.animation_running = False
            self.current_song = "Test Song - Artist"
            
            # Setup GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.heart_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            print("💖 Heart Favorite Animation Display initialized")
            print(f"   Heart button on GPIO pin {heart_button_pin}")
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            raise
    
    def setup_heart_characters(self):
        """Setup custom characters for heart animation frames"""
        if self.heart_chars_loaded:
            return
        
        # Heart at different vertical positions and sizes
        # Character 0: Empty space
        empty = [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000
        ]
        
        # Character 1: Small heart at bottom
        heart_bottom_small = [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b01010,
            0b01110,
            0b00100
        ]
        
        # Character 2: Heart rising (bottom half)
        heart_bottom = [
            0b00000,
            0b00000,
            0b00000,
            0b01010,
            0b11111,
            0b11111,
            0b01110,
            0b00100
        ]
        
        # Character 3: Heart in middle
        heart_middle = [
            0b00000,
            0b01010,
            0b11111,
            0b11111,
            0b11111,
            0b01110,
            0b00100,
            0b00000
        ]
        
        # Character 4: Heart at top
        heart_top = [
            0b01010,
            0b11111,
            0b11111,
            0b11111,
            0b01110,
            0b00100,
            0b00000,
            0b00000
        ]
        
        # Character 5: Heart "floating above" (top portion)
        heart_above = [
            0b01010,
            0b11111,
            0b01110,
            0b00100,
            0b00000,
            0b00000,
            0b00000,
            0b00000
        ]
        
        # Character 6: Sparkling heart (with sparkles)
        heart_sparkle = [
            0b10001,
            0b01010,
            0b11111,
            0b11111,
            0b01110,
            0b10100,
            0b00000,
            0b00001
        ]
        
        # Character 7: Fading heart
        heart_fade = [
            0b00000,
            0b01010,
            0b10101,
            0b10101,
            0b01010,
            0b00100,
            0b00000,
            0b00000
        ]
        
        # Load all heart animation frames
        heart_frames = [empty, heart_bottom_small, heart_bottom, heart_middle, 
                       heart_top, heart_above, heart_sparkle, heart_fade]
        
        for i, frame in enumerate(heart_frames):
            self.lcd.create_char(i, frame)
        
        self.heart_chars_loaded = True
        print("💖 Heart animation characters loaded!")
    
    def animate_multiple_hearts_rising(self, num_hearts=5):
        """Animate multiple hearts rising and floating at different positions"""
        if self.animation_running:
            return  # Prevent multiple animations
        
        self.animation_running = True
        
        try:
            print(f"💖 Multiple hearts rising animation ({num_hearts} hearts)!")
            
            # Save current display content
            original_line1 = self.current_song[:16].ljust(16)
            original_line2 = "♪ Now Playing ♪ ".center(16)
            
            # Create multiple hearts at different positions and phases
            import random
            hearts = []
            for i in range(num_hearts):
                heart = {
                    'position': random.randint(2, 13),  # Random horizontal position
                    'phase': 0,  # Current animation phase
                    'delay': i * 3,  # Stagger start times
                    'active': False
                }
                hearts.append(heart)
            
            # Animation sequence phases for each heart
            heart_phases = [0, 1, 2, 3, 4, 5, 6, 7, 5, 6, 5, 0]  # Include floating effect
            
            # Run animation for enough frames to show all hearts
            total_frames = max(len(heart_phases) + h['delay'] for h in hearts) + 10
            
            for frame in range(total_frames):
                # Clear display
                self.lcd.clear()
                
                # Start with original content
                display_line1 = list(original_line1)
                display_line2 = list(original_line2)
                
                # Update each heart
                for heart in hearts:
                    # Check if this heart should start
                    if frame >= heart['delay'] and not heart['active']:
                        heart['active'] = True
                        heart['phase'] = 0
                    
                    # Animate active hearts
                    if heart['active'] and heart['phase'] < len(heart_phases):
                        char_code = heart_phases[heart['phase']]
                        pos = heart['position']
                        
                        if char_code > 0 and pos < 16:  # Valid character and position
                            # Determine which line to place heart based on phase
                            if char_code in [5, 6]:  # "above" and sparkle phases
                                # Place on top line for "floating above" effect
                                if pos < len(display_line1):
                                    display_line1[pos] = chr(char_code)
                            elif char_code in [1, 2, 3, 4]:  # Rising phases
                                # Place on bottom line
                                if pos < len(display_line2):
                                    display_line2[pos] = chr(char_code)
                        
                        # Advance heart phase
                        heart['phase'] += 1
                
                # Update LCD with all hearts
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(''.join(display_line1))
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(''.join(display_line2))
                
                print(f"   Frame {frame}: Active hearts: {sum(1 for h in hearts if h['active'])}")
                time.sleep(0.2)  # Animation speed
            
            # Sparkle finale - all hearts sparkle together
            print("💖 Sparkle finale!")
            for sparkle_frame in range(6):
                self.lcd.clear()
                display_line1 = list(original_line1)
                
                # Add sparkle hearts at all positions
                for heart in hearts:
                    pos = heart['position']
                    if pos < len(display_line1):
                        sparkle_char = 6 if sparkle_frame % 2 == 0 else 7  # Alternate sparkle/fade
                        display_line1[pos] = chr(sparkle_char)
                
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(''.join(display_line1))
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string("💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖💖")
                
                time.sleep(0.3)
            
            # Flash "FAVORITED!" message
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string("   FAVORITED!   ")
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string("💖 Song Loved! 💖".center(16))
            time.sleep(2)
            
            # Restore original display
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(original_line1)
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(original_line2)
            
        except Exception as e:
            print(f"❌ Animation error: {e}")
        finally:
            self.animation_running = False
    
    def animate_heart_rising(self, position=8):
        """Single heart animation (keeping for compatibility)"""
        self.animate_multiple_hearts_rising(1)
    
    def check_heart_button(self):
        """Check if heart/favorite button is pressed"""
        return GPIO.input(self.heart_button_pin) == GPIO.HIGH
    
    def monitor_heart_button(self):
        """Monitor heart button for presses (blocking)"""
        print("💖 Monitoring heart button... Press to favorite!")
        print("   Press Ctrl+C to stop")
        
        last_state = GPIO.LOW
        
        try:
            while True:
                current_state = GPIO.input(self.heart_button_pin)
                
                # Detect rising edge (button press)
                if current_state == GPIO.HIGH and last_state == GPIO.LOW:
                    print("💖 HEART BUTTON PRESSED!")
                    
                    # Animate heart at random positions for variety
                    import random
                    heart_position = random.randint(4, 12)  # Random position on display
                    
                    # Run multiple hearts animation in separate thread
                    animation_thread = threading.Thread(
                        target=self.animate_multiple_hearts_rising, 
                        args=(5,)  # 5 hearts
                    )
                    animation_thread.daemon = True
                    animation_thread.start()
                    
                    time.sleep(0.3)  # Debounce
                
                last_state = current_state
                time.sleep(0.01)  # Small delay for responsiveness
                
        except KeyboardInterrupt:
            print("\n💖 Heart monitoring stopped")
    
    def demo_heart_animation(self):
        """Demo the heart animation without button"""
        print("💖 Demonstrating multiple hearts animation sequence...")
        
        # Show different numbers of hearts
        heart_counts = [3, 5, 8]  # Different amounts of hearts
        
        for i, count in enumerate(heart_counts):
            print(f"\n💖 Demo {i+1}: {count} floating hearts")
            self.animate_multiple_hearts_rising(count)
            time.sleep(1)
    
    def test_heart_characters(self):
        """Test each heart character individually"""
        print("💖 Testing individual heart characters...")
        
        char_names = ["Empty", "Small Bottom", "Bottom", "Middle", 
                     "Top", "Above", "Sparkle", "Fade"]
        
        for i, name in enumerate(char_names):
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(f"Char {i}: {name}")
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(chr(i) * 8 + "        ")
            
            print(f"Showing: {name}")
            time.sleep(1.5)
    
    def simulate_now_playing(self):
        """Simulate a now playing display with heart functionality"""
        print("💖 Simulating now playing with heart favorite...")
        
        # Sample songs
        songs = [
            "Bohemian Rhapsody - Queen",
            "Stairway Heaven - Led Zep",
            "Hotel California - Eagles",
            "Sweet Child O Mine - GNR",
            "Imagine - John Lennon"
        ]
        
        for i, song in enumerate(songs):
            self.current_song = song
            
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(song[:16].ljust(16))
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string("Press ❤ to fave!".center(16))
            
            print(f"\n🎵 Now Playing: {song}")
            print("   Press heart button to favorite!")
            
            # Monitor for 10 seconds or until button pressed
            start_time = time.time()
            last_button_state = GPIO.LOW
            
            while (time.time() - start_time) < 10:
                current_button_state = GPIO.input(self.heart_button_pin)
                
                if current_button_state == GPIO.HIGH and last_button_state == GPIO.LOW:
                    print("💖 Song favorited!")
                    self.animate_multiple_hearts_rising(5)  # 5 hearts
                    break
                
                last_button_state = current_button_state
                time.sleep(0.1)
    
    def cleanup(self):
        """Clean up GPIO and LCD"""
        try:
            GPIO.cleanup()
            self.lcd.clear()
            self.lcd.close()
        except:
            pass

def main():
    """Main heart favorite test menu"""
    print("💖 Heart Favorite Animation Test Suite")
    print("=" * 50)
    
    heart_display = HeartFavoriteDisplay()
    
    # Setup heart characters
    print("💖 Setting up heart animation characters...")
    heart_display.setup_heart_characters()
    
    tests = [
        ("1", "Test Heart Characters", heart_display.test_heart_characters),
        ("2", "Demo Heart Animation", heart_display.demo_heart_animation),
        ("3", "Monitor Heart Button", heart_display.monitor_heart_button),
        ("4", "Simulate Now Playing", heart_display.simulate_now_playing),
        ("5", "Run All Tests", None),
    ]
    
    print("\nAvailable tests:")
    for key, name, func in tests:
        print(f"{key}) {name}")
    
    choice = input(f"\nChoose test (1-5) [GPIO {heart_display.heart_button_pin} = heart button]: ").strip()
    
    try:
        if choice == "5":
            # Run all tests
            for key, name, func in tests[:-1]:  # Exclude "Run All"
                if func:
                    print(f"\n💖 Running: {name}")
                    if name == "Monitor Heart Button":
                        print("   (Skipping interactive test in batch mode)")
                        continue
                    func()
                    time.sleep(1)
        else:
            # Run specific test
            for key, name, func in tests:
                if choice == key and func:
                    print(f"\n💖 Running: {name}")
                    func()
                    break
            else:
                print("Invalid choice")
        
        print("\n💖 Heart animation test complete!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        heart_display.cleanup()

if __name__ == "__main__":
    main()