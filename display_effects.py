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
        # Content changed - trigger slide transition for now_playing, wave for others
        print(f"🔄 Display content changed: '{line1}' | '{line2}'")
        mode = app_state.get_current_mode()
        if mode == 'now_playing':
            # Capture what is currently visible to avoid jump when text was scrolling
            prev1 = app_state.display_state.get('prev_visible_line1', ' ' * 16)
            prev2 = app_state.display_state.get('prev_visible_line2', ' ' * 16)
            # Read last written content from state if available
            try:
                # If we were in scrolling mode, reconstruct the visible window
                width = 16
                if len(app_state.display_state['content_line1']) > width:
                    pos = max(0, min(app_state.display_state['scroll_pos1'], len(app_state.display_state['content_line1']) - width))
                    prev1 = app_state.display_state['content_line1'][pos:pos+width].ljust(width)
                else:
                    prev1 = app_state.display_state['content_line1'][:width].ljust(width)
                if len(app_state.display_state['content_line2']) > width:
                    pos2 = max(0, min(app_state.display_state['scroll_pos2'], len(app_state.display_state['content_line2']) - width))
                    prev2 = app_state.display_state['content_line2'][pos2:pos2+width].ljust(width)
                else:
                    prev2 = app_state.display_state['content_line2'][:width].ljust(width)
            except Exception:
                pass
            
            app_state.display_state.update({
                'content_line1': line1,
                'content_line2': line2,
                'scroll_pos1': 0,
                'scroll_pos2': 0,
                'scroll_dir1': 1,
                'scroll_dir2': 1,
                'pause_until1': 0,
                'pause_until2': 0,
                # Start slide transition
                'transition_active': True,
                'transition_step': 0,
                'transition_last_update': time.time(),
                'prev_visible_line1': prev1,
                'prev_visible_line2': prev2,
                # Skip wave for transitions; we'll slide instead, then go to scroll
                'wave_complete': True,
                'last_update': time.time()
            })
            # Do not clear here; slide uses current buffer as the base
            return True  # Content changed
        else:
            # Non-now_playing: use wave effect like before
            app_state.display_state.update({
                'content_line1': line1,
                'content_line2': line2,
                'scroll_pos1': 0,
                'scroll_pos2': 0,
                'scroll_dir1': 1,
                'scroll_dir2': 1,
                'pause_until1': 0,
                'pause_until2': 0,
                'transition_active': False,
                'transition_step': 0,
                'wave_complete': False,
                'last_update': time.time()
            })
            lcd.clear()
            return True
    
    # Update content silently for minor changes (like clock seconds)
    app_state.display_state['content_line1'] = line1
    app_state.display_state['content_line2'] = line2
    
    now = time.time()
    width = 16
    scroll_speed = 0.3
    pause_time = 4.0
    wave_speed = 0.15
    
    # If a transition is active, run it first
    if app_state.display_state.get('transition_active'):
        if _update_slide_transition(lcd, line1, line2, now, width):
            # Transition still in progress
            return False
        # Transition finished – fallthrough to scrolling
    
    # Show wave effect first for new content (only if not overridden by transition)
    if not app_state.display_state['wave_complete']:
        return _update_wave_effect(lcd, line1, line2, now, width, wave_speed)
    
    # Scrolling mode for overflow text
    if now - app_state.display_state['last_update'] >= scroll_speed:
        _update_scrolling(lcd, line1, line2, now, width, pause_time)
        app_state.display_state['last_update'] = now
    
    return False  # No content change

def _update_slide_transition(lcd, line1, line2, now, width):
    """Slide old content left out while new content slides in from right.
    Returns True while transition is active, False when finished."""
    step = app_state.display_state.get('transition_step', 0)
    speed = app_state.display_state.get('transition_speed', 0.06)
    last = app_state.display_state.get('transition_last_update', 0)
    if now - last < speed:
        return True  # wait for next frame
    
    old1 = app_state.display_state.get('prev_visible_line1', ' ' * width)
    old2 = app_state.display_state.get('prev_visible_line2', ' ' * width)
    new1_full = (line1 or '')
    new2_full = (line2 or '')
    
    # Build the new incoming windows based on step
    # We slide over exactly width frames: step from 0..width
    max_steps = width
    if step <= max_steps:
        # Compute incoming slice length for this step
        incoming_len = min(step, width)
        # Right-anchored incoming portion: take first incoming_len characters of new text
        incoming1 = new1_full[:incoming_len].rjust(incoming_len)
        incoming2 = new2_full[:incoming_len].rjust(incoming_len)
        # Outgoing portion is old text shifted left by step
        left1 = (old1[step:] if step < width else '')
        left2 = (old2[step:] if step < width else '')
        # Compose: left part + incoming from right, then pad to width
        composed1 = (left1 + incoming1).ljust(width)[:width]
        composed2 = (left2 + incoming2).ljust(width)[:width]
        
        lcd.lcd.cursor_pos = (0, 0)
        lcd.lcd.write_string(composed1)
        lcd.lcd.cursor_pos = (1, 0)
        lcd.lcd.write_string(composed2)
        
        app_state.display_state['transition_step'] = step + 1
        app_state.display_state['transition_last_update'] = now
        return True
    
    # Transition complete: render stable new frame, reset, and allow scrolling
    lcd.lcd.cursor_pos = (0, 0)
    lcd.lcd.write_string((line1[:width] if len(line1) >= width else line1).ljust(width))
    lcd.lcd.cursor_pos = (1, 0)
    lcd.lcd.write_string((line2[:width] if len(line2) >= width else line2).ljust(width))
    app_state.display_state['transition_active'] = False
    app_state.display_state['transition_step'] = 0
    app_state.display_state['last_update'] = now  # start scroll timer after slide
    # Small initial pause at ends so long text doesn't jump immediately
    app_state.display_state['pause_until1'] = now + 1.0
    app_state.display_state['pause_until2'] = now + 1.0
    return False

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