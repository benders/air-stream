```markdown
# TODO

## Soon
[ ] If `confidence` is low, error
[ ] Some kind of time / freshness indicator
[ ] Smaller font
[x] Add unit tests for purpleair.py and utils.py modules
  - [x] Set up pytest framework
  - [x] Write tests for utils.format_time
  - [x] Write tests for purpleair.url_encode
  - [x] Write tests for purpleair.aqiFromPM
  - [x] Write tests for purpleair.aqiColor
  - [x] Write tests for purpleair.calcAQI
  - [x] Write mocks for fetch_sensor_data
  - [x] Document how to run tests in README.md

## Later
[ ] Temperature and Humidity modes

## Lower priority
[ ] Why is the average data not available?
[ ] Support local sensor access
[ ] Show bootup progress before connecting

## Implementation Notes

### API Endpoints

Based on the API documentation, we need to use:
- Base URL: https://api.purpleair.com/v1
- Endpoint for single sensor: /sensors/:sensor_index
- Authentication: API key sent as a query parameter

### Testing Approach
- Use pytest for unit testing
- Create mocks for API responses to test without real API calls
- Test edge cases and error conditions
- Focus on pure functions first (those without side effects)
- Document running tests in README.md

```
