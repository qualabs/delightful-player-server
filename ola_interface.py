import time
import subprocess
import json
from rgbw_colorspace_converter.colors.converters import RGB
from config import *

import ipdb
import sys


def turn_off_all_ligths():
    black = ",".join(["0"] * MAX_CHANNELS)
    black_command = f"ola_set_dmx -u 1 -d {black}"
    subprocess.run(black_command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def blink():
    color_list = ["0"] * MAX_CHANNELS
    lights_pos = [FL, FR, BL, BR]
    for pos in lights_pos:
        color_list[pos] = "255"
        color_list[pos + 1] = "255"
        color_list[pos + 2] = "255"
        color_list[pos + 3] = "255"
        color_list[pos + 4] = "250"
    blink_list = ",".join(color_list)
    command = f"ola_set_dmx -u 1 -d {blink_list}"
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    time.sleep(BLINKING_TIME)
    turn_off_all_ligths()


def fill_colors_list(json_colors):
    color_list = ["0"] * MAX_CHANNELS
    for light_config, channels in LIGHTS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                colors = json_colors["channels"][channel]
                new_rgb = RGB(colors[0],colors[1],colors[2])
                rgbw = new_rgb.rgbw
                print(f'msg: {rgbw}')
                for light_pos in lights:
                    # color_list[light_pos] = str(min(rgbw[3]+50,255))
                    color_list[light_pos] = str(rgbw[3])
                    for rgb in range(3):
                        color = rgbw[rgb]
                        color_list[light_pos+1+rgb] = str(color)
    return ",".join(color_list)


def set_lights(color_list):
    command = f"ola_set_dmx -u 1 -d {color_list}"
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def parse_lights(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)

