#!/usr/bin/env python3
"""
Spotify Player with LCD Display and Smart API Rate Limiting
Event-driven updates with minimal API calls
"""

import time
import os
import threading
import RPi.GPIO as GPIO
from spotify_manager import get_spotify_manager
from lcd import LCD

# 4-Button configuration
BUTTON_PINS = {
    'PREV': 17,     # Previous Track (your current button)
    'PLAY': 18,     # Play/Pause 
    'NEXT': 27,     # Next Track
    'CYCLE': 22,    # Display Cycle
}
DEBOUNCE = 0.3

# Display modes
DISPLAY_MODES = ['now_playing', 'clock', 'debug']
current_display_mode = 0

# Global state
track_changed = False
current_track = None
music_state = {
    'is_playing': False,
    'last_playing_time': 0,
    'stopped_duration': 0,
    'auto_sleep_threshold': 30  # seconds
}
display_state = {
    'mode': 0,
    'content_line1': '',
    'content_line2': '',
    'scroll_pos1': 0,
    'scroll_pos2': 0,
    'scroll_dir1': 1,
    'scroll_dir2': 1,
    'pause_until1': 0,
    'pause_until2': 0,
    'last_update': 0,
    'wave_complete': False
}

def setup_buttons():
    """Initialize GPIO for buttons"""
    GPIO.setmode(GPIO.BCM)
    for pin in BUTTON_PINS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def check_for_track_changes():
    """Smart background thread - only polls when on now_playing display"""
    global current_track, current_display_mode, music_state
    spotify = get_spotify_manager()
    
    while True:
        try:
            # Only poll API when on now_playing display
            if DISPLAY_MODES[current_display_mode] == 'now_playing':
                new_track = spotify.get_current_track()
                
                # Track music playback state
                is_currently_playing = new_track and new_track.get('is_playing', False)
                
                if is_currently_playing != music_state['is_playing']:
                    music_state['is_playing'] = is_currently_playing
                    if is_currently_playing:
                        print("🎵 Music resumed - staying on now_playing")
                        music_state['last_playing_time'] = time.time()
                        music_state['stopped_duration'] = 0
                    else:
                        print("⏸️  Music paused/stopped - starting sleep timer")
                        music_state['stopped_duration'] = 0
                
                # Check for track changes
                if spotify.has_track_changed(current_track, new_track):
                    print(f"🔄 Track change: {new_track['title']} - {new_track['artist']}")
                    current_track = new_track
                    music_state['last_playing_time'] = time.time()
                
                # Auto-sleep logic: switch to clock if music stopped for too long
                if not is_currently_playing:
                    music_state['stopped_duration'] = time.time() - music_state['last_playing_time']
                    if music_state['stopped_duration'] > music_state['auto_sleep_threshold']:
                        print(f"😴 Auto-sleep: Music stopped for {music_state['stopped_duration']:.0f}s, switching to clock")
                        current_display_mode = DISPLAY_MODES.index('clock')
                        music_state['stopped_duration'] = 0  # Reset to avoid repeated switches
                
                time.sleep(8)  # Poll every 8 seconds when on now_playing
            else:
                # Not on now_playing display - sleep longer, no API calls
                print(f"💤 Sleeping - on {DISPLAY_MODES[current_display_mode]} display, no API polling")
                time.sleep(30)  # Much longer sleep when not on now_playing
            
        except Exception as e:
            print(f"Background check error: {e}")
            time.sleep(10)

def get_display_content():
    """Get content based on current display mode"""
    global current_display_mode, current_track
    
    mode = DISPLAY_MODES[current_display_mode]
    
    if mode == 'now_playing':
        if current_track:
            return current_track['title'], current_track['artist']
        return "No track", "Connect Spotify"
    
    elif mode == 'clock':
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%H:%M:%S"), now.strftime("%a %b %d")
    
    elif mode == 'debug':
        spotify = get_spotify_manager()
        api_calls = spotify.get_api_call_count()
        if music_state['is_playing']:
            status = "Playing"
        elif music_state['stopped_duration'] > 0:
            remaining = music_state['auto_sleep_threshold'] - music_state['stopped_duration']
            status = f"Sleep in {remaining:.0f}s" if remaining > 0 else "Sleeping"
        else:
            status = "Ready"
        return f"API: {api_calls} | {status}", f"Mode: {mode}"
    
    return "Unknown", "Mode"

def cycle_display():
    """Cycle to next display mode"""
    global current_display_mode, display_state
    
    current_display_mode = (current_display_mode + 1) % len(DISPLAY_MODES)
    mode_name = DISPLAY_MODES[current_display_mode]
    print(f"🔄 Display mode: {mode_name}")
    
    # Reset display state for new mode
    display_state.update({
        'scroll_pos1': 0,
        'scroll_pos2': 0,
        'scroll_dir1': 1,
        'scroll_dir2': 1,
        'pause_until1': 0,
        'pause_until2': 0,
        'wave_complete': False
    })

