import time
import json
import array

from ola.ClientWrapper import ClientWrapper
from rgbw_colorspace_converter.colors.converters import RGB

from config import *


def turn_off_all_ligths():
    black_color_list = [0] * MAX_CHANNELS
    set_lights(black_color_list)


# Blinks in each light
def blink_all_lights():
    color_list = [0] * MAX_CHANNELS
    lights_pos = [FL, FR, BL, BR]  # each light
    for pos in lights_pos:
        color_list[pos] = BLINKING_COLOR[0]  # Luminosity
        color_list[pos + 1] = BLINKING_COLOR[1]  # R
        color_list[pos + 2] = BLINKING_COLOR[2]  # G
        color_list[pos + 3] = BLINKING_COLOR[3]  # B
        color_list[pos + 4] = BLINKING_COLOR[4]  # Blinking Speed

    set_lights(color_list)
    time.sleep(BLINKING_TIME)

    turn_off_all_ligths()


def fill_colors_list(json_colors):
    color_list = [0] * MAX_CHANNELS
    for light_config, channels in LIGHTS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                colors = json_colors["channels"][channel]
                new_rgb = RGB(colors[0], colors[1], colors[2])
                rgbw = new_rgb.rgbw
                for light_pos in lights:
                    # the first channel of each light has to have the last element of the rgbw color
                    color_list[light_pos] = rgbw[3]
                    if color_list[light_pos] < 30:
                        color_list[light_pos] = 30
                    # fills the rgb channels of each light with the corresponding rgb components of the rgbw color
                    for rgb in range(3):
                        color = rgbw[rgb]
                        color_list[light_pos+1+rgb] = color
    return color_list


def parse_lights(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)


def set_lights(color_list):
    # converts a list into a comma separated string
    # example: [255,255,0,0] into "255,255,0,0"
    # str_color_list = ",".join([str(i) for i in color_list])
    # command = f"ola_set_dmx -u 1 -d {str_color_list}"
    # subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
    #                stderr=subprocess.PIPE)
    data = array.array('B', color_list)
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(UNIVERSE, data, None)


# just for manual testing
# set_lights(parse_lights('{"config":"mono","channels":{"C":[255,0,0]}}'))
