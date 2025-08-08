# 🔄 **CYCLE Button Hold Restart/Restart-Service Feature**

## 📋 **Overview**
This feature provides a robust recovery mechanism that allows users to perform a clean reboot of the Spotify LCD Player by holding the CYCLE button for 5 seconds. By default, it restarts the application process. You can optionally configure it to restart a systemd service (recommended in production) or reboot the OS.

## 🎯 **Purpose**
- **Recovery**: Clean restart without SSH access or power cycling
- **Robustness**: Handle stuck states, memory issues, or software glitches
- **User Experience**: Simple, intuitive recovery mechanism
- **Reliability**: Proper cleanup and graceful restart

## 🎮 **How It Works**

### **Button Behavior**
- **Quick Press (< 5s)**: Normal display mode cycling (now_playing → clock → debug)
- **Hold (≥ 5s)**: Triggers clean reboot sequence

### **Reboot Sequence**
1. **Detection**: CYCLE button held for exactly 5 seconds
2. **Feedback**: LCD displays "Rebooting..." status
3. **Cleanup**: GPIO cleanup, state reset
4. **Restart**: Program restarts using `os.execv()`
5. **Recovery**: Fresh application state

## 🔧 **Technical Implementation**

### **Hold Detection Logic**
```python
# Tracks button press duration
hold_start_times = {name: None for name in BUTTON_PINS}
hold_triggered = {name: False for name in BUTTON_PINS}

# Continuous monitoring during hold
hold_duration = current_time - hold_start_times['CYCLE']
if hold_duration >= 5.0 and not hold_triggered['CYCLE']:
    trigger_reboot()
```

### **Safety Features**
- **Single Trigger**: Prevents multiple reboots during one hold
- **Debounce Protection**: Won't trigger on button bounce
- **State Reset**: Clears hold tracking on button release
- **Error Handling**: Graceful fallback if restart fails

### **Clean Restart Process**
```python
def handle_cycle_hold():
    # 1. User feedback
    lcd.lcd.cursor_pos = (0, 0)
    lcd.lcd.write_string("Rebooting...".ljust(16))
    lcd.lcd.cursor_pos = (1, 0)
    lcd.lcd.write_string("Please wait...".ljust(16))
    
    # 2. GPIO cleanup
    GPIO.cleanup()
    
    # 3. Program restart
    python_executable = sys.executable
    script_args = [python_executable] + sys.argv
    os.execv(python_executable, script_args)
```

## 📊 **Configuration**

### **Timing Parameters**
- **Hold Duration**: 5.0 seconds (configurable)
- **Debounce**: 0.3 seconds (existing)
- **Feedback Delay**: Immediate LCD update

### **Button Mapping**
- **CYCLE Button**: GPIO 22 (existing)
- **Function**: Dual-mode (press/hold)
- **Priority**: Hold takes precedence over press

### **Restart Modes (environment variables)**
- **RESTART_MODE**: process | service | reboot (default: process)
- **SERVICE_NAME**: spotify-player.service (used when RESTART_MODE=service)

## 🛡️ **Safety Considerations**

### **Accidental Trigger Prevention**
- **5-Second Duration**: Long enough to prevent accidents
- **Visual Feedback**: Clear indication before reboot
- **State Tracking**: Prevents multiple triggers
- **Release Reset**: Clears hold state on button release

### **Error Recovery**
- **GPIO Cleanup**: Proper resource cleanup
- **Exception Handling**: Graceful error handling
- **Fallback**: Manual restart instructions if needed
- **State Preservation**: No data corruption during restart

## 🎨 **User Experience**

### **Visual Feedback**
```
LCD Display During Reboot:
┌─────────────────┐
│ Rebooting...    │
│ Please wait...  │
└─────────────────┘
```

### **Console Output**
```
🔄 CYCLE button held for 5 seconds - initiating reboot...
🔄 Restarting Spotify Player...
✅ Ready! No more LCD corruption or threading issues.
```

