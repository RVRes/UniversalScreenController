import pyautogui
from PIL import Image, ImageDraw
from Logger import time_of_function
import os
import time
from pyscreeze import Box

confidence = 0.7
grayscale = True
tolerance = 10


@time_of_function
def findpiconscreen(what):
    b1 = pyautogui.locateOnScreen(what, confidence=confidence, grayscale=False)
    return b1


@time_of_function
def findpiconregion(what, where):
    b1 = pyautogui.locateOnScreen(what, region=where, confidence=0.7, grayscale=True)
    return b1


@time_of_function
def clickonpic(what, where):
    buttonpoint = pyautogui.locateCenterOnScreen(what, region=where, confidence=0.7, grayscale=False)
    if buttonpoint:
        button_x, button_y = buttonpoint
        pyautogui.click(button_x, button_y)
        return True
    else:
        return False


def clearscreen():
    os.system('cls')


@time_of_function
def clickoncoord(where):
    button_x = where.left + int(where.width / 2)
    button_y = where.top + int(where.height / 2)
    pyautogui.click(button_x, button_y)

@time_of_function
def mousedownoncoord(where):
    button_x = where.left + int(where.width / 2)
    button_y = where.top + int(where.height / 2)
    pyautogui.mouseDown(button_x, button_y)


@time_of_function
def mouseup():
    pyautogui.mouseUp()

@time_of_function
def clickandholdoncoord(where, duration):
    mousedownoncoord(where)
    time.sleep(duration)
    mouseup()

@time_of_function
def makescreenshot(name):
    pyautogui.screenshot(name)


@time_of_function
def check_bobber(what, where):
    b1 = pyautogui.locateOnScreen(what, region=where, confidence=0.5, grayscale=True)
    if b1:
        return True
    else:
        return False


@time_of_function
def findpiconregion(what, where):
    b1 = pyautogui.locateOnScreen(what, region=where, confidence=0.7, grayscale=True)
    return b1


def get_time():
    t2 = time.localtime()
    return str(time.strftime("%H:%M:%S", t2))


@time_of_function
def find_files_list(search_string, search_directory):
    files = os.listdir(search_directory)
    images = [i for i in files if i.startswith(search_string)]
    return images


@time_of_function
def screenshot_with_region(name, region):
    def save_zone_with_rectangle(image, zone):
        if zone:
            im = Image.open(image)
            draw = ImageDraw.Draw(im)
            draw.rectangle(zone, outline=(0, 162, 232))
            # out_image = image.split('.')[0] + '_region.png'
            im.save(name, quality=95)

    if name and region:
        pyautogui.screenshot(name)
        region = (region.left, region.top, region.left + region.width, region.top + region.height)
        save_zone_with_rectangle(name, region)


