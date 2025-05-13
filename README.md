# ESP32-RoboDash 🚗📶
A Wi-Fi controlled robot powered by the ESP32 microcontroller. This project features real-time motion control via a web interface, adjustable speed and obstacle stop distance using sliders.
CHECK THE VIDEO : https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7325943913406521344?compact=1

## 🌟 Features

- Control robot movements (forward, back, left, right, stop) via a web interface.
- Adjustable speed and stop distance using interactive sliders.
- Autonomous stop-and-reverse behavior based on obstacle detection using an ultrasonic sensor.
- Operates in Access Point (AP) mode — no external Wi-Fi required.

---

## 📦 Installation

### 🔧 Hardware Requirements

- ESP32 Dev Board  
- Motor driver module (e.g., L298N)  
- 2 DC motors + wheels  
- Ultrasonic sensor (HC-SR04)  
- Power supply (battery pack or USB)  
- Jumper wires + Breadboard

### 📲 Software Requirements

- [Thonny IDE](https://thonny.org/) or [uPyCraft](https://randomnerdtutorials.com/install-uPyCraft-ide-windows/)  
- Python 3.x  
- MicroPython firmware flashed on ESP32  
- Web browser (for control interface)

### 🔌 Flashing & Uploading Code

1. Flash MicroPython firmware to your ESP32 (if not already):
   ```bash
   esptool.py --chip esp32 erase_flash
   esptool.py --chip esp32 --baud 460800 write_flash -z 0x1000 esp32-xxxxxx.bin
   ```

2. Open your IDE and upload the following files:
   - `main.py` (your robot's main control script)

3. Restart the ESP32. You should see a Wi-Fi network named `ESP32_Robot`.

---

## 🚀 Usage

1. Connect your computer or phone to the `ESP32_Robot` Wi-Fi network (password: `12345678`).
2. Open your browser and go to `http://192.168.4.1`.
3. Use the buttons to control direction and the sliders to:
   - Adjust **Speed**
   - Set **Stop Distance**
4. The terminal screen at the bottom will display real-time status such as:
   - Commands sent
   - Current distance readings
   - Automatic behavior (e.g., reversing when an object is too close)

---

## 🛠️ Configuration

You can tweak the default values in `main.py`:

```python
speed = 300              # Default motor speed (range: 100–1023)
stop_distance = 25       # Distance threshold (in cm) to stop or reverse
```

Modify the HTML UI or Python logic to add more sensors, modes (e.g., line-following), or new UI features.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to your branch: `git push origin feature-name`
5. Open a Pull Request

Please follow best practices, comment your code, and test thoroughly before submitting.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy building and expanding your ESP32 robotic projects! 🤖🚀
