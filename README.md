<div align="center">
  <h1>🎮 TruckSim Wheel Vibration (RPM-Based)</h1>
  <p><strong>Realistic controller rumble based on your truck's engine RPM</strong><br>Works with ETS2 & ATS</p>
  
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/ETS2-232F3E?style=for-the-badge&logo=steam&logoColor=white" alt="ETS2"/>
  <img src="https://img.shields.io/badge/ATS-232F3E?style=for-the-badge&logo=steam&logoColor=white" alt="ATS"/>
  <img src="https://img.shields.io/badge/Controller-Rumble-green?style=for-the-badge" alt="Rumble"/>
</div>

<br>

## ✨ What it does

This Python script reads your **truck's engine RPM** in real-time from **Euro Truck Simulator 2** or **American Truck Simulator** and translates it into **vibration/rumble feedback** on your controller (wheel or gamepad).

- Idle → gentle vibration  
- Revving / high RPM → strong, aggressive rumble  
- Perfect for adding immersion with wheels like Logitech G29/G920, Thrustmaster, or even Xbox/PS controllers!

<br>

## 🎮 Features

- Real-time RPM → vibration mapping
- Adjustable vibration intensity & sensitivity
- Supports **ETS2** and **ATS**
- Works with most controllers that support vibration (XInput compatible)
- Lightweight & low CPU usage

<br>

## 📋 Requirements

- Python 3.8+
- Windows (tested on Win10/11)
- **SCS SDK** enabled in game (see Setup below)
- Game running in **windowed** or **borderless** mode (recommended)
- Controller connected & recognized by Windows

**Python packages** (install with `pip`):


pip install pywin32
# Optional - if your script uses it:
# pip install scssdk


## 🛠️ How it works (Simple)

1. Reads telemetry data (RPM) from SCS SDK / shared memory
2. Maps RPM value → vibration strength (0–65535 range for XInput)
3. Sends rumble commands to your controller via pywin32 / XInput

## 🚀 Quick Setup Guide

This guide helps you get the vibration running in ETS2 or ATS in under 10 minutes.

### 1. Download the Python Script

- Go to: https://github.com/afifshowfeer/rpm-haptics-ets2-ats
- Click **Code** → **Download ZIP** (or clone with Git)
- Extract to any folder (e.g. `C:\MyProjects\TruckVibration`)

### 2. Download & Install the SCS Telemetry SDK Plugin

The game needs a DLL plugin to share telemetry data.

**Recommended (2025/2026 compatible):**
- Go to: https://github.com/RenCloud/scs-sdk-plugin
- Download the latest DLL from Releases (usually `scs-sdk-plugin.dll`)

**Alternative sources:**
- https://github.com/nlhans/ets2-sdk-plugin/releases
- https://github.com/Funbit/ets2-telemetry-server (includes DLL)

**Installation steps:**

1. Find your game folder (default Steam paths):
   - **ETS2:** `C:\Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2`
   - **ATS:** `C:\Program Files (x86)\Steam\steamapps\common\American Truck Simulator`

2. Go to `bin\win_x64` (use `win_x86` only if 32-bit – rare)

3. Create folder `plugins` if it doesn't exist

4. Copy the DLL into: `...\bin\win_x64\plugins\`

→ Start the game once → you should see "SDK plugin loaded" message

### 3. Install Python Dependencies (One-time)

Open Command Prompt / PowerShell in your script folder and run:
```bash
pip install pywin32
```

### 4. Run the Script & Play!

1. Connect your controller (make sure vibration works in Windows)
2. Start ETS2 or ATS first (important!)
3. In your script folder run:
```bash
python truck-haptics.py
```

**Vibration behavior:**
- Starts automatically when engine is running
- Gentle at idle/low RPM
- Stronger at high revs
- Stops completely if:
  - Engine is turned off
  - Game is paused (Esc menu)
  - You exit the game

Enjoy the extra immersion! 🚛💨

## Troubleshooting Tips

- **No vibration?** → Test in Windows "Set up USB game controllers" → check rumble there
- **Script can't find game?** → Run game first, try script as Administrator
- **DLL not loading?** → Use 64-bit version for modern Windows/ETS2
- **Still issues?** → Check console output and share errors

## 🙌 Contributing

Pull requests are welcome! Ideas:
- Linux/macOS support
- Better deadzone / curve mapping
- Support for more wheels/controllers

---

Made with ❤️ for all truckers out there  
Happy trucking & rumbling! 🛣️🔊
