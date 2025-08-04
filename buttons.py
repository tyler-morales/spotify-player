import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD
from lcd import LCD# assuming this is your lcd class

# === Config ===
BUTTON_PINS = {
    'A': 17,
    'B': 18,
    'C': 27,
}
DEBOUNCE = 0.2  # seconds

# === Setup LCD ===
lcd = LCD()
lcd.clear()

GPIO.setmode(GPIO.BCM)
for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counts = {name: 0 for name in BUTTON_PINS}
last_states = {name: GPIO.LOW for name in BUTTON_PINS}

print("Press any button (A/B/C)!")

try:
    while True:
        for name, pin in BUTTON_PINS.items():
            state = GPIO.input(pin)
            if state == GPIO.HIGH and last_states[name] == GPIO.LOW:
                counts[name] += 1
                now = time.strftime('%H:%M:%S')
                msg = f"[{now}] Button {name} ({pin}) pressed! Total: {counts[name]}"
                print(msg)
                lcd.clear()
                lcd.write_line_wave(f"{name} pressed!", line=0)
                lcd.write_line_wave(f"Total: {counts[name]}", line=1)
                time.sleep(DEBOUNCE)
            last_states[name] = state
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    lcd.clear()
    lcd.write_line("Goodbye!", line=0)
    GPIO.cleanup()
