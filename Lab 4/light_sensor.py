import digitalio
import board
import board
import time
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont


i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course.
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing
height = display.width
width = display.height
image = Image.new("RGB", (width, height))
rotation = 90
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Get drawing object to draw on Image
draw = ImageDraw.Draw(image)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
y = top


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

while True:
    r, g, b, c = apds.color_data
    brightness = colorutility.calculate_lux(r, g, b)
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    draw.text((x, y), str(brightness), font=font, fill=(0, 0, 0))
    print(brightness)
    if brightness >= 0 and brightness < 300:
        draw.text((x, y+25), "You need more light", font=font, fill=(0, 0, 0))
        print("You need more light")
    elif brightness >= 300 and brightness < 2000:
        draw.text((x, y+25), "The lighting is perfect!", font=font, fill=(0, 0, 0))
        print("The lighting is perfect!")
    else:
        draw.text((x, y+25), "The lighting is too bright", font=font, fill=(0, 0, 0))
        print("The lighting is too bright")
    display.image(image, rotation)
    time.sleep(1)
