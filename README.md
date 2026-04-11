# ESP32 LED Lightstrip Web Controller

This project uses MicroPython on an ESP32 board to control an LED lightstrip via a web interface. Colors are selected using an interactive color wheel, and brightness can be adjusted with a slider. Changes are applied automatically without needing to click buttons.

## Features

- Interactive color wheel showing RGB color space
- White light option (center of wheel)
- Brightness control slider (0-255)
- Party/demo mode with animated rainbow and sparkle effects
- Adjustable speed slider for the party light show
- Real-time color updates
- PIN-protected access with 60-second timeout
- Web server running on ESP32
- Mobile-friendly interface

## Hardware Requirements

- ESP32 board (the currently connected device identifies as `ESP32_GENERIC_S2`)
- WS2812 or compatible LED lightstrip
- Jumper wires
- Power supply for the LED strip (if needed, depending on strip length)

## Circuit Diagram

See [circuit_diagram.txt](circuit_diagram.txt) for detailed connection instructions.

## Project Structure

- `boot.py`: WiFi connection setup (runs on boot)
- `main.py`: Web server and LED control logic
- `index.html`: Web interface with color wheel and brightness slider
- `credentials.py`: WiFi credentials (not committed to git)
- `README.md`: This file
- `circuit_diagram.txt`: Circuit connection details
- `scripts/local_preview_server.py`: Separate reusable local web UI preview server

## Software Setup

1. **Install MicroPython on ESP32S3:**
   - Download the latest MicroPython firmware for ESP32S3 from [micropython.org](https://micropython.org/download/esp32/)
   - Use esptool.py or Thonny IDE to flash the firmware to your ESP32S3 board.

2. **Upload the code:**
   - Upload all files (`boot.py`, `main.py`, `index.html`, `credentials.py`) to the ESP32S3 using Thonny IDE, uPyCraft, or ampy.
   - Update WiFi credentials in `credentials.py` (SSID and PASSWORD).
   - Update LED configuration in `main.py` (`NUM_LEDS` and `PIN`).

3. **Run the code:**
   - Reset the ESP32S3. It will connect to WiFi and start the web server.
   - Note the IP address printed in the serial console.

4. **Access the web interface:**
   - Open a web browser and go to `http://<ESP32_IP>`
   - Enter the PIN (default: 1234) to unlock the controls.
   - Click on the color wheel to select colors or adjust brightness with the slider.
   - Changes are applied automatically to the LED strip.

## Usage

- **PIN Access**: Enter the 4-digit PIN to unlock the color controls. Default PIN is 1234.
- **Color Selection**: Click anywhere on the color wheel. The center provides white light.
- **Brightness**: Use the slider to adjust overall brightness (0 = off, 255 = full).
- **Party mode speed**: When party mode is enabled, a speed slider appears so you can slow down or speed up the light show.
- **Timeout**: Controls lock after 60 seconds of inactivity, requiring PIN re-entry.
- **PIN disabling**: Set `pin_disabled = True` in `credentials.py` to skip PIN input altogether.
- **Mobile**: The interface works on mobile devices connected to the same WiFi network.

VS Code is configured to use the local `typings/` stubs for `machine`, `neopixel`, and `network` while editing.

## Local UI Preview (No Device Required)

A separate reusable preview server is included so you can test the web interface on your Mac without an ESP32 connected.

1. Start the preview server from the project folder:

   ```bash
   python3 scripts/local_preview_server.py --root . --port 8000
   ```

   Or in VS Code run the task `Local UI Preview`.
   Then you can run the task `Open Local UI Preview` to open it automatically.

2. Open the preview in your browser:

   ```text
   http://127.0.0.1:8000
   ```

3. Optional flags:
   - `--pin 1234` to inject a custom preview PIN
   - `--pin-disabled` to skip the PIN prompt
   - `--root /path/to/project` to reuse the same preview tool in another project

The color wheel, brightness slider, party mode toggle, and party speed slider will all respond locally, while the mock server logs the actions in the terminal.

## Deploy to the ESP32

With the board connected over USB, deploy the current files with:

```bash
./scripts/deploy.sh
```

Notes:

- The script auto-detects the board serial port.
- You can also pass a port explicitly, for example:

  ```bash
  ./scripts/deploy.sh /dev/cu.usbmodem101
  ```

- In VS Code, run the task `Deploy to ESP32`.

## Notes

- Ensure your device is on the same WiFi network as the ESP32 for access.
- For longer strips, use an external power supply to avoid overloading the ESP32.
- The color wheel represents the full RGB color gamut achievable with LED strips.
- For security, consider adding authentication if deploying in a public network.
- Ensure the ESP32S3 has sufficient power; use external power for the LED strip if necessary.
