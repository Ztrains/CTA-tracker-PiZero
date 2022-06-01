
import time
import subprocess
import os
import sys
import json

import requests
from datetime import datetime

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# constants for screen height formatting
top = -2
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# load TTF font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# setup buttons on miniPiTFT
topButton = digitalio.DigitalInOut(board.D23)
botButton = digitalio.DigitalInOut(board.D24)
topButton.switch_to_input()
botButton.switch_to_input()





# API docs: https://www.transitchicago.com/developers/ttdocs/
cta_api_key = os.environ.get('CTA_API_KEY')
if (cta_api_key == None):
    sys.exit('API key not detected, need to source .env file first')

cta_api_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&outputType=JSON'.format(cta_api_key)

# CTA map_id constants
belmont_map_id = 41320
southport_map_id = 40360


# CTA stop_id constants
belmont_stop_id_north_red = 30255
belmont_stop_id_south_red = 30256
belmont_stop_id_north_bp = 30257
belmont_stop_id_south_bp = 30258

southport_stop_id_north = 30070
southport_stop_id_south = 30071


# Northbound/Southbound str constants
northboundStr = 'Northbound trains'
southboundStr = 'Southbound trains'

belmontNorthboundStr = 'Belmont NB trains'
belmontSouthboundStr = 'Belmont SB trains'

southportNorthboundStr = 'Southport NB trains'
southportNorthboundStr = 'Southport SB trains'


# Hex color constants
#hexRed   = '#c60c30'    # CTA red line color
#hexRed = '#d60b32'      # red alt 1
hexRed = '#ed0e0e'      # red alt 2
#hexBrown = '#62361b'    # CTA brown line color
hexBrown = '#734021'    # brown alt 1
hexWhite = '#FFFFFF'    # default white color
hexBlue = '#2a79d4'     # blue info color
hexPurple = '#7d22ab'   # purple line color



api_url_with_belmont_mapid = '{}&mapid={}'.format(cta_api_url, belmont_map_id)

response = requests.get(api_url_with_belmont_mapid)
json_response = json.loads(response.text)
ctatt = json_response['ctatt']

etas = ctatt['eta']  # len 8  (num of 'eta' objects)
northboundTrains = []
southboundTrains = []

for eta in etas:
    if eta['trDr'] == '1':
        if len(northboundTrains) < 4:       # only store 4 upcoming trains
            northboundTrains.append(eta)
    elif eta['trDr'] == '5':
        if len(southboundTrains) < 4:
            southboundTrains.append(eta)






# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

y = top
draw.text((x, y), belmontNorthboundStr, font=font, fill='#FFFFFF')
y += font.getsize(belmontNorthboundStr)[1]

#print('---NORTHBOUND TRAINS---')
for train in northboundTrains:
    stopDescription = train["stpDe"]
    trainLine = train['rt']
    estArrival = train['arrT']
    estArrival2 = datetime.fromisoformat(estArrival)
    estArrival3 = estArrival2.strftime('%-I:%M:%S %p')

    #print(f'{trainLine} : {estArrival3}')

    fillColor = hexWhite       # default color is white
    if (trainLine == 'Red'):
        fillColor = hexRed   
    elif (trainLine == 'Brn'):
        fillColor = hexBrown
    elif (trainLine == 'P'):
        fillColor = hexPurple
        trainLine = 'P  '       # add 2 spaces to line up spacing with Red/Brn


    trainInfo = f'{trainLine} - {estArrival3}'
    draw.text((x, y), trainInfo, font=font, fill=fillColor)
    y += font.getsize(trainInfo)[1]

helpInfo = '↑ N↔S - ↓ Refresh'
draw.text((x, y), helpInfo, font=font, fill=hexBlue)
disp.image(image, rotation)


# main loop to catch button presses
while True:
#    if topButton.value and botButton.value:
#        backlight.value = False  # turn off backlight
#    else:
#        backlight.value = True  # turn on backlight

#    if botButton.value and not topButton.value:  # just button A pressed
#        print("top button pressed")
#    if topButton.value and not botButton.value:  # just button B pressed
#        print("top button pressed")
#    if not topButton.value and not botButton.value:  # none pressed
#        print("no buttons pressed")
    print(f'top button val: {topButton.value}')
    print(f'bot button val: {botButton.value}')
    time.sleep(1)