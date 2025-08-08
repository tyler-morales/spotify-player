# DEPRECATED: Legacy page module kept for reference only. Use main.py flow.
# pages/clock.py
import time

def render(lcd, button_pin=None):
    now = time.strftime("%a %H:%M:%S")
    date = time.strftime("%b %d, %Y")
    
    # Clear and show time without infinite scroll
    lcd.clear()
    lcd.write_line_wave("Current Time", line=0)
    lcd.write_line_wave(now, line=1)
