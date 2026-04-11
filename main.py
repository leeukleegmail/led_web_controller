import machine
import neopixel
import socket
import time
import credentials

# LED strip configuration
NUM_LEDS = 64  # Number of LEDs in the strip
PIN = 5  # GPIO pin connected to the data line of the LED strip
PARTY_STEP_MS = 120

np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)
current_color = '#FFFFFF'
party_mode = False
party_offset = 0
last_party_update = 0

ticks_ms = time.ticks_ms  # pyright: ignore[reportAttributeAccessIssue]
ticks_diff = time.ticks_diff  # pyright: ignore[reportAttributeAccessIssue]


def web_page():
    try:
        with open('index.html', 'r') as f:
            html = f.read()
    except OSError:
        return '<h1>Error: Could not load index.html</h1>'

    html = html.replace("let PIN = '0000';", "let PIN = '%s';" % credentials.PIN)
    html = html.replace("let PIN_DISABLED = false;", "let PIN_DISABLED = %s;" % str(credentials.pin_disabled).lower())
    return html


def hex_to_rgb(color_hex):
    return (
        int(color_hex[1:3], 16),
        int(color_hex[3:5], 16),
        int(color_hex[5:7], 16),
    )


def apply_color(color_hex):
    r, g, b = hex_to_rgb(color_hex)
    for i in range(NUM_LEDS):
        np[i] = (r, g, b)
    np.write()
    print('Color set to %s' % color_hex)


def set_color(color_hex):
    global current_color, party_mode
    current_color = color_hex
    party_mode = False
    apply_color(color_hex)


def hsv_to_rgb(hue, saturation=1.0, value=1.0):
    hue = hue % 360
    chroma = value * saturation
    x = chroma * (1 - abs((hue / 60) % 2 - 1))
    m = value - chroma

    if hue < 60:
        r1, g1, b1 = chroma, x, 0
    elif hue < 120:
        r1, g1, b1 = x, chroma, 0
    elif hue < 180:
        r1, g1, b1 = 0, chroma, x
    elif hue < 240:
        r1, g1, b1 = 0, x, chroma
    elif hue < 300:
        r1, g1, b1 = x, 0, chroma
    else:
        r1, g1, b1 = chroma, 0, x

    return (
        int((r1 + m) * 255),
        int((g1 + m) * 255),
        int((b1 + m) * 255),
    )


def run_party_mode_step():
    global party_offset, last_party_update

    for i in range(NUM_LEDS):
        hue = ((i * 360) // NUM_LEDS + party_offset * 12) % 360
        r, g, b = hsv_to_rgb(hue)

        if i == party_offset % NUM_LEDS or i == (party_offset + NUM_LEDS // 2) % NUM_LEDS:
            r, g, b = 255, 255, 255

        np[i] = (r, g, b)

    np.write()
    party_offset = (party_offset + 1) % NUM_LEDS
    last_party_update = ticks_ms()


def set_party_mode(enabled):
    global party_mode, party_offset, last_party_update
    party_mode = enabled
    party_offset = 0
    last_party_update = 0

    if enabled:
        print('Party mode on')
        run_party_mode_step()
    else:
        print('Party mode off')
        apply_color(current_color)


def send_response(conn, body, content_type='text/plain', status='200 OK'):
    headers = 'HTTP/1.1 %s\r\nContent-Type: %s\r\nConnection: close\r\n\r\n' % (status, content_type)
    conn.sendall(headers.encode('utf-8'))
    if isinstance(body, str):
        body = body.encode('utf-8')
    conn.sendall(body)


def get_request_body(request):
    header_end = request.find('\r\n\r\n')
    if header_end == -1:
        return ''
    return request[header_end + 4:].strip()


def handle_client(conn):
    request = conn.recv(1024).decode('utf-8', 'ignore')

    if 'GET / ' in request:
        send_response(conn, web_page(), content_type='text/html')
    elif 'POST /set_color' in request:
        color = get_request_body(request)
        if color.startswith('#') and len(color) == 7:
            set_color(color)
        send_response(conn, 'Color set')
    elif 'POST /set_mode' in request:
        mode_value = get_request_body(request).lower()
        enabled = mode_value in ('party=on', 'party=true', 'party=1', 'on', 'true', '1')
        set_party_mode(enabled)
        send_response(conn, 'Party mode on' if enabled else 'Party mode off')
    else:
        send_response(conn, 'Not found', status='404 Not Found')


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 80))
    server.listen(5)
    server.settimeout(PARTY_STEP_MS / 1000)

    # Set default colour
    set_color(current_color)

    while True:
        if party_mode and ticks_diff(ticks_ms(), last_party_update) >= PARTY_STEP_MS:
            run_party_mode_step()

        try:
            conn, addr = server.accept()
        except OSError:
            continue

        print('Connection from', addr)
        try:
            handle_client(conn)
        finally:
            conn.close()


def main():
    start_server()


if __name__ == '__main__':
    main()