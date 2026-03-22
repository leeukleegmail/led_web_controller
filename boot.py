import network
import time

# WiFi credentials - Update these with your network details
SSID = 'WIFI@HOME'
PASSWORD = '78P@55word'

# Connect to WiFi
print("Connecting wifi")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)
    print("Attempting to connect to network")

print('Connected to WiFi')
ip = wlan.ifconfig()[0]
print('IP address:', ip)
