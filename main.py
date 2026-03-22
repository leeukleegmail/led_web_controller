import machine
import neopixel
import socket
import credentials

# LED strip configuration
NUM_LEDS = 8  # Number of LEDs in the strip
PIN = 5  # GPIO pin connected to the data line of the LED strip (adjust for ESP32S3)

# Initialize NeoPixel strip
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

# Load HTML page from file
def load_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except:
        return '<h1>Error: Could not load index.html</h1>'

html = load_html()
# Inject PIN and pin_disabled flag from credentials into HTML
html = html.replace("let PIN = '0000';", "let PIN = '%s';" % credentials.PIN)
html = html.replace("let PIN_DISABLED = false;", "let PIN_DISABLED = %s;" % str(credentials.pin_disabled).lower())

def web_page():
    return html

def set_color(color_hex):
    # Parse hex color to RGB
    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)
    # Set all LEDs to the selected color
    for i in range(8):
        np[i] = (r, g, b)
    np.write()
    print(f'Color set to {color_hex}')

# Start web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Set default colour
set_color("#FFFFFF")

while True:
    conn, addr = s.accept()
    print('Connection from', addr)
    request = conn.recv(1024)
    request = request.decode('utf-8')
    
    if 'GET / ' in request:
        response = web_page()
        conn.send('HTTP/1.1 200 OK\r\n')
        conn.send('Content-Type: text/html\r\n')
        conn.send('Connection: close\r\n\r\n')
        conn.sendall(response)
    elif 'POST /set_color' in request:
        # Extract the color from the POST body
        header_end = request.find('\r\n\r\n')
        if header_end != -1:
            color = request[header_end + 4:].strip()
            set_color(color)
        conn.send('HTTP/1.1 200 OK\r\n')
        conn.send('Content-Type: text/plain\r\n')
        conn.send('Connection: close\r\n\r\n')
        conn.sendall('Color set')
    
    conn.close()