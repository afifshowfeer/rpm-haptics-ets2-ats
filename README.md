<div align="center">
  <h1>🎮 TruckSim Realistic Engine Rumble V2</h1>
  <p><strong>High-Performance Native Plugin • C++</strong><br>
  Realistic controller vibration for ETS2 & ATS</p>

  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++"/>
  <img src="https://img.shields.io/badge/ETS2-232F3E?style=for-the-badge&logo=steam&logoColor=white" alt="ETS2"/>
  <img src="https://img.shields.io/badge/ATS-232F3E?style=for-the-badge&logo=steam&logoColor=white" alt="ATS"/>
  <img src="https://img.shields.io/badge/XInput-Rumble-green?style=for-the-badge" alt="Rumble"/>
</div>

<br>

## ✨ What's New in V2

**Major Upgrade:** Fully rewritten in **C++** as a **native SCS plugin** (`.dll`).

### Key Improvements:
- Much better performance (60 FPS smooth)
- Lower latency
- More stable
  
## 🎯 Features

- Realistic diesel idle chugging (alternating motors)
- Power band strain & high-RPM buzz
- Throttle load sensitivity
- Road rumble based on speed
- Strong gear shift kicks
- Engine start & stop animations (2-second transitions)
- Acceleration/braking jolts
- Smart engine off guard (no ghost vibration)
- Low-pass filters + deadzone for smoothness

## 📥 Installation (Super Simple)

1. Download the latest **`.dll`** from Releases
2. Copy it to:
   - **ETS2**: `...\Euro Truck Simulator 2\bin\win_x64\plugins\`
   - **ATS**: `...\American Truck Simulator\bin\win_x64\plugins\`
3. (Create the `plugins` folder if it doesn't exist)
4. Start the game

**No Python, no extra programs needed.**

## 🎮 How to Use

- Just drive normally
- Vibration activates automatically when the engine is running
- Works with any XInput-compatible controller ( Primarly Xbox controllers).

## 📋 Requirements

- ETS2 or ATS (latest version recommended)
- Windows 10/11 (64-bit)
- Controller with vibration support

## 🔧 For Developers

Source code is included. Feel Free to make changes.

## 📝 Changelog

### V2.0 (Current)
- Complete rewrite in C++
- Native plugin (no external Python script)
- Improved smoothing & timing
- Better engine start/stop behavior
- More accurate gear shift detection
- Optimized performance

### V1.0
- Original Python version


---

**Made with ❤️ for the truck sim community**

Happy trucking & rumbling! 🚛💨
