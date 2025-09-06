# PurpleAir AQI Display for Kano PixelKit

## First time setup
1. Ensure you have mpremote installed (`pipx install mpremote`)
2. Copy `example-config.py` to `config.py`
3. Edit `config.py` to set your WIFI and PurpleAir details
4. Install Micropython 1.26+ on the Kano PixelKit
5. Copy files to the device with mpremote, reset device, enjoy!

This command will copy all files, then reset the device and leave the serial connection attached. To leave the connection, press `ctl-x`. 

`mpremote cp -r *.py *.bin lib : + reset repl`

## Connect PixelKit as a serial device
1. Install VCP driver from https://ftdichip.com/drivers/vcp-drivers/
2. After reboot, it should appear as `/dev/tty.usbserial-*` or similar

## Installing MicroPython on the PixelKit (retail)

1. Install esptool (`pipx install esptool`)
2. Download from and follow instructions on https://micropython.org/download/ESP32_GENERIC/

More information at https://docs.micropython.org/en/latest/esp32/tutorial/intro.html

Example:
```sh
esptool erase_flash
esptool write_flash 0x1000 ~/Downloads/ESP32_GENERIC-20250809-v1.26.0.bin
```

## External libraries
* https://github.com/adafruit/micropython-adafruit-bitmap-font/blob/master/bitmapfont.py
* mpremote mip install ntptime



