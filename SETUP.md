# 🎵 Spotify LCD Player Setup Guide

## Quick Start (Super Simple!)

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Get Spotify Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your **Client ID** and **Client Secret**
4. Add redirect URI: `http://127.0.0.1:8888/callback`

### 3. Create .env File
```bash
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 4. Authenticate Once
```bash
python3 auth.py
```
This opens your browser, you login to Spotify, and you're done!

### 5. Test Everything
```bash
python3 test.py
```

### 6. Run the Player!
```bash
python3 main.py
```

## 4-Button Controls & Wiring 🎮

### Button Wiring:
- **PREV Button → GPIO 17**: Previous Track
- **PLAY Button → GPIO 18**: Play/Pause  
- **NEXT Button → GPIO 27**: Next Track
- **CYCLE Button → GPIO 22**: Cycle Display Modes

### Wiring Instructions:
1. Connect each button between GPIO pin and GND
2. Internal pull-down resistors are used (no external resistors needed)
3. Button press = GPIO HIGH, release = GPIO LOW

```
Button Layout:
[PREV] [PLAY] [NEXT] [CYCLE]
 GPIO17 GPIO18 GPIO27 GPIO22
```

### Display Modes:
- **Now Playing**: Shows current song and artist
- **Clock**: Shows current time and date  
- **Debug**: Shows API call count and current mode

## LCD Display
- Shows current song title and artist
- Auto-scrolls long text
- Updates when track changes

## Smart API Rate Limiting 🧠

**Problem Solved**: Spotify limits to 100 API calls per hour. Old version was making 3600+ calls/hour!

**New Smart System**:
- ✅ **10-second cache**: Same track data reused for 10 seconds
- ✅ **Event-driven calls**: API called only when you press buttons
- ✅ **External device detection**: Checks every 10 seconds for changes from other devices
- ✅ **Interruptible display**: LCD scrolling stops when track changes
- ✅ **Track ID comparison**: More accurate change detection

**Expected API Usage** (Optimized!):
- **Play/Pause**: Only 1 call (just checks state, no track refresh)
- **Next/Prev**: 2 calls each (1 to skip + 1 to get new track)  
- **External detection**: 6 calls/hour (every 10 minutes)
- **Total**: ~6-15 calls per hour (well under 100/hour limit!)
- Button presses give immediate feedback
- External device changes detected within 10 seconds

## Troubleshooting
- No auth? Run `python3 auth.py` again
- LCD not working? Check I2C address (default 0x27)  
- Buttons not working? Check GPIO wiring
- API errors? Make sure Spotify is playing somewhere
- Rate limited? Check API call count with `python3 test.py`

## API Call Monitoring
```bash
python3 test.py  # Shows caching in action
# Watch for "API Call #X" messages in main.py
```

That's it! 🎉