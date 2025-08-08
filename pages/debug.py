# pages/debug.py
# DEPRECATED: Legacy page module kept for reference only. Use main.py flow.

import time
import os

def render(lcd, button_pin=None):
    # Get current date and time
    date = time.strftime("%b %d, %Y")
    current_time = time.strftime("%H:%M:%S")
    
    # Get system uptime from /proc/uptime (Linux only)
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        uptime_hours = int(uptime_seconds // 3600)
        uptime_mins = int((uptime_seconds % 3600) // 60)
        uptime_str = f"{uptime_hours}h{uptime_mins}m"
    except:
        uptime_str = "N/A"
    
    # Display debug info
    line1 = f"Debug: {date}"
    line2 = f"Up:{uptime_str} {current_time}"
    
    lcd.clear()
    lcd.write_line_wave(line1, line=0)
    lcd.write_line_wave(line2, line=1)