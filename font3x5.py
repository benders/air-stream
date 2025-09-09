WIDTH = 3
HEIGHT = 5
FONT = {
    # 0x30  0
    "0": [
        "###",
        "# #",
        "# #",
        "# #",
        "###",
    ],

    # 0x31  1
    "1": [
        " # ",
        "## ",
        " # ",
        " # ",
        "###",
    ],

    # 0x32  2
    "2": [
        "###",
        "  #",
        "###",
        "#  ",
        "###",
    ],

    # 0x33  3
    "3": [
        "###",
        "  #",
        "###",
        "  #",
        "###",
    ],
    
    # 0x34  4
    "4": [
        "# #",
        "# #",
        "###",
        "  #",
        "  #",
    ],
    
    # 0x35  5
    "5": [
        "###",
        "#  ",
        "###",
        "  #",
        "###",
    ],
    
    # 0x36  6
    "6": [
        "###",
        "#  ",
        "###",
        "# #",
        "###",
    ],

    # 0x37  7
    "7": [
        "###",
        "  #",
        "  #",
        "  #",
        "  #",
    ],

    # 0x38  8
    "8": [
        "###",
        "# #",
        "###",
        "# #",
        "###",
    ],
    
    # 0x39  9
    "9": [
        "###",
        "# #",
        "###",
        "  #",
        "###",
    ]
}

def plot_char(char, x_offset, y_offset, pixel_function, *args, **kwargs):
    for y, row in enumerate(FONT[char]):
        for x, col in enumerate(row):
            if col == '#':
                pixel_function(x + x_offset, y + y_offset, *args, **kwargs)

def text(string, x_offset, y_offset, pixel_function, *args, **kwargs):
    for i, char in enumerate(string):
        plot_char(char, x_offset + i * (WIDTH + 1), y_offset, pixel_function, *args, **kwargs)

if __name__ == "__main__":
    import PixelKit as kit
    COLOR = (0x10, 0x10, 0x10)
    kit.clear()
    text("6789", 0, 0, kit.set_pixel, COLOR)
    kit.render()