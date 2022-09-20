import time
import subprocess
import json

from config import *


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
    color_list[FL] = LIGHT_INTENSITY
    color_list[FR] = LIGHT_INTENSITY
    color_list[BL] = LIGHT_INTENSITY
    color_list[BR] = LIGHT_INTENSITY

    for light_config, channels in LIGTHS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                for light_pos in lights:
                    for irgb in range(3):
                        color_list[light_pos+1+irgb] = str(json_colors["channels"][channel][irgb])
    return ",".join(color_list)


def set_lights(color_list):
    command = f"ola_set_dmx -u 1 -d {color_list}"
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def parse_ligths(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)

