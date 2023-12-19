import re
class SettingUIChecker:

    def __init__(self, text):
        self.text = text

    def Checker1(self, text):
        pattern = re.compile(r'^[1-2]\.\d$')
        return pattern.match(text)