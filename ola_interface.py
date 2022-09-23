import time
import subprocess
import json

from config import *
from colors import COLORS


import ipdb
import sys

def light_intensity(rgb):
    # intensity = round(sum(rgb) / 3)
    # intensity = (0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2])
    intensity = find_luminance(rgb)
    #if intensity < 50:
    #    intensity = 50
    #elif intensity < 100:
    #    intensity = 100
    #elif intensity < 150:
    #    intensity = 150
    #elif intensity < 200:
    #    intensity = 200
    #else:
    #    intensity = 250
    return str(intensity)


def closest_color(my_rgb):
    for k in range(0, 255, 5):
        for color, rgb in COLORS.items():
            closest_red = rgb[0] in range(my_rgb[0]-k, my_rgb[0]+k)
            closest_green = rgb[1] in range(my_rgb[1]-k, my_rgb[1]+k)
            closest_blue = rgb[2] in range(my_rgb[2]-k, my_rgb[2]+k)
            if closest_red and closest_green and closest_blue:
                print(color, rgb)
                return rgb


def damecolor(rgb):
    #ipdb.set_trace()
    # closest = closest_color(rgb)
    closest = rgb
    color_list = str(light_intensity(closest))
    color_list += f",{closest[0]},{closest[1]},{closest[2]}"
    print(f"color_list: {color_list}")
    command = f"ola_set_dmx -u 1 -d {color_list}"
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)

# color = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
# damecolor(color)
#damecolor((255,20,147))

#closest_color((8,90,20))

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
    #color_list[FL] = LIGHT_INTENSITY
    #color_list[FR] = LIGHT_INTENSITY
    #color_list[BL] = LIGHT_INTENSITY
    #color_list[BR] = LIGHT_INTENSITY
    #ipdb.set_trace()
    for light_config, channels in LIGTHS.items():
        if json_colors["config"] == light_config:
            for channel, lights in channels.items():
                # json_colors["channels"][channel] = closest_color(json_colors["channels"][channel])
                #ipdb.set_trace()
                for light_pos in lights:
                    color_list[light_pos] = light_intensity(json_colors["channels"][channel])
                    for rgb in range(3):
                        #ipdb.set_trace()
                        color = json_colors["channels"][channel][rgb]
                        if rgb == 0 and color > 0:
                            color = str(min(255, int(color+25)))
                        # if rgb == 1 and color > 0:
                            # color = str(max(0, int(color-25)))
                        if rgb == 2 and color > 0:
                            color = str(max(0, int(color-25)))
                        color_list[light_pos+1+rgb] = str(color)
    return ",".join(color_list)


def set_lights(color_list):
    command = f"ola_set_dmx -u 1 -d {color_list}"
    #print(color_list)
    subprocess.run(command, check=True, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def parse_ligths(websocket_message):
    json_colors = json.loads(websocket_message)
    return fill_colors_list(json_colors)


def find_luminance(rgb):
    
    #step1: convert into 0-1 range
    vR = rgb[0] / 255;
    vG = rgb[1] / 255;
    vB = rgb[2] / 255;
    #step2 find luminance
    Y = (0.2126 * sRGBtoLin(vR) + 0.7152 * sRGBtoLin(vG) + 0.0722 * sRGBtoLin(vB))
    #step2 find perceive light
    light = YtoLstar(Y)
    return light
    

def sRGBtoLin(colorChannel):
    if ( colorChannel <= 0.04045 ):
                return colorChannel / 12.92
    else:
        return (( colorChannel + 0.055)/1.055)**2.4
        


def YtoLstar(Y):
    if ( Y <= (216/24389)):
            return Y * (24389/27)
    else: 
        return (Y**(1/3)) * 116 - 16
        
#color_list = parse_ligths('{"config":"mono","channels":{"C":[0,0,0]}}')
#set_lights(color_list)
