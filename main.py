import network
import time
from ota_updater import OTAUpdater

SSID = '' #Set WiFi SSID
PASSWORD = '' #Set WiFi Password
GIT_REPO = 'https://github.com/ghvinerias/esp32-universal-remote' #Change With your repo


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting...")
        time.sleep(1)
    print("Connected! IP:", wlan.ifconfig()[0])

def check_for_updates():
    ota = OTAUpdater(GIT_REPO)
    ota.install_update_if_available()

connect_wifi()
check_for_updates()

# run app
try:
    import app.app_main as app_main
    app_main.run()
except Exception as e:
    print("App failed:", e)

