# Standard libraries
import time

# Local libraries
import PixelKit as kit
import bitmapfont

# Custom code
import config
import purpleair

def fetch_dial():
    dial = kit.dial.read()
    return (dial / 4096.0)

def screen_test():
    colors = [
        purpleair.WHITE,
        purpleair.GREEN,
        purpleair.YELLOW,
        purpleair.ORANGE,
        purpleair.RED,
        purpleair.PURPLE,
        purpleair.MAROON,
        (0,0,0)
    ]
    for h in range(0,kit.HEIGHT):
        row_color = adjust_color(fetch_dial(), colors[h])
        for w in range(0,kit.WIDTH):
            kit.set_pixel(w,h,row_color)
        kit.render()
        time.sleep(0.1)

def adjust_color(brightness: float, color: tuple) -> tuple:
    if not 0 <= brightness <= 1.0:
        raise ValueError("Factor must be between 0 and 1.0")
    return tuple(int(val * brightness) for val in color)


screen_test()

bf = bitmapfont.BitmapFont(kit.WIDTH, kit.HEIGHT, kit.set_pixel)
bf.init()

while True:
    sensor_data = purpleair.fetch_sensor_data(config.CONFIG["api_key"], config.CONFIG["sensor_id"])
    purpleair.display_sensor_data(sensor_data)

    sensor = sensor_data.get("sensor", {})
    pm25 = sensor.get("pm2.5_a")
    aqi = purpleair.aqiFromPM(pm25)
    color = purpleair.aqiColor(aqi)
    color = adjust_color(fetch_dial(), color)

    value_string = "%d" % aqi
    kit.clear()
    bf.text(value_string, 0, 0, color)
    kit.render()
    time.sleep(600)
