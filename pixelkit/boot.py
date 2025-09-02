# This file is executed on every boot (including wake-boot from deepsleep)
# import esp

#esp.osdebug(None)
#import webrepl
#webrepl.start()

import config

def do_connect():
    import machine
    import network
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(CONFIG['ssid'], CONFIG['psk'])
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

do_connect()
