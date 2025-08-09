"""
Linux MPRIS backend using playerctl CLI.
Works on Raspberry Pi OS when a MPRIS-compatible player is running
(spotifyd, ncspot, or librespot with librespot-mpris, etc.).
"""
import subprocess
import shutil
from typing import Optional, Dict

PREFERRED_PLAYERS = [
    "spotify",
    "spotifyd",
    "ncspot",
    "librespot",
    "chromium",
    "vlc",
]


class LinuxMPRIS:
    def __init__(self, player: Optional[str] = None):
        if not self.available():
            raise RuntimeError(
                "playerctl not found. Install with: sudo apt-get update && sudo apt-get install -y playerctl"
            )
        self.player = player or self._detect_player()

    @staticmethod
    def available() -> bool:
        return shutil.which("playerctl") is not None

    def _run(self, *args: str) -> str:
        cmd = ["playerctl"]
        if self.player:
            cmd += ["-p", self.player]
        cmd += list(args)
        out = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if out.returncode != 0:
            raise subprocess.CalledProcessError(out.returncode, cmd, out.stdout, out.stderr)
        return (out.stdout or "").strip()

    def _detect_player(self) -> Optional[str]:
        try:
            out = subprocess.run(["playerctl", "-l"], check=False, capture_output=True, text=True)
            players = (out.stdout or "").strip().splitlines()
        except Exception:
            players = []
        # Prefer known Spotify-related players first
        for pref in PREFERRED_PLAYERS:
            for p in players:
                if pref in p:
                    return p
        return players[0] if players else None

    def get_current_track(self) -> Dict[str, object]:
        # Playback status
        try:
            status = self._run("status")
        except subprocess.CalledProcessError:
            return {
                "title": "Nothing playing",
                "artist": "No player",
                "track_id": None,
                "is_playing": False,
            }

        # Metadata
        fmt = "{{mpris:trackid}}||{{xesam:title}}||{{join(xesam:artist, ', ')}}"
        try:
            raw = self._run("metadata", "--format", fmt)
        except subprocess.CalledProcessError:
            raw = "||"
        parts = (raw or "").split("||")
        mpris_id = parts[0] if len(parts) > 0 else None
        title = parts[1] if len(parts) > 1 else "Unknown"
        artist = parts[2] if len(parts) > 2 else "Unknown"

        # Extract Spotify track id if present
        track_id = None
        if mpris_id:
            if "spotify:track:" in mpris_id:
                track_id = mpris_id.split("spotify:track:")[-1]
            else:
                # Keep the raw MPRIS id if not a Spotify URI
                track_id = mpris_id

        return {
            "title": title or "Unknown",
            "artist": artist or "Unknown",
            "track_id": track_id,
            "is_playing": status.strip().lower() == "playing",
        }

    def play_pause(self) -> bool:
        try:
            self._run("play-pause")
            return True
        except subprocess.CalledProcessError:
            return False

    def next_track(self) -> bool:
        try:
            self._run("next")
            return True
        except subprocess.CalledProcessError:
            return False

    def previous_track(self) -> bool:
        try:
            self._run("previous")
            return True
        except subprocess.CalledProcessError:
            return False
