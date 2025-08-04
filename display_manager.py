"""
Display Manager Module
Handles display content generation and mode management
"""

import app_state
from japanese_processor import get_japanese_processor

# Cache for Japanese processing to avoid repeated romanization
_japanese_cache = {}

def get_display_content():
    """Get content based on current display mode"""
    mode = app_state.get_current_mode()
    
    if mode == 'welcome':
        return "Welcome :)", "Starting up..."
    
    elif mode == 'now_playing':
        if app_state.current_track:
            title = app_state.current_track['title']
            artist = app_state.current_track['artist']
            
            # Process Japanese text if processor is available
            if app_state.is_japanese_romanization_enabled():
                # Create cache key from original title and artist
                cache_key = f"{title}|{artist}"
                
                # Check if we already processed this content
                if cache_key in _japanese_cache:
                    return _japanese_cache[cache_key]
                
                # Process Japanese text
                japanese_proc = get_japanese_processor()
                track_info = {'title': title, 'artist': artist}
                processed = japanese_proc.process_track_info(track_info, romanize_enabled=True)
                
                # Log romanization only if it occurred and wasn't cached
                if title != processed['title'] or artist != processed['artist']:
                    print(f"🈳 Display romanized: '{title}' -> '{processed['title']}'")
                    print(f"🈳 Display romanized: '{artist}' -> '{processed['artist']}'")
                
                # Cache the result
                result = (processed['title'], processed['artist'])
                _japanese_cache[cache_key] = result
                
                return result
            
            return title, artist
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
    
    if mode == 'welcome':
        # Welcome message should always trigger wave effect
        return True
    
    elif mode in ['clock', 'debug']:
        # Only restart wave effect on major changes, not every second
        old_line1_base = app_state.display_state['content_line1'].split(':')[0] if ':' in app_state.display_state['content_line1'] else app_state.display_state['content_line1']
        new_line1_base = line1.split(':')[0] if ':' in line1 else line1
        return (old_line1_base != new_line1_base or line2 != app_state.display_state['content_line2'])
    else:
        # For now_playing, any change is significant
        return (line1 != app_state.display_state['content_line1'] or line2 != app_state.display_state['content_line2'])