from machine import Pin, I2C
import network
import urequests
import ujson
import ssd1306
import time

# ==== WiFi connection ====
#ssid = ''
#password = ''

#sta = network.WLAN(network.STA_IF)
#sta.active(True)
#sta.connect(ssid, password)

#while not sta.isconnected():
#    print('Connecting to WiFi...')
#    time.sleep(1)
#
#ip_address = sta.ifconfig()[0]
#print('Connected:', ip_address)

# ==== OLED ====
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ==== Menus ====
main_menu = ["Load Remote", "Item kutu", "Item 3", "Item 4", "Item 5", "Item 6", "Check for Updates"]
submenu_item_6 = ["..", "Load Remote", "SubItem 2", "SubItem 3", "SubItem 4", "SubItem 5"]
menu_stack = [main_menu]
current_index = 0
dynamic_submenu = []

# ==== Rotary Encoder ====
pin_clk = Pin(18, Pin.IN, Pin.PULL_UP)
pin_dt = Pin(19, Pin.IN, Pin.PULL_UP)
pin_btn = Pin(5, Pin.IN, Pin.PULL_UP)

last_clk = pin_clk.value()

debounce_time = 0
debounce_delay = 300  # ms


def ota_update():
    try:
        oled.fill(0)
        oled.text("Checking for", 0, 0)
        oled.text("updates...", 0, 8)
        oled.show()

        response = urequests.get("http://10.10.10.187:3000/main.py")
        if response.status_code == 200:
            print("Status code:", response.status_code)
            with open('main.py', 'w') as f:
                f.write(response.text)
            oled.fill(0)
            oled.text("Update done!", 0, 20)
            oled.text("Restarting...", 0, 30)
            oled.show()
            time.sleep(2)
            machine.reset()
        else:
            oled.fill(0)
            oled.text("No update", 0, 0)
            oled.text("available.", 0, 8)
            oled.show()
            print("OTA failed:", e)
            time.sleep(2)
            draw_menu(menu_stack[-1], current_index)

        response.close()

    except Exception as e:
        oled.fill(0)
        oled.text("Update failed!", 0, 8)
        oled.show()
        print("OTA failed:", e)
        time.sleep(2)
        draw_menu(menu_stack[-1], current_index)

# ==== Functions ====

def draw_menu(menu, selected_index):
    oled.fill(0)
    oled.text("Ultimate Remote", 0, 0)
    oled.text(ip_address, 0, 8)
    oled.hline(0, 15, 128, 1)

    max_visible = 4  # number of items visible at once
    top_index = max(0, selected_index - max_visible + 1) if selected_index >= max_visible else 0

    for i in range(top_index, min(top_index + max_visible, len(menu))):
        prefix = "> " if i == selected_index else "  "
        oled.text(prefix + menu[i], 0, 18 + (i - top_index) * 10)

    oled.show()


def fetch_menu():
    global dynamic_submenu
    try:
        response = urequests.get('https://api.npoint.io/1ba7bf0b976b13ec8630')
        json_data = response.json()
        response.close()
        items = json_data.get('menu_items', [])
        dynamic_submenu = [".."] + items  # prepend ".."
        print('Fetched menu:', dynamic_submenu)
        if dynamic_submenu:
            menu_stack.append(dynamic_submenu)
            return True
        else:
            return False
    except Exception as e:
        print('Fetch failed:', e)
        return False

# ==== Initial display ====
draw_menu(menu_stack[-1], current_index)

# ==== Main loop ====
while True:
    clk_val = pin_clk.value()
    dt_val = pin_dt.value()

    now = time.ticks_ms()

    if clk_val != last_clk:
        if time.ticks_diff(now, debounce_time) > debounce_delay:
            debounce_time = now
            if dt_val != clk_val:
                current_index = (current_index + 1) % len(menu_stack[-1])
            else:
                current_index = (current_index - 1) % len(menu_stack[-1])
            draw_menu(menu_stack[-1], current_index)
    last_clk = clk_val

    if pin_btn.value() == 0:
        current_menu = menu_stack[-1]
        selected_item = current_menu[current_index]

        if selected_item == "..":
            if len(menu_stack) > 1:
                menu_stack.pop()
            current_index = 0
            draw_menu(menu_stack[-1], current_index)

        elif current_menu == main_menu and selected_item == "Load Remote":
            oled.fill(0)
            oled.text("Loading...", 0, 20)
            oled.show()
            if fetch_menu():
                current_index = 0
                draw_menu(menu_stack[-1], current_index)
            else:
                oled.fill(0)
                oled.text("Fetch failed", 0, 20)
                oled.show()
                time.sleep(1)
                draw_menu(menu_stack[-1], current_index)
        
        elif current_menu == main_menu and selected_item == "Check for Updates":
            ota_update()
                
        elif current_menu == main_menu and selected_item == "Item 6":
            menu_stack.append(submenu_item_6)
            current_index = 0
            draw_menu(menu_stack[-1], current_index)

            if selected_item == "..":
                if len(menu_stack) > 1:
                    menu_stack.pop()
                current_index = 0
                draw_menu(menu_stack[-1], current_index)

        else:
            oled.fill(0)
            oled.text("Selected:", 0, 0)
            oled.text(selected_item, 0, 20)
            oled.show()
            time.sleep(1)
            draw_menu(menu_stack[-1], current_index)

        # wait for button release
        while pin_btn.value() == 0:
            time.sleep(0.01)

    time.sleep(0.01)




