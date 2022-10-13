import time
from time import strftime
import subprocess
import digitalio
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import adafruit_mpr121
import random

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

# Setup capacitive touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

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

# Input -> number mapping
mapping = {1: "1", 3: "2", 5: "3", 10: "4", 8: "5", 6: "6"}

# Functions
def getInput():
    while(True):
        for i in mapping:
            if mpr121[i].value:
                return mapping[i]

def displayVals(vals):
    for val in vals:
        print(val)
        draw.text((x, y), str(val), font=medFont, fill="#FFFFFF")
        time.sleep(1)

def newVal(vals):
    newVal = str(random.randrange(1, 7))
    while len(vals) > 0 and newVal == vals[-1]:
        newVal = str(random.randrange(1, 7))
    vals.append(newVal)

def testVals(vals):
    for val in vals:
        guess = getInput()
        print(guess)
        if guess != val:
            return False
    return True

inGame = True
vals = []
highScore = 0

def game():
    score = 0
    while(inGame):
        newVal(vals)
        print(vals)
        time.sleep(1)
        inGame = testVals(vals)
        if inGame:
            score += 1

# Time variable
stress = 0
emote = "😊"

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 100)
medFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    y =top

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    
    if buttonA.value:
        highScore = max(highScore, inGame())
        #print("up")

    # Both buttons for select screen
    draw.text((x, y), str("High Score: " + str(highScore)), font=medFont, fill="#FFFFFF")
    y+= medFont.getsize("str")[1]
    # draw.text((x, y), str("Use the buttons to track"), font=font, fill="#FFFFFF")
    # y += font.getsize("str")[1]
    # draw.text((x, y), str("how stressed you are"), font=font, fill="#FFFFFF")
    # y += font.getsize("str")[1]
    # draw.text((x, y), str("throughout the day!"), font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)
