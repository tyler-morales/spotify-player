"""
Background Tasks Module
Handles background monitoring and auto-sleep functionality
"""

import time
import threading
import app_state

def check_for_track_changes():
    """Smart background thread - only polls when on now_playing display"""
    from spotify_manager import get_spotify_manager
    spotify = get_spotify_manager()
    
    while True:
        try:
            # Only poll API when on now_playing display
            if app_state.get_current_mode() == 'now_playing':
                new_track = spotify.get_current_track()
                
                # Track music playback state
                is_currently_playing = new_track and new_track.get('is_playing', False)
                
                if is_currently_playing != app_state.music_state['is_playing']:
                    app_state.music_state['is_playing'] = is_currently_playing
                    if is_currently_playing:
                        print("🎵 Music resumed - staying on now_playing")
                        app_state.music_state['last_playing_time'] = time.time()
                        app_state.music_state['stopped_duration'] = 0
                    else:
                        print("⏸️  Music paused/stopped - starting sleep timer")
                        app_state.music_state['stopped_duration'] = 0
                
                # Check for track changes
                if spotify.has_track_changed(app_state.current_track, new_track):
                    print(f"🔄 Track change: {new_track['title']} - {new_track['artist']}")
                    app_state.current_track = new_track
                    app_state.music_state['last_playing_time'] = time.time()
                
                # Auto-sleep logic: switch to clock if music stopped for too long
                if not is_currently_playing:
                    app_state.music_state['stopped_duration'] = time.time() - app_state.music_state['last_playing_time']
                    if app_state.music_state['stopped_duration'] > app_state.music_state['auto_sleep_threshold']:
                        print(f"😴 Auto-sleep: Music stopped for {app_state.music_state['stopped_duration']:.0f}s, switching to clock")
                        app_state.set_display_mode(app_state.DISPLAY_MODES.index('clock'))
                        app_state.music_state['stopped_duration'] = 0  # Reset to avoid repeated switches
                
                time.sleep(8)  # Poll every 8 seconds when on now_playing
            else:
                # Not on now_playing display - sleep longer, no API calls
                print(f"💤 Sleeping - on {app_state.get_current_mode()} display, no API polling")
                time.sleep(30)  # Much longer sleep when not on now_playing
            
        except Exception as e:
            print(f"Background check error: {e}")
            time.sleep(10)

def start_background_monitoring():
    """Start the background thread for track change monitoring"""
    bg_thread = threading.Thread(target=check_for_track_changes, daemon=True)
    bg_thread.start()
    return bg_thread