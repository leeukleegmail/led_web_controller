import network
import time
import credentials

# Connect to WiFi
print("Connecting wifi")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(credentials.SSID, credentials.PASSWORD)

while not wlan.isconnected():
    time.sleep(1)
    print("Attempting to connect to network")

print('Connected to WiFi')
ip = wlan.ifconfig()[0]
print('IP address:', ip)
