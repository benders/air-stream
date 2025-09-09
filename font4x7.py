class Font4x7:
    WIDTH = 4
    HEIGHT = 7
    FONT = {
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

    def __init__(self, region_width, region_height, pixel_func):
        self.region_width = region_width
        self.region_height = region_height
        self.pixel_func = pixel_func

    def _safe_pixel(self, x, y, *args, **kwargs):
        if 0 <= x < self.region_width and 0 <= y < self.region_height:
            self.pixel_func(x, y, *args, **kwargs)

    # Draw a character as long as any part of the character is in the display region
    def draw_char(self, char, x_offset, y_offset, *args, **kwargs):
        if char not in self.FONT:
            raise ValueError(f"Character '{char}' not found in font.")

        if x_offset + self.WIDTH < 0 or y_offset + self.HEIGHT < 0:
            return
        elif x_offset > self.region_width or y_offset > self.region_height:
            return
        
        for y, row in enumerate(self.FONT[char]):
            for x, col in enumerate(row):
                if col == '#':
                    self._safe_pixel(x + x_offset, y + y_offset, *args, **kwargs)

    def text(self, string, x_offset, y_offset, *args, **kwargs):
        for i, char in enumerate(string):
            self.draw_char(char, x_offset + i * (self.WIDTH + 1), y_offset, *args, **kwargs)

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
