import XInput
import truck_telemetry
import time

class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.value = None

    def update(self, new_value):
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1.0 - self.alpha) * self.value
        return self.value

def map_to_vibration(rpm, idle_rpm, max_rpm, throttle, speed, gear_changed, accel, engine_running, t_since_engine_toggle):
    """
    Realistic RPM-to-controller-vibration mapping.
    Returns (left_motor_0_to_1, right_motor_0_to_1)
    """
    is_starting = engine_running and t_since_engine_toggle < 2.0
    is_stopping = not engine_running and t_since_engine_toggle < 2.0
    
    off_threshold = idle_rpm * 0.7
    if (not engine_running and rpm < off_threshold and not is_stopping) or (rpm < 100 and not is_starting and not is_stopping):
        return 0.0, 0.0
        
    left = 0.0
    right = 0.0
    
    chug_limit = idle_rpm + 750.0 
    powerband_start = idle_rpm + 650.0
    
    # 1. Idle & Low RPM Chugging 
    if rpm < chug_limit:
        # Fades from max at idle_rpm to 0 at chug_limit
        range_size = chug_limit - idle_rpm
        if range_size <= 0: range_size = 500.0
        chug_intensity = max(0.0, 1.0 - ((rpm - idle_rpm) / range_size))
        
        # Alternating/pulsing: Mostly left motor, slightly shifting emphasis
        t = time.perf_counter()
        cycle = int(t * 2.0) % 2  # Deep slower toggle (~500ms)
        if cycle == 0:
            left += 0.8 * chug_intensity
            right += 0.05 * chug_intensity
        else:
            left += 0.5 * chug_intensity
            right += 0.25 * chug_intensity
            
    # 2. Power Band & High RPM Curve
    if rpm >= powerband_start:
        safe_max_rpm = max(max_rpm, powerband_start + 500)
        strain_rpm = rpm - powerband_start
        strain_max = safe_max_rpm - powerband_start
        
        ratio = min(1.0, max(0.0, strain_rpm / strain_max))
        
        # Increased base value and sharpness
        intensity = ratio ** 1.6
        
        right += 0.25 + (intensity * 0.9)
        left += 0.20 + (intensity * 0.5)
        
    # 3. Load/throttle multiplier
    throttle_factor = max(0.55, throttle * 1.5)
    left *= throttle_factor
    right *= throttle_factor
    
    # 4. Speed/terrain road rumble mixed in
    # Subtle road mix: Add a tiny constant base (light cabin shake even when stationary)
    road_rumble = 0.03 + min(0.35, abs(speed) * 0.012)
    left += road_rumble
    right += road_rumble
    
    # 5. Acceleration/Braking boost 
    if abs(accel) > 0.1: 
        accel_boost = min(0.5, abs(accel) * 1.0)
        left += accel_boost
        right += accel_boost * 0.7
        
    # 6. Gear Shift kick
    if gear_changed:
        left = max(left, 1.0)
        right = max(right, 1.0)
        
    # 7. Engine start/stop gentle shake
    if is_starting:
        shake = min(1.0, max(0.0, 1.0 - abs(1.0 - t_since_engine_toggle)))
        left = max(left, 0.5 * shake)
        right = max(right, 0.3 * shake)
    elif is_stopping:
        shake = max(0.0, 1.0 - (t_since_engine_toggle / 2.0))
        left *= shake
        right *= shake

    # Clamp everything between 0.0 and 1.0
    left = max(0.0, min(1.0, left))
    right = max(0.0, min(1.0, right))
    
    return left, right

def main():
    # Optimisation & smoothness tips: Update rate exactly 60 Hz 
    # (Prompt requested 30 Hz at start but 60 Hz at end, 60 Hz offers better smoothness)
    UPDATE_RATE = 60
    INTERVAL = 1.0 / UPDATE_RATE
    
    rpm_filter = LowPassFilter(0.25)
    throttle_filter = LowPassFilter(0.30)
    
    last_speed = 0.0
    last_gear = 0
    last_rpm_raw = 0.0
    
    engine_was_running = False
    last_engine_toggle_time = 0.0
    
    print("--- ATS Telemetry Rumble (Realistic Diesel V2) ---")
    print(f"--- Running at {UPDATE_RATE} Hz ---")
    print("--- Press Ctrl+C to stop ---")
    
    count = 0
    while True:
        try:
            truck_telemetry.init()
            print("✅ Connected to ATS Telemetry. Waiting for game to start...")
            break
        except Exception:
            count += 1
            if count == 5:
                count = 2
            if count == 1:
                print("Is game turned on????")
                print("Is plugin connected????")
            time.sleep(1)

    try:
        while True:
            start_t = time.perf_counter()
            
            data = truck_telemetry.get_data()
            
            if not data or data.get('paused', False):
                XInput.set_vibration(0, 0, 0)
                # Still sleep to maintain loop timing
                elapsed = time.perf_counter() - start_t
                if INTERVAL > elapsed:
                    time.sleep(INTERVAL - elapsed)
                continue

            # Fetch telemetry values
            # Handle float conversions safely as sometimes they can be None or weird types depending on plugin
            raw_rpm = float(data.get('engineRpm', 0.0) or 0.0)
            max_rpm_val = data.get('engineRpmMax', 2500.0)
            max_rpm = float(max_rpm_val) if max_rpm_val else 2500.0
            
            idle_rpm_val = data.get('engineRpmIdle', 550.0)
            idle_rpm = float(idle_rpm_val) if idle_rpm_val else 550.0
            
            throttle = float(data.get('throttle', 0.0) or data.get('gameThrottle', 0.0) or 0.0)
            speed = float(data.get('speed', 0.0) or 0.0)
            gear = data.get('gear', 0)
            engine_running = bool(data.get('engineEnabled', False))
            
            # Deadzone: ignore RPM changes smaller than 20 RPM
            if abs(raw_rpm - last_rpm_raw) < 20:
                raw_rpm = last_rpm_raw
            else:
                last_rpm_raw = raw_rpm
                
            # Apply low-pass filters
            rpm = rpm_filter.update(raw_rpm)
            filtered_throttle = throttle_filter.update(throttle)
            
            # Calculate simple acceleration (current_speed - previous_speed)
            accel = speed - last_speed
            last_speed = speed
            
            # Gear shifts
            gear_changed = False
            if gear != last_gear:
                gear_changed = True
                last_gear = gear
                
            # Engine on/off transitions
            if engine_running != engine_was_running:
                engine_was_running = engine_running
                last_engine_toggle_time = start_t
                
            t_since_engine_toggle = start_t - last_engine_toggle_time
            
            # map_to_vibration logic
            left_val, right_val = map_to_vibration(
                rpm=rpm,
                idle_rpm=idle_rpm,
                max_rpm=max_rpm,
                throttle=filtered_throttle,
                speed=speed,
                gear_changed=gear_changed,
                accel=accel,
                engine_running=engine_running,
                t_since_engine_toggle=t_since_engine_toggle
            )
            
            # Scale to 0-65535 for XInput
            left_motor = int(left_val * 65535)
            right_motor = int(right_val * 65535)
            
            XInput.set_vibration(0, left_motor, right_motor)
            
            # Precise timing: sleep remaining time
            elapsed = time.perf_counter() - start_t
            sleep_time = INTERVAL - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Always set vibration to 0 when script exits
        print("\nStopping rumble...")
        XInput.set_vibration(0, 0, 0)
        print("Script terminated.")

if __name__ == "__main__":
    main()