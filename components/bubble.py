import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class BubbleWindow(QMainWindow):
    def __init__(self, imagePath: str, posiX: int, posiY: int):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        pixmap = QPixmap(imagePath)
        width = pixmap.width()
        height = pixmap.height()
        screen = QDesktopWidget().screenGeometry()
        desktop = QDesktopWidget().availableGeometry()

        # Adjust the initial position to ensure the window is visible
        if desktop.width() < posiX + width:
            posiX = desktop.width() - width

        if desktop.height() < posiY + height:
            posiY = desktop.height() - height

        self.setGeometry(posiX, posiY, width, height)

        # Create QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.setGeometry(0, 0, width, height)

        self.image_label.move(0, 0)

        self.show()

        # Fade-in animation
        self.fade_in_animation = QPropertyAnimation(self, b'windowOpacity')
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setDuration(1000)  # Fade-in time is set to 1 second
        self.fade_in_animation.finished.connect(self.start_display_timer)

        # Create a timer to start fading out after 3 seconds
        self.display_timer = QTimer(self)
        self.display_timer.timeout.connect(self.start_fade_out)
        self.display_timer.start(3000)  # 3 seconds before triggering fade-out

        # Start fade-in animation
        self.fade_in_animation.start()

    def start_display_timer(self):
        # Stop fade-in animation and start a timer to fade out after 3 seconds
        self.display_timer.start(3000)

    def start_fade_out(self):
        # Fade-out animation
        self.fade_out_animation = QPropertyAnimation(self, b'windowOpacity')
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setDuration(2000)  # Fade-out time is set to 2 seconds
        self.fade_out_animation.finished.connect(self.close)
        self.fade_out_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BubbleWindow("../data/rumia/hideBubble.png",11000,1800)
    sys.exit(app.exec_())
