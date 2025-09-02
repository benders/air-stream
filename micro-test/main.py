# Write your code here :-)
import PixelKit as kit
import time
import config

def fetch_dial():
    dial = kit.dial.read()
    return round(dial / 4096.0 * 99)

def fetch_temp():
    import esp32
    return esp32.raw_temperature()

import purpleair

import bitmapfont

bf = bitmapfont.BitmapFont(16,8, kit.set_pixel)
bf.init()

while True:
    sensor_data = purpleair.fetch_sensor_data(config.CONFIG["api_key"], config.CONFIG["sensor_id"])
    purpleair.display_sensor_data(sensor_data)

    sensor = sensor_data.get("sensor", {})
    pm25 = sensor.get("pm2.5_a")
    aqi = purpleair.aqiFromPM(pm25)

    value_string = "%d" % aqi
    kit.clear()
    bf.text(value_string, 0, 0, (0, 0, 0x10))
    kit.render()
    time.sleep(600)

# from neopixel_matrix import NeoPixelMatrix, Color
# np_matrix = NeoPixelMatrix(pin=kit.NEOPIXEL_PIN, width=16, height=8, direction=NeoPixelMatrix.HORIZONTAL, brightness=0.1)
# np_matrix.text("0", 0, 0, color=Color.BLUE)
