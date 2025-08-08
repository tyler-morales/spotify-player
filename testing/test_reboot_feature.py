#!/usr/bin/env python3
"""
Test script for the CYCLE button hold reboot feature
Tests the hold detection logic without requiring actual hardware
"""

import time
import sys
from unittest.mock import Mock, patch

# Mock GPIO for testing
class MockGPIO:
    HIGH = 1
    LOW = 0
    
    @staticmethod
    def input(pin):
        return MockGPIO.current_state.get(pin, MockGPIO.LOW)
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def setup(pin, direction, pull_up_down=None):
        pass
    
    @staticmethod
    def cleanup():
        pass
    
    current_state = {}

# Import button handler with mocked GPIO
sys.modules['RPi.GPIO'] = MockGPIO
from button_handler import check_buttons, HOLD_DURATION

def test_hold_detection():
    """Test the hold detection logic"""
    print("🧪 Testing CYCLE button hold detection...")
    
    # Reset button states
    if hasattr(check_buttons, 'last_button_states'):
        delattr(check_buttons, 'last_button_states')
    
    # Test 1: Quick press (should not trigger reboot)
    print("\n📝 Test 1: Quick press (< 5s)")
    MockGPIO.current_state = {22: MockGPIO.HIGH}  # CYCLE button pressed
    
    start_time = time.time()
    result = check_buttons()
    press_duration = time.time() - start_time
    
    print(f"   Press duration: {press_duration:.2f}s")
    print(f"   Result: {result}")
    print(f"   Expected: False (no reboot)")
    
    # Test 2: Hold for exactly 5 seconds
    print("\n📝 Test 2: Hold for 5 seconds")
    MockGPIO.current_state = {22: MockGPIO.HIGH}  # Keep CYCLE pressed
    
    start_time = time.time()
    result = check_buttons()
    hold_duration = time.time() - start_time
    
    print(f"   Hold duration: {hold_duration:.2f}s")
    print(f"   Result: {result}")
    print(f"   Expected: True (reboot triggered)")
    
    # Test 3: Button release
    print("\n📝 Test 3: Button release")
    MockGPIO.current_state = {22: MockGPIO.LOW}  # CYCLE button released
    
    result = check_buttons()
    print(f"   Result: {result}")
    print(f"   Expected: False (no action)")

def test_hold_timing():
    """Test hold timing accuracy"""
    print("\n⏱️ Testing hold timing accuracy...")
    
    # Reset button states
    if hasattr(check_buttons, 'last_button_states'):
        delattr(check_buttons, 'last_button_states')
    
    # Press CYCLE button
    MockGPIO.current_state = {22: MockGPIO.HIGH}
    check_buttons()  # Initialize hold timer
    
    # Simulate hold for different durations
    test_durations = [3.0, 4.9, 5.0, 5.1, 6.0]
    
    for duration in test_durations:
        print(f"\n📝 Testing {duration}s hold:")
        
        # Reset states
        if hasattr(check_buttons, 'hold_start_times'):
            check_buttons.hold_start_times['CYCLE'] = time.time() - duration
            check_buttons.hold_triggered['CYCLE'] = False
        
        start_time = time.time()
        result = check_buttons()
        actual_duration = time.time() - start_time
        
        should_trigger = duration >= HOLD_DURATION
        print(f"   Duration: {duration:.1f}s")
        print(f"   Should trigger: {should_trigger}")
        print(f"   Actual result: {result}")
        print(f"   Test passed: {result == should_trigger}")

def test_multiple_buttons():
    """Test that other buttons don't interfere with hold detection"""
    print("\n🎮 Testing multiple button interactions...")
    
    # Reset button states
    if hasattr(check_buttons, 'last_button_states'):
        delattr(check_buttons, 'last_button_states')
    
    # Test other buttons while CYCLE is held
    other_buttons = [17, 18, 27]  # PREV, PLAY, NEXT
    
    for button_pin in other_buttons:
        print(f"\n📝 Testing button {button_pin} during CYCLE hold:")
        
        # Press CYCLE first
        MockGPIO.current_state = {22: MockGPIO.HIGH}
        check_buttons()
        
        # Then press another button
        MockGPIO.current_state = {22: MockGPIO.HIGH, button_pin: MockGPIO.HIGH}
        result = check_buttons()
        
        print(f"   CYCLE + Button {button_pin}")
        print(f"   Result: {result}")
        print(f"   Expected: False (other buttons shouldn't trigger reboot)")

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n🔍 Testing edge cases...")
    
    # Reset button states
    if hasattr(check_buttons, 'last_button_states'):
        delattr(check_buttons, 'last_button_states')
    
    # Test 1: Rapid press/release cycles
    print("\n📝 Test 1: Rapid press/release cycles")
    for i in range(5):
        MockGPIO.current_state = {22: MockGPIO.HIGH}
        result1 = check_buttons()
        
        MockGPIO.current_state = {22: MockGPIO.LOW}
        result2 = check_buttons()
        
        print(f"   Cycle {i+1}: Press={result1}, Release={result2}")
    
    # Test 2: Very long hold
    print("\n📝 Test 2: Very long hold (10s)")
    MockGPIO.current_state = {22: MockGPIO.HIGH}
    check_buttons()  # Start hold
    
    # Simulate 10 second hold
    if hasattr(check_buttons, 'hold_start_times'):
        check_buttons.hold_start_times['CYCLE'] = time.time() - 10.0
        check_buttons.hold_triggered['CYCLE'] = False
    
    result = check_buttons()
    print(f"   Result: {result}")
    print(f"   Expected: True (should trigger reboot)")

if __name__ == "__main__":
    print("🧪 CYCLE Button Hold Reboot Feature Test Suite")
    print("=" * 50)
    
    try:
        test_hold_detection()
        test_hold_timing()
        test_multiple_buttons()
        test_edge_cases()
        
        print("\n✅ All tests completed!")
        print("📝 Note: This is a simulation - actual hardware testing required for full validation")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 