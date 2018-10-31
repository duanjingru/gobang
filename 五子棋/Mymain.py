
import sys
import cgitb
cgitb.enable(format='error')
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QCheckBox,QLineEdit,QListWidget,QListWidgetItem,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QIcon
from singleplayer import SinglePlayer
from doubleplayer import DoublePlayer
from networkplayer import NetworkPlayer,SetWindow
from game import DjrPushButton
import pygame


class MainWindow(QWidget):
    def __init__(self,parent=None):#父控件 不指定以屏幕作为父窗体
        super().__init__(parent=parent)
        self.setWindowTitle("小可爱的五子棋")#窗体标题
        self.setFixedSize(760,650)#设置窗体固定大小
        #设置背景图片
        window_tupian=QPalette()
        #setBrush设置给谁设置什么
        window_tupian.setBrush(self.backgroundRole(),QBrush(QPixmap('source/五子棋界面.png')))
        self.setPalette(window_tupian)
        self.setWindowIcon(QIcon('source/icon.png'))#设置窗体图标
        #设置三个按钮到对应的位置 给三个按钮绑定处理函数 实现页面跳转
        self.single_btn = DjrPushButton("source/人机对战_normal.png","source/人机对战_hover.png","source/人机对战_press.png",self)
        self.double_btn = DjrPushButton("source/双人对战_normal.png","source/双人对战_hover.png","source/双人对战_press.png",self)
        self.network_btn = DjrPushButton("source/联机对战_normal.png","source/联机对战_hover.png","source/联机对战_press.png",self)
        self.single_btn.move(250,300)
        self.double_btn.move(250,400)
        self.network_btn.move(250,500)
        #设置按键对应的函数
        #接收返回的信号
        self.single_btn.clicked.connect(self.single)
        self.double_btn.clicked.connect(self.double)
        self.network_btn.clicked.connect(self.network)
        self.game_window = None#游戏窗体


    def single(self):
        self.game_window=SinglePlayer()
        #返回信号
        self.game_window.backSingal.connect(self.back)
        self.game_window.restartSingal.connect(self.single)
        self.game_window.show()
        self.game_window.setWindowTitle("单人模式")
        self.close()

    def double(self):
        self.game_window = DoublePlayer()
        self.game_window.backSingal.connect(self.back)
        self.game_window.restartSingal.connect(self.double)
        self.game_window.show()
        self.game_window.setWindowTitle("双人对战")
        self.close()

    def network(self):
        self.game_window = SetWindow(main_window=self)#返回主界面
        self.game_window.show()
        self.game_window.setWindowIcon(QIcon('source/icon.png'))  # 设置窗体图标
        self.game_window.setWindowTitle("网络配置")
        self.close()

    def back(self):
        #捕获到对应的返回的信号
        #把自己显示出来
        self.show()



if __name__ == '__main__':
    #创建QT应用对象
    app=QApplication(sys.argv)
    w=MainWindow()
    w.show()  # 窗体显示
    # 进入消息循环
    sys.exit(app.exec_())
