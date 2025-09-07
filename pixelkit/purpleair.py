#!/usr/bin/env python3
"""
PurpleAir Sensor Data Retrieval

This script queries the PurpleAir API to retrieve data from a specific sensor.
It uses the API key and sensor ID from config.yml file.
"""

import os
import sys
import json
import urequests

WHITE = (255,255,255)
GREEN  = (0, 228, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 126, 0)
RED   = (255, 0, 0)
PURPLE = (143, 63, 151)
MAROON = (126, 0, 35)

def url_encode(string):
    encoded_string = ""
    for character in string:
        if character.isalpha() or character.isdigit():
            encoded_string += character
        else:
            encoded_string += f"%{ord(character):x}"
    return encoded_string

def fetch_sensor_data(api_key, sensor_id):
    """
    Fetch data for a specific sensor from PurpleAir API.

    Args:
        api_key (str): PurpleAir API key
        sensor_id (str or int): ID of the sensor to query

    Returns:
        dict: Sensor data in JSON format
    """
    base_url = "https://api.purpleair.com/v1"
    endpoint = f"/sensors/{sensor_id}"
    url = f"{base_url}{endpoint}"

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    # Fields to request from the API (can be customized based on needs)
    params = {
        # "fields": "name,latitude,longitude,altitude,humidity,temperature,pressure,last_seen,pm2.5_a,pm2.5_10minute_a,confidence"
        # "fields": "name,humidity,temperature,pressure,last_seen,pm2.5,pm2.5_10minute,confidence"
        "fields": "last_seen,pm2.5,confidence"
    }

    param_string = "fields=" + url_encode(params["fields"])

    try:
        print(f"Fetching data for sensor {sensor_id}")
        response = urequests.get(url + "?" + param_string, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            sys.exit(1)
    except ValueError as e:
        print(f"Request error: {e}")
        sys.exit(1)

def format_timestamp(timestamp):
    """
    Convert Unix timestamp to human-readable date/time.

    Args:
        timestamp (int): Unix timestamp

    Returns:
        str: Formatted date and time
    """
    if timestamp:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

def display_sensor_data(data):
    """
    Display formatted sensor data.

    Args:
        data (dict): Sensor data from PurpleAir API
    """
    try:
        sensor = data.get("sensor", {})

        # Extract basic information
        name = sensor.get("name", "Unknown")
        # last_seen = format_timestamp(sensor.get("last_seen"))

        # Extract location data
        # latitude = sensor.get("latitude")
        # longitude = sensor.get("longitude")
        # altitude = sensor.get("altitude")

        # Extract environmental readings
        # humidity = sensor.get("humidity")
        # temperature = sensor.get("temperature")
        # pressure = sensor.get("pressure")

        # Extract PM2.5 readings
        pm25 = sensor.get("pm2.5")
        # pm25_10minute = sensor.get("pm2.5_10minute")

        # Extract confidence value
        confidence = sensor.get("confidence")

        # Display the information
        print("\n=== PurpleAir Sensor Data ===")
        # print(f"Sensor Name: {name}")
        #print(f"Last Updated: {last_seen}")
        # print("\n--- Location ---")
        # print(f"Latitude: {latitude}")
        # print(f"Longitude: {longitude}")
        # print(f"Altitude: {altitude} meters")
        # print("\n--- Environmental Conditions ---")
        # print(f"Humidity: {humidity}%")
        # print(f"Temperature: {temperature}°C")
        # print(f"Pressure: {pressure} hPa")
        print("\n--- Air Quality (PM2.5) ---")
        print(f"Current pm2.5: {pm25} µg/m³")
        # print(f"Average pm2.5: {pm25_10minute} µg/m³")
        print(f"Current AQI from pm2.5: {aqiFromPM(pm25)}")
        print(f"Confidence: {confidence}%")
        print("\n================================")

    except KeyError as e:
        print(f"Error parsing API response: {e}")
        print("Could not parse all sensor data. Response format may have changed.")
        print("Raw data:", json.dumps(data, indent=2))

# Convert US AQI from raw pm2.5 data
def aqiFromPM(pm):
    if not float(pm):
        return "-"
    if pm == 'undefined':
        return "-"
    if pm < 0:
        return pm
    if pm > 1000:
        return "-"
    """
                                        AQI   | RAW PM2.5
    Good                               0 - 50 | 0.0 – 12.0
    Moderate                         51 - 100 | 12.1 – 35.4
    Unhealthy for Sensitive Groups  101 – 150 | 35.5 – 55.4
    Unhealthy                       151 – 200 | 55.5 – 150.4
    Very Unhealthy                  201 – 300 | 150.5 – 250.4
    Hazardous                       301 – 400 | 250.5 – 350.4
    Hazardous                       401 – 500 | 350.5 – 500.4
    """

    if pm > 350.5:
        return calcAQI(pm, 500, 401, 500.4, 350.5)  # Hazardous
    elif pm > 250.5:
        return calcAQI(pm, 400, 301, 350.4, 250.5)  # Hazardous
    elif pm > 150.5:
        return calcAQI(pm, 300, 201, 250.4, 150.5)  # Very Unhealthy
    elif pm > 55.5:
        return calcAQI(pm, 200, 151, 150.4, 55.5)  # Unhealthy
    elif pm > 35.5:
        return calcAQI(pm, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups
    elif pm > 12.1:
        return calcAQI(pm, 100, 51, 35.4, 12.1)  # Moderate
    elif pm >= 0:
        return calcAQI(pm, 50, 0, 12, 0)  # Good
    else:
        return 'undefined'

def aqiColor(aqi):
    aqi = round(aqi)
    if aqi > 300.5:
        return MAROON
    elif aqi > 201.5:
        return PURPLE
    elif aqi > 151.5:
        return RED
    elif aqi > 101.5:
        return ORANGE
    elif aqi > 51.5:
        return YELLOW
    elif aqi > 0:
        return GREEN
    else:
        return WHITE


# Calculate AQI from standard ranges
def calcAQI(Cp, Ih, Il, BPh, BPl):
    a = (Ih - Il)
    b = (BPh - BPl)
    c = (Cp - BPl)
    return round((a / b) * c + Il)


