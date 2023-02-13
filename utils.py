from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import datetime
from logger import logger

def highlight_pixel(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.rectangle([x-5, y-5, x+5, y+5], outline="red")

def make_time_readable(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def make_time_spent_readable(time):
    return datetime.datetime.fromtimestamp(time).strftime('%M:%S')

def is_color_different(rgb1, rgb2, level = 30):
    r_diff = abs(rgb1[0] - rgb2[0])
    g_diff = abs(rgb1[1] - rgb2[1])
    b_diff = abs(rgb1[2] - rgb2[2])
    logger.info("r_diff: %s, g_diff: %s, b_diff: %s", r_diff, g_diff, b_diff)

    if r_diff > level or g_diff > level or b_diff > level:
        return True
    else:
        return False

def print_rgb_color(rgb):
    print("\033[38;2;{};{};{}mThis text is in RGB color\033[0m".format(rgb[0], rgb[1], rgb[2]))

rgb = (255, 0, 0)

print_rgb_color(rgb)