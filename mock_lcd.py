"""
Mock LCD Display Module
Provides a console-based ASCII representation of a 16x2 LCD display
using keyboard characters for development and testing purposes.
"""

import time
import sys
import os

class MockLCD:
    """Mock LCD that renders to console using ASCII characters"""
    
    def __init__(self, address=0x27, cols=16, rows=2):
        self.cols = cols
        self.rows = rows
        self.address = address
        self.display_buffer = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.cursor_row = 0
        self.cursor_col = 0
        print(f"🖥️  Mock LCD initialized ({cols}x{rows}) at address {hex(address)}")
        self._render_display()

    def clear(self):
        """Clear the display buffer and render"""
        self.display_buffer = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.cursor_row = 0
        self.cursor_col = 0
        self._render_display()

    def _render_display(self):
        """Render the current display buffer to console"""
        # Clear previous output and move cursor up
        if hasattr(self, '_first_render') and not self._first_render:
            # Move cursor up 4 lines to overwrite previous display
            sys.stdout.write('\033[4A')
        else:
            self._first_render = False
        
        # Top border
        print('┌' + '─' * self.cols + '┐')
        
        # Content rows
        for row in self.display_buffer:
            content = ''.join(row)
            print('│' + content + '│')
        
        # Bottom border
        print('└' + '─' * self.cols + '┘')
        sys.stdout.flush()

    @property
    def cursor_pos(self):
        """Get current cursor position"""
        return (self.cursor_row, self.cursor_col)

    @cursor_pos.setter
    def cursor_pos(self, pos):
        """Set cursor position (row, col)"""
        row, col = pos
        self.cursor_row = max(0, min(row, self.rows - 1))
        self.cursor_col = max(0, min(col, self.cols - 1))

    def write_string(self, text):
        """Write string at current cursor position"""
        for i, char in enumerate(text):
            if self.cursor_col + i < self.cols:
                self.display_buffer[self.cursor_row][self.cursor_col + i] = char
        self._render_display()


class MockLCDWrapper:
    """Wrapper class that mimics the lcd.LCD interface"""
    
    def __init__(self, address=0x27, cols=16, rows=2):
        self.lcd = MockLCD(address, cols, rows)

    def clear(self):
        self.lcd.clear()

    def write_line_wave(self, text, line=0, speed=0.1, interrupt_callback=None):
        """Typewriter effect for first appearance - same as real LCD"""
        self.lcd.cursor_pos = (line, 0)
        self.lcd.write_string(' ' * 16)
        self.lcd.cursor_pos = (line, 0)
        
        for i in range(1, min(len(text), 16) + 1):
            # Check for interrupt before each character
            if interrupt_callback and interrupt_callback():
                return  # Stop wave animation if interrupted
            
            self.lcd.cursor_pos = (line, 0)
            self.lcd.write_string(text[:i].ljust(16))
            if speed > 0:
                time.sleep(speed)
        
        self.lcd.cursor_pos = (line, 0)
        self.lcd.write_string(text[:16].ljust(16))

    def scroll_both(self, line1, line2, width=16, scroll_speed=0.25, pause=5, button_pin=None, interrupt_callback=None):
        """Scrolling animation for both lines - same logic as real LCD but without GPIO"""
        
        # Fade-in on both lines with proper wave effect
        self.write_line_wave(line1, 0, speed=0.1, interrupt_callback=interrupt_callback)
        if interrupt_callback and interrupt_callback():
            return  # Exit if interrupted during first line
        self.write_line_wave(line2, 1, speed=0.1, interrupt_callback=interrupt_callback)
        if interrupt_callback and interrupt_callback():
            return  # Exit if interrupted during second line

        # Setup scroll state
        def make_state(text):
            over = len(text) > width
            idx = 0
            direction = 1
            pause_until = None
            return {'text': text, 'over': over, 'idx': idx, 'dir': direction, 'pause_until': None}

        l1 = make_state(line1)
        l2 = make_state(line2)

        last_update1 = time.monotonic()
        last_update2 = time.monotonic()

        while True:
            now = time.monotonic()
            
            # For mock LCD, we can't check GPIO buttons, so just use interrupt callback
            # Check for callback interrupt (track change, etc.)
            if interrupt_callback and interrupt_callback():
                return  # Break out for track update
            
            # --- LINE 1 ---
            if l1['over'] and (now - last_update1) >= scroll_speed:
                # Should we pause at ends?
                if l1['pause_until'] is not None and now < l1['pause_until']:
                    pass  # still paused
                else:
                    seg = l1['text'][l1['idx']:l1['idx']+width]
                    self.lcd.cursor_pos = (0, 0)
                    self.lcd.write_string(seg.ljust(width))
                    # Next frame: move index
                    if l1['dir'] == 1 and l1['idx'] >= len(l1['text']) - width:
                        l1['dir'] = -1
                        l1['pause_until'] = now + pause
                    elif l1['dir'] == -1 and l1['idx'] <= 0:
                        l1['dir'] = 1
                        l1['pause_until'] = now + pause
                    else:
                        l1['idx'] += l1['dir']
                    last_update1 = now
            elif not l1['over']:
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(l1['text'].ljust(width))

            # --- LINE 2 ---
            if l2['over'] and (now - last_update2) >= scroll_speed:
                if l2['pause_until'] is not None and now < l2['pause_until']:
                    pass
                else:
                    seg = l2['text'][l2['idx']:l2['idx']+width]
                    self.lcd.cursor_pos = (1, 0)
                    self.lcd.write_string(seg.ljust(width))
                    if l2['dir'] == 1 and l2['idx'] >= len(l2['text']) - width:
                        l2['dir'] = -1
                        l2['pause_until'] = now + pause
                    elif l2['dir'] == -1 and l2['idx'] <= 0:
                        l2['dir'] = 1
                        l2['pause_until'] = now + pause
                    else:
                        l2['idx'] += l2['dir']
                    last_update2 = now
            elif not l2['over']:
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(l2['text'].ljust(width))

            time.sleep(0.05)  # Small sleep to prevent excessive CPU usage

    def display(self, line1, line2, button_pin=None, interrupt_callback=None):
        """Display method that calls scroll_both"""
        self.scroll_both(line1, line2, button_pin=button_pin, interrupt_callback=interrupt_callback)