from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)


oled.fill(0)
oled.text("Hello, ESPHome!", 0, 0)
oled.hline(0, 8, 128, 1)
oled.hline(0, 9, 128, 1)
oled.hline(0, 10, 128, 1)
oled.hline(0, 11, 128, 1)
oled.hline(0, 12, 128, 1)
oled.hline(0, 13, 128, 1)
oled.hline(0, 14, 128, 1)
oled.hline(0, 15, 128, 1)
oled.text("Hello, ESPHome!", 0, 16)
oled.text("Hello, ESPHome!", 0, 16)
oled.show()


