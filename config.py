# ola configs
MAX_CHANNELS = 512
BLINKING_TIME = 1

FL = 0
FR = 100
BL = 200
BR = 300

LIGHTS = {"mono": {"C": (FL, FR, BL, BR)},
          "stereo": {"L": (FL, BL), "R": (FR, BR)},
          "surround": {"FL": (FL,), "FR": (FR,), "BL": (BL,), "BR": (BR,)},
          }

# websocket configs
WEBSOCKET_IP = '10.30.1.168'
WEBSOCKET_PORT = 5679

