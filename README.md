# ESP32S3 LED Lightstrip Web Controller

This project uses MicroPython on an ESP32S3 board to control an LED lightstrip via a web interface. The color can be selected using a color wheel (HTML5 color picker).

## Hardware Requirements

- ESP32S3 board
- WS2812 or compatible LED lightstrip
- Jumper wires
- Power supply for the LED strip (if needed, depending on strip length)

## Circuit Diagram

```
ESP32S3 Board          LED Lightstrip
-------------          -------------
GND ------------------- GND
5V  ------------------- 5V (if powered from ESP32, otherwise external power)
GPIO 48 --------------- Data In

Note: For longer strips or higher brightness, use an external 5V power supply.
Connect the external power's GND to ESP32 GND for common ground.
```

## Software Setup

1. **Install MicroPython on ESP32S3:**
   - Download the latest MicroPython firmware for ESP32S3 from [micropython.org](https://micropython.org/download/esp32/)
   - Use esptool.py or Thonny IDE to flash the firmware to your ESP32S3 board.

2. **Upload the code:**
   - Use Thonny IDE, uPyCraft, or ampy to upload `main.py` to the ESP32S3.
   - Update the WiFi credentials in `main.py` (SSID and PASSWORD).

3. **Configure LED strip:**
   - Update `NUM_LEDS` and `PIN` in `main.py` according to your setup.

4. **Run the code:**
   - Reset the ESP32S3. It will connect to WiFi and start the web server.
   - Note the IP address printed in the serial console.

5. **Access the web interface:**
   - Open a web browser and go to `http://<ESP32_IP>`
   - Use the color picker to select a color and click "Set Color" to change the LED strip color.

## Notes

- The color picker uses the browser's native color input, which provides a color wheel on most devices.
- The web server is basic and serves a single page.
- For security, consider adding authentication if deploying in a public network.
- Ensure the ESP32S3 has sufficient power; use external power for the LED strip if necessary.