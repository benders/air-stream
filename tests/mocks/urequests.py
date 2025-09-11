"""
Mock for urequests module, which is used in MicroPython but not available in standard Python.
This allows tests to run on a standard Python environment.
"""

class Response:
    """Mock Response class for urequests"""
    
    def __init__(self, status_code=200, text="", json_data=None):
        self.status_code = status_code
        self.text = text
        self._json = json_data
    
    def json(self):
        """Return JSON data"""
        return self._json

def get(url, headers=None):
    """Mock get function for urequests"""
    # This will be mocked in tests
    pass

def post(url, headers=None, data=None):
    """Mock post function for urequests"""
    # This will be mocked in tests
    pass