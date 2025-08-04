"""
Display Effects Module
Handles complex display animations like wave effects and scrolling
"""

import time
import app_state

def update_display_with_effects(lcd):
    """Non-blocking display update with pendulum scrolling and wave effects"""
    from display_manager import get_display_content, has_significant_content_change
    
    line1, line2 = get_display_content()
    
    # Check if content significantly changed
    if has_significant_content_change(line1, line2):
        # Content changed - reset everything and show wave effect
        print(f"🔄 Display content changed: '{line1}' | '{line2}'")
        app_state.display_state.update({
            'content_line1': line1,
            'content_line2': line2,
            'scroll_pos1': 0,
            'scroll_pos2': 0,
            'scroll_dir1': 1,
            'scroll_dir2': 1,
            'pause_until1': 0,
            'pause_until2': 0,
            'wave_complete': False,
            'last_update': time.time()
        })
        lcd.clear()
        return True  # Content changed
    
    # Update content silently for minor changes (like clock seconds)
    app_state.display_state['content_line1'] = line1
    app_state.display_state['content_line2'] = line2
    
    now = time.time()
    width = 16
    scroll_speed = 0.3
    pause_time = 4.0
    wave_speed = 0.15
    
    # Show wave effect first for new content
    if not app_state.display_state['wave_complete']:
        return _update_wave_effect(lcd, line1, line2, now, width, wave_speed)
    
    # Scrolling mode for overflow text
    if now - app_state.display_state['last_update'] >= scroll_speed:
        _update_scrolling(lcd, line1, line2, now, width, pause_time)
        app_state.display_state['last_update'] = now
    
    return False  # No content change

def _update_wave_effect(lcd, line1, line2, now, width, wave_speed):
    """Handle wave effect animation for new content"""
    if now - app_state.display_state['last_update'] >= wave_speed:
        wave_pos1 = app_state.display_state['scroll_pos1']
        wave_pos2 = app_state.display_state['scroll_pos2']
        
        # Show progressive text reveal
        if wave_pos1 <= width:
            text_to_show1 = line1[:wave_pos1].ljust(width) 
            lcd.lcd.cursor_pos = (0, 0)
            lcd.lcd.write_string(text_to_show1)
            app_state.display_state['scroll_pos1'] += 1
        
        if wave_pos2 <= width:
            text_to_show2 = line2[:wave_pos2].ljust(width)
            lcd.lcd.cursor_pos = (1, 0)
            lcd.lcd.write_string(text_to_show2)
            app_state.display_state['scroll_pos2'] += 1
            
        app_state.display_state['last_update'] = now
        
        # Wave complete when both lines fully revealed
        if app_state.display_state['scroll_pos1'] > width and app_state.display_state['scroll_pos2'] > width:
            app_state.display_state['wave_complete'] = True
            app_state.display_state['scroll_pos1'] = 0
            app_state.display_state['scroll_pos2'] = 0
            print("✨ Wave effect complete, starting scroll mode")
    
    return False  # Still in wave mode

def _update_scrolling(lcd, line1, line2, now, width, pause_time):
    """Handle scrolling animation for long text"""
    # Line 1 scrolling
    if len(line1) > width:
        _scroll_line(lcd, line1, 0, 1, now, width, pause_time)
    else:
        # Short text - just display it
        lcd.lcd.cursor_pos = (0, 0)
        lcd.lcd.write_string(line1.ljust(width))
    
    # Line 2 scrolling (same logic)
    if len(line2) > width:
        _scroll_line(lcd, line2, 1, 2, now, width, pause_time)
    else:
        lcd.lcd.cursor_pos = (1, 0)
        lcd.lcd.write_string(line2.ljust(width))

def _scroll_line(lcd, text, lcd_line, state_line, now, width, pause_time):
    """Handle scrolling for a single line"""
    pos_key = f'scroll_pos{state_line}'
    dir_key = f'scroll_dir{state_line}'
    pause_key = f'pause_until{state_line}'
    
    if app_state.display_state[pause_key] <= now:
        # Ensure position stays within valid bounds
        max_pos = len(text) - width
        pos = max(0, min(app_state.display_state[pos_key], max_pos))
        segment = text[pos:pos + width]
        lcd.lcd.cursor_pos = (lcd_line, 0)
        lcd.lcd.write_string(segment.ljust(width))
        
        # Check boundaries BEFORE moving position
        if app_state.display_state[pos_key] >= max_pos and app_state.display_state[dir_key] == 1:
            app_state.display_state[dir_key] = -1
            app_state.display_state[pause_key] = now + pause_time
            print(f"📜 Line {state_line} reached end (pos={pos}), reversing direction")
        elif app_state.display_state[pos_key] <= 0 and app_state.display_state[dir_key] == -1:
            app_state.display_state[dir_key] = 1
            app_state.display_state[pause_key] = now + pause_time  
            print(f"📜 Line {state_line} reached start (pos={pos}), reversing direction")
        else:
            # Only move position if not pausing
            app_state.display_state[pos_key] += app_state.display_state[dir_key]