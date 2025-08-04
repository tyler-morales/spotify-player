"""
Display Manager Module
Handles display content generation and mode management
"""

import app_state

def get_display_content():
    """Get content based on current display mode"""
    mode = app_state.get_current_mode()
    
    if mode == 'now_playing':
        if app_state.current_track:
            return app_state.current_track['title'], app_state.current_track['artist']
        return "No track", "Connect Spotify"
    
    elif mode == 'clock':
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%H:%M:%S"), now.strftime("%a %b %d")
    
    elif mode == 'debug':
        from spotify_manager import get_spotify_manager
        spotify = get_spotify_manager()
        api_calls = spotify.get_api_call_count()
        if app_state.music_state['is_playing']:
            status = "Playing"
        elif app_state.music_state['stopped_duration'] > 0:
            remaining = app_state.music_state['auto_sleep_threshold'] - app_state.music_state['stopped_duration']
            status = f"Sleep in {remaining:.0f}s" if remaining > 0 else "Sleeping"
        else:
            status = "Ready"
        return f"API: {api_calls} | {status}", f"Mode: {mode}"
    
    return "Unknown", "Mode"

def has_significant_content_change(line1, line2):
    """Check if content change is significant enough to trigger wave effect"""
    mode = app_state.get_current_mode()
    
    if mode in ['clock', 'debug']:
        # Only restart wave effect on major changes, not every second
        old_line1_base = app_state.display_state['content_line1'].split(':')[0] if ':' in app_state.display_state['content_line1'] else app_state.display_state['content_line1']
        new_line1_base = line1.split(':')[0] if ':' in line1 else line1
        return (old_line1_base != new_line1_base or line2 != app_state.display_state['content_line2'])
    else:
        # For now_playing, any change is significant
        return (line1 != app_state.display_state['content_line1'] or line2 != app_state.display_state['content_line2'])