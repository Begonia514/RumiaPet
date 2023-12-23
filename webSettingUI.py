import sys,csv,os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from style import Style
from config import ConfigGetter


class ItemDialog(QDialog):
    def __init__(self, item, parent=None):
        super(ItemDialog, self).__init__(parent)
        self.item = item
        self.initUI()

    def initUI(self):
        '''
        用于建立编辑收藏项的UI
        :return:
        '''
        cfg = ConfigGetter()
        cfg.webSettingIsChange = False
        self.setWindowTitle('编辑项目')
        self.setGeometry(300, 300, 300, 150)

        nameLabel = QLabel('名称:')
        nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        urlLabel = QLabel('URL:')
        urlLabel.adjustSize()

        self.nameEdit = QLineEdit(self.item.text())
        self.nameEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.urlEdit = QTextEdit(self.item.data(Qt.UserRole))
        self.urlEdit.setMinimumHeight(100)
        self.urlEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置字体大小
        font = QFont()
        font.setPointSize(14)  # 设置字体大小
        self.nameEdit.setFont(font)
        self.urlEdit.setFont(font)

        okButton = QPushButton('确定')
        okButton.clicked.connect(self.accept)

        deleteButton = QPushButton('删除')
        deleteButton.clicked.connect(self.deleteItem)

        cancelButton = QPushButton('取消')
        cancelButton.clicked.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox.addWidget(deleteButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(nameLabel)
        vbox.addWidget(self.nameEdit)
        vbox.addWidget(urlLabel)
        vbox.addWidget(self.urlEdit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def deleteItem(self):
        '''
        删除收藏时触发
        :return:
        '''
        cfg = ConfigGetter()
        reply = QMessageBox(QMessageBox.Question, "删除收藏", "确认要将删除此项收藏吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == qyes:
            cfg.webSettingIsChange = True
            self.item.listWidget().takeItem(self.item.listWidget().row(self.item))
            self.accept()

class webList(QListWidget):
    def __init__(self, parent=None):
        super(webList, self).__init__(parent)

    def dropEvent(self, event):
        cfg = ConfigGetter()
        cfg.webSettingIsChange = True
        try:
            super().dropEvent(event)
        except Exception as e:
            print(e)

class WebWindow(QTabWidget):
    def __init__(self):
        super(WebWindow, self).__init__()
        self.setGeometry(0,0,800,540)
        self.background_label = QWidget(self)
        self.background_label.setGeometry(0,0,800,540)
        self.background_label.setStyleSheet("background-image: url(./data/rumia/bkg36.png);"
                                            "background-color: rgba(192, 192, 192, 10);"
                                            "QWidget { border: none; }")

        self.initUI()

    # def currentChanged(self):
    #     print("web change")
    def itemChanged(self):
        '''
        项进行位置交换或移动时触发
        :return:
        '''
        cfg = ConfigGetter()
        cfg.webSettingIsChange = True

    def initUI(self):
        '''
        用于建立“网站设置”栏UI的函数
        :return:
        '''
        cfg = ConfigGetter()
        cfg.webSettingIsChange = False
        self.setObjectName('RumiaSetting')
        # self.setWindowTitle('Item交换与编辑')


        font = QFont('萝莉体')
        font.setBold(True)
        font.setWeight(75)

        # 顶部提示
        self.tipLabel = QLabel('双击每一项以编辑', self)
        self.tipLabel.setFont(font)


        self.listWidget = QListWidget(self)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("background-color: transparent;")
        self.listWidget.itemChanged.connect(self.itemChanged)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragDropMode(QListWidget.InternalMove)
        self.listWidget.itemDoubleClicked.connect(self.editItem)

        self.listWidget.setIconSize(QSize(50, cfg.webItemHeight))  # 设置Item图标的大小

        self.listWidget.setSpacing(cfg.webItemHeight // 8)  # 设置Item之间的间隔

        self.loadItemsFromCSV()  # 从CSV文件加载数据

        # 添加按钮
        self.addButton = QPushButton('添加项', self)
        #self.addButton.setGeometry(QRect(50, 480, 120, 40))
        self.addButton.setFixedSize(120, 40)
        self.addButton.setObjectName("restorationConfig")
        self.addButton.setFont(font)
        self.addButton.clicked.connect(self.addWebItem)
        self.addButton.setStyleSheet(Style.defaultConfigButton)
        self.addButton.setFixedHeight(40)

        # self.saveButton = QPushButton('保存')
        # self.saveButton.clicked.connect(self.saveItemsToCSV)
        # self.saveButton.setStyleSheet(Style.defaultButton)

        self.maxItems = 15

        vbox = QVBoxLayout()
        vbox.addWidget(self.tipLabel)
        vbox.addWidget(self.listWidget)
        vbox.addWidget(self.addButton)
        # vbox.addWidget(self.saveButton)

        self.setLayout(vbox)

    def closeEvent(self):
        print('webTab Close')

    def addWebItem(self):
        cfg = ConfigGetter()
        cfg.webSettingIsChange = True
        cfg = ConfigGetter()
        if self.listWidget.count() < self.maxItems:
            newItem = QListWidgetItem('New Item')
            newItem.setData(Qt.UserRole, 'https://example.com/')

            newItem.setSizeHint(QSize(newItem.sizeHint().width(), cfg.webItemHeight))  # 设置Item的高度
            # 设置Item内部字体大小
            font = QFont("SimSun", 14)  # 设置字体大小
            font.setBold(False)
            newItem.setFont(font)
            self.listWidget.addItem(newItem)
        else:
            self.addButton.setText(f'最多{self.maxItems}个item')

    def editItem(self, item):
        cfg = ConfigGetter()
        dialog = ItemDialog(item, self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            cfg.webSettingIsChange = True
            item.setText(dialog.nameEdit.text())
            item.setData(Qt.UserRole, dialog.urlEdit.toPlainText())
        # #自下而上 一层层传递
        # isChange = isChange or dialog.isChange

    def loadItemsFromCSV(self):
        cfg = ConfigGetter()
        filePath = cfg.webDataPath
        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                file.close()
                pass
        try:
            with open(filePath,'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    item = QListWidgetItem(row[0])
                    item.setData(Qt.UserRole, row[1])
                    item.setSizeHint(QSize(item.sizeHint().width(), cfg.webItemHeight))
                    font = QFont("SimSun", 14)  # 设置字体大小
                    font.setBold(False)
                    item.setFont(font)
                    self.listWidget.addItem(item)
        except FileNotFoundError:
            pass

    def saveItemsToCSV(self):

        cfg = ConfigGetter()
        cfg.webSettingIsChange = False
        items = self.getNowItems()

        try:
            with open(cfg.webDataPath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for item in items:
                    writer.writerow(item)
        except FileNotFoundError as e:
            raise e

    def getNowItems(self):
        items = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            name = item.text()
            url = item.data(Qt.UserRole)
            items.append([name, url])
        return items


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置全局主题风格
    app.setStyle('Fusion')
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(173, 216, 230, 150))  # 天蓝色半透明背景
    app.setPalette(palette)

    mainWindow = WebWindow()
    mainWindow.show()

    sys.exit(app.exec_())
