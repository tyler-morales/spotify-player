#!/usr/bin/env python3
"""
Test script for Japanese text processing functionality
Run this to test Japanese detection and romanization without Spotify
"""

from japanese_processor import get_japanese_processor
import app_state

def test_japanese_processing():
    """Test Japanese text detection and romanization"""
    print("🧪 Testing Japanese Text Processing")
    print("=" * 50)
    
    # Get processor
    processor = get_japanese_processor()
    
    # Update app state with processor availability
    app_state.set_japanese_processor_availability(processor.is_available())
    
    print(f"Japanese processor available: {processor.is_available()}")
    print(f"Romanization enabled: {app_state.is_japanese_romanization_enabled()}")
    print()
    
    # Test cases
    test_cases = [
        ("Hello World", "English text"),
        ("こんにちは", "Hiragana"),
        ("カタカナ", "Katakana"), 
        ("漢字", "Kanji"),
        ("米津玄師", "Japanese artist name"),
        ("Lemon", "English song title"),
        ("打上花火", "Japanese song title"),
        ("DAOKO×米津玄師", "Mixed Japanese/English"),
        ("あいみょん - マリーゴールド", "Artist - Song format"),
        ("", "Empty string"),
        (None, "None value")
    ]
    
    print("Text Detection Tests:")
    print("-" * 30)
    for text, description in test_cases:
        if text is not None:
            has_japanese = processor.has_japanese_characters(text)
            print(f"'{text}' ({description}): {'✓ Japanese' if has_japanese else '✗ No Japanese'}")
        else:
            print(f"None ({description}): ✗ No Japanese")
    
    print("\nRomanization Tests:")
    print("-" * 30)
    for text, description in test_cases:
        if text is not None and processor.has_japanese_characters(text):
            romanized = processor.romanize_text(text)
            print(f"'{text}' -> '{romanized}' ({description})")
    
    print("\nTrack Info Processing Test:")
    print("-" * 30)
    test_track_info = {
        'title': '打上花火',
        'artist': 'DAOKO×米津玄師',
        'track_id': 'test123'
    }
    
    print(f"Original: {test_track_info['title']} - {test_track_info['artist']}")
    
    # Test with romanization enabled
    processed = processor.process_track_info(test_track_info, romanize_enabled=True)
    print(f"Romanized: {processed['title']} - {processed['artist']}")
    
    # Test with romanization disabled
    processed_disabled = processor.process_track_info(test_track_info, romanize_enabled=False)
    print(f"Not romanized: {processed_disabled['title']} - {processed_disabled['artist']}")
    
    print("\nProcessor Status:")
    print("-" * 30)
    print(f"Japanese processor available: {app_state.is_japanese_romanization_enabled()}")
    print(f"Always romanizes Japanese text when detected: {processor.is_available()}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_japanese_processing()