## 🔄 **Use Cases**

### **When to Use**
- **Stuck Display**: LCD showing incorrect or frozen content
- **Memory Issues**: High memory usage or slow performance
- **API Problems**: Spotify API connection issues
- **State Corruption**: Application state inconsistencies
- **Development**: Quick restart during testing

### **When NOT to Use**
- **Normal Operation**: Use quick press for mode cycling
- **Network Issues**: Won't fix network connectivity problems
- **Hardware Issues**: Won't fix physical button or LCD problems

## 📈 **Benefits**

### **Reliability**
- **Self-Recovery**: No external intervention needed
- **Clean State**: Fresh application state after restart
- **Resource Cleanup**: Proper memory and GPIO cleanup
- **Error Isolation**: Isolates software issues from hardware

### **User Experience**
- **Intuitive**: Natural extension of existing button behavior
- **Accessible**: No technical knowledge required
- **Fast**: Quick recovery without power cycling
- **Safe**: Won't cause data loss or corruption

### **Maintenance**
- **Remote Recovery**: Can recover from remote locations
- **Development**: Faster iteration during development
- **Debugging**: Quick reset for testing scenarios
- **Production**: Reliable recovery mechanism for end users

## 🔮 **Future Enhancements**

### **Potential Improvements**
- **Configurable Duration**: User-adjustable hold time
- **Multiple Hold Actions**: Different actions for different hold durations
- **Status Indication**: Visual countdown during hold
- **Confirmation**: Double-hold for critical operations
- **Logging**: Reboot reason tracking and logging

### **Advanced Features**
- **Safe Mode**: Boot with minimal features for troubleshooting
- **Factory Reset**: Complete reset to default settings
- **Update Mode**: Boot into update/configuration mode
- **Diagnostic Mode**: Boot with enhanced logging and debugging

## 📝 **Implementation Notes**

### **File Changes**
- **button_handler.py**: Enhanced with hold detection logic
- **No other files**: Self-contained feature

### **Dependencies**
- **Existing**: Uses current GPIO and LCD infrastructure
- **No New**: No additional packages or libraries required

### **Testing**
- **Unit Tests**: Hold duration and trigger logic
- **Integration**: Full reboot sequence testing
- **Edge Cases**: Button bounce, rapid presses, power issues

---

## 🔧 **Recent Fixes**

### **Issues Resolved**
1. **Reboot Not Working**: Fixed `os.execv()` argument format
2. **Welcome Screen Missing**: Fixed display mode initialization and LCD message display
3. **Button Cycling**: Fixed display mode cycling logic to properly skip welcome mode

### **Technical Fixes**
- **os.execv() Format**: Changed from `['python3'] + sys.argv` to `[python_executable] + sys.argv`
- **LCD Display**: Changed from non-existent `write_line()` to direct `lcd.cursor_pos` and `write_string()`
- **Mode Cycling**: Fixed cycling logic to properly handle welcome mode (index 0) and cycle through functional modes
- **Welcome Content**: Added "Welcome :)" / "Starting up..." content in display_manager.py

### **Verification**
- ✅ Reboot command construction works correctly
- ✅ LCD reboot message displays properly
- ✅ Welcome screen appears after reboot
- ✅ Button cycling works after reboot
- ✅ Hold detection logic functions correctly

---

## 🎉 **Summary**

The CYCLE button hold reboot feature provides a robust, user-friendly recovery mechanism that enhances the reliability and maintainability of the Spotify LCD Player. It follows established patterns for embedded systems while maintaining the simplicity and elegance of the existing codebase.

**Key Value**: Enables users to recover from software issues without technical intervention, making the system more robust and user-friendly in production environments.

## Recommendations
- **Development**: process
- **Production under systemd**: service (ensures logs, restarts, and watchdogs work properly)
- **Hardware/OS fault recovery**: reboot