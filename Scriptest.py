# -*- coding:utf-8 -*-

import win32gui
import win32api
import win32con
import win32clipboard
import time
from PIL import ImageGrab
from PIL import Image
# import numpy as np
import operator


class GameAssist:

    def __init__(self, wdname):
        """初始化"""

        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()

        # 窗口显示最前面
        win32gui.SetForegroundWindow(self.hwnd)

        # 主截图的左上角坐标和右下角坐标
        # self.scree_left_and_right_point = win32gui.GetWindowRect(self.hwnd)
        self.scree_left_and_right_point = (1695, 785, 2535, 1135)

        # 物品栏宽高
        self.im_width = 70

    def screenshot(self):
        """屏幕截图"""

        # 1、用grab函数截图，参数为左上角和右下角左标
        image = ImageGrab.grab(self.scree_left_and_right_point)
        image.save('as.png')

        # 2、分切小图
        image_list = {}
        offset = self.im_width

        # 5行12列
        for x in range(5):
            image_list[x] = {}
            for y in range(12):
                # print("show",x, y)
                # exit()
                top = x * offset + 10
                left = y * offset + 10
                right = (y + 1) * offset - 10
                bottom = (x + 1) * offset - 10

                # 用crop函数切割成小图标，参数为图标的左上角和右下角左边
                im = image.crop((left, top, right, bottom))
                # 将切割好的图标存入对应的位置
                image_list[x][y] = im
                # savepath = 'list'+str(x)+','+str(y)+'.png'
                # print(savepath)
                # im.save(savepath)
        return image_list

    def isMatch(self, im1, im2):
        """汉明距离判断两个图标是否一样"""

        # 1、缩小图标，转成灰度
        image1 = im1.resize((20, 20), Image.ANTIALIAS).convert("L")
        image2 = im2.resize((20, 20), Image.ANTIALIAS).convert("L")

        # 将灰度图标转成01串,即系二进制数据
        pixels1 = list(image1.getdata())
        pixels2 = list(image2.getdata())

        avg1 = sum(pixels1) / len(pixels1)
        avg2 = sum(pixels2) / len(pixels2)
        hash1 = "".join(map(lambda p: "1" if p > avg1 else "0", pixels1))
        hash2 = "".join(map(lambda p: "1" if p > avg2 else "0", pixels2))

        # 统计两个01串不同数字的个数
        match = sum(map(operator.ne, hash1, hash2))
        print(match)

        # 阀值设为10
        return match

    def movemouse(self, x, y):
        """移动鼠标"""

        point = (x, y)
        win32api.SetCursorPos(point)

    def keyboardclick(self):
        """复制物品文本"""

        time.sleep(0.2)
        win32api.keybd_event(17, 0, 0, 0)
        win32api.keybd_event(67, 0, 0, 0)
        time.sleep(0.2)
        win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)
        win32clipboard.OpenClipboard()
        text_result = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return text_result

    # 程序入口、控制中心
    def start(self):

        # 1、先截取游戏区域大图，然后分切每个小图
        image_list = self.screenshot()
        # 2、遍历所有非空物品格
        for x1 in range(4):
            for y1 in range(5):
                if self.isMatch(image_list[x1][y1], image_list[0][0]) > 100:
                    print(x1, y1)
                    xx1 = self.scree_left_and_right_point[0] + (self.im_width//2) + self.im_width * (y1)
                    yy1 = self.scree_left_and_right_point[1] + (self.im_width//2) + self.im_width * (x1)
                    print(xx1, yy1)
                    self.movemouse(xx1, yy1)
                    text = self.keyboardclick()
                    if '稀 有 度: 通货' in text:
                        # time.sleep(1)
                        # self.movemouse(980, 190)
                        # time.sleep(0.5)
                        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                        # time.sleep(0.5)
                        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                        # time.sleep(1)
                        # self.movemouse(xx1, yy1)
                        # time.sleep(0.5)
                        win32api.keybd_event(17, 0, 0, 0)
                        # time.sleep(0.2)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                        time.sleep(0.2)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                        # time.sleep(0.2)
                        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
                        # time.sleep(0.2)

                    print(text)
        # 2、识别小图标，收集编号
        # self.image2num(image_list)

        # print(self.im2num_arr)

        # 3、遍历查找可以相连的坐标
        # while not self.isAllZero(self.im2num_arr):
        #     for x1 in range(1, 9):
        #         for y1 in range(1, 13):
        #             if self.im2num_arr[x1][y1] == 0:
        #                 continue

        #             for x2 in range(1, 9):
        #                 for y2 in range(1, 13):
        #                     # 跳过为0 或者同一个
        #                     if self.im2num_arr[x2][y2] == 0 or (x1 == x2 and y1 == y2):
        #                         continue
        #                     if self.isReachable(x1, y1, x2, y2):
        #                         self.clickAndSetZero(x1, y1, x2, y2)
        # x = 1735
        # y = 824
        # self.movemouse(x, y)
        # text = self.keyboardclick()
        # print(text)


if __name__ == "__main__":
    # wdname 为连连看窗口的名称，必须写完整
    wdname = u'Path of Exile'
    # wdname = u'WeGame'
    # wdname = u'PyWin32'

    demo = GameAssist(wdname)
    demo.start()
