import digitalio
import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
from datetime import datetime, timedelta

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


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


# get a time from the user
usertime = ""
while not usertime:
    try:
        # get a time the user wishes to wake up
        usertime = input('Type the date and time you wish to wake up in the format "xx/xx/xxxx xx:xx" in military time and hit enter: ')
        # put it in a format so we can manipulate it
        wakeup = datetime.strptime(usertime, "%m/%d/%Y %H:%M")
        thirtybefore = wakeup - timedelta(minutes=30)
        fifteenbefore = wakeup - timedelta(minutes=15)
        # put it in a format so we can compare it with the current time
        wakeup = datetime.strftime(wakeup, "%m/%d/%Y %H:%M")
        thirtybefore = datetime.strftime(thirtybefore, "%m/%d/%Y %H:%M")
        fifteenbefore = datetime.strftime(fifteenbefore, "%m/%d/%Y %H:%M")
    except ValueError:
        # catch if a user inputs an incorrect format
        print("Please input the date and time in the correct format")
        usertime = ""
#Main loop
while True:
    currenttime = datetime.strftime(datetime.now(), "%m/%d/%Y %H:%M")
    if wakeup == currenttime:
        backlight.value = True
        display.fill(color565(255, 255, 255))
    if thirtybefore == currenttime:
        backlight.value = True
        display.fill(color565(255, 153, 153))
    if fifteenbefore == currenttime:
        backlight.value = True
        display.fill(color565(255, 255, 102))
