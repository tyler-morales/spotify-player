#!/usr/bin/env python3
"""
Test display integration with Japanese processing
"""

import app_state
from japanese_processor import get_japanese_processor
from display_manager import get_display_content

def test_display_integration():
    print("🧪 Testing Display Integration with Japanese Processing")
    print("=" * 60)
    
    # Initialize Japanese processor
    japanese_proc = get_japanese_processor()
    app_state.set_japanese_processor_availability(japanese_proc.is_available())
    
    print(f"Japanese processor available: {japanese_proc.is_available()}")
    print(f"Romanization enabled: {app_state.is_japanese_romanization_enabled()}")
    print()
    
    # Test cases with different track info
    test_cases = [
        {
            'title': 'Lemon',
            'artist': 'Kenshi Yonezu',
            'description': 'English title, English artist'
        },
        {
            'title': '打上花火',
            'artist': 'DAOKO×米津玄師', 
            'description': 'Japanese title, mixed artist'
        },
        {
            'title': 'あいみょん',
            'artist': 'マリーゴールド',
            'description': 'Japanese title, Japanese artist'
        },
        {
            'title': 'Pretender',
            'artist': 'Official髭男dism',
            'description': 'English title, mixed artist'
        }
    ]
    
    # Set display mode to now_playing
    app_state.set_display_mode(app_state.DISPLAY_MODES.index('now_playing'))
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Original: '{test_case['title']}' - '{test_case['artist']}'")
        
        # Set current track in app state
        app_state.current_track = {
            'title': test_case['title'],
            'artist': test_case['artist'],
            'track_id': f'test{i}'
        }
        
        # Get display content (this should apply Japanese processing)
        line1, line2 = get_display_content()
        
        print(f"Display:  '{line1}' - '{line2}'")
        
        # Check if romanization occurred
        if (line1 != test_case['title'] or line2 != test_case['artist']):
            print("✓ Romanization applied")
        else:
            print("✗ No romanization (expected for non-Japanese text)")
        
        print()
    
    print("✅ Display integration test completed!")

if __name__ == "__main__":
    test_display_integration()