import pyautogui
from PIL import Image
import configparser
import os

#单例模式
class ConfigGetter():
    cfg = None
    def __new__(cls, *args, **kwargs):
        if cls.cfg == None:
           cls.cfg = Config()

        return cls.cfg



class Config():

    def __init__(self):
        '''
        读取设置，并存入内存
        '''
        self.fp_dir = os.getcwd()
        self.config = configparser.ConfigParser()
        self.configpath = self.fp_dir + '/config.ini'
        self.config.read(self.configpath, encoding="utf-8-sig")
        # self.petidraw = self.config.get("config", "petids")
        # self.petids = self.petidraw.split(',')
        self.petid = self.config.get("config", "petid")
        self.traypath = self.config.get("config", "traypath")
        self.webDataPath = self.config.get("web","webDataPath")
        self.webItemHeight = self.config.getint("web","itemHeight")

        self.scheduleItemHeight = self.config.getint("schedule","itemHeight")
        self.todoListPath = self.config.get("schedule","todoListPath")
        self.doneListPath = self.config.get("schedule","doneListPath")




        self.petconfig = configparser.ConfigParser()
        self.petconfigpath = self.fp_dir + "/data/" + self.petid + "/petconfig.ini"
        self.petconfig.read(self.petconfigpath, encoding="utf-8-sig")
        self.petname = self.petconfig.get("config", "petname")
        self.petscale = self.petconfig.getfloat("config", "petscale")
        self.bottomfix = self.petconfig.getint("config", "bottomfix")
        self.gamespeed = self.petconfig.getint("config", "gamespeed")
        self.petspeed = self.petconfig.getint("config", "petspeed")
        self.throwout = self.petconfig.get("config", "throwout")
        self.intotray = self.petconfig.get("config", "intotray")
        self.mirror = self.petconfig.get("config", "mirror")
        self.dropspeed = self.petconfig.getint("config", "dropspeed")
        self.gravity = self.petconfig.getint("config", "gravity")
        self.dragingfixx = self.petconfig.getint("config", "dragingfixx")
        self.dragingfixy = self.petconfig.getint("config", "dragingfixy")
        self.fixdragspeedx = self.petconfig.getfloat("config", "dragspeedx")
        self.fixdragspeedy = self.petconfig.getfloat("config", "dragspeedy")

        self.petactionsraw = self.petconfig.get("config", "petaction")
        self.petactionnumraw = self.petconfig.get("config", "petactionnum")
        self.petactionrateraw = self.petconfig.get("config", "petactionrate")
        self.standactionraw = self.petconfig.get("config", "standaction")
        self.standactionnumraw = self.petconfig.get("config", "standactionnum")
        self.standactionrateraw = self.petconfig.get("config", "standactionrate")
        self.quitactionnum = self.petconfig.getint("config","quitactionnum")

        self.petactions = self.petactionsraw.split(',')
        self.petactionnum = self.petactionnumraw.split(',')
        self.petactionrate = self.petactionrateraw.split(',')
        self.standaction = self.standactionraw.split(',')
        self.standactionnum = self.standactionnumraw.split(',')
        self.standactionrate = self.standactionrateraw.split(',')

        self.image_url = './data/' + self.petid + '/'
        self.image = self.image_url + 'main.png'
        self.im = Image.open(self.image)
        self.petwidth = int(self.im.size[0] * self.petscale)
        self.petheight = int(self.im.size[1] * self.petscale)
        self.bottomfix = int(self.bottomfix * self.petscale)
        self.screenwidth, self.screenheight = 0, 0
        self.deskwidth, self.deskheight = 0, 0



        self.deskbottom = 0
        self.onfloor = 1
        self.drop = 1
        self.dropa = 0
        self.draging = 0
        self.playid = 1
        self.playtime = 0
        self.playnum = 1
        self.playstand = -1
        self.petaction, self.petaction2 = 0, 0
        self.mouseposx1, self.mouseposx2, self.mouseposx3, self.mouseposx4 = 0, 0, 0, 0
        self.mouseposy1, self.mouseposy2,self. mouseposy3, self.mouseposy4 = 0, 0, 0, 0
        self.dragspeedx, self.dragspeedy = 0, 0
        self.petleft, self.pettop = 0, 0
        self.gameleft, self.gamebottom = 0, 0
        self.imgpath = 'main.png'
        self.quit = 0
        self.ischangescale = 0
        self.hiding = 0
        self.hidden = 0

        self.petSettingIsChange = False
        self.webSettingIsChange = False
        self.scheduleIsChange = False

        #SettingUI校验
        self.settingUICheck = True

        #(不可修改)显示屏长宽
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()