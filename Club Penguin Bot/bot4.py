"""
    Club Penguin Mining Bot V.4
    __author__ = "Jonathan Kalisch"
"""

import pyautogui
import time
import random
import winsound
from PIL import ImageGrab
import math

ERROR = 4
SPEED = 226
DELAY = 1.05

DARK_DARKEST = (41, 17, 39)
DARK_MID = (49, 27, 50)
DARK_LIGHTEST = (56, 36, 61)

LIGHT_DARKEST = (72, 33, 34)
LIGHT_MID = (90, 51, 52)
LIGHT_LIGHTEST = (108, 69, 70)

MIN_TIME = 1
MAX_TIME = 2

BLUR = 32
BLOCK = 300
STEP = 3

COUNTING_COLOR = (255, 204, 102)
COUNT = 1052

Colors = [DARK_DARKEST, DARK_MID, DARK_LIGHTEST, LIGHT_DARKEST, LIGHT_MID,
          LIGHT_LIGHTEST]


# checks if the rgb values match up to a range
def same_color(shade1, shade2):
    return abs(shade1-shade2) < ERROR


# checks if given color matches a dirt shade
def is_dirt((r, g, b)):
    for color in Colors:
        if same_color(r, color[0]) and same_color(g, color[1]) and same_color(
                b, color[2]):
            return True
    return False


# checks if a block of pixels is dirt
def check_block(x, y, pixels):
    for x2 in range(x-BLOCK, x+BLOCK, STEP):
        for y2 in range(y-BLOCK, y+BLOCK, STEP):
            if not is_dirt(pixels[x, y]):
                return False
    return True


# randomly finds dirt within the given area
def get_dirt():
    im = ImageGrab.grab()
    dim = im.size
    pixels = im.load()
    shrunk = im.resize((int(dim[0]/BLUR), int(dim[1]/BLUR)))
    pixelated = shrunk.resize((dim[0], dim[1]))
    pixelated = pixelated.load()

    while True:
        x = random.randrange(0, im.size[0])
        y = random.randrange(0, im.size[1])
        if is_dirt(pixelated[x,y]) and check_block(x, y, pixels):
            return x, y


# calculate the time needed for the penguin to walk
def calc_time(x, y, x2, y2, ratio):
    dist_x = abs(x2-x)
    dist_y = abs(y2-y)

    dist = math.sqrt(dist_x**2 + dist_y**2)
    return dist/SPEED * DELAY * ratio


# an innocent approach to finding the screen size
def get_ratio():
    im = ImageGrab.grab()
    pixels = im.load()
    count = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pixels[x, y] == COUNTING_COLOR:
                count += 1
    print count
    return math.sqrt(COUNT/float(count))     # ratio of areas is the ratio of
    # distances squared


# actual bot code
time.sleep(3)
winsound.Beep(1000, 100)
x, y = pyautogui.position()
ratio = get_ratio()
print ratio
while True:
    winsound.Beep(1000, 100)
    new_x, new_y = get_dirt()
    t = calc_time(x, y, new_x, new_y, ratio)
    x, y = new_x, new_y

    pyautogui.moveTo(x, y, 1)
    pyautogui.click()

    time.sleep(t)
    pyautogui.hotkey("d")
    time.sleep(11.5)
