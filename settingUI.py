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

        self.initUI()

    def textChange(self,text):
        cfg = ConfigGetter()
        # print(f"changed:{text}")
        cfg.petSettingIsChange=True


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

        self.defaultConfig1 = QPushButton(self)
        self.defaultConfig1.setGeometry(QRect(50, 450, 100, 33))
        self.defaultConfig1.setObjectName("defaultConfig1")
        self.defaultConfig1.setStyleSheet(Style.defaultConfigButton)


        self.label_17 = QLabel(self)
        self.label_17.setGeometry(QRect(10, 70, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_17.setObjectName("label_17")

        self.settingscale = QLineEdit(self)
        self.settingscale.setGeometry(QRect(110, 70, 113, 21))
        self.settingscale.setObjectName("settingscale")
        self.settingscale.textChanged.connect(self.textChange)


        self.label_18 = QLabel(self)
        self.label_18.setGeometry(QRect(10, 10, 431, 16))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_18.setObjectName("label_18")

        self.label_19 = QLabel(self)
        self.label_19.setGeometry(QRect(10, 100, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_19.setObjectName("label_19")

        self.settingbottomfix = QLineEdit(self)
        self.settingbottomfix.setGeometry(QRect(110, 100, 113, 21))
        self.settingbottomfix.setObjectName("settingbottomfix")
        self.settingbottomfix.textChanged.connect(self.textChange)


        self.label_20 = QLabel(self)
        self.label_20.setGeometry(QRect(10, 160, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_20.setObjectName("label_20")

        self.settingspeedx = QLineEdit(self)
        self.settingspeedx.setGeometry(QRect(110, 160, 113, 21))
        self.settingspeedx.setObjectName("settingspeedx")
        self.settingspeedx.textChanged.connect(self.textChange)


        self.label_21 = QLabel(self)
        self.label_21.setGeometry(QRect(260, 160, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_21.setObjectName("label_21")

        self.settingspeedy = QLineEdit(self)
        self.settingspeedy.setGeometry(QRect(360, 160, 113, 21))
        self.settingspeedy.setObjectName("settingspeedy")
        self.settingspeedy.textChanged.connect(self.textChange)


        self.label_22 = QLabel(self)
        self.label_22.setGeometry(QRect(260, 190, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_22.setObjectName("label_22")

        self.settinggravity = QLineEdit(self)
        self.settinggravity.setGeometry(QRect(360, 190, 113, 21))
        self.settinggravity.setObjectName("settinggravity")
        self.settinggravity.textChanged.connect(self.textChange)


        self.label_23 = QLabel(self)
        self.label_23.setGeometry(QRect(260, 130, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_23.setObjectName("label_23")

        self.settinggamespeed = QLineEdit(self)
        self.settinggamespeed.setGeometry(QRect(360, 130, 113, 21))
        self.settinggamespeed.setObjectName("settinggamespeed")
        self.settinggamespeed.textChanged.connect(self.textChange)


        self.settingthrowout = QCheckBox(self)
        self.settingthrowout.setGeometry(QRect(10, 220, 91, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingthrowout.setFont(font)
        self.settingthrowout.setIconSize(QSize(20, 20))
        self.settingthrowout.setObjectName("settingthrowout")
        self.settingthrowout.stateChanged.connect(self.stateChange)


        self.settingintotray = QCheckBox(self)
        self.settingintotray.setGeometry(QRect(110, 220, 91, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingintotray.setFont(font)
        self.settingintotray.setObjectName("settingintotray")
        self.settingintotray.stateChanged.connect(self.stateChange)


        self.label_26 = QLabel(self)
        self.label_26.setGeometry(QRect(10, 330, 91, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_26.setObjectName("label_26")

        self.label_27 = QLabel(self)
        self.label_27.setGeometry(QRect(10, 130, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_27.setObjectName("label_27")

        self.settingpetspeed = QLineEdit(self)
        self.settingpetspeed.setGeometry(QRect(110, 130, 113, 21))
        self.settingpetspeed.setObjectName("settingpetspeed")
        self.settingpetspeed.textChanged.connect(self.textChange)


        self.label_29 = QLabel(self)
        self.label_29.setGeometry(QRect(260, 100, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_29.setFont(font)
        self.label_29.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_29.setObjectName("label_29")

        self.settingdragingfixx = QLineEdit(self)
        self.settingdragingfixx.setGeometry(QRect(360, 100, 113, 21))
        self.settingdragingfixx.setObjectName("settingdragingfixx")
        self.settingdragingfixx.textChanged.connect(self.textChange)


        self.settingdragingfixy = QLineEdit(self)
        self.settingdragingfixy.setGeometry(QRect(610, 100, 113, 21))
        self.settingdragingfixy.setObjectName("settingdragingfixy")
        self.settingdragingfixy.textChanged.connect(self.textChange)


        self.label_30 = QLabel(self)
        self.label_30.setGeometry(QRect(510, 100, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_30.setFont(font)
        self.label_30.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_30.setObjectName("label_30")


        self.settingmirror = QCheckBox(self)
        self.settingmirror.setGeometry(QRect(640, 300, 91, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.settingmirror.setFont(font)
        self.settingmirror.setObjectName("settingmirror")
        self.settingmirror.stateChanged.connect(self.stateChange)


        self.label_35 = QLabel(self)
        self.label_35.setGeometry(QRect(10, 190, 101, 21))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_35.setFont(font)
        self.label_35.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.label_35.setObjectName("label_35")

        self.settingdropspeed = QLineEdit(self)
        self.settingdropspeed.setGeometry(QRect(110, 190, 113, 21))
        self.settingdropspeed.setObjectName("settingdropspeed")
        self.settingdropspeed.textChanged.connect(self.textChange)



        self.retranslateUi()

        self.readcfg(self)
        cfg.petSettingIsChange = False

    def retranslateUi(self):

        self.defaultConfig1.setText("恢复默认")

        self.label_17.setToolTip("1就是原尺寸，0.5就是一半，2就是2倍")
        self.label_17.setText("#缩放比例：")
        self.settingscale.setToolTip("1就是原尺寸，0.5就是一半，2就是2倍")
        self.label_18.setText("鼠标在参数名或输入框上悬停，可查看各参数说明")
        self.label_19.setToolTip("底部偏移距离")
        self.label_19.setText("#底部偏移：")
        self.settingbottomfix.setToolTip("底部偏移距离，可以用来制作一部分爪子露在开始菜单外面的样子。正数往下")
        self.label_20.setToolTip("丢来丢去的速度（水平）")
        self.label_20.setText("#水平扔出：")
        self.settingspeedx.setToolTip("丢来丢去的速度（水平）")
        self.label_21.setToolTip("丢来丢去的速度（竖直）")
        self.label_21.setText("#竖直扔出：")
        self.settingspeedy.setToolTip("丢来丢去的速度（竖直）")
        self.label_22.setToolTip("重力加速度，影响掉落速度")
        self.label_22.setText("#重力加速度：")
        self.settinggravity.setToolTip("重力加速度，影响掉落速度")
        self.label_23.setToolTip("动画播放速度，数值越小播放得越快")
        self.label_23.setText("#刷新速度：")
        self.settinggamespeed.setToolTip("动画播放速度，数值越小播放得越快")
        self.settingthrowout.setToolTip("是否可以往两边扔出去，打勾为允许")
        self.settingthrowout.setText("两边扔出")
        self.settingintotray.setToolTip("是否可以往开始菜单里走，打勾为允许")
        self.settingintotray.setText("进入菜单")

        self.label_27.setToolTip("往左往右走路的速度，越大越快")
        self.label_27.setText("#走路速度：")
        self.settingpetspeed.setToolTip("往左往右走路的速度，越大越快")

        self.label_29.setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。正数往右")
        self.label_29.setText("#拖拽偏移X：")
        self.settingdragingfixx.setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。正数往右")
        self.settingdragingfixy.setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。y正数往下")
        self.label_30.setToolTip("拖拽时坐标偏移，用于改变拖拽时宠物和鼠标的相对位置，比如要拎起脖子之类的。y正数往下")
        self.label_30.setText("#拖拽偏移Y：")

        self.settingmirror.setToolTip("往右走的动画，使用往左走的动画的镜像，这样就只要画一组图了")
        self.settingmirror.setText("右走镜像")
        self.label_35.setToolTip("字面意思")
        self.label_35.setText("#掉落速度：")
        self.settingdropspeed.setToolTip("掉落速度")
        # self.QTabWidget1.setTabText(self.QTabWidget1.indexOf(), _translate("宠物设置"))


    def readcfg(self, MainWindow):
        cfg = ConfigGetter()
        self.settingscale.setText(str(cfg.petscale))
        self.settingbottomfix.setText(str(cfg.bottomfix))
        self.settingdragingfixx.setText(str(cfg.dragingfixx))
        self.settingdragingfixy.setText(str(cfg.dragingfixy))
        self.settingpetspeed.setText(str(cfg.petspeed))
        self.settinggamespeed.setText(str(cfg.gamespeed))
        self.settingspeedx.setText(str(cfg.fixdragspeedx))
        self.settingspeedy.setText(str(cfg.fixdragspeedy))
        self.settinggravity.setText(str(cfg.gravity))
        self.settingdropspeed.setText(str(cfg.dropspeed))


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

        petconfig.set("config", "petscale", self.settingscale.text())
        petconfig.set("config", "bottomfix", self.settingbottomfix.text())
        petconfig.set("config", "dragingfixx", self.settingdragingfixx.text())
        petconfig.set("config", "dragingfixy", self.settingdragingfixy.text())
        petconfig.set("config", "petspeed", self.settingpetspeed.text())
        petconfig.set("config", "gamespeed", self.settinggamespeed.text())
        petconfig.set("config", "dragspeedx", self.settingspeedx.text())
        petconfig.set("config", "dragspeedy", self.settingspeedy.text())
        petconfig.set("config", "gravity", self.settinggravity.text())
        petconfig.set("config", "dropspeed", self.settingdropspeed.text())

        petconfig.set("config", "throwout", str(self.settingthrowout.isChecked()))
        petconfig.set("config", "intotray", str(self.settingintotray.isChecked()))
        petconfig.set("config", "mirror", str(self.settingmirror.isChecked()))
        petconfig.write(open(cfg.petconfigpath, "w", encoding="utf-8-sig"))

        if str(cfg.petscale) != self.settingscale.text() :
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

        cfg.petSettingIsChange = False
        self.loadpetconfig()
        self.readcfg(self)

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
