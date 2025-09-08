# TODO

## Soon
[ ] If `confidence` is low, error
[ ] Some kind of time / freshness indicator
[ ] Smaller font

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
