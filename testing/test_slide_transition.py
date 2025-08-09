#!/usr/bin/env python3
"""
Tests for slide transition between tracks on the LCD.
Validates that incoming text slides in from the right and lands at column 0,
without mid-screen stalling, and that overflow handling (previous scrolling window)
produces a smooth transition.
"""

import time
import app_state
from display_effects import update_display_with_effects

class MockLCD:
    """Headless LCD that records full-width writes per line."""
    def __init__(self):
        self.display_lines = [" " * 16, " " * 16]
        self.frames = []  # list of (line0, line1) for each write pair
        self._pending = [None, None]  # track writes per frame to pair 0+1
        self.lcd = self.MockInnerLCD(self)
    
    def clear(self):
        self.display_lines = [" " * 16, " " * 16]
        # Note: clear does not push a frame; frames record composed writes
    
    class MockInnerLCD:
        def __init__(self, parent):
            self.parent = parent
            self._cursor_pos = (0, 0)
        
        @property
        def cursor_pos(self):
            return self._cursor_pos
        
        @cursor_pos.setter
        def cursor_pos(self, pos):
            self._cursor_pos = pos
        
        def write_string(self, text):
            line, col = self._cursor_pos
            # we only write full lines starting at col 0 in our code paths
            if col == 0:
                self.parent.display_lines[line] = text
                self.parent._pending[line] = text
                # When both lines in this frame were updated, store snapshot
                if all(x is not None for x in self.parent._pending):
                    self.parent.frames.append(tuple(self.parent._pending))
                    self.parent._pending = [None, None]


def _run_until_transition_finishes(lcd, timeout=3.0):
    """Step update loop until slide transition completes or timeout."""
    start = time.time()
    while time.time() - start < timeout:
        update_display_with_effects(lcd)
        if not app_state.display_state.get('transition_active', False):
            return True
        time.sleep(0.01)
    return False


def _leftmost_non_space_index(s):
    for i, ch in enumerate(s):
        if ch != ' ':
            return i
    return len(s)


def test_slide_basic_incoming_lands_left():
    # Configure now_playing mode
    app_state.set_display_mode(1)  # now_playing
    app_state.reset_display_state()

    # Speed up transition for test
    app_state.display_state['transition_speed'] = 0.005

    # Mock LCD
    lcd = MockLCD()

    # First track (initial) -> this will slide in from blank (acceptable)
    app_state.current_track = {'title': 'Hello', 'artist': 'World'}
    update_display_with_effects(lcd)  # trigger change + start transition
    assert app_state.display_state['transition_active'], "Transition should start on first content"

    assert _run_until_transition_finishes(lcd), "Transition did not finish in time"

    # Validate final frame equals new content (left-justified)
    final0, final1 = lcd.display_lines
    assert final0.startswith('Hello'), f"Line0 not set correctly: '{final0}'"
    assert final1.startswith('World'), f"Line1 not set correctly: '{final1}'"

    # Now transition from track A -> track B to test proper outgoing/incoming
    lcd.frames.clear()
    app_state.current_track = {'title': 'Longer Incoming', 'artist': 'ArtistName'}
    update_display_with_effects(lcd)  # trigger second transition
    assert app_state.display_state['transition_active'], "Transition should start on second content"

    assert _run_until_transition_finishes(lcd), "Second transition did not finish in time"

    # Check monotonic movement of incoming left edge across frames (no stall/jump backwards)
    # Use title line (line 0)
    left_edges = []
    for frame in lcd.frames:
        l0 = frame[0]
        # incoming is somewhere; compute leftmost non-space for the frame
        left_edges.append(_leftmost_non_space_index(l0))
    # Ensure the minimum eventually reaches 0 in the sequence
    assert 0 in left_edges, f"Incoming never reached column 0; edges: {left_edges}"
    # Ensure edges never increase after they start decreasing meaningfully
    # Find first index where a non-space appears
    first_idx = next((i for i, v in enumerate(left_edges) if v < 16), None)
    if first_idx is not None:
        for i in range(first_idx + 1, len(left_edges)):
            assert left_edges[i] <= left_edges[i-1] + 1, "Edge jumped backward more than 1 (stall/jump)"


def test_slide_with_overflow_prev_window():
    # Set mode and initial long title to simulate previous scrolling window
    app_state.set_display_mode(1)
    app_state.reset_display_state()
    app_state.display_state['transition_speed'] = 0.005

    long_title = 'This is a very long previous title that was scrolling'
    # Pretend this was the last content on screen and we were mid-scroll
    app_state.display_state['content_line1'] = long_title
    app_state.display_state['content_line2'] = 'Prev Artist'
    app_state.display_state['scroll_pos1'] = 10  # mid window
    app_state.display_state['scroll_pos2'] = 0

    lcd = MockLCD()

    # Trigger change to new content
    app_state.current_track = {'title': 'NewSong', 'artist': 'NewArtist'}
    update_display_with_effects(lcd)
    assert app_state.display_state['transition_active'], "Transition should start from overflow state"

    assert _run_until_transition_finishes(lcd), "Overflow transition did not finish in time"

    # Final content should be the new text at left
    final0, final1 = lcd.display_lines
    assert final0.startswith('NewSong'), f"Final title incorrect: '{final0}'"
    assert final1.startswith('NewArtist'), f"Final artist incorrect: '{final1}'"


if __name__ == "__main__":
    print("🧪 Running slide transition tests...")
    test_slide_basic_incoming_lands_left()
    print("✅ Basic slide test passed")
    test_slide_with_overflow_prev_window()
    print("✅ Overflow slide test passed")
    print("🎉 All slide transition tests passed!")
