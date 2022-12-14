# OLA and Lights configs
UNIVERSE = 1
MAX_CHANNELS = 512

BLINKING_TIME = 0.5
BLINKING_COLOR = (255, 255, 255, 255, 250)

FL = 0
FR = 100
BL = 200
BR = 300

LIGHTS = {"mono": {"C": (FL, FR, BL, BR)},
          "stereo": {"L": (FL, BL), "R": (FR, BR)},
          "surround": {"FL": (FL,), "FR": (FR,), "BL": (BL,), "BR": (BR,)},
          }

# websocket configs
WEBSOCKET_IP = "0.0.0.0"
WEBSOCKET_PORT = 5679