def update_display_content(lcd):
    """Non-blocking display update with pendulum scrolling"""
    global display_state, current_display_mode
    
    line1, line2 = get_display_content()
    
    # For clock/debug modes, don't restart wave effect on every second change
    mode = DISPLAY_MODES[current_display_mode]
    significant_change = True
    
    if mode in ['clock', 'debug']:
        # Only restart wave effect on major changes, not every second
        old_line1_base = display_state['content_line1'].split(':')[0] if ':' in display_state['content_line1'] else display_state['content_line1']
        new_line1_base = line1.split(':')[0] if ':' in line1 else line1
        significant_change = (old_line1_base != new_line1_base or line2 != display_state['content_line2'])
    else:
        # For now_playing, any change is significant
        significant_change = (line1 != display_state['content_line1'] or line2 != display_state['content_line2'])
    
    # Check if content significantly changed
    if significant_change:
        # Content changed - reset everything and show wave effect
        print(f"🔄 Display content changed: '{line1}' | '{line2}'")
        display_state.update({
            'content_line1': line1,
            'content_line2': line2,
            'scroll_pos1': 0,
            'scroll_pos2': 0,
            'scroll_dir1': 1,
            'scroll_dir2': 1,
            'pause_until1': 0,
            'pause_until2': 0,
            'wave_complete': False,
            'last_update': time.time()
        })
        lcd.clear()
        return True  # Content changed
    
    # Update content silently for minor changes (like clock seconds)
    display_state['content_line1'] = line1
    display_state['content_line2'] = line2
    
    now = time.time()
    width = 16
    scroll_speed = 0.3
    pause_time = 4.0
    wave_speed = 0.15
    
    # Show wave effect first for new content
    if not display_state['wave_complete']:
        if now - display_state['last_update'] >= wave_speed:
            wave_pos1 = display_state['scroll_pos1']
            wave_pos2 = display_state['scroll_pos2']
            
            # Show progressive text reveal
            if wave_pos1 <= width:
                text_to_show1 = line1[:wave_pos1].ljust(width) 
                lcd.lcd.cursor_pos = (0, 0)
                lcd.lcd.write_string(text_to_show1)
                display_state['scroll_pos1'] += 1
            
            if wave_pos2 <= width:
                text_to_show2 = line2[:wave_pos2].ljust(width)
                lcd.lcd.cursor_pos = (1, 0)
                lcd.lcd.write_string(text_to_show2)
                display_state['scroll_pos2'] += 1
                
            display_state['last_update'] = now
            
            # Wave complete when both lines fully revealed
            if display_state['scroll_pos1'] > width and display_state['scroll_pos2'] > width:
                display_state['wave_complete'] = True
                display_state['scroll_pos1'] = 0
                display_state['scroll_pos2'] = 0
                print("✨ Wave effect complete, starting scroll mode")
        
        return False  # Still in wave mode
    
    # Scrolling mode for overflow text
    if now - display_state['last_update'] >= scroll_speed:
        # Line 1 scrolling
        if len(line1) > width:
            if display_state['pause_until1'] <= now:
                # Ensure position stays within valid bounds
                max_pos = len(line1) - width
                pos = max(0, min(display_state['scroll_pos1'], max_pos))
                segment = line1[pos:pos + width]
                lcd.lcd.cursor_pos = (0, 0)
                lcd.lcd.write_string(segment.ljust(width))
                
                # Check boundaries BEFORE moving position
                if display_state['scroll_pos1'] >= max_pos and display_state['scroll_dir1'] == 1:
                    display_state['scroll_dir1'] = -1
                    display_state['pause_until1'] = now + pause_time
                    print(f"📜 Line 1 reached end (pos={pos}), reversing direction")
                elif display_state['scroll_pos1'] <= 0 and display_state['scroll_dir1'] == -1:
                    display_state['scroll_dir1'] = 1
                    display_state['pause_until1'] = now + pause_time  
                    print(f"📜 Line 1 reached start (pos={pos}), reversing direction")
                else:
                    # Only move position if not pausing
                    display_state['scroll_pos1'] += display_state['scroll_dir1']
        else:
            # Short text - just display it
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(line1.ljust(width))
        
        # Line 2 scrolling (same logic)
        if len(line2) > width:
            if display_state['pause_until2'] <= now:
                # Ensure position stays within valid bounds
                max_pos = len(line2) - width
                pos = max(0, min(display_state['scroll_pos2'], max_pos))
                segment = line2[pos:pos + width]
                lcd.lcd.cursor_pos = (1, 0)
                lcd.lcd.write_string(segment.ljust(width))
                
                # Check boundaries BEFORE moving position
                if display_state['scroll_pos2'] >= max_pos and display_state['scroll_dir2'] == 1:
                    display_state['scroll_dir2'] = -1
                    display_state['pause_until2'] = now + pause_time
                    print(f"📜 Line 2 reached end (pos={pos}), reversing direction")
                elif display_state['scroll_pos2'] <= 0 and display_state['scroll_dir2'] == -1:
                    display_state['scroll_dir2'] = 1
                    display_state['pause_until2'] = now + pause_time
                    print(f"📜 Line 2 reached start (pos={pos}), reversing direction")
                else:
                    # Only move position if not pausing
                    display_state['scroll_pos2'] += display_state['scroll_dir2']
        else:
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(line2.ljust(width))
        
        display_state['last_update'] = now
    
    return False  # No content change

