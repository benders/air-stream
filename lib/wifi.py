import network
import config
import time

def draw_logo(x0, y0, pixel_function, *args, **kwargs):
    WIFI_LOGO = [
        '..######..',
        '.########.',
        '##......##',
        '#..####..#',
        '..######..',
        '..#....#..',
        '....##....',
        '....##....',
    ]

    for y, row in enumerate(WIFI_LOGO):
        for x, col in enumerate(row):
            if col == '#':
                pixel_function(x + x0, y + y0, *args, **kwargs)

def isconnected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()

def do_connect():
    # Constants for connection
    MAX_RETRIES = 10        # Number of retries before resetting WLAN
    SHORT_DELAY = 1000      # Milliseconds between connection attempts
    CONNECTION_TIMEOUT = 20 # Seconds to wait for connection before timeout
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    try:
        if not wlan.isconnected():
            print('Connecting to network... ' + config.CONFIG['ssid'])
            
            # Reset connection state
            wlan.disconnect()
            wlan.active(False)

            time.sleep(1)  # Brief pause after disconnect

            # Attempt to connect
            wlan.active(True)
            wlan.connect(config.CONFIG['ssid'], config.CONFIG['psk'])
            
            # Set a deadline for connection attempt
            start_time = time.ticks_ms()
            retry_count = 0
            
            # Wait for connection with timeout
            while not wlan.isconnected():
                # Check for timeout
                if time.ticks_diff(time.ticks_ms(), start_time) > CONNECTION_TIMEOUT * 1000:
                    print(f"Connection timeout after {CONNECTION_TIMEOUT} seconds")
                    break
                
                # Periodically check status
                status = wlan.status()
                if status == network.STAT_CONNECTING:
                    print("Still connecting...")
                elif status == network.STAT_WRONG_PASSWORD:
                    print("Wrong password! Check your config.")
                    raise ValueError("Wrong password")
                elif status == network.STAT_NO_AP_FOUND:
                    print("Network not found! Check SSID in config.")
                    raise ValueError("Network not found")
                elif status == network.STAT_CONNECT_FAIL:
                    print("Connection failed!")
                    raise Exception("Connection failed")
                else:
                    raise Exception("Unknown connection error")

                time.sleep_ms(SHORT_DELAY)
                
        # If successfully connected, print info and exit
        if wlan.isconnected():
            print('Connected! Network config:', wlan.ifconfig())
            return True
        
    except OSError as e:
        print(f"Network error: {e}")
        print("Resetting WLAN adapter...")
        try:
            wlan.active(False)
            time.sleep(2)
            wlan.active(True)
        except Exception as e2:
            print(f"Error resetting WLAN: {e2}")
        time.sleep(5)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(5)
    
    return False

if __name__ == "__main__":
    import PixelKit as kit

    kit.clear()
    draw_logo(3, 0, kit.set_pixel, (0x10, 0x10, 0x10))
    kit.render()
