#!/usr/bin/env python3
"""
Super Simple Spotify Authentication
Just run this once to get authenticated!
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def authenticate():
    """Super simple Spotify authentication"""
    
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
    
    if not client_id or not client_secret:
        print("❌ ERROR: Missing Spotify credentials!")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create an app and get Client ID & Secret")  
        print("3. Add redirect URI: http://127.0.0.1:8888/callback")
        print("4. Create .env file with:")
        print("   SPOTIPY_CLIENT_ID=your_client_id")
        print("   SPOTIPY_CLIENT_SECRET=your_client_secret")
        return False
    
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    
    try:
        print("🎵 Authenticating with Spotify...")
        print(f"Using Client ID: {client_id}")
        print(f"Redirect URI: {redirect_uri}")
        
        sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret, 
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache",
            open_browser=True
        )
        
        # Get the authorization URL
        auth_url = sp_oauth.get_authorize_url()
        print(f"\n🌐 COPY THIS URL TO YOUR BROWSER:")
        print(f"{auth_url}")
        print("\n📋 After you login, you'll be redirected to a page that says 'INVALID_CLIENT: Invalid redirect URI'")
        print("📋 Copy the ENTIRE URL from your browser address bar and paste it here:")
        
        # Get the response URL from user
        response_url = input("\nPaste the redirect URL here: ")
        
        # Extract the authorization code
        code = sp_oauth.parse_response_code(response_url)
        
        if code:
            print("🔄 Getting access token...")
            token_info = sp_oauth.get_access_token(code)
            
            # Test the connection
            sp = spotipy.Spotify(auth_manager=sp_oauth)
            user = sp.current_user()
            print(f"✅ Authenticated as: {user['display_name']}")
            return True
        else:
            print("❌ No authorization code found in URL")
            return False
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Make sure you copied the COMPLETE redirect URL!")
        return False

if __name__ == "__main__":
    success = authenticate()
    if success:
        print("🎉 Ready to rock! Run your main app now.")
    else:
        print("💥 Fix the issues above and try again.")