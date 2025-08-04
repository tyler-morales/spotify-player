"""
Button Handler Module
Manages GPIO button configuration and event handling
"""

import time
import RPi.GPIO as GPIO
import app_state
import os
import sys

# 4-Button configuration
BUTTON_PINS = {
    'PREV': 17,     # Previous Track
    'PLAY': 18,     # Play/Pause 
    'NEXT': 27,     # Next Track
    'CYCLE': 22,    # Display Cycle
}
DEBOUNCE = 0.3
HOLD_DURATION = 5.0  # 5 seconds for reboot

def setup_buttons():
    """Initialize GPIO for buttons"""
    GPIO.setmode(GPIO.BCM)
    for pin in BUTTON_PINS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def handle_prev_button():
    """Handle previous track button press"""
    from spotify_manager import get_spotify_manager
    spotify = get_spotify_manager()
    spotify.previous_track()
    
    # Auto-wake: switch to now_playing when playback buttons pressed
    if app_state.get_current_mode() != 'now_playing':
        print("🎵 Auto-wake: Playback button pressed, switching to now_playing")
        app_state.set_display_mode(app_state.DISPLAY_MODES.index('now_playing'))
    
    time.sleep(1)  # Give Spotify time to change track
    new_track = spotify.get_current_track(force_refresh=True)
    if spotify.has_track_changed(app_state.current_track, new_track):
        app_state.current_track = new_track
    
    app_state.music_state['is_playing'] = True
    app_state.music_state['last_playing_time'] = time.time()
    app_state.music_state['stopped_duration'] = 0

def handle_play_button():
    """Handle play/pause button press"""
    from spotify_manager import get_spotify_manager
    spotify = get_spotify_manager()
    spotify.play_pause()
    
    # Auto-wake: switch to now_playing when playback buttons pressed
    if app_state.get_current_mode() != 'now_playing':
        print("🎵 Auto-wake: Play/Pause pressed, switching to now_playing")
        app_state.set_display_mode(app_state.DISPLAY_MODES.index('now_playing'))
    
    # Update music state
    app_state.music_state['is_playing'] = not app_state.music_state['is_playing']  # Toggle
    if app_state.music_state['is_playing']:
        app_state.music_state['last_playing_time'] = time.time()
        app_state.music_state['stopped_duration'] = 0
    
    print(f"⏯️  Play/Pause - Music {'playing' if app_state.music_state['is_playing'] else 'paused'}")

def handle_next_button():
    """Handle next track button press"""
    from spotify_manager import get_spotify_manager
    spotify = get_spotify_manager()
    spotify.next_track()
    
    # Auto-wake: switch to now_playing when playback buttons pressed
    if app_state.get_current_mode() != 'now_playing':
        print("🎵 Auto-wake: Playback button pressed, switching to now_playing")
        app_state.set_display_mode(app_state.DISPLAY_MODES.index('now_playing'))
    
    time.sleep(1)  # Give Spotify time to change track
    new_track = spotify.get_current_track(force_refresh=True)
    if spotify.has_track_changed(app_state.current_track, new_track):
        app_state.current_track = new_track
    
    app_state.music_state['is_playing'] = True
    app_state.music_state['last_playing_time'] = time.time()
    app_state.music_state['stopped_duration'] = 0

def handle_cycle_button():
    """Handle display cycle button press"""
    from spotify_manager import get_spotify_manager
    spotify = get_spotify_manager()
    mode_name = app_state.cycle_display_mode()
    print(f"🔄 Display mode: {mode_name}")
    
    # Auto-wake: if we cycle to now_playing and music is playing, reset sleep timer
    if app_state.get_current_mode() == 'now_playing':
        app_state.current_track = spotify.get_current_track(force_refresh=True)
        if app_state.current_track and app_state.current_track.get('is_playing', False):
            print("🎵 Auto-wake: Switched to now_playing with active music")
            app_state.music_state['is_playing'] = True
            app_state.music_state['last_playing_time'] = time.time()
            app_state.music_state['stopped_duration'] = 0

def handle_cycle_hold():
    """Handle 5-second hold on CYCLE button for reboot"""
    print("🔄 CYCLE button held for 5 seconds - initiating reboot...")
    
    # Clear display to show reboot status
    from lcd import LCD
    try:
        lcd = LCD()
        lcd.clear()
        lcd.write_line("Rebooting...", 0)
        lcd.write_line("Please wait...", 1)
    except Exception as e:
        print(f"LCD error during reboot: {e}")
    
    # Clean up GPIO
    try:
        GPIO.cleanup()
    except Exception as e:
        print(f"GPIO cleanup error: {e}")
    
    print("🔄 Restarting Spotify Player...")
    
    # Restart the program
    try:
        os.execv(sys.executable, ['python3'] + sys.argv)
    except Exception as e:
        print(f"Restart failed: {e}")
        print("Please restart manually")
        sys.exit(1)


# Button action mapping
BUTTON_HANDLERS = {
    'PREV': handle_prev_button,
    'PLAY': handle_play_button,
    'NEXT': handle_next_button,
    'CYCLE': handle_cycle_button,
}

def check_buttons():
    """Check button states and handle presses - returns True if any button was pressed"""
    button_pressed = False
    
    # Initialize button states and hold tracking if not exists
    if not hasattr(check_buttons, 'last_button_states'):
        check_buttons.last_button_states = {name: GPIO.LOW for name in BUTTON_PINS}
        check_buttons.hold_start_times = {name: None for name in BUTTON_PINS}
        check_buttons.hold_triggered = {name: False for name in BUTTON_PINS}
    
    current_time = time.time()
    
    for name, pin in BUTTON_PINS.items():
        state = GPIO.input(pin)
        
        # Button press detection (rising edge)
        if state == GPIO.HIGH and check_buttons.last_button_states[name] == GPIO.LOW:
            print(f"🎮 Button {name} pressed!")
            
            # Start hold timer for CYCLE button
            if name == 'CYCLE':
                check_buttons.hold_start_times[name] = current_time
                check_buttons.hold_triggered[name] = False
            
            # Handle immediate button action (for non-hold buttons)
            if name in BUTTON_HANDLERS and name != 'CYCLE':
                BUTTON_HANDLERS[name]()
            
            time.sleep(DEBOUNCE)  # Debounce
            button_pressed = True
        
        # Button release detection (falling edge)
        elif state == GPIO.LOW and check_buttons.last_button_states[name] == GPIO.HIGH:
            # Reset hold tracking for CYCLE button
            if name == 'CYCLE':
                check_buttons.hold_start_times[name] = None
                check_buttons.hold_triggered[name] = False
                
                # If we didn't trigger hold, do normal cycle action
                if not check_buttons.hold_triggered[name]:
                    if name in BUTTON_HANDLERS:
                        BUTTON_HANDLERS[name]()
        
        # Hold detection for CYCLE button
        elif state == GPIO.HIGH and name == 'CYCLE' and check_buttons.hold_start_times[name]:
            hold_duration = current_time - check_buttons.hold_start_times[name]
            
            # Check if hold duration reached and not already triggered
            if hold_duration >= HOLD_DURATION and not check_buttons.hold_triggered[name]:
                check_buttons.hold_triggered[name] = True
                handle_cycle_hold()
                return True  # Exit immediately for reboot
        
        check_buttons.last_button_states[name] = state
    
    return button_pressed