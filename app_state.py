"""
Application State Management
Centralized state for the Spotify LCD Player
"""

# Display modes
DISPLAY_MODES = ['now_playing', 'clock', 'debug']

# Global state variables
current_display_mode = 0
track_changed = False
current_track = None

# Music playback state
music_state = {
    'is_playing': False,
    'last_playing_time': 0,
    'stopped_duration': 0,
    'auto_sleep_threshold': 30  # seconds
}

# Display rendering state
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

def reset_display_state():
    """Reset display state for new mode or content"""
    global display_state
    display_state.update({
        'scroll_pos1': 0,
        'scroll_pos2': 0,
        'scroll_dir1': 1,
        'scroll_dir2': 1,
        'pause_until1': 0,
        'pause_until2': 0,
        'wave_complete': False
    })

def get_current_mode():
    """Get the current display mode name"""
    return DISPLAY_MODES[current_display_mode]

def set_display_mode(mode_index):
    """Set display mode by index"""
    global current_display_mode
    current_display_mode = mode_index % len(DISPLAY_MODES)
    reset_display_state()

def cycle_display_mode():
    """Cycle to next display mode"""
    global current_display_mode
    current_display_mode = (current_display_mode + 1) % len(DISPLAY_MODES)
    reset_display_state()
    return get_current_mode()