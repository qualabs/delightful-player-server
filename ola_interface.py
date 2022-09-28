import time
import json
import array

from ola.ClientWrapper import ClientWrapper

from config import *
from manage_colors import rgb_to_lrgb


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


# example of json_colors: {"config":"mono","channels":{"C":[0,0,0]}}
def fill_colors_list(json_colors):
    color_list = [0] * MAX_CHANNELS
    for light_config, channels in LIGHTS.items():
        # example of light_config: "mono"
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                # example of channel: "C"
                rgb = json_colors["channels"][channel]
                colors = rgb_to_lrgb(rgb)
                # example of lights: (FL, FR, BL, BR)
                for light_pos in lights:
                    for i in range(4):
                        # fills the rgb channels of each light
                        color_list[light_pos + i] = colors[i]
    return color_list


def parse_lights(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)


def set_lights(color_list):
    data = array.array('B', color_list)
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(UNIVERSE, data, None)


# just for manual testing
# set_lights(parse_lights('{"config":"mono","channels":{"C":[255,0,0]}}'))
