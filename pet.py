from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PIL import Image
import random
import sys,os,csv,webbrowser
import configparser
from setting import *
from config import  ConfigGetter
from scheduleUI import TodoApp
from components.bubble import *

class App(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(App, self).__init__(parent)
        # initialize
        self.is_follow_mouse = False
        self.settingMenu = None

        
        #Windows
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)

        
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.repaint()
        
        screen = QDesktopWidget().screenGeometry()
        desktop = QDesktopWidget().availableGeometry()
        self.tray()

        cfg = ConfigGetter()

        cfg.screenwidth = screen.width()
        cfg.screenheight=screen.height()
        cfg.deskwidth=desktop.width()
        cfg.deskheight=desktop.height()
        cfg.gameleft=cfg.screenwidth-cfg.deskwidth
        cfg.gamebottom=cfg.screenheight-cfg.deskheight

        if cfg.intotray!="True":
            cfg.petleft = cfg.deskwidth-cfg.petwidth*cfg.petscale
            cfg.pettop = cfg.deskheight-cfg.petheight*cfg.petscale-cfg.bottomfix
        else:
            cfg.gameleft=0
            cfg.gamebottom=0
            cfg.petleft = cfg.screenwidth-cfg.petwidth*cfg.petscale
            cfg.pettop = cfg.screenheight-cfg.petheight*cfg.petscale-cfg.bottomfix

        # initial image
        petimage = cfg.image_url + 'start.png'
        #print(petimage)
        pix = QPixmap(petimage)
        pix = pix.scaled(int(cfg.petwidth*cfg.petscale),
                         int(cfg.petheight*cfg.petscale),
                         aspectRatioMode=Qt.KeepAspectRatio)
        self.lb1 = QLabel(self)
        self.lb1.setPixmap(pix)
        self.lb1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lb1.customContextMenuRequested.connect(self.rightMenu)

        # display first pic
        cfg.petleft = int(cfg.petleft)
        cfg.pettop = int(cfg.pettop)
        self.move(cfg.petleft,cfg.pettop)
        self.resize(int(cfg.petwidth*cfg.petscale),
                    int(cfg.petheight*cfg.petscale))
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game)
        self.timer.start(cfg.gamespeed)
    
    def game(self):
        '''
        主循环，核心功能为：寻找合适图片，寻找合适位置，放置图片
        :return:
        '''
        right=0
        cfg = ConfigGetter()

        if cfg.intotray != "True":
            cfg.gamebottom = cfg.screenheight-cfg.deskheight
        else:
            cfg.gamebottom = 0

        #handle quit
        if cfg.quit == 1:
            if cfg.playid<=cfg.quitactionnum:
                cfg.imgpath = 'quit' + str(cfg.playid) + '.png'
                cfg.playid+=1
            else:
                #final
                self.quit()
        elif cfg.hiding == 1:
            if cfg.playid<=cfg.quitactionnum:
                cfg.imgpath = 'quit' + str(cfg.playid) + '.png'
                cfg.playid+=1
            else:
                #final
                self.hide()


        # handle drag and fall
        elif cfg.drop==1 and cfg.onfloor==0 :
            if cfg.draging==1:
                #print("Draging")
                cfg.playnum=int(cfg.petactionnum[3])
                if cfg.playid<int(cfg.petactionnum[3]):
                        cfg.imgpath=cfg.petactions[3]+str(cfg.playid)+'.png'
                        cfg.playid+=1
                else:
                    #final action
                    cfg.imgpath=cfg.petactions[3]+str(cfg.playid)+'.png'
                    cfg.playid=1
                
            elif cfg.draging==0:
                #falling
                cfg.playnum=int(cfg.petactionnum[4])
                if cfg.playid<int(cfg.petactionnum[4]):
                        cfg.imgpath=cfg.petactions[4]+str(cfg.playid)+'.png'
                        cfg.playid+=1
                else:
                    cfg.imgpath=cfg.petactions[4]+str(cfg.playid)+'.png'
                    cfg.playid=1
                
            self.drop()



        # handle standing
        elif cfg.drop==0 or cfg.onfloor==1:
            
            if cfg.playtime==0:
                cfg.petaction=random.random()
                cfg.playstand=-1
                cfg.playid=1

            if cfg.petaction>=(float(cfg.petactionrate[0])+float(cfg.petactionrate[1])) \
                    and (cfg.petleft+cfg.petwidth*cfg.petscale+cfg.gameleft+cfg.petspeed)<cfg.deskwidth:
                ##print("Walking right")
                right=1
                cfg.playnum=int(cfg.petactionnum[2])
                if cfg.playid<int(cfg.petactionnum[2]):
                    cfg.imgpath=cfg.petactions[2]+str(cfg.playid)+'.png'
                    cfg.playid+=1
                    
                else:
                    cfg.imgpath=cfg.petactions[2]+str(cfg.playid)+'.png'
                    cfg.playid=1
                
                
                cfg.petleft=cfg.petleft+cfg.petspeed
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)

                if cfg.playtime==0:
                    playtimemin=3
                    playtimemax=int((((cfg.deskwidth-
                                (cfg.petleft+cfg.petwidth*cfg.petscale+cfg.gameleft)
                                       ))/cfg.petspeed)/cfg.playnum)
                    if playtimemax<=3:
                        playtimemax=3
                cfg.playtime-=1


            elif cfg.petaction<(float(cfg.petactionrate[0])+float(cfg.petactionrate[1])) \
                    and cfg.petaction>=float(cfg.petactionrate[0]) and (cfg.petleft-cfg.gameleft)>cfg.petspeed:
                cfg.playnum=int(cfg.petactionnum[1])
                if cfg.playid<int(cfg.petactionnum[1]):
                    cfg.imgpath=cfg.petactions[1]+str(cfg.playid)+'.png'
                    cfg.playid+=1

                else:
                    cfg.imgpath=cfg.petactions[1]+str(cfg.playid)+'.png'
                    cfg.playid=1

                cfg.petleft=cfg.petleft-cfg.petspeed
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)
                
                if cfg.playtime==0:
                    playtimemin=3
                    playtimemax=int((cfg.petleft-cfg.gameleft)
                                    /cfg.petspeed/cfg.playnum)
                    if playtimemax<=1:
                        playtimemax=1
                cfg.playtime=int(cfg.playtime)-1

                
            elif cfg.petaction<float(cfg.petactionrate[0]):
                # 站立循环

                if cfg.playstand==-1:
                    temp=random.random()
                    temp2=0

                    for i in range(len(cfg.standactionrate)):
                        
                        if float(cfg.standactionrate[i])==0:
                            continue
                        temp2=temp2+float(cfg.standactionrate[i])
                        ##print("内循环："+str(i)+"cfg.累计概率："+str(temp2))
                        if temp<temp2:
                            cfg.petaction2=i
                            cfg.playnum=int(cfg.standactionnum[i])
                            cfg.playstand=1

                            break

                    if cfg.playstand==-1:
                        cfg.playnum=int(cfg.standactionnum[0])
                        cfg.playstand=1
                

                if cfg.playstand<int(cfg.standactionnum[cfg.petaction2]):
                    #imgpath=standaction[i]+str(playid)+'.png'
                    cfg.imgpath=cfg.standaction[cfg.petaction2]+str(cfg.playstand)+'.png'
                    cfg.playstand+=1
                else:
                    cfg.imgpath=cfg.standaction[cfg.petaction2]+str(cfg.playstand)+'.png'
                    cfg.playstand=1
                    cfg.playid=1
                
                if cfg.playtime==0:
                    playtimemin=1
                    playtimemax=1
                    
                cfg.playtime=int(cfg.playtime)-1

                
                
            else:
                cfg.petaction=random.random()
                cfg.playstand=-1
            
            if cfg.playtime==-1:
                cfg.playtime=random.randint(1,playtimemax)*cfg.playnum
                
                
        cfg.petimage = cfg.image_url + cfg.imgpath
        print(cfg.petimage)
        #petimage=petimage.mirrored(True, False)
        pix = QPixmap(cfg.petimage)
        if right==1:
            tempimg = pix.toImage()
            tempimg = tempimg.mirrored(True, False)
            pix=QPixmap.fromImage(tempimg)
            
        pix=pix.scaled(int(cfg.petwidth*cfg.petscale),
                       int(cfg.petheight*cfg.petscale),
                       aspectRatioMode=Qt.KeepAspectRatio)
        if cfg.ischangescale == 1 :
            self.resize(int(cfg.petwidth*cfg.petscale),
                           int(cfg.petheight*cfg.petscale))
            self.lb1.setGeometry(0,0,
                                 int(cfg.petwidth*cfg.petscale),
                                 int(cfg.petheight*cfg.petscale))
            cfg.ischangescale=0
        self.lb1.setPixmap(pix)

        pass



    def rightMenu(self):
        '''
        设置露米娅右击菜单内容
        :return:
        '''
        cfg = ConfigGetter()
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'), '隐藏', self, triggered=self.playHide))
        menu.addAction(QAction(QIcon('./data/icon/schedule.png'), '日程表', self, triggered=self.schedule))

        webMenu = QMenu('webMenu')
        webMenu.setTitle('收藏的网站')
        webData = self.readCsv(cfg.webDataPath)
        for name, url in webData:
            webMenu.addAction(
                QAction(name, self, triggered=(lambda _, url=url: webbrowser.open(url)))
            )
        menu.addMenu(webMenu)
        menu.addAction(QAction(QIcon('./data/icon/settings.png'), '设置', self, triggered=self.setting))
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.playQuit))

        menu.exec_(QCursor.pos())
    def readCsv(self,filePath: str):
        '''
        读取对应filePath的csv文件并返回内容数组
        :param filePath: 文件路径
        :return: 一般为二维数组
        '''
        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                file.close()
                pass
        with open(filePath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)

    def writeCsv(filePath: str, data: list):
        '''
        将数组写入csv文件
        :param data: 要写入的二维数组
        :return:
        '''
        # 数据准备
        # data = [
        #     ['哔哩哔哩', 'www.bilibili.com'],
        #     ['南大网络', 'p.nju.edu.cn']
        # ]

        # 打开CSV文件进行写入
        with open(filePath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
    def mousePressEvent(self, event):
        cfg = ConfigGetter()
        if event.button()==Qt.LeftButton:
            self.is_follow_mouse = True
            cfg.onfloor=0
            cfg.draging=1
            if cfg.quit != 1:
                # means new action
                cfg.playid=1
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        cfg = ConfigGetter()

        if Qt.LeftButton and self.is_follow_mouse:
            cfg.petleft = QCursor.pos().x()-cfg.petwidth*cfg.petscale/2+cfg.dragingfixx*cfg.petscale
            cfg.pettop = QCursor.pos().y()-cfg.petheight*cfg.petscale/2+cfg.dragingfixy*cfg.petscale

            cfg.mouseposx4=cfg.mouseposx3
            cfg.mouseposx3=cfg.mouseposx2
            cfg.mouseposx2=cfg.mouseposx1
            cfg.mouseposx1=QCursor.pos().x()

            cfg.mouseposy4=cfg.mouseposy3
            cfg.mouseposy3=cfg.mouseposy2
            cfg.mouseposy2=cfg.mouseposy1
            cfg.mouseposy1=QCursor.pos().y()

            cfg.petleft = int(cfg.petleft)
            cfg.pettop = int(cfg.pettop)
            self.move(cfg.petleft, cfg.pettop)
            event.accept()

    def mouseReleaseEvent(self, event):
        cfg = ConfigGetter()
        if event.button()==Qt.LeftButton:
            if cfg.quit != 1:
                cfg.playid=1
            cfg.onfloor=0
            cfg.draging=0
            self.is_follow_mouse = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            cfg.dropa=1
            cfg.dragspeedx=(cfg.mouseposx1-cfg.mouseposx3)/2*cfg.fixdragspeedx
            cfg.dragspeedy=(cfg.mouseposy1-cfg.mouseposy3)/2*cfg.fixdragspeedy
            cfg.mouseposx1=cfg.mouseposx3=0
            cfg.mouseposy1=cfg.mouseposy3=0
            ##print("mouseReleaseEvent")

    def tray(self):
        '''
        任务栏小图标相关
        :return:
        '''
        cfg = ConfigGetter()
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(cfg.traypath))
        menu = QMenu(self)

        menu.addAction(QAction(cfg.petname, self))
        menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'),'显示', self, triggered=self.show))
        menu.addAction(QAction(QIcon('./data/icon/visible.png'), '隐藏', self, triggered=self.playHide))
        menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))

        menu.addSeparator()
        menu.addAction(QAction(QIcon('./data/icon/settings.png'), '设置', self, triggered=self.setting))
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.playQuit))
        
        tray.setContextMenu(menu)
        tray.show()


    def schedule(self):
        self.scheduleWindow = TodoApp()
        self.scheduleWindow.show()
    def setting(self):
        '''
        打开详细设置菜单
        :return:
        '''
        self.settingMenu = Setting()
        # self.settingMenu.isChange = False
        self.settingMenu.show()
        
    def drop(self):
        '''
        用于处理露米娅掉落时的逻辑
        :return:
        '''
        #掉落
        cfg = ConfigGetter()

        # print("Dropping")
        if cfg.onfloor==0 and cfg.draging==0:
            dropnext=cfg.pettop+cfg.dragspeedy+cfg.dropspeed
            movenext=cfg.petleft+cfg.dragspeedx
            if cfg.throwout!="True":
                if movenext<=cfg.gameleft:
                    movenext=cfg.gameleft
                elif movenext>cfg.screenwidth-cfg.petwidth*cfg.petscale:
                    movenext=(cfg.screenwidth-cfg.petwidth*cfg.petscale)
            
            cfg.dragspeedy=cfg.dragspeedy+cfg.gravity



            # on floor
            if dropnext>=(cfg.screenheight-cfg.petheight*cfg.petscale
                          -cfg.gamebottom-cfg.bottomfix):
                cfg.pettop=cfg.screenheight-cfg.petheight*cfg.petscale-cfg.gamebottom-cfg.bottomfix
                cfg.petleft=movenext
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)
                cfg.onfloor=1
                cfg.dropa=0
               
            elif dropnext<(cfg.screenheight-cfg.petheight*cfg.petscale
                           -cfg.gamebottom-cfg.bottomfix):
                cfg.pettop=dropnext
                cfg.petleft=movenext
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)
                

        
    def switchdrop(self):
        cfg = ConfigGetter()
        # global drop
        sender = self.sender()
        if sender.text()=="禁用掉落":
            sender.setText("开启掉落")
            cfg.drop=0
        else:
            sender.setText("禁用掉落")
            cfg.drop=1
            
    def dropon(self):
        cfg = ConfigGetter()
        # global drop
        cfg.drop=1
        
    def dropoff(self):
        cfg = ConfigGetter()
        # global drop
        cfg.drop=0
        
    def playQuit(self):
        '''
        用于设置quit的flag，便于主循环接下来播放quit动画
        :return:
        '''
        cfg = ConfigGetter()
        cfg.quit = 1
        cfg.playid = 1

    def playHide(self):
        cfg = ConfigGetter()
        # quit优先级最高
        if cfg.quit == 1:
            return
        if cfg.hidden == 1:
            self.hide()
        cfg.hiding = 1
        cfg.playid = 1

    def hide(self):
        cfg = ConfigGetter()
        self.setVisible(False)
        self.bubble = BubbleWindow("./data/rumia/hideBubble.png", cfg.screenwidth*2//3, cfg.deskheight)
        self.bubble.show()
        cfg.hiding = 0
        cfg.hidden = 1



    def show(self):
        cfg = ConfigGetter()
        cfg.hidden = 0
        self.setVisible(True)

    # def restart_program(self):
    #     python = sys.executable
    #     os.execl(python, python, * sys.argv)

    def quit(self):
        self.close()
        sys.exit()



