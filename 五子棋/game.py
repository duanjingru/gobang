import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QCheckBox,QLineEdit,QListWidget,QListWidgetItem,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QIcon
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import pygame
pygame.init()
class DjrPushButton(QLabel):
    #按钮触发信号
    clicked = pyqtSignal()
    #继承QLabel切换图片 按钮
    def __init__(self,str1,str2,str3,parent):
        super().__init__(parent)
        #加载三态图片 重设大小
        self.pic_nomal = QPixmap(str1)
        self.pic_hover = QPixmap(str2)
        self.pic_press = QPixmap(str3)
        #显示正常大小下的图片
        self.resize(self.pic_nomal.size())
        self.setPixmap(self.pic_nomal)
    def enterEvent(self, a0: QtCore.QEvent):
         self.setPixmap(self.pic_hover)
    def leaveEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.pic_nomal)
    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.setPixmap(self.pic_press)
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        #鼠标释放的时候发射信号
        self.setPixmap(self.pic_hover)
        self.clicked.emit()

#封装一个棋子类
class Chess(QLabel):
    def __init__(self,color='w',parent=None):
        super().__init__(parent)
        self.color = color
        if color == 'b':
            pic = QPixmap("source/黑子.png")
        elif color == 'w':
            pic = QPixmap("source/白子.png")
        self.resize(pic.size())
        self.setPixmap(pic)

class biaoshi(QLabel):
    def __init__(self,parent = None):
        super().__init__(parent)
        biaoshi = QPixmap("source/标识.png")
        self.resize(biaoshi.size())
        self.setPixmap(biaoshi)










#基础类 存放相关的基础数据
class GameWindow(QWidget):
    #返回的信号
    backSingal = pyqtSignal()
    restartSingal = pyqtSignal()
    def __init__(self,parent=None):#父控件 不指定以屏幕作为父窗体
        super().__init__(parent)
        self.setup_ui()#调用这个函数页面的搭建

    def setup_ui(self):
        #界面的搭建

        self.setFixedSize(760, 650)  # 设置窗体固定大小
        # 设置背景图片
        window_tupian = QPalette()
                        # setBrush设置给谁设置什么
        window_tupian.setBrush(self.backgroundRole(), QBrush(QPixmap('source/游戏界面.png')))
        self.setPalette(window_tupian)
        self.setWindowIcon(QIcon('source/icon.png'))  # 设置窗体图标
        #设置按钮
        self.back_btn=DjrPushButton("source/返回按钮_normal.png","source/返回按钮_hover.png","source/返回按钮_press.png",self)
        self.back_btn.clicked.connect(self.back)
        self.restart_btn=DjrPushButton("source/开始按钮_normal.png","source/开始按钮_hover.png","source/开始按钮_press.png",self)
        self.restart_btn.clicked.connect(self.restart)
        self.lose_btn=DjrPushButton("source/认输按钮_normal.png","source/认输按钮_hover.png","source/认输按钮_press.png",self)
        self.lose_btn.clicked.connect(self.lose)
        self.regret_btn=DjrPushButton("source/悔棋按钮_normal.png","source/悔棋按钮_hover.png","source/悔棋按钮_press.png",self)
        self.regret_btn.clicked.connect(self.regret)
        self.back_btn.move(680,10)
        self.restart_btn.move(640,240)
        self.lose_btn.move(640,310)
        self.regret_btn.move(640,380)


    def back(self):
        #关闭本窗体 告诉别人我要返回
        #发射一个自定义的信号
        self.backSingal.emit()
        self.close()
    def restart(self):
        self.restartSingal.emit()
        self.close()
    def lose(self):
        pass
    def regret(self):
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent):
        pass

def is_win(chessboard):
    '''
    判断棋盘上是否有玩家胜利
    :param chessboard: 19*19的二维数组
    :return: 没有返回False，有的话，返回胜利者的颜色
    '''
    for j in range(0,19): # 注意这里会出现数组越界的情况，我们在代码中直接pass掉
        for i in range(0,19):
            if chessboard[i][j] is not None:
                c = chessboard[i][j].color
                # 判断右、右下、下、左下四个方向是否构成五子连珠，如果构成了，就可以。
                # 右
                try:
                    if chessboard[i+1][j] is not None:
                        if chessboard[i+1][j].color == c:
                            if chessboard[i+2][j] is not None:
                                if chessboard[i+2][j].color == c:
                                    if chessboard[i+3][j] is not None:
                                        if chessboard[i+3][j].color == c:
                                            if chessboard[i+4][j] is not None:
                                                if chessboard[i+4][j].color == c:
                                                    return c
                except IndexError:
                    pass
                # 右下
                try:
                    if chessboard[i+1][j+1] is not None:
                        if chessboard[i+1][j+1].color == c:
                            if chessboard[i+2][j+2] is not None:
                                if chessboard[i+2][j+2].color == c:
                                    if chessboard[i+3][j+3] is not None:
                                        if chessboard[i+3][j+3].color == c:
                                            if chessboard[i+4][j+4] is not None:
                                                if chessboard[i+4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 下
                try:
                    if chessboard[i][j+1] is not None:
                        if chessboard[i][j+1].color == c:
                            if chessboard[i][j+2] is not None:
                                if chessboard[i][j+2].color == c:
                                    if chessboard[i][j+3] is not None:
                                        if chessboard[i][j+3].color == c:
                                            if chessboard[i][j+4] is not None:
                                                if chessboard[i][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 左下
                try:
                    if chessboard[i-1][j+1] is not None:
                        if chessboard[i-1][j+1].color == c:
                            if chessboard[i-2][j+2] is not None:
                                if chessboard[i-2][j+2].color == c:
                                    if chessboard[i-3][j+3] is not None:
                                        if chessboard[i-3][j+3].color == c:
                                            if chessboard[i-4][j+4] is not None:
                                                if chessboard[i-4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass

    # 所有的都不成立，返回False
    return False





