import time
from lcd import LCD

# Setup
lcd = LCD()

# Song data
title = "6 AM Mimosa"
artist = "DJ BORING"

try:
    lcd.clear()
    
    # Display track title & artist
    lcd.display(title, artist)

except KeyboardInterrupt:
    lcd.clear()
    pass 
finally:
    lcd.clear()
