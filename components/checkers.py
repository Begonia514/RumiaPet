import re

import config


class SettingUIChecker:

    def __init__(self, text):
        self.text = text

    # 校验1到2之间的一位小数
    def Checker0(self, text):
        pattern = re.compile(r'^0\.[5-9]$|^1\.0$')
        return pattern.match(text)

    # 校验0到屏幕高度height之间的整数
    def Checker1(self, text):
        cfg = config.ConfigGetter()
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= cfg.SCREEN_HEIGHT:
            return True
        else:
            return False

    # 校验0到4之间的一位小数
    def Checker2(self, text):
        pattern = re.compile(r'^[0-3](\.[0-9])?|4(\.0)?$')
        return pattern.match(text)
    def Checker3(self, text):
        pattern = re.compile(r'^[0-3](\.[0-9])?|4(\.0)?$')
        return pattern.match(text)

    def Checker4(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= 10:
            return True
        else:
            return False

    def Checker5(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 100 <= value <= 200:
            return True
        else:
            return False

    def Checker6(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= 40:
            return True
        else:
            return False

    def Checker7(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= 64:
            return True
        else:
            return False

    def Checker8(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= 64:
            return True
        else:
            return False

    def Checker9(self, text):
        if text.isdigit():
            value = int(text)
        else:
            return False

        if 0 <= value <= 100:
            return True
        else:
            return False