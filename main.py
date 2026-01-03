# Standard libraries
import time
import json
import machine
import urandom
import urequests

# Local libraries
import PixelKit as kit

# Custom code
import config
import purpleair
import utils
import wifi_utils

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

def show_wifi_logo(color=(0x10, 0x10, 0x10)):
    kit.clear()
    wifi_utils.draw_logo(3, 0, kit.set_pixel, color)
    kit.render()

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
        print(f"Latitude: {sensor.get('latitude')}")
        print(f"Longitude: {sensor.get('longitude')}")
        print(f"Altitude: {sensor.get('altitude')} meters")
        print("================================\n")

    except KeyError as e:
        print(f"Error parsing API response: {e}")
        print("Could not parse all sensor data. Response format may have changed.")
        print("Raw data:", json.dumps(data))
    except Exception as e:
        print(f"Error parsing sensor metadata: {e}")
        # Continue even if we can't display the metadata


# Connect to the network
def connect_to_wifi():
    print("Starting network connection...")

    # Display white logo
    show_wifi_logo((0x10, 0x10, 0x10))

    # Attempt to connect to Wi-Fi forever
    WIFI_RETRY_DELAY = 15
    while True:
        try:
            wifi_utils.do_connect()
        except Exception as e:
            print(f"Error connecting to Wi-Fi: {e}")

        if wifi_utils.isconnected():
            print("Connection successful!")
            show_wifi_logo((0x0, 0x0, 0x10)) # Blue logo
            time.sleep(1)
            break
        else:
            print(f"Connection failed, retrying in {WIFI_RETRY_DELAY} seconds...")
            show_wifi_logo((0x10, 0x0, 0x0)) # Red logo
            time.sleep(WIFI_RETRY_DELAY)
            show_wifi_logo((0x0, 0x0, 0x0)) # Black logo

#
# Initialize, then run forever
#

if __name__ == "__main__":
    # Start the watchdog timer
    UPDATE_DELAY_SEC = 120
    WATCHDOG = machine.WDT(timeout=int(UPDATE_DELAY_SEC * 2.5 * 1000))

    connect_to_wifi()
    WATCHDOG.feed()

    # Initialize the bitmap font
    font = Font4x7(kit.WIDTH, kit.HEIGHT, kit.set_pixel)

    # METADATA_FIELDS = ["name", "latitude", "longitude", "altitude", "last_seen"]
    METADATA_FIELDS = ["name", "last_seen"]
    # AIR_QUALITY_FIELDS = ["pm2.5", "confidence", "humidity", "temperature", "pressure", "last_seen"]
    AIR_QUALITY_FIELDS = ["pm2.5"]

    purpleair_client = purpleair.PurpleAirClient(urequests, config.CONFIG["api_key"])

    try:
        sensor_metadata = purpleair_client.fetch_sensor_data(config.CONFIG["sensor_id"], METADATA_FIELDS)
        print(sensor_metadata)
        display_sensor_metadata(sensor_metadata)
        WATCHDOG.feed()
    except Exception as e:
        print(f"Error fetching sensor metadata: {e}")
        # Continue with the program even if we can't get the initial metadata
    
    # Display screen test AFTER initial Metadata fetch
    screen_test()

    # Scroll the sensor name across the display
    display_name = sensor_metadata.get("sensor", {}).get("name", "NAME ERROR").upper()
    utils.scroll_text(kit, font, display_name, adjust_color(fetch_dial(), purpleair.WHITE), speed=0.1)

    deadline = 0
    
    aqi = 999
    raw_color = purpleair.WHITE

    while True:
        # Refresh the sensor data if it is stale
        if time.ticks_diff(time.ticks_ms(), deadline) > 0:
            try:
                sensor_data = purpleair_client.fetch_sensor_data(config.CONFIG["sensor_id"], AIR_QUALITY_FIELDS)
                print(sensor_data)
                sensor = sensor_data.get("sensor", {})
                pm25 = sensor.get("pm2.5")
                aqi = purpleair.aqiFromPM(pm25)
                raw_color = purpleair.aqiColor(aqi)

                # Set new deadline
                deadline = time.ticks_add(time.ticks_ms(), UPDATE_DELAY_SEC * 1000)
                deadline = time.ticks_add(deadline, urandom.randrange(0, 30 * 1000))
                print(f"Update in {time.ticks_diff(deadline, time.ticks_ms()) / 1000} seconds")
                WATCHDOG.feed()
            except OSError as e:
                print(f"OSError while fetching sensor data: {e}")
                print("Will reset in 30 seconds...")
                time.sleep(30)
                import machine
                machine.reset()
            except Exception as e:
                print(f"Error fetching sensor data: {e}")
                # Set a shorter deadline for retry on error
                deadline = time.ticks_add(time.ticks_ms(), 30 * 1000)  # Retry after 30 seconds
                print(f"Will retry in 30 seconds")
                # Set blank display on error
                raw_color = purpleair.RED
                aqi = None  # Blank display

        color = adjust_color(fetch_dial(), raw_color)

        value_string = "%3d" % aqi if aqi is not None else "ERR"  # Error if aqi is None
        kit.clear()
        font.text(value_string, 0, 0, color)
        kit.render()
        time.sleep(0.1)
