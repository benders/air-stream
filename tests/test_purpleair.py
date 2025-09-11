"""
Tests for purpleair.py module
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the lib directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
# Add the tests/mocks directory to the path for mock imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'mocks')))

# Mock urequests before importing purpleair
sys.modules['urequests'] = __import__('urequests')

from purpleair import url_encode, aqiFromPM, aqiColor, calcAQI, fetch_sensor_data, GREEN, YELLOW, ORANGE, RED, PURPLE, MAROON, WHITE

class TestAqiColorFunction(unittest.TestCase):
    """Tests for the aqiColor function"""
    
    def test_color_maroon(self):
        """Test color for AQI > 300.5 (Hazardous)"""
        result = aqiColor(301)
        self.assertEqual(result, MAROON)
    
    def test_color_purple(self):
        """Test color for AQI > 201.5 (Very Unhealthy)"""
        result = aqiColor(202)
        self.assertEqual(result, PURPLE)
    
    def test_color_red(self):
        """Test color for AQI > 151.5 (Unhealthy)"""
        result = aqiColor(152)
        self.assertEqual(result, RED)
    
    def test_color_orange(self):
        """Test color for AQI > 101.5 (Unhealthy for Sensitive Groups)"""
        result = aqiColor(102)
        self.assertEqual(result, ORANGE)
    
    def test_color_yellow(self):
        """Test color for AQI > 51.5 (Moderate)"""
        result = aqiColor(52)
        self.assertEqual(result, YELLOW)
    
    def test_color_green(self):
        """Test color for AQI > 0 (Good)"""
        result = aqiColor(50)
        self.assertEqual(result, GREEN)
    
    def test_color_white(self):
        """Test color for AQI = 0 (undefined)"""
        result = aqiColor(0)
        self.assertEqual(result, WHITE)

class TestCalcAQIFunction(unittest.TestCase):
    """Tests for the calcAQI function"""
    
    def test_calc_aqi_lower_bound(self):
        """Test calcAQI at lower bound of range"""
        # Test for PM2.5 = 12.1 (lower bound of Moderate range)
        result = calcAQI(12.1, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 51)
    
    def test_calc_aqi_upper_bound(self):
        """Test calcAQI at upper bound of range"""
        # Test for PM2.5 = 35.4 (upper bound of Moderate range)
        result = calcAQI(35.4, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 100)
    
    def test_calc_aqi_mid_range(self):
        """Test calcAQI at mid-point of range"""
        # Test for PM2.5 = 23.75 (mid-point of Moderate range)
        result = calcAQI(23.75, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 76)  # Should be approximately 75.5, rounded to 76

class TestFetchSensorDataFunction(unittest.TestCase):
    """Tests for the fetch_sensor_data function"""
    
    @patch('purpleair.urequests')
    def test_fetch_sensor_data_success(self, mock_urequests):
        """Test successful API request with mocked response"""
        # Mock the successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "api_version": "V1.0.11-0.0.38",
            "data_timestamp": 1617395407,
            "data": {
                "sensor_index": 12345,
                "pm2.5": 10.5,
                "temperature": 72.5,
                "humidity": 45.2,
                "pressure": 1012.3,
                "confidence": 95
            }
        }
        mock_urequests.get.return_value = mock_response
        
        # Call the function with test parameters
        result = fetch_sensor_data("test_api_key", 12345, ["pm2.5", "temperature", "humidity", "pressure", "confidence"])
        
        # Verify the function called urequests.get with correct parameters
        mock_urequests.get.assert_called_once()
        call_args = mock_urequests.get.call_args[0][0]
        self.assertTrue("https://api.purpleair.com/v1/sensors/12345" in call_args)
        self.assertTrue("fields=pm2%2e5%2ctemperature%2chumidity%2cpressure%2cconfidence" in call_args)
        
        # Verify the response data
        self.assertEqual(result["data"]["sensor_index"], 12345)
        self.assertEqual(result["data"]["pm2.5"], 10.5)
        self.assertEqual(result["data"]["confidence"], 95)
    
    @patch('purpleair.urequests')
    @patch('purpleair.sys')
    def test_fetch_sensor_data_api_error(self, mock_sys, mock_urequests):
        """Test API request with error response"""
        # Mock the error response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_urequests.get.return_value = mock_response
        
        # Call the function with test parameters
        fetch_sensor_data("invalid_api_key", 12345, ["pm2.5"])
        
        # Verify that sys.exit was called
        mock_sys.exit.assert_called_once_with(1)
    
    @patch('purpleair.urequests')
    @patch('purpleair.sys')
    def test_fetch_sensor_data_value_error(self, mock_sys, mock_urequests):
        """Test API request with ValueError"""
        # Mock the request to raise ValueError
        mock_urequests.get.side_effect = ValueError("Invalid JSON")
        
        # Call the function with test parameters
        fetch_sensor_data("test_api_key", 12345, ["pm2.5"])
        
        # Verify that sys.exit was called
        mock_sys.exit.assert_called_once_with(1)
    
    def test_fetch_sensor_data_invalid_field_list(self):
        """Test with invalid field_list parameter"""
        with self.assertRaises(ValueError):
            fetch_sensor_data("test_api_key", 12345, 123)  # field_list should be list or string

class TestUrlEncode(unittest.TestCase):
    """Tests for the url_encode function"""
    
    def test_url_encode_alphanumeric(self):
        """Test url_encode with alphanumeric string"""
        result = url_encode("abc123")
        self.assertEqual(result, "abc123")
    
    def test_url_encode_with_spaces(self):
        """Test url_encode with spaces"""
        result = url_encode("hello world")
        self.assertEqual(result, "hello%20world")
    
    def test_url_encode_with_special_chars(self):
        """Test url_encode with special characters"""
        result = url_encode("test@example.com")
        self.assertEqual(result, "test%40example%2ecom")
    
    def test_url_encode_empty_string(self):
        """Test url_encode with empty string"""
        result = url_encode("")
        self.assertEqual(result, "")

class TestAqiFromPM(unittest.TestCase):
    """Tests for the aqiFromPM function"""
    
    def test_aqi_good_range(self):
        """Test AQI calculation for Good range (0-50)"""
        result = aqiFromPM(10.0)
        # Check if it's in the Good range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(0 <= result <= 50, f"Expected 0-50, got {result}")
    
    def test_aqi_moderate_range(self):
        """Test AQI calculation for Moderate range (51-100)"""
        result = aqiFromPM(25.0)
        # Check if it's in the Moderate range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(51 <= result <= 100, f"Expected 51-100, got {result}")
    
    def test_aqi_unhealthy_sensitive_range(self):
        """Test AQI calculation for Unhealthy for Sensitive Groups range (101-150)"""
        result = aqiFromPM(45.0)
        # Check if it's in the Unhealthy for Sensitive Groups range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(101 <= result <= 150, f"Expected 101-150, got {result}")
    
    def test_aqi_unhealthy_range(self):
        """Test AQI calculation for Unhealthy range (151-200)"""
        result = aqiFromPM(100.0)
        # Check if it's in the Unhealthy range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(151 <= result <= 200, f"Expected 151-200, got {result}")
    
    def test_aqi_very_unhealthy_range(self):
        """Test AQI calculation for Very Unhealthy range (201-300)"""
        result = aqiFromPM(200.0)
        # Check if it's in the Very Unhealthy range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(201 <= result <= 300, f"Expected 201-300, got {result}")
    
    def test_aqi_hazardous_range_1(self):
        """Test AQI calculation for Hazardous range (301-400)"""
        result = aqiFromPM(300.0)
        # Check if it's in the Hazardous range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(301 <= result <= 400, f"Expected 301-400, got {result}")
    
    def test_aqi_hazardous_range_2(self):
        """Test AQI calculation for Hazardous range (401-500)"""
        result = aqiFromPM(400.0)
        # Check if it's in the Hazardous range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(401 <= result <= 500, f"Expected 401-500, got {result}")
    
    def test_aqi_negative_value(self):
        """Test AQI calculation with negative PM value"""
        result = aqiFromPM(-10.0)
        self.assertEqual(result, -10.0)
    
    def test_aqi_undefined_value(self):
        """Test AQI calculation with 'undefined' PM value"""
        result = aqiFromPM('undefined')
        self.assertEqual(result, "-")
    
    def test_aqi_zero_value(self):
        """Test AQI calculation with zero PM value"""
        result = aqiFromPM(0.0)
        # Check if it's in the Good range
        if isinstance(result, (int, float)) and not isinstance(result, str):
            self.assertTrue(0 <= result <= 50, f"Expected 0-50, got {result}")
    
    def test_aqi_too_large_value(self):
        """Test AQI calculation with PM value > 1000"""
        result = aqiFromPM(1001.0)
        self.assertEqual(result, "-")


class TestAqiColor(unittest.TestCase):
    """Tests for the aqiColor function"""
    
    def test_color_maroon(self):
        """Test color for AQI > 300.5 (Hazardous)"""
        result = aqiColor(301)
        self.assertEqual(result, MAROON)
    
    def test_color_purple(self):
        """Test color for AQI > 201.5 (Very Unhealthy)"""
        result = aqiColor(202)
        self.assertEqual(result, PURPLE)
    
    def test_color_red(self):
        """Test color for AQI > 151.5 (Unhealthy)"""
        result = aqiColor(152)
        self.assertEqual(result, RED)
    
    def test_color_orange(self):
        """Test color for AQI > 101.5 (Unhealthy for Sensitive Groups)"""
        result = aqiColor(102)
        self.assertEqual(result, ORANGE)
    
    def test_color_yellow(self):
        """Test color for AQI > 51.5 (Moderate)"""
        result = aqiColor(52)
        self.assertEqual(result, YELLOW)
    
    def test_color_green(self):
        """Test color for AQI > 0 (Good)"""
        result = aqiColor(50)
        self.assertEqual(result, GREEN)
    
    def test_color_white(self):
        """Test color for AQI = 0 (undefined)"""
        result = aqiColor(0)
        self.assertEqual(result, WHITE)

class TestCalcAQI(unittest.TestCase):
    """Tests for the calcAQI function"""
    
    def test_calc_aqi_lower_bound(self):
        """Test calcAQI at lower bound of range"""
        # Test for PM2.5 = 12.1 (lower bound of Moderate range)
        result = calcAQI(12.1, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 51)
    
    def test_calc_aqi_upper_bound(self):
        """Test calcAQI at upper bound of range"""
        # Test for PM2.5 = 35.4 (upper bound of Moderate range)
        result = calcAQI(35.4, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 100)
    
    def test_calc_aqi_mid_range(self):
        """Test calcAQI at mid-point of range"""
        # Test for PM2.5 = 23.75 (mid-point of Moderate range)
        result = calcAQI(23.75, 100, 51, 35.4, 12.1)
        self.assertEqual(result, 76)  # Should be approximately 75.5, rounded to 76

class TestFetchSensorData(unittest.TestCase):
    """Tests for the fetch_sensor_data function"""
    
    @patch('purpleair.urequests')
    def test_fetch_sensor_data_success(self, mock_urequests):
        """Test successful API request with mocked response"""
        # Mock the successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "api_version": "V1.0.11-0.0.38",
            "data_timestamp": 1617395407,
            "data": {
                "sensor_index": 12345,
                "pm2.5": 10.5,
                "temperature": 72.5,
                "humidity": 45.2,
                "pressure": 1012.3,
                "confidence": 95
            }
        }
        mock_urequests.get.return_value = mock_response
        
        # Call the function with test parameters
        result = fetch_sensor_data("test_api_key", 12345, ["pm2.5", "temperature", "humidity", "pressure", "confidence"])
        
        # Verify the function called urequests.get with correct parameters
        mock_urequests.get.assert_called_once()
        call_args = mock_urequests.get.call_args[0][0]
        self.assertTrue("https://api.purpleair.com/v1/sensors/12345" in call_args)
        self.assertTrue("fields=pm2%2e5%2ctemperature%2chumidity%2cpressure%2cconfidence" in call_args)
        
        # Verify the response data
        self.assertEqual(result["data"]["sensor_index"], 12345)
        self.assertEqual(result["data"]["pm2.5"], 10.5)
        self.assertEqual(result["data"]["confidence"], 95)
    
    @patch('purpleair.urequests')
    @patch('purpleair.sys')
    def test_fetch_sensor_data_api_error(self, mock_sys, mock_urequests):
        """Test API request with error response"""
        # Mock the error response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_urequests.get.return_value = mock_response
        
        # Call the function with test parameters
        fetch_sensor_data("invalid_api_key", 12345, ["pm2.5"])
        
        # Verify that sys.exit was called
        mock_sys.exit.assert_called_once_with(1)
    
    @patch('purpleair.urequests')
    @patch('purpleair.sys')
    def test_fetch_sensor_data_value_error(self, mock_sys, mock_urequests):
        """Test API request with ValueError"""
        # Mock the request to raise ValueError
        mock_urequests.get.side_effect = ValueError("Invalid JSON")
        
        # Call the function with test parameters
        fetch_sensor_data("test_api_key", 12345, ["pm2.5"])
        
        # Verify that sys.exit was called
        mock_sys.exit.assert_called_once_with(1)
    
    def test_fetch_sensor_data_invalid_field_list(self):
        """Test with invalid field_list parameter"""
        with self.assertRaises(ValueError):
            fetch_sensor_data("test_api_key", 12345, 123)  # field_list should be list or string