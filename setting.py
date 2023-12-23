import petSettingUI
from config import ConfigGetter
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from webSettingUI import WebWindow
from petSettingUI import Petwindow
from style import Style


class PetSetting(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self, parent=None):
        super(PetSetting, self).__init__(parent)

        self.setupUi(self)

    def setupUi(self, MainWindow):
        '''
        建立设置菜单的大框架的UI
        :param MainWindow: Setting的父类
        :return:
        '''
        self.setWindowTitle("宠物设置界面")
        self.setWindowIcon(QIcon('./favicon.ico'))
        MainWindow.setObjectName("RumiaSetting")
        MainWindow.setFixedSize(800, 540)

        self.settingUI = Petwindow()
        self.settingUI.setParent(self)

        font = QFont("萝莉体")
        font.setBold(True)
        font.setWeight(75)

        self.saveAllButton = QPushButton(self)
        self.saveAllButton.setGeometry(QRect(650, 480, 120, 40))
        self.saveAllButton.setObjectName("save")
        self.saveAllButton.setStyleSheet(Style.defaultButton)
        self.saveAllButton.setFont(font)
        self.saveAllButton.setText("全部保存")
        self.saveAllButton.clicked.connect(self.saveAll)

        QMetaObject.connectSlotsByName(MainWindow)

        # self.QTabWidget1.currentChanged.connect(self.tabChanged)

    def saveAll(self):
        cfg = ConfigGetter()
        if cfg.settingUICheck:
            try:
                self.petTab.savecfg2()
                self.webTab.saveItemsToCSV()
            except Exception as e:
                QMessageBox.critical(self, '发生错误', f'发生了一个错误:\n{type(e).__name__}: {str(e)}')
                return
            info = QMessageBox(QMessageBox.Information, "提示", "修改成功！")
            qyes = info.addButton(self.tr("确定"), QMessageBox.YesRole)
            info.exec_()
        else:
            info = QMessageBox(QMessageBox.Information, "提示", "存在不符合要求的输入")
            qyes = info.addButton(self.tr("确定"), QMessageBox.YesRole)
            info.exec_()

    def closeEvent(self, event):
        '''
        用于解决设置窗口被关闭时的事件，主要关注退出时是否有未保存的设置
        :param event:
        :return:
        '''
        cfg = ConfigGetter()
        isChange = cfg.petSettingIsChange or \
                   cfg.webSettingIsChange
        print(f"{cfg.petSettingIsChange}")
        print(f"{cfg.webSettingIsChange}")

        if not isChange:
            self.hide()
            event.ignore()
            return

        reply = QMessageBox(QMessageBox.Question, "设置未保存", "有修改但未保存，确定要退出吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()

        if reply.clickedButton() == qyes:
            self.hide()
            event.ignore()
        else:
            event.ignore()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

class WebSetting(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self, parent=None):
        super(WebSetting, self).__init__(parent)

        self.setupUi(self)

    def setupUi(self, MainWindow):
        '''
        建立设置菜单的大框架的UI
        :param MainWindow: Setting的父类
        :return:
        '''
        self.setWindowTitle("网站设置界面")
        self.setWindowIcon(QIcon('./favicon.ico'))
        MainWindow.setObjectName("RumiaSetting")
        MainWindow.setFixedSize(800, 540)

        self.settingUI = WebWindow()
        self.settingUI.setParent(self)

        font = QFont("萝莉体")
        font.setBold(True)
        font.setWeight(75)

        self.saveAllButton = QPushButton(self)
        self.saveAllButton.setGeometry(QRect(650, 487, 120, 40))
        self.saveAllButton.setObjectName("save")
        self.saveAllButton.setStyleSheet(Style.defaultButton)
        self.saveAllButton.setFont(font)
        self.saveAllButton.setText("全部保存")
        self.saveAllButton.clicked.connect(self.saveAll)

        QMetaObject.connectSlotsByName(MainWindow)

        # self.QTabWidget1.currentChanged.connect(self.tabChanged)

    def saveAll(self):
        cfg = ConfigGetter()
        if cfg.settingUICheck:
            try:
                self.petTab.savecfg2()
                self.webTab.saveItemsToCSV()
            except Exception as e:
                QMessageBox.critical(self, '发生错误', f'发生了一个错误:\n{type(e).__name__}: {str(e)}')
                return
            info = QMessageBox(QMessageBox.Information, "提示", "修改成功！")
            qyes = info.addButton(self.tr("确定"), QMessageBox.YesRole)
            info.exec_()
        else:
            info = QMessageBox(QMessageBox.Information, "提示", "存在不符合要求的输入")
            qyes = info.addButton(self.tr("确定"), QMessageBox.YesRole)
            info.exec_()

    def closeEvent(self, event):
        '''
        用于解决设置窗口被关闭时的事件，主要关注退出时是否有未保存的设置
        :param event:
        :return:
        '''
        cfg = ConfigGetter()
        isChange = cfg.petSettingIsChange or \
                   cfg.webSettingIsChange
        print(f"{cfg.petSettingIsChange}")
        print(f"{cfg.webSettingIsChange}")

        if not isChange:
            self.hide()
            event.ignore()
            return

        reply = QMessageBox(QMessageBox.Question, "设置未保存", "有修改但未保存，确定要退出吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()

        if reply.clickedButton() == qyes:
            self.hide()
            event.ignore()
        else:
            event.ignore()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None