# Spotipy is optional when using MPRIS only
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except Exception:
    spotipy = None
    SpotifyOAuth = None
import os
from dotenv import load_dotenv
import time
import platform

# Load environment variables
load_dotenv()

# Try to import Linux MPRIS (playerctl) backend
try:
    from linux_mpris import LinuxMPRIS
except Exception:
    LinuxMPRIS = None

class SpotifyManager:
    def __init__(self):
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        
        # Required scope for reading currently playing track and controlling playback
        self.scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"
        
        self.sp = None
        self.last_track_id = None
        self.cached_track_info = {"title": "No track playing", "artist": "Connect to Spotify"}
        self.cache_timestamp = 0
        self.cache_duration = 10  # Cache for 10 seconds
        self.api_call_count = 0

        # Backend selection
        self.local = None
        default_backend = 'local' if platform.system() == 'Linux' else 'web'
        backend_pref = os.getenv('SPOTIFY_BACKEND', default_backend)

        if backend_pref == 'local':
            if platform.system() == 'Linux' and LinuxMPRIS is not None and LinuxMPRIS.available():
                try:
                    player_name = os.getenv('SPOTIFY_MPRIS_PLAYER')  # e.g. spotify, spotifyd, ncspot
                    self.local = LinuxMPRIS(player=player_name)
                    print(f"Using Linux MPRIS control via playerctl (player: {self.local.player or 'auto'})")
                except Exception as e:
                    print(f"Linux MPRIS unavailable: {e}")
                    self.local = None
        
        # Authenticate Web API only if not using local backend
        if not self.local:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Spotify using OAuth"""
        if self.local:
            # Local backend does not need Web API auth
            return
        if SpotifyOAuth is None:
            print("Spotipy not installed; Web API disabled. Install spotipy to enable fallback.")
            self.sp = None
            return
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                cache_path=".spotify_cache"
            )
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            print("Spotify authentication successful!")
            
            # Test the connection
            self.get_current_track()
            
        except Exception as e:
            print(f"Spotify authentication failed: {e}")
            self.sp = None
    
    def get_current_track(self, force_refresh=False):
        """Get currently playing track information with smart caching"""
        # Local Linux backend path (no Web API, no rate limits)
        if self.local:
            track_info = self.local.get_current_track()
            # Update cache timestamp and last_track_id for consistency
            self.cached_track_info = track_info
            self.cache_timestamp = time.time()
            self.last_track_id = track_info.get('track_id')
            return track_info

        if not self.sp:
            return self.cached_track_info
        
        current_time = time.time()
        
        # Check if we should use cached data
        if not force_refresh and (current_time - self.cache_timestamp) < self.cache_duration:
            return self.cached_track_info
        
        # Time to make an API call
        try:
            print(f"🔄 API Call #{self.api_call_count + 1} - Fetching current track...")
            self.api_call_count += 1
            current_track = self.sp.current_playback()
            
            if current_track is None or not current_track.get('is_playing'):
                track_info = {"title": "Nothing playing", "artist": "Paused or stopped", "track_id": None, "is_playing": False}
            else:
                track = current_track['item']
                if track is None:
                    track_info = {"title": "Unknown track", "artist": "No track data", "track_id": None, "is_playing": True}
                else:
                    # Extract track information
                    track_id = track['id']
                    title = track['name']
                    artists = [artist['name'] for artist in track['artists']]
                    artist = ', '.join(artists)
                    track_info = {"title": title, "artist": artist, "track_id": track_id, "is_playing": True}
                    self.last_track_id = track_id
            
            # Update cache
            self.cached_track_info = track_info
            self.cache_timestamp = current_time
            
            return track_info
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return self.cached_track_info
    
    def has_track_changed(self, old_track, new_track):
        """Compare tracks more accurately including track_id"""
        if old_track is None or new_track is None:
            return True
        
        # Compare by track_id first (most reliable)
        old_id = old_track.get('track_id')
        new_id = new_track.get('track_id')
        
        if old_id != new_id:
            return True
            
        # Fallback to title+artist comparison for edge cases
        return (old_track.get('title') != new_track.get('title') or 
                old_track.get('artist') != new_track.get('artist'))
    
    def is_authenticated(self):
        """Check if Spotify is properly authenticated"""
        # Local backend needs no auth
        if self.local:
            return True
        return self.sp is not None
    
    def refresh_connection(self):
        """Attempt to refresh the Spotify connection"""
        print("Refreshing Spotify connection...")
        self._authenticate()
    
    def play_pause(self):
        """Toggle play/pause - optimized to minimize API calls"""
        if self.local:
            return self.local.play_pause()
        if not self.sp:
            return False
        try:
            # First get current state to decide what to do
            current = self.sp.current_playback()
            self.api_call_count += 1
            print(f"🔄 API Call #{self.api_call_count} - Checking playback state...")
            
            if current and current.get('is_playing'):
                self.sp.pause_playback()
                print("⏸️  Paused - no track change")
            else:
                self.sp.start_playback()
                print("▶️  Playing - no track change")
            
            # No additional API call needed - play/pause doesn't change track!
            return True
        except Exception as e:
            print(f"Play/pause error: {e}")
            return False
    
    def next_track(self):
        """Skip to next track - track info will be refreshed by caller"""
        if self.local:
            return self.local.next_track()
        if not self.sp:
            return False
        try:
            self.sp.next_track()
            print("⏭️  Next track - caller will refresh track info")
            return True
        except Exception as e:
            print(f"Next track error: {e}")
            return False
    
    def previous_track(self):
        """Skip to previous track - track info will be refreshed by caller"""
        if self.local:
            return self.local.previous_track()
        if not self.sp:
            return False
        try:
            self.sp.previous_track()
            print("⏮️  Previous track - caller will refresh track info")
            return True
        except Exception as e:
            print(f"Previous track error: {e}")
            return False
    
    def get_api_call_count(self):
        """Get the number of API calls made this session"""
        return self.api_call_count
    
    def reset_api_call_count(self):
        """Reset the API call counter"""
        self.api_call_count = 0

# Global instance
spotify_manager = None

def get_spotify_manager():
    """Get or create the global Spotify manager instance"""
    global spotify_manager
    if spotify_manager is None:
        spotify_manager = SpotifyManager()
    return spotify_manager