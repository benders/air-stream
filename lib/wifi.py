def show_wifi_logo(x0, y0, pixel_function, *args, **kwargs):
    WIFI_LOGO = [
        '..######..',
        '.########.',
        '##......##',
        '#..####..#',
        '..######..',
        '..#....#..',
        '....##....',
        '....##....',
    ]

    for y, row in enumerate(WIFI_LOGO):
        for x, col in enumerate(row):
            if col == '#':
                pixel_function(x + x0, y + y0, *args, **kwargs)

if __name__ == "__main__":
    import PixelKit as kit

    kit.clear()
    show_wifi_logo(3, 0, kit.set_pixel, (0x10, 0x10, 0x10))
    kit.render()
