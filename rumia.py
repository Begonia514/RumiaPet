'''
python == 3.10.6
'''

from PyQt5.QtWidgets import QApplication
import sys
from pet import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())
