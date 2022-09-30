# delightful_player_server
Server of the Delightful player project.

Using python and OLA library it connects to the DMX interface.

--------------------------------------
## Previous configurations
* OLA needs to have a universe created.
* The lights need bo be configured on the 7Channel mode.
* The plugins that have to be disabled are:
  * Enttec Open DMX, to do it you can run: 'sudo ola_conf_plugins.sh disable opendmx'.
  * Serial USB, to do it you can run: 'sudo ola_conf_plugins.sh disable usbserial'.
* The plugins that have to be enabled are:
  * FTDI USB DMX, to do it you can run: 'sudo ola_conf_plugins.sh enable ftdi'.
* These are all the plugins that were activated/deactivated while the feature was tested:

| Id  | Plugin Name         | Active |
|-----|---------------------|--------|
| 1   | Dummy               | Yes    |
| 2   | ArtNet              | No     |
| 3   | ShowNet             | No     |
| 4   | ESP Net             | No     |
| 5   | Serial USB          | No     |
| 6   | Enttec Open DMX     | No     |
| 7   | SandNet             | No     |
| 8   | StageProfi          | Yes    |
| 9   | Pathport            | No     |
| 11  | E1.31 (sACN)        | No     |
| 13  | FTDI USB DMX        | Yes    |
| 15  | SPI                 | Yes    |
| 16  | KiNET               | Yes    |
| 17  | KarateLight         | Yes    |
| 18  | Milford Instruments | Yes    |
| 19  | Renard              | Yes    |
| 20  | UART native DMX     | Yes    |
| 21  | Open Pixel Control  | Yes    |
| 22  | GPIO                | Yes    |

--------------------------------------
## Files

### config.py
In this file there are all the configurations:
* About websocket server
  * WEBSOCKET_IP
  * WEBSOCKET_PORT
* About OLA and about the lights:
  * UNIVERSE
  * MAX_CHANNELS
  * BLINKING_TIME  # For how much time the lights blink after a new client is connected.
  * BLINKING_COLOR  # (Luminocity, Red, Green, Blue, Blinking Speed).
  * FL  # The first channel of the light in the Front Left position.
  * FR  # The first channel of the light in the Front Right position.
  * BL  # The first channel of the light in the Back Left position.
  * BR  # The first channel of the light in the Back Right position.
  * LIGHTS  # Uses the last 4 constants to manage the different lights/colors modes (mono, stereo and surround).


### serverSocket.py
The server starts listening websockets connections.
It receives colors, expects a json format i.e. '{"config":"mono","channels":{"C":[0,0,0]}}'.
Sends the json to ola_interface.py to use the colors in the lights.

### ola_interface.py
It parses the json received in order to get a color list to use it with the OLA interface that needs a list of values for each channel.
Sends rgb colors to manage_colors.py to get the real colors for the lights.

### manage_colors.py
It receives a color in (r, g, b) format to transform it into a format that the lights can bright correctly.
Calculates the colors to show.
Sends back to ola_interface.py in a (l, r, g, b) format, where l is the luminosity.  
