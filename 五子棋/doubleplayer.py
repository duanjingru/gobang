from game import GameWindow,Chess,is_win,biaoshi
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

import pygame

class DoublePlayer(GameWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.pic3 = False#交替落子
        self.xy = []
        self.chessboard = [[None for i in range(0, 19)] for j in range(0, 19)]
        self.isover = False
        self.biaoshi = None






    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):

        if self.isover == True:
            return
        bwin = QPixmap("source/黑棋胜利.png")
        self.win = QLabel(self)
        self.win.setPixmap(bwin)
        self.win.move(100, 100)
        wwin = QPixmap("source/白棋胜利.png")

        self.win2 = QLabel(self)
        self.win2.setPixmap(wwin)
        self.win2.move(100, 100)



        for i in range(0,19):
            for j in range(0,19):
                if a0.x() in range(50+30*i,80+30*i) and a0.y() in range(50+30*j,80+30*j):
                    p =  [j,i]
                    if p not in self.xy:
                        if not self.pic3 :
                            self.chess = Chess(color = 'b',parent=self)
                            self.chess.move(50+30*i,50+30*j)
                            #在棋盘数组中保存棋子对象
                            self.chessboard[j][i] = self.chess
                            self.xy.append(p)
                            sound = pygame.mixer.Sound("source/luozisheng.wav")
                            sound.set_volume(1)
                            sound.play()
                            self.chess.show()
                            self.pic3=True
                        else:
                            self.chess2 = Chess(color = 'w',parent=self)
                            self.chess2.move(50+30*i,50+30*j)
                            self.chessboard[j][i] = self.chess2
                            self.xy.append(p)
                            sound = pygame.mixer.Sound("source/luozisheng.wav")
                            sound.set_volume(1)
                            sound.play()
                            self.chess2.show()
                            self.pic3 = False
        if self.xy:
            l = self.xy[-1]
            x = l[0]
            y = l[1]
            if self.biaoshi:
                self.biaoshi.close()
                self.biaoshi = None
            if self.biaoshi == None:
                self.biaoshi = biaoshi(parent=self)
                self.biaoshi.move(50 + 30 * y, 50 + 30 * x)
                self.biaoshi.show()
        color = is_win(self.chessboard)
        if color is False:
            return
        else:
            if color == 'w':
                self.win2.show()
            if color == 'b':
                self.win.show()
            self.isover = True
            self.biaoshi.close()

    def regret(self):
        if self.isover == True:
            return
        if  self.xy:
            l=self.xy[-1]
            x = l[0]
            y = l[1]
            self.chessboard[x][y].close()
            self.chessboard[x][y] = None
            self.xy.remove(self.xy[-1])
            if self.xy:
                l = self.xy[-1]
                x = l[0]
                y = l[1]
                self.biaoshi.move(50+30*y , 50+30*x)
            else:
                self.biaoshi.close()
            self.pic3 = not self.pic3

    def lose(self):
        if self.isover == True:
            return
        self.biaoshi.close()
        if self.pic3 == False:
            self.win2.show()
            self.isover = True
        if self.pic3 == True:
            self.win.show()
            self.isover = True






