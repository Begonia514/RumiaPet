import checkers
from style import Style
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from config import ConfigGetter
import os,configparser,sys
from PIL import Image

class petWindow(QTabWidget):
    def __init__(self):
        super(petWindow, self).__init__()
        self.numberOfInput = 10

        self.initUI()

    def textChange(self):
        cfg = ConfigGetter()

        checks = []
        for i in range(self.numberOfInput):
            checks.append(True)

        checks[0] = checkers.SettingUIChecker.Checker1(self, self.inputBoxes[0].text())
        # checks[1] = ......
        # checks[2] = ......
        # ......

        totalCheck = True
        for i in range(self.numberOfInput):
            if checks[i]:
                self.inputBoxes[i].setStyleSheet("QLineEdit { border: 1px solid black; }")
                checks[i] = True
            else:
                self.inputBoxes[i].setStyleSheet("QLineEdit { border: 1px solid red; }")
                checks[i] = False
            totalCheck = totalCheck & checks[i]

        cfg.petSettingIsChange=True

        cfg.settingUICheck = totalCheck



    def stateChange(self,state):
        cfg = ConfigGetter()
       # print(f"state:{state}")
        cfg.petSettingIsChange = True

    def initUI(self):
        '''
        用于建立“宠物设置”栏UI的函数
        :return:
        '''
        cfg = ConfigGetter()
        cfg.petSettingIsChange = False

        # 恢复默认按钮
        self.restorationConfig = QPushButton(self)
        self.restorationConfig.setGeometry(QRect(10, 370, 100, 33))
        self.restorationConfig.setObjectName("restorationConfig")
        self.restorationConfig.setStyleSheet(Style.defaultConfigButton)
        self.restorationConfig.clicked.connect(self.saveDefaultMsg)

        self.tip = QLabel(self)
        self.tip.setGeometry(QRect(10, 10, 431, 16))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tip.setFont(font)
        self.tip.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        self.tip.setObjectName("tip")

        self.labels = []
        self.inputBoxes = []
        for i in range (self.numberOfInput):
            self.labels.append(QLabel(self))
            self.inputBoxes.append(QLineEdit(self))

        for i in range (self.numberOfInput):
            font = QFont()
            font.setBold(False)
            font.setWeight(50)
            self.labels[i].setFont(font)
            self.labels[i].setTextInteractionFlags(
                Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
            self.labels[i].setObjectName("label_"+str(i))

            self.inputBoxes[i].setObjectName("input_"+str(i))
            self.inputBoxes[i].textChanged.connect(self.textChange)
#######################
# 各个组件位置和细节设置  #
#######################
        self.labels[0].setGeometry(QRect(10, 70, 101, 21))
        self.inputBoxes[0].setGeometry(QRect(110, 70, 113, 21))

        self.labels[1].setGeometry(QRect(10, 130, 101, 21))
        self.inputBoxes[1].setGeometry(QRect(110, 130, 113, 21))

        self.labels[2].setGeometry(QRect(10, 250, 101, 21))
        self.inputBoxes[2].setGeometry(QRect(110, 250, 113, 21))

        self.labels[3].setGeometry(QRect(260, 70, 101, 21))
        self.inputBoxes[3].setGeometry(QRect(360, 70, 113, 21))

        self.labels[4].setGeometry(QRect(260, 130, 101, 21))
        self.inputBoxes[4].setGeometry(QRect(360, 130, 113, 21))

        self.labels[5].setGeometry(QRect(260, 190, 101, 21))
        self.inputBoxes[5].setGeometry(QRect(360, 190, 113, 21))

        self.labels[6].setGeometry(QRect(10, 190, 101, 21))
        self.inputBoxes[6].setGeometry(QRect(110, 190, 113, 21))

        self.labels[7].setGeometry(QRect(260, 250, 101, 21))
        self.inputBoxes[7].setGeometry(QRect(360, 250, 113, 21))

        self.labels[8].setGeometry(QRect(260, 310, 101, 21))
        self.inputBoxes[8].setGeometry(QRect(360, 310, 113, 21))

        self.labels[9].setGeometry(QRect(10, 310, 101, 21))
        self.inputBoxes[9].setGeometry(QRect(110, 310, 113, 21))


        self.settingthrowout = QCheckBox(self)
        self.settingthrowout.setGeometry(QRect(560, 70, 113, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingthrowout.setFont(font)
        self.settingthrowout.setIconSize(QSize(20, 20))
        self.settingthrowout.setObjectName("settingthrowout")
        self.settingthrowout.stateChanged.connect(self.stateChange)

        self.settingintotray = QCheckBox(self)
        self.settingintotray.setGeometry(QRect(560, 190, 113, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingintotray.setFont(font)
        self.settingintotray.setObjectName("settingintotray")
        self.settingintotray.stateChanged.connect(self.stateChange)

        self.settingmirror = QCheckBox(self)
        self.settingmirror.setGeometry(QRect(560, 310, 113, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingmirror.setFont(font)
        self.settingmirror.setObjectName("settingmirror")
        self.settingmirror.stateChanged.connect(self.stateChange)


        self.retranslateUi()

        self.readcfg(self)
        cfg.petSettingIsChange = False

    def retranslateUi(self):

        self.restorationConfig.setText("恢复默认")
        self.tip.setText("鼠标在参数名或输入框上悬停，可查看各参数说明")

        self.labels[0].setToolTip("1就是原尺寸，0.5就是一半，2就是2倍")
        self.labels[0].setText("缩放比例：")
        self.inputBoxes[0].setToolTip("请输入一位小数，范围是1到2之间")
        self.labels[1].setToolTip("底部偏移距离")
        self.labels[1].setText("底部偏移：")
        self.inputBoxes[1].setToolTip("底部偏移距离，可以用来制作一部分爪子露在开始菜单外面的样子。正数往下")
        self.labels[2].setToolTip("丢来丢去的速度（水平）")
        self.labels[2].setText("水平扔出：")
        self.inputBoxes[2].setToolTip("丢来丢去的速度（水平）")
        self.labels[3].setToolTip("丢来丢去的速度（竖直）")
        self.labels[3].setText("竖直扔出：")
        self.inputBoxes[3].setToolTip("丢来丢去的速度（竖直）")
        self.labels[4].setToolTip("重力加速度，影响掉落速度")
        self.labels[4].setText("重力加速度：")
        self.inputBoxes[4].setToolTip("重力加速度，影响掉落速度")
        self.labels[5].setToolTip("动画播放速度，数值越小播放得越快")
        self.labels[5].setText("刷新速度：")
        self.inputBoxes[5].setToolTip("动画播放速度，数值越小播放得越快")
        self.labels[6].setToolTip("往左往右走路的速度，越大越快")
        self.labels[6].setText("走路速度：")
        self.inputBoxes[6].setToolTip("往左往右走路的速度，越大越快")
        self.labels[7].setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。正数往右")
        self.labels[7].setText("拖拽偏移X：")
        self.inputBoxes[7].setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。正数往右")
        self.labels[8].setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。y正数往下")
        self.labels[8].setText("拖拽偏移Y：")
        self.inputBoxes[8].setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。y正数往下")
        self.labels[9].setToolTip("字面意思")
        self.labels[9].setText("掉落速度：")
        self.inputBoxes[9].setToolTip("掉落速度")

        self.settingthrowout.setToolTip("是否可以往两边扔出去，打勾为允许")
        self.settingthrowout.setText("两边扔出")
        self.settingintotray.setToolTip("是否可以往开始菜单里走，打勾为允许")
        self.settingintotray.setText("进入菜单")
        self.settingmirror.setToolTip("往右走的动画，使用往左走的动画的镜像，这样就只要画一组图了")
        self.settingmirror.setText("右走镜像")
        # self.QTabWidget1.setTabText(self.QTabWidget1.indexOf(), _translate("宠物设置"))


    def readcfg(self, MainWindow):
        cfg = ConfigGetter()
        self.inputBoxes[0].setText(str(cfg.petscale))
        self.inputBoxes[1].setText(str(cfg.bottomfix))
        self.inputBoxes[7].setText(str(cfg.dragingfixx))
        self.inputBoxes[8].setText(str(cfg.dragingfixy))
        self.inputBoxes[6].setText(str(cfg.petspeed))
        self.inputBoxes[5].setText(str(cfg.gamespeed))
        self.inputBoxes[2].setText(str(cfg.fixdragspeedx))
        self.inputBoxes[3].setText(str(cfg.fixdragspeedy))
        self.inputBoxes[4].setText(str(cfg.gravity))
        self.inputBoxes[9].setText(str(cfg.dropspeed))


        if cfg.throwout == "True":
            self.settingthrowout.setChecked(True)
        else:
            self.settingthrowout.setChecked(False)

        if cfg.intotray == "True":
            self.settingintotray.setChecked(True)
        else:
            self.settingintotray.setChecked(False)

        if cfg.mirror == "True":
            self.settingmirror.setChecked(True)
        else:
            self.settingmirror.setChecked(False)


    def savecfg2(self):
        cfg = ConfigGetter()
        petconfig = cfg.petconfig

        petconfig.set("config", "petscale", self.inputBoxes[0].text())
        petconfig.set("config", "bottomfix", self.inputBoxes[1].text())
        petconfig.set("config", "dragingfixx", self.inputBoxes[7].text())
        petconfig.set("config", "dragingfixy", self.inputBoxes[8].text())
        petconfig.set("config", "petspeed", self.inputBoxes[6].text())
        petconfig.set("config", "gamespeed", self.inputBoxes[5].text())
        petconfig.set("config", "dragspeedx", self.inputBoxes[2].text())
        petconfig.set("config", "dragspeedy", self.inputBoxes[3].text())
        petconfig.set("config", "gravity", self.inputBoxes[4].text())
        petconfig.set("config", "dropspeed", self.inputBoxes[9].text())

        petconfig.set("config", "throwout", str(self.settingthrowout.isChecked()))
        petconfig.set("config", "intotray", str(self.settingintotray.isChecked()))
        petconfig.set("config", "mirror", str(self.settingmirror.isChecked()))
        petconfig.write(open(cfg.petconfigpath, "w", encoding="utf-8-sig"))

        if str(cfg.petscale) != self.inputBoxes[0].text() :
            cfg.ischangescale = 1

        self.loadpetconfig()
        self.readcfg(self)

        cfg.petSettingIsChange = False

    def saveDefaultMsg(self):
        reply = QMessageBox(QMessageBox.Question, "恢复默认", "确认要将该页设置的恢复默认吗？")
        qyes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        qno = reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if reply.clickedButton() == qyes:
            self.saveDefault()

    def saveDefault(self):
        cfg = ConfigGetter()
        petconfig = cfg.petconfig
        # petconfig.set("config", "petname", self.settingpetname.text())
        petconfig.set("config", "petscale", '1.0')
        petconfig.set("config", "bottomfix", '0')
        petconfig.set("config", "dragingfixx", '0')
        petconfig.set("config", "dragingfixy", '64')
        petconfig.set("config", "petspeed", '20')
        petconfig.set("config", "gamespeed", '200')
        petconfig.set("config", "dragspeedx", '1.0')
        petconfig.set("config", "dragspeedy", '1.0')
        petconfig.set("config", "gravity", '10')
        petconfig.set("config", "dropspeed", '60')
        petconfig.set("config", "throwout", 'False')
        petconfig.set("config", "intotray", 'False')
        petconfig.set("config", "mirror", 'True')
        petconfig.write(open(cfg.petconfigpath, "w", encoding="utf-8-sig"))

        if str(cfg.petscale) != '1.0' :
            cfg.ischangescale = 1

        self.loadpetconfig()
        self.readcfg(self)
        cfg.petSettingIsChange = False

    def loadconfig(self):
        cfg = ConfigGetter()
        config = configparser.ConfigParser()
        cfg.configpath = cfg.fp_dir + '/config.ini'
        config.read(cfg.configpath, encoding="utf-8-sig")
        cfg.petidraw = config.get("config", "petids")
        cfg.petids = cfg.petidraw.split(',')
        cfg.petid = config.get("config", "petid")
        cfg.traypath = config.get("config", "traypath")

    def loadpetconfig(self):
        cfg = ConfigGetter()
        print("LoadPetconfig")

        cfg.fp_dir = os.getcwd()
        cfg.petconfig = configparser.ConfigParser()
        cfg.petconfig.read(cfg.fp_dir + "/data/" + cfg.petid + "/petconfig.ini", encoding="utf-8-sig")

        # print(fp_dir+"/"+petid+"/petconfig.ini")
        petconfig = configparser.ConfigParser()
        petconfig.read(cfg.fp_dir + "/data/" + cfg.petid + "/petconfig.ini", encoding="utf-8-sig")
        # cfg.petname=petconfig.get("config", "petname")
        cfg.petscale = petconfig.getfloat("config", "petscale")
        cfg.bottomfix = petconfig.getint("config", "bottomfix")
        cfg.gamespeed = petconfig.getint("config", "gamespeed")
        cfg.petspeed = petconfig.getint("config", "petspeed")
        cfg.throwout = petconfig.get("config", "throwout")
        cfg.intotray = petconfig.get("config", "intotray")
        cfg.mirror = petconfig.get("config", "mirror")
        cfg.gravity = petconfig.getint("config", "gravity")
        cfg.dropspeed = petconfig.getint("config", "dropspeed")
        cfg.dragingfixx = petconfig.getint("config", "dragingfixx")
        cfg.dragingfixy = petconfig.getint("config", "dragingfixy")
        cfg.fixdragspeedx = petconfig.getfloat("config", "dragspeedx")
        cfg.fixdragspeedy = petconfig.getfloat("config", "dragspeedy")
        cfg.petactionsraw = petconfig.get("config", "petaction")
        cfg.petactionnumraw = petconfig.get("config", "petactionnum")
        cfg.petactionrateraw = petconfig.get("config", "petactionrate")
        cfg.standactionraw = petconfig.get("config", "standaction")
        cfg.standactionnumraw = petconfig.get("config", "standactionnum")
        cfg.standactionrateraw = petconfig.get("config", "standactionrate")

        cfg.petactions = cfg.petactionsraw.split(',')
        cfg.petactionnum = cfg.petactionnumraw.split(',')
        cfg.petactionrate = cfg.petactionrateraw.split(',')
        cfg.standaction = cfg.standactionraw.split(',')
        cfg.standactionnum = cfg.standactionnumraw.split(',')
        cfg.standactionrate = cfg.standactionrateraw.split(',')
        cfg.image_url = './data/' + cfg.petid + '/'
        cfg.image = cfg.image_url + 'main.png'
        cfg.im = Image.open(cfg.image)
        cfg.petwidth = int(cfg.im.size[0] * cfg.petscale)
        cfg.petheight = int(cfg.im.size[1] * cfg.petscale)
