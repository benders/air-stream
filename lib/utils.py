#
# Various helpful utility functions
#

import time

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

def scroll_text(kit, font, text, color, speed=0.05):
    """
    Scroll text across the PixelKit display.
    
    Args:
        kit: PixelKit instance
        font: Bitmap font instance
        text (str): Text to scroll
        color (tuple): RGB color tuple for the text
        speed (float): Delay between frames in seconds
    """
    text_width = len(text) * (font.WIDTH + 1) - 1
    display_width = kit.WIDTH

    # Start scrolling from right edge of display
    for offset in range(display_width, -text_width - 1, -1):
        kit.clear()
        font.text(text, offset, 0, color)
        kit.render()
        time.sleep(speed)