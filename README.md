# PurpleAir AQI Display for Kano PixelKit

## First time setup
1. Ensure you have mpremote installed (`pipx install mpremote`)
2. Copy `example-config.py` to `config.py`
3. Edit `config.py` to set your WIFI and PurpleAir details
4. Install Micropython 1.26+ on the Kano PixelKit
5. Copy files to the device with mpremote, reset device, enjoy!

This command will copy all files, then reset the device and leave the serial connection attached. To leave the connection, press `ctl-x`. 

`mpremote cp -r boot.py config.py main.py lib : + reset repl`

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

## Pixelfont library

Uses the pixelfonts package from https://github.com/benders/micropython-pixelfonts

Library can be updated with:
```sh
micropython -m mip install github:benders/micropython-pixelfonts --target lib
```

## Install MicroPython Stubs
```sh
# Install stubs for a specific version.
pip install -U micropython-esp32-stubs~=1.26.0 --target typings --no-user
```

## Running Tests

The project uses pytest for unit testing. Tests are located in the `tests/` directory.

### Setting up for testing

1. Install development dependencies:
   ```sh
   pip install -r requirements-dev.txt
   ```

2. Make sure you are in the project root directory.

### Running all tests

```sh
pytest
```

### Running specific tests

To run tests for a specific module:
```sh
pytest tests/test_utils.py
pytest tests/test_purpleair.py
```

To run a specific test case:
```sh
pytest tests/test_utils.py::TestFormatTime
pytest tests/test_purpleair.py::TestUrlEncode
```

To run a specific test method:
```sh
pytest tests/test_utils.py::TestFormatTime::test_format_time_8_tuple
```

### Test coverage

To run tests with coverage report:
```sh
pytest --cov=lib
```

## Test Organization

- `tests/test_utils.py`: Tests for utility functions in the `utils.py` module.
- `tests/test_purpleair.py`: Tests for PurpleAir API interaction and AQI calculations in the `purpleair.py` module.

Test cases are organized by function or logical group of functions within each test file.

## Error Handling

The application is designed to be resilient against various types of errors:

### Network Error Handling

- **API Errors**: When the PurpleAir API returns error status codes, the application will log the error, display a blank screen, and retry after a shorter timeout.
- **Network Connectivity**: If network connectivity issues occur, the application catches the errors, logs them, and continues operation without crashing.
- **JSON Parsing Errors**: If response data cannot be parsed, the application handles the error gracefully.

### Main Loop Resilience

- The main loop is designed to never exit due to errors.
- If sensor data cannot be retrieved, the display shows a blank screen instead of invalid data.
- The system automatically retries failed operations after a short delay.
- All error states are logged to the console for debugging.

### Testing Error Conditions

The test suite includes comprehensive tests for error conditions:
- API error responses
- Network connectivity issues
- Data parsing problems

Run the error handling tests with:
```sh
pytest tests/test_purpleair.py::TestFetchSensorData::test_fetch_sensor_data_api_error
pytest tests/test_purpleair.py::TestFetchSensorData::test_fetch_sensor_data_network_error
pytest tests/test_purpleair.py::TestFetchSensorData::test_fetch_sensor_data_value_error
```
