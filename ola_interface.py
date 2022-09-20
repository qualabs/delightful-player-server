import time
import subprocess
import json

from config import *
from colors import COLORS


def light_intensity(rgb):
    intensity = round(sum(rgb) / 3)
    if intensity < 50:
        intensity = 50
    elif intensity < 100:
        intensity = 100
    elif intensity < 150:
        intensity = 150
    elif intensity < 200:
        intensity = 200
    else:
        intensity = 250
    return str(intensity)


def closest_color(my_rgb):
    closest = ""
    min_dif = 255 * 3
    for color, rgb in COLORS.items():
        red_dif = abs(my_rgb[0] - rgb[0])
        green_dif = abs(my_rgb[1] - rgb[1])
        blue_dif = abs(my_rgb[2] - rgb[2])
        dif = red_dif + green_dif + blue_dif
        if dif < min_dif:
            min_dif = dif
            closest = color
    return COLORS[closest]


def turn_on_all_ligths():
    white = ",".join(["255"] * MAX_CHANNELS)
    white_command = f"ola_set_dmx -u 1 -d {white}"
    subprocess.run(white_command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def turn_off_all_ligths():
    black = ",".join(["0"] * MAX_CHANNELS)
    black_command = f"ola_set_dmx -u 1 -d {black}"
    subprocess.run(black_command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def blink():
    for i in range(BLINK_TIMES):
        turn_on_all_ligths()
        time.sleep(SLEEP_BETWEEN_BLINKS)
        turn_off_all_ligths()
        time.sleep(SLEEP_BETWEEN_BLINKS)


def fill_colors_list(json_colors):
    color_list = ["0"] * MAX_CHANNELS

    for light_config, channels in LIGTHS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                json_colors["channels"][channel] = closest_color(json_colors["channels"][channel])
                for light_pos in lights:
                    color_list[light_pos] = light_intensity(json_colors["channels"][channel])
                    for rgb in range(3):
                        color = json_colors["channels"][channel][rgb]
                        if rgb == 0:
                            color = str(min(255, int(color+25)))
                        if rgb == 2:
                            color = str(max(0, int(color-25)))
                        color_list[light_pos+1+rgb] = str(color)
    return ",".join(color_list)


def set_lights(color_list):
    command = f"ola_set_dmx -u 1 -d {color_list}"
    print(color_list)
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def parse_ligths(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)


#color_list = parse_ligths('{"config":"mono","channels":{"C":[130,60,10]}}')
#set_lights(color_list)
