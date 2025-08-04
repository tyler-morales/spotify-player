#!/usr/bin/env python3
"""
Spotify Player with LCD Display and Smart API Rate Limiting
Event-driven updates with minimal API calls

Modularized version with clean separation of concerns:
- app_state: Global state management
- button_handler: Button GPIO and event handling  
- display_manager: Display content generation
- display_effects: Complex animations and scrolling
- background_tasks: Background monitoring thread
"""

import time
import RPi.GPIO as GPIO
from spotify_manager import get_spotify_manager
from lcd import LCD
from japanese_processor import get_japanese_processor

# Import modularized components
import app_state
from button_handler import setup_buttons, check_buttons
from display_effects import update_display_with_effects
from background_tasks import start_background_monitoring

def main():
    print("🎵 Starting Smart Spotify LCD Player with 4 Buttons...")
    print("🎮 PREV (GPIO17) | PLAY (GPIO18) | NEXT (GPIO27) | CYCLE (GPIO22)")
    print("🧠 Single-threaded with pendulum scrolling - no LCD corruption!")
    print("💤 Smart sleep: Auto-switches to clock after 30s of no music")
    print("🌅 Auto-wake: Returns to now_playing when music resumes or buttons pressed")
    print("📦 Modularized architecture for better maintainability")
    
    # Initialize components
    spotify = get_spotify_manager()
    lcd = LCD()
    japanese_proc = get_japanese_processor()
    
    # Initialize Japanese processor availability
    app_state.set_japanese_processor_availability(japanese_proc.is_available())
    if japanese_proc.is_available():
        print("🈳 Japanese romanization enabled")
    else:
        print("⚠️ Japanese romanization unavailable (pykakasi not installed)")
    
    if not spotify.is_authenticated():
        print("❌ Spotify not authenticated! Run: python3 auth.py")
        return
    
    setup_buttons()
    
    # Start background thread for external device detection
    bg_thread = start_background_monitoring()
    
    # Get initial track info
    app_state.current_track = spotify.get_current_track(force_refresh=True)
    
    print("✅ Ready! No more LCD corruption or threading issues.")
    print(f"📊 API calls this session: {spotify.get_api_call_count()}")
    
    try:
        lcd.clear()
        
        while True:
            # Check buttons (event-driven API calls)
            button_pressed = check_buttons()
            
            # Single-threaded display update - no corruption possible!
            content_changed = update_display_with_effects(lcd)
            if content_changed and app_state.get_current_mode() == 'now_playing':
                print(f"📊 Total API calls: {spotify.get_api_call_count()}")
            
            time.sleep(0.05)  # Responsive checking
            
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye! Total API calls this session: {spotify.get_api_call_count()}")
        lcd.clear()
        GPIO.cleanup()

if __name__ == "__main__":
    main()