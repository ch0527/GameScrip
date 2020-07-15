# -*- coding:utf-8 -*-

import win32gui
# import time
# from PIL import ImageGrab, Image
# import numpy as np
# import operator


class GameAssist:

    def __init__(self, wdname):
        """初始化"""

        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()

