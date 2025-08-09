"""
Button Handler Module
Manages GPIO button configuration and event handling
"""

import time
import RPi.GPIO as GPIO
import app_state
import os
import sys
import subprocess
import shutil

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
    """Handle 5-second hold on CYCLE button for restart/recovery"""
    print("🔄 CYCLE button held for 5 seconds - initiating recovery...")

    # Determine restart mode from environment
    restart_mode = os.getenv("RESTART_MODE", "process").strip().lower()
    services_env = os.getenv("SERVICES_TO_RESTART", "").strip()
    single_service = os.getenv("SERVICE_NAME", "").strip()
    services = []
    if services_env:
        services = [s.strip() for s in services_env.split(',') if s.strip()]
    elif single_service:
        services = [single_service]

    # Prepare LCD message based on action
    line1 = "Restarting app" if restart_mode == "process" else (
        "Restarting svc" if restart_mode == "service" else "Rebooting OS...")

    # Clear display to show status
    from lcd import LCD
    try:
        lcd = LCD()
        lcd.clear()
        lcd.lcd.cursor_pos = (0, 0)
        lcd.lcd.write_string((line1 + "...")[:16].ljust(16))
        lcd.lcd.cursor_pos = (1, 0)
        lcd.lcd.write_string("Please wait...".ljust(16))
        time.sleep(0.5)
    except Exception as e:
        print(f"LCD error during restart message: {e}")

    # Clean up GPIO before taking action
    try:
        GPIO.cleanup()
    except Exception as e:
        print(f"GPIO cleanup error: {e}")

    def restart_process():
        print("🚀 Restarting current process via execv")
        try:
            python_executable = sys.executable
            script_args = [python_executable] + sys.argv
            os.execv(python_executable, script_args)
        except Exception as e:
            print(f"Process restart failed: {e}")
            print("Please restart manually")
            sys.exit(1)

    # Execute selected mode with fallbacks
    try:
        if restart_mode == "service":
            if not services:
                print("⚠️ No services configured (SERVICE_NAME or SERVICES_TO_RESTART). Falling back to process restart.")
                return restart_process()
            if not shutil.which("systemctl"):
                print("⚠️ systemctl not available. Falling back to process restart.")
                return restart_process()

            # Restart listed services (e.g., raspotify, then this app's service)
            for svc in services:
                print(f"🔁 systemctl restart {svc}")
                try:
                    subprocess.run(["systemctl", "restart", svc], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except Exception as svc_err:
                    print(f"Service restart error for {svc}: {svc_err}")
            time.sleep(0.5)
            # Exit so the manager (systemd) fully takes over
            sys.exit(0)

        elif restart_mode == "reboot":
            print("💻 Requesting OS reboot")
            if shutil.which("systemctl"):
                subprocess.run(["systemctl", "reboot"], check=False)
            else:
                subprocess.run(["reboot"], check=False)
            # If reboot command returns (permissions?), fall back
            time.sleep(1)
            return restart_process()

        else:
            # Default: process restart
            return restart_process()

    except Exception as e:
        print(f"Recovery action failed: {e}")
        return restart_process()


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