#!/usr/bin/env python3
"""
Font4x7 class for 4x7 pixel bitmap font.
Implements numerals 0-9 in a 4x7 pixel grid.
"""

from ..basefont import BaseFont

class Font4x7(BaseFont):
    """4x7 pixel bitmap font for numerals"""
    
    WIDTH = 4
    HEIGHT = 7
    FONT = {
        # 0x20  (space)
        " ": [
            "    ",
            "    ",
            "    ",
            "    ",
            "    ",
            "    ",
            "    ",
        ],

        # 0x30  0
        "0": [
            " ## ",
            "#  #",
            "#  #",
            "#  #",
            "#  #",
            "#  #",
            " ## ",
        ],

        # 0x31  1
        "1": [
            " #  ",
            "##  ",
            " #  ",
            " #  ",
            " #  ",
            " #  ",
            "###",
        ],

        # 0x32  2
        "2": [
            " ## ",
            "#  #",
            "   #",
            "  # ",
            " #  ",
            "#   ",
            "####",
        ],

        # 0x33  3
        "3": [
            " ## ",
            "#  #",
            "   #",
            "  # ",
            "   #",
            "#  #",
            " ## ",
        ],
        
        # 0x34  4
        "4": [
            "#  #",
            "#  #",
            "#  #",
            "####",
            "   #",
            "   #",
            "   #",
        ],
        
        # 0x35  5
        "5": [
            "####",
            "#   ",
            "### ",
            "   #",
            "   #",
            "#  #",
            " ## ",
        ],
        
        # 0x36  6
        "6": [
            " ## ",
            "#   ",
            "#   ",
            "### ",
            "#  #",
            "#  #",
            " ## ",
        ],

        # 0x37  7
        "7": [
            "####",
            "#  #",
            "   #",
            "  # ",
            " #  ",
            " #  ",
            " #  ",
        ],

        # 0x38  8
        "8": [
            " ## ",
            "#  #",
            "#  #",
            " ## ",
            "#  #",
            "#  #",
            " ## ",
        ],
        
        # 0x39  9
        "9": [
            " ## ",
            "#  #",
            "#  #",
            " ###",
            "   #",
            "   #",
            " ## ",
        ]
    }

if __name__ == "__main__":
    import PixelKit as kit
    import time

    # Constants
    COLOR = (0x10, 0x10, 0x10)
    SCROLL_TEXT = "0123456789"
    SCROLL_SPEED = 0.1  # seconds between scroll steps
    DISPLAY_WIDTH = 16  # Typical width for PixelKit display
    DISPLAY_HEIGHT = 8  # Typical height for PixelKit display

    font = Font4x7(DISPLAY_WIDTH, DISPLAY_HEIGHT, kit.set_pixel)

    # Calculate the total width of the text
    text_width = len(SCROLL_TEXT) * (font.WIDTH + 1) - 1  # -1 because we don't need spacing after the last char

    try:
        # Infinite scrolling loop
        position = DISPLAY_WIDTH  # Start from the right edge
        
        while True:
            kit.clear()
            
            # Draw the text at the current position
            font.text(SCROLL_TEXT, position, 0, COLOR)
            kit.render()
            
            # Move the text position left by one pixel
            position -= 1
            
            # If the text has scrolled completely off the left edge, reset to the right
            if position < -text_width:
                position = DISPLAY_WIDTH
                
            # Small delay to control scroll speed
            time.sleep(SCROLL_SPEED)
            
    except KeyboardInterrupt:
        # Allow for clean exit with Ctrl+C
        print("Scrolling stopped")
        kit.clear()
        kit.render()