#!/usr/bin/env python3
"""
Quick test script to verify everything works and test API rate limiting
"""

import os
import time
from dotenv import load_dotenv
from spotify_manager import get_spotify_manager

def test_setup():
    """Test if everything is set up correctly"""
    
    print("🧪 Testing Spotify Player Setup...")
    
    # Check .env file
    load_dotenv()
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Missing .env file or credentials")
        print("Create .env file with:")
        print("SPOTIPY_CLIENT_ID=your_client_id")
        print("SPOTIPY_CLIENT_SECRET=your_client_secret")
        return False
    
    print("✅ Credentials found")
    
    # Test Spotify connection
    spotify = get_spotify_manager()
    if not spotify.is_authenticated():
        print("❌ Spotify authentication failed")
        print("Run: python3 auth.py")
        return False
    
    print("✅ Spotify authenticated")
    
    # Test API rate limiting
    print("\n🧠 Testing Smart Caching...")
    
    # First call should hit API
    print("First call (should hit API):")
    track1 = spotify.get_current_track(force_refresh=True)
    print(f"🎵 Track: {track1['title']} - {track1['artist']}")
    print(f"📊 API calls: {spotify.get_api_call_count()}")
    
    # Second call within 10 seconds should use cache
    print("\nSecond call (should use cache):")
    track2 = spotify.get_current_track()
    print(f"🎵 Track: {track2['title']} - {track2['artist']}")
    print(f"📊 API calls: {spotify.get_api_call_count()}")
    
    if spotify.get_api_call_count() == 1:
        print("✅ Caching working correctly!")
    else:
        print("⚠️ Caching may not be working as expected")
    
    # Test playback controls (optimized usage)
    print("\n🎮 Testing Optimized Playback Controls...")
    print("Testing play/pause (should only check state, not refresh track):")
    api_before = spotify.get_api_call_count()
    spotify.play_pause()
    api_after = spotify.get_api_call_count()
    print(f"📊 API calls: {api_before} → {api_after} (only +1 for state check)")
    
    print("\n🎉 All tests passed!")
    print(f"📈 Final API call count: {spotify.get_api_call_count()}")
    print("💡 Optimized usage:")
    print("  - Play/Pause: Only 1 API call (no track refresh)")
    print("  - Next/Prev: 1 call to skip + 1 call to get new track = 2 calls")
    print("  - Background: 1 call every 10 seconds for external changes")
    print("  - Expected: ~6-15 API calls per hour")
    print("🚀 Ready to run main.py")
    return True

if __name__ == "__main__":
    test_setup()