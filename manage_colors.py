from rgbw_colorspace_converter.colors.converters import RGB

from colors import COLORS


def pure_r_g_b(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    pure_red = not green and not blue
    pure_green = not red and not blue
    pure_blue = not red and not green
    if pure_red:
        return (red, red, 0, 0)
    if pure_green:
        return (green, 0, green, 0)
    if pure_blue:
        return (blue, 0, 0, blue)

    return None


def white_in_rgb(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    red_close_to_green = red in range(green-15, green+15)
    green_close_to_blue = green in range(blue-15, blue+15)
    blue_close_to_red = blue in range(red-15, red+15)
    if red_close_to_green and green_close_to_blue and blue_close_to_red and red > 60:
        green = max(0, green - 40)
        blue = max(0, blue - 60)
        return (green, red, green, blue)

    return None


# This function is used just to be a little more precise in a few special colors.
# Is for detail. You can remove it and the colors will be fine anyway.
def special_color(my_rgb):
    # example of perfect_rgb_str: "255,215,0"
    # example of light_rgb: (250, 250, 100, 0).
    for perfect_rgb_str, light_rgb in COLORS.items():
        # example of perfect_rgb: [255, 215, 0]
        perfect_rgb = [int(c) for c in perfect_rgb_str.split(",")]
        match_red = perfect_rgb[0] == my_rgb[0]
        match_green = perfect_rgb[1] == my_rgb[1]
        match_blue = perfect_rgb[2] == my_rgb[2]
        if match_red and match_green and match_blue:
            # print(perfect_rgb_str, light_rgb)
            return light_rgb

    return None


# rgb: tuple with color components (red, gree, blue)
# returns lrgb: tuple with color components (luminosity, red, gree, blue)
def rgb_to_lrgb(rgb):
    # is Red, Green or Blue
    pure = pure_r_g_b(rgb)
    if pure:
        return pure

    # Difficult colors
    special = special_color(rgb)
    if special:
        return special

    # is white, gray or black
    white = white_in_rgb(rgb)
    if white:
        return white

    # Otherwise
    rgbw = RGB(rgb[0], rgb[1], rgb[2]).rgbw
    # the first channel of each light has to have the last element of the rgbw color
    # That light is too low for some cases
    ret = [rgbw[3], rgbw[0], rgbw[1], rgbw[2]]
    if ret[0] < 30:
        ret[0] = 30

    return tuple(ret)

