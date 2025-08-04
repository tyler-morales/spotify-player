import RPi.GPIO as GPIO
import time
from lcd import LCD
from pages import clock, now_playing, debug

BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lcd = LCD()

class ClockPage:
    def display(self):
        clock.render(lcd, button_pin=BUTTON_PIN)

class NowPlayingPage:
    def display(self):
        now_playing.render(lcd, button_pin=BUTTON_PIN)

class DebugPage:
    def display(self):
        debug.render(lcd, button_pin=BUTTON_PIN)

pages = [ClockPage(), NowPlayingPage(), DebugPage()]
page_idx = 0

try:
    while True:
        print(f"Displaying page {page_idx}: {type(pages[page_idx]).__name__}")
        
        # Check button state before display
        initial_button_state = GPIO.input(BUTTON_PIN)
        
        pages[page_idx].display()  # This may return early if button pressed
        
        # Check if display was interrupted by button press
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            print("Button pressed during display! Swapping page.")
            # Wait for button release to avoid repeated triggering
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                time.sleep(0.05)
        else:
            # Normal case - wait for button press
            print("Waiting for button press...")
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.05)
            print("Button pressed! Swapping page.")
        
        page_idx = (page_idx + 1) % len(pages)
        time.sleep(0.1)  # Debounce
        lcd.clear()  # Clear LCD before switching pages
finally:
    lcd.clear()
    GPIO.cleanup()
