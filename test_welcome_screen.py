#!/usr/bin/env python3
"""
Test welcome screen behavior without hardware
"""

import time
import app_state
from display_manager import get_display_content, has_significant_content_change
from display_effects import update_display_with_effects

class MockLCD:
    """Mock LCD for testing"""
    def __init__(self):
        self.display_lines = ["", ""]
        self.cleared = False
    
    def clear(self):
        self.display_lines = ["", ""]
        self.cleared = True
        print("🖥️  LCD cleared")
    
    class MockInnerLCD:
        def __init__(self, parent):
            self.parent = parent
            self._cursor_pos = (0, 0)
        
        @property
        def cursor_pos(self):
            return self._cursor_pos
            
        @cursor_pos.setter
        def cursor_pos(self, pos):
            self._cursor_pos = pos
        
        def write_string(self, text):
            line, col = self._cursor_pos
            if 0 <= line < 2:
                # Simulate writing to LCD
                if col == 0:  # Writing full line
                    self.parent.display_lines[line] = text.rstrip()
                    print(f"📺 LCD Line {line}: '{text.rstrip()}'")
    
    def __init__(self):
        self.display_lines = ["", ""]
        self.cleared = False
        self.lcd = self.MockInnerLCD(self)

def test_welcome_screen():
    print("🧪 Testing Welcome Screen Behavior")
    print("=" * 50)
    
    # Initialize mock LCD
    lcd = MockLCD()
    
    # Test 1: Welcome screen content
    print("\n1. Testing welcome screen content...")
    app_state.set_display_mode(0)  # welcome mode
    app_state.reset_display_state()
    
    line1, line2 = get_display_content()
    print(f"Welcome content: '{line1}' | '{line2}'")
    
    # Test 2: Content change detection
    print("\n2. Testing content change detection...")
    
    # First call should detect change
    change1 = has_significant_content_change(line1, line2)
    print(f"First change detection: {change1} (should be True)")
    
    # Update display state
    app_state.display_state['content_line1'] = line1
    app_state.display_state['content_line2'] = line2
    
    # Second call should not detect change
    change2 = has_significant_content_change(line1, line2)
    print(f"Second change detection: {change2} (should be False)")
    
    # Test 3: Simulate welcome display sequence
    print("\n3. Simulating welcome display sequence...")
    
    # Reset state for clean test
    app_state.set_display_mode(0)
    app_state.reset_display_state()
    lcd.clear()
    
    print("🌊 Starting welcome wave effect simulation...")
    welcome_start_time = time.time()
    welcome_shown = False
    iteration_count = 0
    
    while time.time() - welcome_start_time < 1.0:  # Shortened for test
        content_changed = update_display_with_effects(lcd)
        if content_changed and not welcome_shown:
            print("✨ Welcome message displayed on LCD")
            welcome_shown = True
        iteration_count += 1
        time.sleep(0.05)
    
    print(f"⏰ Welcome test completed after {iteration_count} iterations")
    print(f"Final LCD display:")
    print(f"  Line 0: '{lcd.display_lines[0]}'")
    print(f"  Line 1: '{lcd.display_lines[1]}'")
    
    # Test 4: Mode switching after welcome
    print("\n4. Testing mode switching after welcome...")
    
    # Simulate switching to now_playing
    app_state.set_display_mode(1)  # now_playing
    current_mode = app_state.get_current_mode()
    print(f"Switched to: {current_mode}")
    
    # Test button cycling (should skip welcome)
    print("\n5. Testing button cycling (should skip welcome)...")
    modes = []
    for i in range(4):
        mode = app_state.cycle_display_mode()
        modes.append(mode)
        print(f"Cycle {i+1}: {mode}")
    
    expected = ['clock', 'debug', 'now_playing', 'clock']
    if modes == expected:
        print("✅ Button cycling works correctly (skips welcome)")
    else:
        print(f"❌ Button cycling issue: expected {expected}, got {modes}")
    
    print("\n✅ Welcome screen test completed!")

if __name__ == "__main__":
    test_welcome_screen()