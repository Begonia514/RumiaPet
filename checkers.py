import re
class SettingUIChecker:

    def __init__(self, text):
        self.text = text

    def OneDecimalChecker(self, text, intPart):
        pattern = re.compile(r'^[0-4]\.\d$')
        return pattern.match(text)