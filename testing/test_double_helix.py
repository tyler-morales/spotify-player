#!/usr/bin/env python3
"""
Double Helix Animation Test
Creates a spinning DNA double helix animation using custom LCD characters
"""

from RPLCD.i2c import CharLCD
import time
import math

class DoubleHelixDisplay:
    def __init__(self):
        """Initialize LCD for double helix animation"""
        try:
            self.lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)
            self.helix_chars_loaded = False
            print("🧬 DNA Double Helix Animation Display initialized")
        except Exception as e:
            print(f"❌ LCD initialization failed: {e}")
            raise
    
    def setup_helix_characters(self):
        """Setup 8 custom characters for smooth helix rotation"""
        if self.helix_chars_loaded:
            return
        
        # Each character represents the helix at a different rotation phase (0-7)
        # Two intertwining helical strands with 45-degree phase steps
        helix_phases = []
        
        for phase in range(8):
            char_pattern = [0b00000] * 8  # Start with empty 5x8 grid
            
            # Calculate helix positions for this phase
            for row in range(8):
                # Normalize row to 0-1 for mathematical calculations
                row_pos = row / 7.0
                
                # Calculate helix angles (add phase offset)
                angle1 = (row_pos * 4 * math.pi) + (phase * math.pi / 4)  # First strand
                angle2 = angle1 + math.pi  # Second strand (180° offset)
                
                # Convert angles to x positions (0-4 for 5-pixel width)
                # Use sine wave mapped to pixel positions
                x1 = int(2 + 1.5 * math.sin(angle1))  # Range: 0.5 to 3.5 -> 0 to 4
                x2 = int(2 + 1.5 * math.sin(angle2))  # Range: 0.5 to 3.5 -> 0 to 4
                
                # Clamp to valid pixel positions (0-4)
                x1 = max(0, min(4, x1))
                x2 = max(0, min(4, x2))
                
                # Set the bits for both strands (avoid overlap by checking positions)
                if x1 == x2:
                    # If they would overlap, offset one slightly or make it brighter
                    char_pattern[row] |= (1 << (4 - x1))
                else:
                    # Set both strand positions
                    char_pattern[row] |= (1 << (4 - x1))
                    char_pattern[row] |= (1 << (4 - x2))
            
            helix_phases.append(char_pattern)
        
        # Create all 8 helix phase characters
        for i, pattern in enumerate(helix_phases):
            self.lcd.create_char(i, pattern)
        
        self.helix_chars_loaded = True
        print("🧬 Double helix character phases loaded!")
        
        # Debug: print the patterns
        for i, pattern in enumerate(helix_phases):
            print(f"Phase {i}:")
            for row in pattern:
                binary_str = format(row, '05b').replace('0', '·').replace('1', '█')
                print(f"  {binary_str}")
    
    def animate_helix(self, duration_seconds=10, speed=0.2):
        """Animate the double helix spinning"""
        print(f"🧬 Starting double helix animation for {duration_seconds} seconds...")
        
        start_time = time.time()
        phase = 0
        
        try:
            while (time.time() - start_time) < duration_seconds:
                # Clear and show current helix phase
                self.lcd.clear()
                
                # Fill both lines with the current helix phase
                helix_line = chr(phase) * 16
                
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(helix_line)
                self.lcd.cursor_pos = (1, 0) 
                self.lcd.write_string(helix_line)
                
                # Move to next phase
                phase = (phase + 1) % 8
                
                # Show phase info
                elapsed = time.time() - start_time
                print(f"Phase {phase}, Time: {elapsed:.1f}s")
                
                time.sleep(speed)
                
        except KeyboardInterrupt:
            print("\n🧬 Helix animation stopped by user")
    
    def animate_traveling_helix(self, duration_seconds=15, speed=0.15):
        """Animate helix that travels across the screen"""
        print(f"🧬 Starting traveling double helix animation...")
        
        start_time = time.time()
        position = 0
        phase = 0
        
        try:
            while (time.time() - start_time) < duration_seconds:
                self.lcd.clear()
                
                # Create a helix that moves across the screen
                line1 = " " * 16
                line2 = " " * 16
                
                # Place helix characters at different positions
                for i in range(3):  # 3 helix segments
                    pos = (position + i * 4) % 20  # Wrap around with offset
                    if 0 <= pos < 16:
                        helix_char = chr((phase + i) % 8)
                        line1 = line1[:pos] + helix_char + line1[pos+1:]
                        line2 = line2[:pos] + helix_char + line2[pos+1:]
                
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(line1)
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(line2)
                
                # Update position and phase
                position = (position + 1) % 20
                phase = (phase + 1) % 8
                
                elapsed = time.time() - start_time
                print(f"Pos: {position}, Phase: {phase}, Time: {elapsed:.1f}s")
                
                time.sleep(speed)
                
        except KeyboardInterrupt:
            print("\n🧬 Traveling helix stopped by user")
    
    def demo_helix_phases(self):
        """Demo showing each helix phase individually"""
        print("🧬 Demonstrating each helix phase...")
        
        for phase in range(8):
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(f"Phase {phase}:      ")
            self.lcd.cursor_pos = (1, 0)
            self.lcd.write_string(chr(phase) * 8 + "        ")
            
            print(f"Showing Phase {phase}")
            time.sleep(1.5)
    
    def create_dna_text_effect(self):
        """Create DNA text with helix backgrounds"""
        print("🧬 DNA Text Effect...")
        
        messages = [
            ("  DNA PLAYER   ", "🧬 DNA Music Player"),
            ("   SPOTIFY     ", "🎵 Spotify DNA Mode"),
            ("  DOUBLE HELIX ", "🧬 Double Helix Viz"),
            ("   GENETIC     ", "🧬 Genetic Beats"),
        ]
        
        for text, description in messages:
            print(f"Showing: {description}")
            
            # Animate background while showing text
            for i in range(16):  # 16 animation frames
                self.lcd.clear()
                
                # Text on top line
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(text)
                
                # Animated helix on bottom line
                phase = i % 8
                helix_bg = chr(phase) * 16
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(helix_bg)
                
                time.sleep(0.1)
            
            time.sleep(1)
    
    def cleanup(self):
        """Clean up LCD display"""
        try:
            self.lcd.clear()
            self.lcd.close()
        except:
            pass

