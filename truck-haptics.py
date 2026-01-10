import XInput
import truck_telemetry
import time
import math

# --- 💡 TUNABLE "FEEL" KNOBS ---

# --- FIX 1: Set to your actual idle RPM / max RPM ---
# (e.g., 500 RPM idle / 2400 RPM max = 0.21)
IDLE_RPM_RATIO = 0.22 

# --- FIX 2: Increased "kick" for the weak motor at idle ---
# If 500 RPM is still silent, raise this to 0.25 or 0.30
MIN_IDLE_BUZZ = 0.26  # Was 0.05, now 20%

# Min power the STRONG (left) motor needs to turn on
STRONG_MOTOR_DEAD_ZONE = 18000 

# --- FIX 3: Flatter, less exponential curve ---
# 1.0 = linear. 2.5 = very exponential.
RUMBLE_CURVE_POWER = 1.0  # Was 2.5

# Smoothing factor
SMOOTHING = 0.1 
# ---
count=0
while True:
    try:
        truck_telemetry.init() 
        print("✅ Connected to ATS Telemetry. Waiting for game to start...")
        break
    except FileNotFoundError:
        count=count+1
        if count==5:
            count=2
        if count==1:
            print("Is game is turned on????")
            print("Is plugin connected????")
        

print("--- Telemetry Rumble Script (v3 - Tuned Curve) ---")
print("--- Press Ctrl+C to stop ---")
print(f"Settings: Idle Buzz={MIN_IDLE_BUZZ}, Curve={RUMBLE_CURVE_POWER}")

current_strong_rumble = 0.0
current_weak_rumble = 0.0
target_strong_rumble = 0
target_weak_rumble = 0

last_print_time = 0
print_interval = 0.1

try:
    while True:
        data = truck_telemetry.get_data()
        
        if data:
            rpm = data.get('engineRpm', 0)
            max_rpm = data.get('engineRpmMax', 0)
            engineenabled=data.get('engineEnabled',0)
            paused=data.get('paused',0)
            
            # --- START: YOUR REQUESTED CHANGE ---
            # If RPM is below 100 (e.g., engine stalled), force all rumble off.
            if engineenabled==False or paused==True:
                target_strong_rumble = 0
                target_weak_rumble = 0
                
                # Optional: Update console to show this new state
                current_time = time.time()
                if current_time - last_print_time >= print_interval:
                    print(f"\rRPM < 100. Motors off.                                 ", end="")
                    last_print_time = current_time
            # --- END: YOUR REQUESTED CHANGE ---

            elif rpm is not None and max_rpm is not None and max_rpm > 0:
                
                rumble_ratio = min(rpm / max_rpm, 1.0)
                
                remapped_ratio = (rumble_ratio - IDLE_RPM_RATIO) / (1.0 - IDLE_RPM_RATIO)
                remapped_ratio = max(0.0, min(1.0, remapped_ratio))
                
                rumble_power = remapped_ratio ** RUMBLE_CURVE_POWER
                
                # Calculate WEAK motor target ("buzz")
                weak_ratio = MIN_IDLE_BUZZ + ((1.0 - MIN_IDLE_BUZZ) * rumble_power)
                target_weak_rumble = int(weak_ratio * 65535)

                # Calculate STRONG motor target ("rumble")
                if rumble_power > 0:
                    target_strong_rumble = int(STRONG_MOTOR_DEAD_ZONE + ((65535 - STRONG_MOTOR_DEAD_ZONE) * rumble_power))
                else:
                    target_strong_rumble = 0 # Off at idle

                # Update console
                current_time = time.time()
                if current_time - last_print_time >= print_interval:
                    print(f"\rRPM: {rpm:4.0f} | Power: {rumble_power:4.2f} | Strong: {target_strong_rumble:5d} | Weak: {target_weak_rumble:5d}  ", end="")
                    last_print_time = current_time

            else:
                target_strong_rumble = 0
                target_weak_rumble = 0
                print(f"\rOn menu or engine off. Rumble set to 0.                       ", end="")
        
        else:
            target_strong_rumble = 0
            target_weak_rumble = 0
            print(f"\rNo telemetry data received (game paused?).                         ", end="")

        # Smooth interpolation (lerp) for each motor
        current_strong_rumble += (target_strong_rumble - current_strong_rumble) * SMOOTHING
        current_weak_rumble += (target_weak_rumble - current_weak_rumble) * SMOOTHING
        
        XInput.set_vibration(0, int(current_strong_rumble), int(current_weak_rumble))
        
       # time.sleep(0.008)

finally:
    # Cleanup
    print("\nStopping rumble...")
    XInput.set_vibration(0, 0, 0)
    print("Script terminated.")