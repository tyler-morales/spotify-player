# 🔌 GPIO Wiring Guide

## Button Connections

Each button connects between a GPIO pin and Ground (GND):

```
Raspberry Pi GPIO Layout:
                    3V3  (1) (2)  5V    
                   GPIO2 (3) (4)  5V    
                   GPIO3 (5) (6)  GND   
                   GPIO4 (7) (8)  GPIO14
                     GND (9) (10) GPIO15
                  GPIO17 (11)(12) GPIO18  ← PREV & PLAY buttons
                  GPIO27 (13)(14) GND    ← NEXT button & GND
                  GPIO22 (15)(16) GPIO23  ← CYCLE button
                     3V3 (17)(18) GPIO24
                  GPIO10 (19)(20) GND
                   GPIO9 (21)(22) GPIO25
                  GPIO11 (23)(24) GPIO8
                     GND (25)(26) GPIO7
```

## Button Wiring:

### PREV Button (GPIO 17):
- Connect one side to GPIO 17 (Pin 11)
- Connect other side to GND (Pin 9, 14, 20, 25, or 39)

### PLAY/PAUSE Button (GPIO 18):
- Connect one side to GPIO 18 (Pin 12)  
- Connect other side to GND

### NEXT Button (GPIO 27):
- Connect one side to GPIO 27 (Pin 13)
- Connect other side to GND (Pin 14 is convenient)

### CYCLE Button (GPIO 22):
- Connect one side to GPIO 22 (Pin 15)
- Connect other side to GND

## LCD Connection (I2C):
- VCC → 3V3 (Pin 1 or 17)
- GND → GND (any GND pin)
- SDA → GPIO 2 (Pin 3)
- SCL → GPIO 3 (Pin 5)

## Notes:
- No pull-up/pull-down resistors needed (software configured)
- All buttons are active HIGH (pressed = 3.3V, released = 0V)
- Use momentary push buttons (not latching switches)
- Any gauge wire is fine for buttons (22-26 AWG recommended)