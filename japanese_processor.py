"""
Japanese Text Processor
Handles detection and romanization of Japanese text for LCD display
"""

import re
try:
    import pykakasi
    PYKAKASI_AVAILABLE = True
except ImportError:
    PYKAKASI_AVAILABLE = False
    print("pykakasi not available - Japanese romanization disabled")

class JapaneseProcessor:
    def __init__(self):
        self.kks = None
        global PYKAKASI_AVAILABLE
        if PYKAKASI_AVAILABLE:
            try:
                self.kks = pykakasi.kakasi()
                print("Japanese processor initialized successfully")
            except Exception as e:
                print(f"Failed to initialize pykakasi: {e}")
                PYKAKASI_AVAILABLE = False
    
    def has_japanese_characters(self, text):
        """
        Detect if text contains Japanese characters (hiragana, katakana, or kanji)
        """
        if not text:
            return False
        
        # Unicode ranges for Japanese characters
        hiragana_pattern = r'[\u3040-\u309F]'  # Hiragana
        katakana_pattern = r'[\u30A0-\u30FF]'  # Katakana
        kanji_pattern = r'[\u4E00-\u9FAF]'     # CJK Unified Ideographs (Kanji)
        
        japanese_pattern = f'({hiragana_pattern}|{katakana_pattern}|{kanji_pattern})'
        
        return bool(re.search(japanese_pattern, text))
    
    def romanize_text(self, text):
        """
        Convert Japanese text to romaji using pykakasi
        Returns original text if no Japanese characters or pykakasi unavailable
        """
        if not text or not self.has_japanese_characters(text):
            return text
        
        global PYKAKASI_AVAILABLE
        if not PYKAKASI_AVAILABLE or not self.kks:
            print(f"Cannot romanize '{text}' - pykakasi not available")
            return text
        
        try:
            result = self.kks.convert(text)
            # Extract romaji from the conversion result
            romaji_parts = []
            for item in result:
                # pykakasi returns dict with 'hepburn' key for romaji
                if 'hepburn' in item:
                    romaji_parts.append(item['hepburn'])
                elif 'orig' in item:
                    # Fallback to original if no romaji conversion
                    romaji_parts.append(item['orig'])
            
            romanized = ''.join(romaji_parts)
            return romanized
            
        except Exception as e:
            print(f"Error romanizing '{text}': {e}")
            return text
    
    def process_track_info(self, track_info, romanize_enabled=True):
        """
        Process track info dictionary, romanizing Japanese text if enabled
        """
        if not track_info or not romanize_enabled:
            return track_info
        
        processed_info = track_info.copy()
        
        # Process title
        if 'title' in processed_info:
            processed_info['title'] = self.romanize_text(processed_info['title'])
        
        # Process artist
        if 'artist' in processed_info:
            processed_info['artist'] = self.romanize_text(processed_info['artist'])
        
        return processed_info
    
    def is_available(self):
        """Check if Japanese processing is available"""
        global PYKAKASI_AVAILABLE
        return PYKAKASI_AVAILABLE and self.kks is not None

# Global instance
japanese_processor = None

def get_japanese_processor():
    """Get or create the global Japanese processor instance"""
    global japanese_processor
    if japanese_processor is None:
        japanese_processor = JapaneseProcessor()
    return japanese_processor