def main():
    """Main double helix test menu"""
    print("🧬 Double Helix DNA Animation Test Suite")
    print("=" * 50)
    
    helix_display = DoubleHelixDisplay()
    
    # Setup the helix characters
    print("🧬 Setting up double helix character phases...")
    helix_display.setup_helix_characters()
    
    tests = [
        ("1", "Demo Individual Phases", helix_display.demo_helix_phases),
        ("2", "Spinning Helix (10s)", lambda: helix_display.animate_helix(10, 0.2)),
        ("3", "Fast Spinning Helix (15s)", lambda: helix_display.animate_helix(15, 0.1)),
        ("4", "Traveling Helix (15s)", lambda: helix_display.animate_traveling_helix(15, 0.15)),
        ("5", "DNA Text Effects", helix_display.create_dna_text_effect),
        ("6", "Run All Animations", None),
    ]
    
    print("\nAvailable animations:")
    for key, name, func in tests:
        print(f"{key}) {name}")
    
    choice = input("\nChoose animation (1-6): ").strip()
    
    try:
        if choice == "6":
            # Run all animations
            for key, name, func in tests[:-1]:  # Exclude "Run All"
                if func:
                    print(f"\n🧬 Running: {name}")
                    func()
                    time.sleep(1)
        else:
            # Run specific animation
            for key, name, func in tests:
                if choice == key and func:
                    print(f"\n🧬 Running: {name}")
                    func()
                    break
            else:
                print("Invalid choice")
        
        print("\n🧬 Animation complete!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Animation interrupted by user")
    except Exception as e:
        print(f"\n❌ Animation failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        helix_display.cleanup()

if __name__ == "__main__":
    main()