# PurpleAir AQI Display for Kano PixelKit

## First time setup
1. Ensure you have mpremote installed (`pipx install mpremote`)
2. Copy `example-config.py` to `config.py`
3. Edit `config.py` to set your WIFI and PurpleAir details
4. Install Micropython 1.26+ on the Kano PixelKit
5. Copy files to the device with mpremote, reset device, enjoy!


## External libraries
* https://github.com/adafruit/micropython-adafruit-bitmap-font/blob/master/bitmapfont.py
* mpremote mip install ntptime


## Kano PixelKit (Retail) setup

1. Install VCP driver from https://ftdichip.com/drivers/vcp-drivers/
2. Install micropython 1.26+ for ESP32 https://micropython.org/download/ESP32_GENERIC/


