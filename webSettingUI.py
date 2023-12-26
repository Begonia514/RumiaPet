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
        font = QFont('萝莉体')
        font.setPointSize(14)  # 设置字体大小
        self.nameEdit.setFont(font)
        self.urlEdit.setFont(font)

        okButton = QPushButton('确定')
        okButton.clicked.connect(self.accept)
        okButton.setFont(font)

        deleteButton = QPushButton('删除')
        deleteButton.clicked.connect(self.deleteItem)
        deleteButton.setFont(font)

        cancelButton = QPushButton('取消')
        cancelButton.clicked.connect(self.reject)
        cancelButton.setFont(font)

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
        font = QFont('萝莉体')
        reply = QMessageBox(QMessageBox.Question, "删除收藏", "确认要将删除此项收藏吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.setFont(font)
        qyes.setFont(font)
        qno.setFont(font)
        reply.exec_()
        if reply.clickedButton() == qyes:
            cfg.webSettingIsChange = True
            # 更改addButton
            if self.item.listWidget().count() <= cfg.maxWebItem:
                self.item.listWidget().parentWidget().addButton.setText('添加项')

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
        if self.listWidget.count() < cfg.maxWebItem:
            self.addButton.setText('添加项')

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
        self.tipLabel = QLabel('双击每一项以编辑，拖拽以排列顺序', self)
        self.tipLabel.setFont(font)


        self.listWidget = webList(self)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet(  "QListWidget {" \
                                        "background-color: rgba(255, 255, 255, 128);" \
                                        "}" \
                                        "QListWidget::item { background-color: rgba(63, 63, 63, 63); border: 2px solid black; border-radius: 5px; }")
        print(self.listWidget.styleSheet())
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
        if self.listWidget.count() >= cfg.maxWebItem:
            self.addButton.setText(f'最多{cfg.maxWebItem}个item')

        # self.saveButton = QPushButton('保存')
        # self.saveButton.clicked.connect(self.saveItemsToCSV)
        # self.saveButton.setStyleSheet(Style.defaultButton)



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

        if self.listWidget.count() >= cfg.maxWebItem:
            self.addButton.setText(f'最多{cfg.maxWebItem}个item')
            return



        dialog = QDialog(self)
        dialog.setWindowTitle('添加待办')

        titleEdit = QLineEdit()
        describeEdit = QTextEdit()

        titleEdit.setPlaceholderText('名称')
        describeEdit.setPlaceholderText('url')

        # 设置字体大小
        font = QFont('萝莉体')
        font.setPointSize(14)
        titleEdit.setFont(font)
        describeEdit.setFont(font)
        dialog.setFont(font)

        formLayout = QFormLayout()
        formLayout.addRow('名称:', titleEdit)
        formLayout.addRow('url:', describeEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        # 将按钮文本改为中文
        buttonBox.button(QDialogButtonBox.Ok).setText('确定')
        buttonBox.button(QDialogButtonBox.Cancel).setText('取消')

        formLayout.addRow(buttonBox)

        dialog.setLayout(formLayout)

        result = dialog.exec_()

        if result == QDialog.Accepted:
            name = titleEdit.text()
            url = describeEdit.toPlainText()  # 修正此行，使用 toPlainText() 方法获取文本

            if not name or not url:
                QMessageBox.warning(self, '警告', '名称与url都不能为空!')
                return

            cfg.webSettingIsChange = True

            newItem = QListWidgetItem(name)
            newItem.setData(Qt.UserRole, url)

            newItem.setSizeHint(QSize(newItem.sizeHint().width(), cfg.webItemHeight))  # 设置Item的高度
            # 设置Item内部字体大小
            font = QFont("萝莉体", 14)  # 设置字体大小
            font.setBold(False)
            newItem.setFont(font)
            self.listWidget.addItem(newItem)

            if self.listWidget.count() >= cfg.maxWebItem:
                self.addButton.setText(f'最多{cfg.maxWebItem}个item')


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
                    font = QFont("萝莉体", 14)  # 设置字体大小
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
