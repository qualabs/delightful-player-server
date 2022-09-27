import time
import subprocess
import json
from rgbw_colorspace_converter.colors.converters import RGB
from config import *

import ipdb
import sys

def closest_color(my_rgb):
    for k in range(0, 255, 5):
        for color, rgb in COLORS.items():
            closest_red = rgb[0] in range(my_rgb[0]-k, my_rgb[0]+k)
            closest_green = rgb[1] in range(my_rgb[1]-k, my_rgb[1]+k)
            closest_blue = rgb[2] in range(my_rgb[2]-k, my_rgb[2]+k)
            if closest_red and closest_green and closest_blue:
                print(color, rgb)
                return rgb


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
    pass
    #turn_off_all_ligths()
    ##time.set_lights()
    #for i in range(BLINK_TIMES):
    #    turn_on_all_ligths()
    #    time.sleep(SLEEP_BETWEEN_BLINKS)
    #    turn_off_all_ligths()
    #    time.sleep(SLEEP_BETWEEN_BLINKS)


def fill_colors_list(json_colors):
    color_list = ["0"] * MAX_CHANNELS
    for light_config, channels in LIGTHS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                colors = json_colors["channels"][channel]
                new_rgb = RGB(colors[0],colors[1],colors[2])
                rgbw = new_rgb.rgbw
                print(f'msg: {rgbw}')
                for light_pos in lights:
                    # color_list[light_pos] =  str(min(rgbw[3]+50,255))                    
                    color_list[light_pos] =  str(rgbw[3])                    
                    for rgb in range(3):
                        color = rgbw[rgb]
                        color_list[light_pos+1+rgb] = str(color)
    return ",".join(color_list)


def set_lights(color_list):
    command = f"ola_set_dmx -u 1 -d {color_list}"
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def parse_ligths(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)

