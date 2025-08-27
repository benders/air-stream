# PurpleAir API Sensor Data Retrieval Script

## Plan
1. Read the configuration from config.yml (API key and sensor ID)
2. Set up HTTP request to the PurpleAir API
3. Send a GET request to retrieve sensor data
4. Parse and process the JSON response
5. Display the relevant information in a structured format
6. Handle errors and edge cases
7. Add proper documentation

## API Endpoints
Based on the API documentation, we need to use:
- Base URL: https://api.purpleair.com/v1
- Endpoint for single sensor: /sensors/:sensor_index
- Authentication: API key sent as a query parameter

## Implementation Status
- [x] Set up configuration loading
- [x] Implement HTTP request with proper headers
- [x] Process and parse response
- [x] Format and display data
- [x] Add error handling
- [ ] Add command-line arguments (optional)
- [x] Write documentation

## Usage
1. Ensure you have the required Python packages installed:
   ```
   pip install pyyaml requests
   ```
2. Make sure your config.yml contains valid API key and sensor ID
3. Run the script:
   ```
   ./probe.py
   ```

## Notes
- The script currently requests specific fields from the API. These can be customized in the `fetch_sensor_data` function.
- Error handling is implemented for common failure scenarios.
- Timestamps are converted to human-readable format.
