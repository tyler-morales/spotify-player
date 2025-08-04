# pages/now_playing.py
import time
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_manager import get_spotify_manager

def render(lcd, button_pin=None):
    # Get Spotify manager instance
    spotify = get_spotify_manager()
    
    # Fetch current track info
    track_info = spotify.get_current_track()
    title = track_info['title']
    artist = track_info['artist']
    
    # Add some visual indicator if not authenticated
    if not spotify.is_authenticated():
        title = "⚠ " + title
    
    # Clear and show track info with scrolling that can be interrupted
    lcd.clear()
    lcd.display(title, artist, button_pin=button_pin)
