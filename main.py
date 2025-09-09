# Standard libraries
import time
import json
import urandom

# Local libraries
import PixelKit as kit
# import ntptime

# Custom code
import config
import purpleair
import utils
from pixelfonts import Font4x7

def fetch_dial():
    dial = kit.dial.read()
    return (dial / 8192.0 + 0.05)

def screen_test():
    colors = [
        purpleair.WHITE,
        purpleair.GREEN,
        purpleair.YELLOW,
        purpleair.ORANGE,
        purpleair.RED,
        purpleair.PURPLE,
        purpleair.MAROON,
        purpleair.WHITE
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

def display_sensor_metadata(data):
    try:
        sensor = data.get("sensor", {})

        # Extract basic information
        name = sensor.get("name", "Unknown")
        last_seen_utc = time.gmtime(sensor.get("last_seen"))
        last_seen = utils.format_time(last_seen_utc)

        # Display the information
        print("\n=== PurpleAir Sensor Metadata ===")
        print(f"Sensor Updated: {last_seen} (UTC)")
        print(f"Sensor Name: {name}")
        print("\n--- Location ---")
        print(f"Latitude: {sensor.get("latitude")}")
        print(f"Longitude: {sensor.get("longitude")}")
        print(f"Altitude: {sensor.get("altitude")} meters")
        print("================================\n")

    except KeyError as e:
        print(f"Error parsing API response: {e}")
        print("Could not parse all sensor data. Response format may have changed.")
        print("Raw data:", json.dumps(data, indent=2))


def display_sensor_data(data):
    try:
        sensor = data.get("sensor", {})
        time_stamp = data.get("time_stamp")

        last_seen_stamp = sensor.get("last_seen")
        last_seen = utils.format_time(time.gmtime(last_seen_stamp))

        age = time_stamp - last_seen_stamp

        pm25 = sensor.get("pm2.5")
        # confidence = sensor.get("confidence", None)

        print("\n=== PurpleAir Sensor Data ===")
        print(f"Sensor Updated: {last_seen} (UTC)")
        print(f"{age} seconds ago")
        # print("\n--- Environmental Conditions ---")
        # print(f"Humidity: {humidity}%")
        # print(f"Temperature: {temperature}°C")
        # print(f"Pressure: {pressure} hPa")
        print("\n--- Air Quality (PM2.5) ---")
        print(f"Current pm2.5: {pm25} µg/m³")
        print(f"Current AQI from pm2.5: {purpleair.aqiFromPM(pm25)}")
        # print(f"Confidence: {confidence}%")
        print("================================\n")

    except KeyError as e:
        print(f"Error parsing API response: {e}")
        print("Could not parse all sensor data. Response format may have changed.")
        print("Raw data:", json.dumps(data, indent=2))

#
# Initialize, then run forever
#

if __name__ == "__main__":
    screen_test()

    # Initialize the RTC
    # ntptime.settime()

    bf = Font4x7(kit.WIDTH, kit.HEIGHT, kit.set_pixel)

    METADATA_FIELDS = ["name", "latitude", "longitude", "altitude", "last_seen"]
    # AIR_QUALITY_FIELDS = ["pm2.5", "confidence", "humidity", "temperature", "pressure"]
    AIR_QUALITY_FIELDS = ["pm2.5", "last_seen"]

    sensor_metadata = purpleair.fetch_sensor_data(config.CONFIG["api_key"], config.CONFIG["sensor_id"], METADATA_FIELDS)
    print(sensor_metadata)
    display_sensor_metadata(sensor_metadata)

    UPDATE_DELAY_SEC = 120
    deadline = 0
    
    aqi = 999
    raw_color = purpleair.WHITE

    while True:
        # Refresh the sensor data if it is stale
        if time.ticks_diff(time.ticks_ms(), deadline) > 0:
            sensor_data = purpleair.fetch_sensor_data(config.CONFIG["api_key"], config.CONFIG["sensor_id"], AIR_QUALITY_FIELDS)
            print(sensor_data)
            display_sensor_data(sensor_data)
            sensor = sensor_data.get("sensor", {})
            pm25 = sensor.get("pm2.5")
            aqi = purpleair.aqiFromPM(pm25)
            raw_color = purpleair.aqiColor(aqi)

            # Set new deadline
            deadline = time.ticks_add(time.ticks_ms(), UPDATE_DELAY_SEC * 1000)
            deadline = time.ticks_add(deadline, urandom.randrange(0, 30 * 1000))
            print(f"Update in {time.ticks_diff(deadline, time.ticks_ms()) / 1000} seconds")

        color = adjust_color(fetch_dial(), raw_color)

        value_string = "%3d" % aqi
        kit.clear()
        bf.text(value_string, 0, 0, color)
        kit.render()
        time.sleep(0.1)
