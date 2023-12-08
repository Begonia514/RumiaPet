from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys,csv,os
from config import ConfigGetter
from style import Style


class scheduleList(QListWidget):
    def __init__(self, parent=None):
        super(scheduleList, self).__init__(parent)

    def dropEvent(self, event):
        if event.source() and event.source().objectName() != self.objectName():
            cfg = ConfigGetter()

            dialog = ItemDialog(event.source().currentItem())
            newItem = QListWidgetItem(dialog.titleEdit.text())
            newItem.setData(Qt.UserRole,dialog.describeEdit.toPlainText())
            newItem.setFlags(newItem.flags() | Qt.ItemIsUserCheckable)
            if self.objectName()== "todoList":
                newItem.setCheckState(Qt.Unchecked)
            else:
                newItem.setCheckState(Qt.Checked)

            newItem.setSizeHint(QSize(newItem.sizeHint().width(), cfg.scheduleItemHeight))  # 设置Item的高度
            # 设置Item内部字体大小
            font = QFont("SimSun", 14)  # 设置字体大小
            font.setBold(False)
            newItem.setFont(font)

            position = event.pos()
            dropIndex = self.indexAt(position)
            if dropIndex.isValid():
                row = dropIndex.row()
                self.insertItem(row, newItem)
            else:
                self.addItem(newItem)

            sourceItem = event.source().currentItem()
            row = event.source().row(sourceItem)
            event.source().takeItem(row)
        else:
            try:
                super().dropEvent(event)
            except Exception as e:
                print(e)

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
        cfg.scheduleIsChange = False
        self.setWindowTitle('编辑日程')
        self.setGeometry(300, 300, 300, 150)

        titleLabel = QLabel('标题:')
        titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        describeLabel = QLabel('描述:')
        describeLabel.adjustSize()

        self.titleEdit = QLineEdit(self.item.text())
        self.titleEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


        self.describeEdit = QTextEdit(self.item.data(Qt.UserRole))
        self.describeEdit.setMinimumHeight(100)
        # 设置 QTextEdit 的大小策略，使其能够在垂直方向上动态扩展
        self.describeEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 设置字体大小
        font = QFont()
        font.setPointSize(14)  # 设置字体大小
        self.titleEdit.setFont(font)
        self.describeEdit.setFont(font)

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
        vbox.addWidget(titleLabel)
        vbox.addWidget(self.titleEdit)
        vbox.addWidget(describeLabel)
        vbox.addWidget(self.describeEdit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)



    def deleteItem(self):
        '''
        删除日程时触发
        :return:
        '''
        cfg = ConfigGetter()
        reply = QMessageBox(QMessageBox.Question, "删除日程", "确认要将删除此项日程吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == qyes:
            cfg.scheduleIsChange = True
            self.item.listWidget().takeItem(self.item.listWidget().row(self.item))
            self.accept()

class TodoApp(QWidget):
    def __init__(self):
        super(TodoApp, self).__init__()

        self.initUI()

    def initUI(self):
        cfg = ConfigGetter()
        cfg.scheduleIsChange = False
        self.manageMode = False
        # self.setGeometry(300, 300, 400, 400)
        self.resize(500, 600)
        self.setWindowTitle('待办日程')


        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tipLabel = QLabel('拖拽或勾选，双击每一项以编辑', self)
        self.tipLabel.setFont(font)

        self.manageButton = QPushButton('管理', self)
        self.manageButton.setFixedWidth(80)
        self.manageButton.clicked.connect(self.toggleManagementMode)


        self.deleteButton = QPushButton('删除', self)
        self.deleteButton.setFixedWidth(80)
        self.deleteButton.clicked.connect(self.deleteSelectedItems)
        self.deleteButton.setStyleSheet("background-color: pink;")
        self.deleteButton.setEnabled(False)
        self.deleteButton.setVisible(False)

        ceilingHbox = QHBoxLayout()
        ceilingHbox.addWidget(self.tipLabel)
        ceilingHbox.addWidget(self.deleteButton)
        ceilingHbox.addWidget(self.manageButton)


        font.setBold(False)
        self.leftTipLabel = QLabel('待办',self)
        self.leftTipLabel.setFont(font)

        self.rightTipLabel = QLabel('已办',self)
        self.rightTipLabel.setFont(font)

        # 左侧待办列表
        self.todoListWidget = scheduleList(self)
        self.todoListWidget.setObjectName("todoList")
        self.todoListWidget.itemDoubleClicked.connect(self.editItem)
        self.todoListWidget.setDragDropMode(QListWidget.DragDrop)
        self.todoListWidget.setDefaultDropAction(Qt.MoveAction)
        self.todoListWidget.itemChanged.connect(self.itemChanged)

        # self.todoListWidget.itemDropped.connect(self.todoDrop)


        # 右侧已办列表
        self.doneListWidget = scheduleList(self)
        self.doneListWidget.setObjectName("doneList")
        self.doneListWidget.itemDoubleClicked.connect(self.editItem)
        self.doneListWidget.setDragDropMode(QListWidget.DragDrop)
        self.doneListWidget.setDefaultDropAction(Qt.MoveAction)
        self.doneListWidget.itemChanged.connect(self.itemChanged)

        # self.doneListWidget.itemDropped.connect(self.doneDrop)


        self.loadItemsFromCSV()


        # 添加按钮
        self.addButton = QPushButton('添加待办')
        self.addButton.clicked.connect(self.addTodoItem)
        self.addButton.setStyleSheet(Style.defaultButton)

        self.saveButton = QPushButton('保存修改')
        self.saveButton.clicked.connect(self.saveToCSV)
        # self.saveButton.setStyleSheet(Style.defaultButton)


        # 布局
        vbox = QVBoxLayout()
        vbox.addLayout(ceilingHbox)

        leftVbox = QVBoxLayout()
        leftVbox.addWidget(self.leftTipLabel)
        leftVbox.addWidget(self.todoListWidget)
        leftVbox.addWidget(self.addButton)

        rightVbox = QVBoxLayout()
        rightVbox.addWidget(self.rightTipLabel)
        rightVbox.addWidget(self.doneListWidget)


        hbox = QHBoxLayout()
        hbox.addLayout(leftVbox)
        hbox.addLayout(rightVbox)

        vbox.addLayout(hbox)
        # vbox.addWidget(self.addButton)
        vbox.addWidget(self.saveButton)

        self.setLayout(vbox)

    def toggleManagementMode(self):
        if not self.manageMode:

            self.manageMode = True

            for i in range(self.todoListWidget.count()):
                item = self.todoListWidget.item(i)
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(~Qt.ItemIsSelectable & ~Qt.ItemIsDragEnabled |
                #               Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

            for i in range(self.doneListWidget.count()):
                item = self.doneListWidget.item(i)
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(~Qt.ItemIsSelectable & ~Qt.ItemIsDragEnabled |
                #               Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Unchecked)
            self.addButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.deleteButton.setEnabled(True)
            self.deleteButton.setVisible(True)
            self.tipLabel.setText("选中想要删除的选项，并点击删除按钮")
            self.manageButton.setText('退出管理')


        else:
            for i in range(self.todoListWidget.count()):
                item = self.todoListWidget.item(i)
                item.setTextAlignment(Qt.AlignLeft)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                              Qt.ItemIsUserCheckable  |
                              Qt.ItemIsDragEnabled )
                item.setCheckState(Qt.Unchecked)

            for i in range(self.doneListWidget.count()):
                item = self.doneListWidget.item(i)
                item.setTextAlignment(Qt.AlignLeft)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                              Qt.ItemIsUserCheckable  |
                              Qt.ItemIsDragEnabled )
                item.setCheckState(Qt.Checked)

            self.manageMode = False
            self.tipLabel.setText('拖拽或勾选，双击每一项以编辑')
            self.manageButton.setText('管理')
            self.addButton.setEnabled(True)
            self.saveButton.setEnabled(True)
            self.deleteButton.setEnabled(False)
            self.deleteButton.setVisible(False)


    def deleteSelectedItems(self):
        reply = QMessageBox(QMessageBox.Question, "删除日程", "确认要将删除此项日程吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == qno:
            return


        todoLen = self.todoListWidget.count()
        doneLen = self.doneListWidget.count()
        hasDel = 0
        index = 0
        while index<todoLen:
            item = self.todoListWidget.item(index)
            print(item.text())
            print(item.checkState())
            if item.checkState() == Qt.Checked:
                self.todoListWidget.takeItem(index-hasTrans)
                todoLen -= 1;hasTrans += 1
            index+=1

        hasDel = 0
        index = 0
        while index<doneLen:
            item = self.doneListWidget.item(index)
            if item.checkState() == Qt.Checked:
                self.doneListWidget.takeItem(index-hasTrans)
                doneLen -= 1;hasTrans += 1
            index+=1


    def itemChanged(self,item):
        cfg = ConfigGetter()
        # meaning: todoList <-> Unchecked    doneList <-> Checked
        #it means correct status
        if self.manageMode :
            # if item.checkState() == Qt.Checked:
            #     item.setCheckState(Qt.Unchecked)
            # else:
            #     item.setCheckState(Qt.Unchecked)
            return

        cfg.scheduleIsChange = True
        if (item.listWidget().objectName() == "todoList") == (item.checkState() == Qt.Unchecked):
            # try:
            #     super().itemChanged(item)
            # except Exception as e:
            #     print(e)
            return

        cfg = ConfigGetter()

        dialog = ItemDialog(item)
        newItem = QListWidgetItem(dialog.titleEdit.text())
        newItem.setData(Qt.UserRole, dialog.describeEdit.toPlainText())
        newItem.setFlags(newItem.flags() | Qt.ItemIsUserCheckable)
        newItem.setSizeHint(QSize(newItem.sizeHint().width(), cfg.scheduleItemHeight))  # 设置Item的高度
        newItem.setCheckState(item.checkState())
        # 设置Item内部字体大小
        font = QFont("SimSun", 14)  # 设置字体大小
        font.setBold(False)
        newItem.setFont(font)


        if newItem.checkState() == Qt.Checked: #it means should goto doneList
            self.doneListWidget.insertItem(0,newItem)
            row = self.todoListWidget.row(item)
            self.todoListWidget.takeItem(row)

        else:
            self.todoListWidget.addItem(newItem)
            row = self.doneListWidget.row(item)
            self.doneListWidget.takeItem(row)



    def loadItemsFromCSV(self):
        cfg = ConfigGetter()
        self.loadItem(cfg.todoListPath)
        self.loadItem(cfg.doneListPath)


    def loadItem(self,filePath):
        cfg = ConfigGetter()
        if not os.path.exists(filePath):
            with open(filePath, 'w'):
                pass

        try:
            with open(filePath,'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    item = QListWidgetItem(row[0])
                    item.setData(Qt.UserRole, row[1])
                    item.setSizeHint(QSize(item.sizeHint().width(), cfg.scheduleItemHeight))
                    font = QFont("SimSun", 14)  # 设置字体大小
                    font.setBold(False)
                    item.setFont(font)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    if filePath == cfg.todoListPath:
                        item.setCheckState(Qt.Unchecked)
                        self.todoListWidget.addItem(item)
                    else:
                        item.setCheckState(Qt.Checked)
                        self.doneListWidget.addItem(item)

        except FileNotFoundError:
            pass

    def getItems(self,list:QListWidget):
        items = []
        for i in range(list.count()):
            item = list.item(i)
            title = item.text()
            describe = item.data(Qt.UserRole)
            items.append([title, describe])
        return items
    def saveToCSV(self):
        try:
            todoItems = self.getItems(self.todoListWidget)
            self.saveItemsToCSV(todoItems,'./data/schedule/todolist.csv')
            doneItems = self.getItems(self.doneListWidget)
            self.saveItemsToCSV(doneItems,'./data/schedule/donelist.csv')
        except FileNotFoundError as e:
            QMessageBox.critical(self, '发生错误', f'发生了一个错误:\n{type(e).__name__}: {str(e)}')
            return

        info = QMessageBox(QMessageBox.Information, "提示", "修改成功！")
        qyes = info.addButton(self.tr("确定"), QMessageBox.YesRole)
        info.exec_()
    def saveItemsToCSV(self,items,path):
        cfg = ConfigGetter()
        cfg.scheduleIsChange = False
        try:
            with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for item in items:
                    writer.writerow(item)
        except FileNotFoundError as e:
            raise e


    def addTodoItem(self):
        cfg = ConfigGetter()

        dialog = QDialog(self)
        dialog.setWindowTitle('添加待办')

        titleEdit = QLineEdit()
        describeEdit = QTextEdit()

        titleEdit.setPlaceholderText('标题')
        describeEdit.setPlaceholderText('描述')

        # 设置字体大小
        font = QFont()
        font.setPointSize(14)
        titleEdit.setFont(font)
        describeEdit.setFont(font)

        formLayout = QFormLayout()
        formLayout.addRow('标题:', titleEdit)
        formLayout.addRow('描述:', describeEdit)

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
            title = titleEdit.text()
            describe = describeEdit.toPlainText()  # 修正此行，使用 toPlainText() 方法获取文本

            if not title:
                QMessageBox.warning(self, '警告', '标题不能为空!')
                return

            cfg.scheduleIsChange = True
            todoItem = QListWidgetItem(title)
            todoItem.setData(Qt.UserRole, describe)
            todoItem.setSizeHint(QSize(todoItem.sizeHint().width(), cfg.scheduleItemHeight))
            font = QFont("SimSun", 14)  # 设置字体大小
            font.setBold(False)
            todoItem.setFont(font)
            todoItem.setFlags(todoItem.flags() | Qt.ItemIsUserCheckable)
            todoItem.setCheckState(Qt.Unchecked)
            self.todoListWidget.addItem(todoItem)



    def editItem(self, item):
        cfg = ConfigGetter()
        dialog = ItemDialog(item, self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            cfg.scheduleIsChange = True
            item.setText(dialog.titleEdit.text())
            item.setData(Qt.UserRole, dialog.describeEdit.toPlainText())
        # 自下而上 一层层传递
        # isChange = isChange or dialog.isChange


    def todoDrop(self):
        print("todo drop")

    def doneDrop(self):
        print("done drop")

    def dragEnterEvent(self,event):
        print("dragEnter")

    def closeEvent(self, event):
        '''
        用于解决设置窗口被关闭时的事件，主要关注退出时是否有未保存的内容
        :param event:
        :return:
        '''
        cfg = ConfigGetter()
        if not cfg.scheduleIsChange:
            self.hide()
            event.ignore()
            return

        reply = QMessageBox(QMessageBox.Question, "修改未保存", "有修改但未保存，确定要退出吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()

        if reply.clickedButton() == qyes:
            self.hide()
            event.ignore()
        else:
            event.ignore()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