def main():
    global track_changed, current_track, display_state, current_display_mode
    
    print("🎵 Starting Smart Spotify LCD Player with 4 Buttons...")
    print("🎮 PREV (GPIO17) | PLAY (GPIO18) | NEXT (GPIO27) | CYCLE (GPIO22)")
    print("🧠 Single-threaded with pendulum scrolling - no LCD corruption!")
    print("💤 Smart sleep: Auto-switches to clock after 30s of no music")
    print("🌅 Auto-wake: Returns to now_playing when music resumes or buttons pressed")
    
    # Initialize components
    spotify = get_spotify_manager()
    lcd = LCD()
    
    if not spotify.is_authenticated():
        print("❌ Spotify not authenticated! Run: python3 auth.py")
        return
    
    setup_buttons()
    
    # Start background thread for external device detection
    bg_thread = threading.Thread(target=check_for_track_changes, daemon=True)
    bg_thread.start()
    
    # Get initial track info
    current_track = spotify.get_current_track(force_refresh=True)
    
    print("✅ Ready! No more LCD corruption or threading issues.")
    print(f"📊 API calls this session: {spotify.get_api_call_count()}")
    
    try:
        lcd.clear()
        last_button_states = {name: GPIO.LOW for name in BUTTON_PINS}
        
        while True:
            # Check buttons (event-driven API calls)
            for name, pin in BUTTON_PINS.items():
                state = GPIO.input(pin)
                if state == GPIO.HIGH and last_button_states[name] == GPIO.LOW:
                    print(f"🎮 Button {name} pressed!")
                    
                    # Handle button actions
                    if name == 'PREV':
                        spotify.previous_track()
                        # Auto-wake: switch to now_playing when playback buttons pressed
                        if DISPLAY_MODES[current_display_mode] != 'now_playing':
                            print("🎵 Auto-wake: Playback button pressed, switching to now_playing")
                            current_display_mode = DISPLAY_MODES.index('now_playing')
                        time.sleep(1)  # Give Spotify time to change track
                        new_track = spotify.get_current_track(force_refresh=True)
                        if spotify.has_track_changed(current_track, new_track):
                            current_track = new_track
                        music_state['is_playing'] = True
                        music_state['last_playing_time'] = time.time()
                        music_state['stopped_duration'] = 0
                            
                    elif name == 'PLAY':
                        spotify.play_pause()
                        # Auto-wake: switch to now_playing when playback buttons pressed
                        if DISPLAY_MODES[current_display_mode] != 'now_playing':
                            print("🎵 Auto-wake: Play/Pause pressed, switching to now_playing")
                            current_display_mode = DISPLAY_MODES.index('now_playing')
                        # Update music state
                        music_state['is_playing'] = not music_state['is_playing']  # Toggle
                        if music_state['is_playing']:
                            music_state['last_playing_time'] = time.time()
                            music_state['stopped_duration'] = 0
                        print(f"⏯️  Play/Pause - Music {'playing' if music_state['is_playing'] else 'paused'}")
                            
                    elif name == 'NEXT':
                        spotify.next_track()
                        # Auto-wake: switch to now_playing when playback buttons pressed
                        if DISPLAY_MODES[current_display_mode] != 'now_playing':
                            print("🎵 Auto-wake: Playback button pressed, switching to now_playing")
                            current_display_mode = DISPLAY_MODES.index('now_playing')
                        time.sleep(1)  # Give Spotify time to change track
                        new_track = spotify.get_current_track(force_refresh=True)
                        if spotify.has_track_changed(current_track, new_track):
                            current_track = new_track
                        music_state['is_playing'] = True
                        music_state['last_playing_time'] = time.time()
                        music_state['stopped_duration'] = 0
                            
                    elif name == 'CYCLE':
                        cycle_display()
                        # Auto-wake: if we cycle to now_playing and music is playing, reset sleep timer
                        if DISPLAY_MODES[current_display_mode] == 'now_playing':
                            current_track = spotify.get_current_track(force_refresh=True)
                            if current_track and current_track.get('is_playing', False):
                                print("🎵 Auto-wake: Switched to now_playing with active music")
                                music_state['is_playing'] = True
                                music_state['last_playing_time'] = time.time()
                                music_state['stopped_duration'] = 0
                    
                    time.sleep(DEBOUNCE)  # Debounce
                last_button_states[name] = state
            
            # Single-threaded display update - no corruption possible!
            content_changed = update_display_content(lcd)
            if content_changed and DISPLAY_MODES[current_display_mode] == 'now_playing':
                print(f"📊 Total API calls: {spotify.get_api_call_count()}")
            
            time.sleep(0.05)  # Responsive checking
            
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye! Total API calls this session: {spotify.get_api_call_count()}")
        lcd.clear()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
