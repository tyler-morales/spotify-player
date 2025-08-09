"""
macOS-native Spotify control using AppleScript via osascript.
No Web API or extra dependencies required.
"""
import subprocess
from typing import Dict


class MacOSSpotify:
    def _osascript(self, script: str) -> str:
        try:
            out = subprocess.run(
                ["osascript", "-e", script],
                check=False,
                capture_output=True,
                text=True,
            )
            return (out.stdout or "").strip()
        except Exception:
            return ""

    def get_current_track(self) -> Dict[str, object]:
        script = r'''
        if application "Spotify" is running then
            tell application "Spotify"
                set s to (player state) as string
                try
                    set t to current track
                    set title to name of t
                    set artist to artist of t
                    set sid to id of t
                on error
                    set title to "Unknown track"
                    set artist to "No track data"
                    set sid to ""
                end try
                return s & "||" & title & "||" & artist & "||" & sid
            end tell
        else
            return "stopped||||"
        end if
        '''
        res = self._osascript(script)
        # Expected format: state||title||artist||spotify_uri
        parts = (res or "").split("||")
        state = parts[0] if len(parts) > 0 else "stopped"
        title = parts[1] if len(parts) > 1 else "Nothing playing"
        artist = parts[2] if len(parts) > 2 else ""
        sid = parts[3] if len(parts) > 3 else None

        is_playing = state == "playing"
        if not title:
            title = "Nothing playing"
        if not artist:
            artist = "Paused or stopped" if not is_playing else ""

        # Convert Spotify URI to an ID if present (spotify:track:ID)
        track_id = None
        if sid and sid.startswith("spotify:track:"):
            track_id = sid.split(":")[-1]

        return {
            "title": title,
            "artist": artist,
            "track_id": track_id,
            "is_playing": is_playing,
        }

    def play_pause(self) -> bool:
        script = 'tell application "Spotify" to playpause'
        self._osascript(script)
        return True

    def next_track(self) -> bool:
        script = 'tell application "Spotify" to next track'
        self._osascript(script)
        return True

    def previous_track(self) -> bool:
        script = 'tell application "Spotify" to previous track'
        self._osascript(script)
        return True
