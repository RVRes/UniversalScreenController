# import pyautogui
import time
# from pyscreeze import Box
# import sysm
# from PIL import Image, ImageDraw
# from Logger import time_of_function
#
# screenWidth, screenHeight = pyautogui.size()
# print(screenWidth, screenHeight)
#
# # Mouse position
# deadline = time.monotonic() + 0
# while time.monotonic() < deadline:
#     currentMouseX, currentMouseY = pyautogui.position()
#     print(currentMouseX, currentMouseY)
#     time.sleep(1)
#
# # pyautogui.alert('This is the message to display.')
#
# # drawings mouse
# # distance = 200
# distance = 0
# while distance > 0:
#     pyautogui.drag(distance, 0, duration=0.5)  # move right
#     distance -= 5
#     pyautogui.drag(0, distance, duration=0.5)  # move down
#     pyautogui.drag(-distance, 0, duration=0.5)  # move left
#     distance -= 5
#     pyautogui.drag(0, -distance, duration=0.5)  # move up
#
# # screenshots
# # t1 = time.monotonic()
# # pyautogui.screenshot('img/foo.png')
# # print('full screenshot in: ', time.monotonic() -t1, 's.')
#
# # t1 = time.monotonic()
# # pyautogui.screenshot()
# # print('screenshot object in: ', time.monotonic() - t1, 's.')
# #
# # t1 = time.monotonic()
# # pyautogui.screenshot('img/foo2.png', region=(0, 0, 680, 380))
# # print('1/4 screenshot in: ', time.monotonic() -t1, 's.')
# #
# # t1 = time.monotonic()
# # pyautogui.screenshot(region=(0, 0, 680, 380))
# # print('1/4 screenshot object in: ', time.monotonic() -t1, 's.')
#
# # t1 = time.monotonic()
# # b1 = pyautogui.locateOnScreen('SCREENSHOTS/b1.png')
# # print('found in', time.monotonic() - t1, 's.')
# # print(b1)
# #
# # t1 = time.monotonic()
# # b1 = pyautogui.locateOnScreen('IMG/throw_rod.png', confidence=0.7, grayscale=True)
# # print('found in', time.monotonic() - t1, 's.')
# # print(b1, type (b1))
#
# # b1 = (b1.left + 100, b1.top, b1.width, b1.height)
#
# # for i in range(0, 10):
# #     t1 = time.monotonic()
# #     b2 = pyautogui.locateOnScreen('IMG/throw_rod.png', region=b1, confidence=0.7,
# #                                   grayscale=True)
# #     print('found in region', time.monotonic() - t1, 's.')
# #     print(b2)
#
# # b1 = sysm.find_zone_onpic('IMG/throw_rod.png', 'SCREENSHOTS/sc1.png')
#
# # im = Image.new('RGB', (500, 300), (219, 193, 27))
#
#
# # Рисуем синий прямоугольник с белой оконтовкой.
#
#
# # @time_of_function
# # def findbobber_region(where, color, bobber_area):
# #     for i in range(where['left'], where['left'] + where['width']):
# #         for j in range(where['top'], where['top'] + where['height']):
# #             color_found = pyautogui.pixelMatchesColor(i, j, color, tolerance=tolerance)
# #             if color_found:
# #                 region = Box(left=i - bobber_area, top=j - bobber_area, width=bobber_area * 2, height=bobber_area * 2)
# #                 return region
#
# # @time_of_function
# # def check_bobber(where, color):
# #     for i in range(where.left, where.left + where.width):
# #         for j in range(where.top, where.top + where.height):
# #             color_found = pyautogui.pixelMatchesColor(i, j, color, tolerance=tolerance)
# #             if color_found:
# #                 return True
# #             else:
# #                 return False
#
#
#
#
# color = (36, 255, 0)
# for i in range(10, 600):
#     for j in range(50, 400):
#         # color_found = pyautogui.pixelMatchesColor(i, j, (36, 255, 0), tolerance=10)
#         color_found =pyautogui.pixelMatchesColor(100, 200, (130, 135, 144))
#         # print(i,j,color_found)
#         if color_found:
#             region = Box(left=i - 20, top=j - 20, width=20 * 2, height=20 * 2)
#             print(region)
#
#
#
# @time_of_function
# def findbobber_region(what, where, bobber_area):
#     b1 = pyautogui.locateOnScreen(what, region=where, confidence=0.7, grayscale=True)
#     if b1:
#         # b2 = Box(left=b1.left - bobber_area, top=b1.top, width=b1.width + bobber_area*2, height=b1.height + bobber_area*2)
#         # b2 = Box(left=b1.left +2 , top=b1.top + 23, width=b1.width+45, height=b1.height)
#         b2 = Box(left=593, top=153, width=70, height=50)
#         return b2
#
#
#
#     def pull_fish(self):
#         sysm.mousedownoncoord(self.push_rod_region)
#         time.sleep(1)
#         sysm.mouseup()
#         sysm.mousedownoncoord(self.push_rod_region)
#         time.sleep(1)
#         sysm.mouseup()
#         sysm.mousedownoncoord(self.push_rod_region)
#         time.sleep(4)
#         sysm.mousedownoncoord(self.push_rod_region)
#         time.sleep(5)
#         # sysm.screenshot_with_region(self.sceenshotsdir + '/scr_region_3.png', self.push_rod_region)
#         sysm.mouseup()
#         fish_grabbed = sysm.findpiconregion(self.grab_fish_img, self.game_area)
#         if fish_grabbed:
#             sysm.clickonpic(self.grab_fish_img, self.game_area)
#             time.sleep(1)

print(time.monotonic())

for j in range(2, 10):
    strn=''
    for i in range(1, 5):
        strn +=str(int((0.1 + i / j)*100)/100)+' '
    print(j, strn)
