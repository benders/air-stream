#
# Various helpful utility functions
#

def format_time(time_tuple):
    """
    Convert MicroPython time tuple to human-readable timestamp.
    
    Args:
        time_tuple: Either an 8-tuple (year, month, mday, hour, minute, second, weekday, yearday)
                    or a 9-tuple (year, month, mday, hour, minute, second, weekday, yearday, isdst)
        
    Returns:
        str: Formatted timestamp in '%Y-%m-%d %H:%M:%S' format
    """
    # Extract the first 6 elements which are the same in both formats
    year, month, day, hour, minute, second = time_tuple[:6]
    
    # Format with leading zeros where needed
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        year, month, day, hour, minute, second
    )