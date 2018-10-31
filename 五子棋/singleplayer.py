from game import GameWindow
from game import GameWindow,Chess,is_win,biaoshi
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import pygame

class SinglePlayer(GameWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pic3 = False  # 交替落子
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
        for i in range(0, 19):
            for j in range(0, 19):
                if a0.x() in range(50 + 30 * i, 80 + 30 * i) and a0.y() in range(50 + 30 * j, 80 + 30 * j):
                    p = (j,i)
                    if p not in self.xy:

                        if not self.pic3:
                            self.chess = Chess(color='b', parent=self)

                            self.chess.move(50 + 30 * i, 50 + 30 * j)
                            # 在棋盘数组中保存棋子对象
                            self.chessboard[j][i] = self.chess
                            self.xy.append(p)
                            sound = pygame.mixer.Sound("source/luozisheng.wav")
                            sound.set_volume(1)
                            sound.play()
                            self.chess.show()
                            if self.biaoshi:
                                self.biaoshi.close()
                                self.biaoshi = None
                            if self.biaoshi == None:
                                self.biaoshi = biaoshi(parent=self)
                                self.biaoshi.move(50+ 30 * i, 50 + 30 * j)
                                self.biaoshi.show()
                                self.pic3 = True
                        else:
                            self.chess = Chess(color='w', parent=self)
                            self.chess.move(50 + 30 * i, 50 + 30 * j)
                            # 在棋盘数组中保存棋子对象
                            self.chessboard[j][i] = self.chess
                            self.xy.append(p)
                            sound = pygame.mixer.Sound("source/luozisheng.wav")
                            sound.set_volume(1)
                            sound.play()
                            self.chess.show()
                            if self.biaoshi:
                                self.biaoshi.close()
                                self.biaoshi = None
                            if self.biaoshi == None:
                                self.biaoshi = biaoshi(parent=self)
                                self.biaoshi.move(50 + 30 * i, 50 + 30 * j)
                                self.biaoshi.show()
                                self.pic3 = False

        color = is_win(self.chessboard)
        if color is False:
            pass
        else:
            if color == 'w':
                self.win2.show()
            if color == 'b':
                self.win.show()
            self.biaoshi.close()
            self.isover = True
        if self.xy == []:
            return
        else:
            self.auto_run()

    def regret(self):
        if self.isover == True:
            return
        if self.xy:
            l = self.xy[-1]
            x = l[0]
            y = l[1]
            self.chessboard[x][y].close()
            self.chessboard[x][y] = None
            self.xy.remove(self.xy[-1])
            l = self.xy[-1]
            x = l[0]
            y = l[1]
            self.chessboard[x][y].close()
            self.chessboard[x][y] = None
            self.xy.remove(self.xy[-1])
            if self.xy:
                l = self.xy[-1]
                x = l[0]
                y = l[1]
                self.biaoshi.move(50+ 30 * y, 50 + 30 * x)
            else:
                self.biaoshi.close()


    def lose(self):
        if self.isover == True:
            return
        if self.pic3 == False:
            self.win2.show()
            self.biaoshi.close()
            self.isover = True
        if self.pic3 == True:
            self.win.show()
            self.biaoshi.close()
            self.isover = True

    def auto_run(self):
        if self.isover == True:
            return
        # 分别保存黑子，白子分数的数组
        scores_c = [[0 for i in range(0,19)] for j in range(0,19)]
        scores_p = [[0 for i in range(0,19)] for j in range(0,19)]
        # 计算所有点的分数
        for j in range(0,19):
            for i in range(0,19):
                if self.chessboard[i][j] is None:

                 # 如果有棋子了，找下一个点
                # 假设下黑棋的分数
                    self.chessboard[i][j] = Chess('b',self)
                    scores_c[i][j] += self.score(i,j,'b')
                    # 假设下白棋的分数
                    self.chessboard[i][j] = Chess('w',self)
                    scores_p[i][j] += self.score(i,j,'w')
                    # 恢复棋盘为空
                    self.chessboard[i][j] = None
                else:
                    continue

        # 先将两个二维数组，转成一位数组便于运算
        r_scores_c = []
        r_scores_p = []
        for item in scores_c:
            r_scores_c += item
        for item in scores_p:
            r_scores_p += item

        # 最终分数，取两者中更大的一个，然后将取值合并成为一个数组
        result = [max(a,b) for a,b in zip(r_scores_c,r_scores_p)]
        # 取出最大值点的下标
        chess_index = result.index(max(result))
        # 通过下标计算出落子的位置
        xx = chess_index // 19
        yy = chess_index % 19

        # 落子
        if self.pic3:
            self.chess = Chess('w',self)
        else :
            self.chess = Chess('b',self)

        x = xx * 30 + 50
        y = yy * 30 + 50
        self.chess.move(y,x)
        self.chess.show()
        if self.biaoshi:
            self.biaoshi.close()
            self.biaoshi = None
        if self.biaoshi == None:
            self.biaoshi = biaoshi(parent=self)
            self.biaoshi.move(y,x)
            self.biaoshi.show()


        sound = pygame.mixer.Sound("source/luozisheng.wav")
        sound.set_volume(1)
        sound.play()
        self.chessboard[xx][yy] = self.chess
        self.xy.append((xx, yy))
        self.pic3 = not self.pic3
        color = is_win(self.chessboard)
        if color is False:
            pass
        else:
            if color == 'w':
                self.win2.show()
            if color == 'b':
                self.win.show()
            self.isover = True
            self.biaoshi.close()

    def score(self, x, y, color):
        '''
        计算，如果在x,y这个点下color颜色的棋子，会得到多少分
        '''
        blank_score = [0, 0, 0, 0]
        chess_score = [0, 0, 0, 0]

        # 右方向
        for i in range(x, x + 5):
            if i >= 19:
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color == color:
                    # 如果是相同点，同色点分数加一
                    chess_score[0] += 1
                    # 朝同一个方向进行，每次遇到相同的颜色，都加一分
                else:
                    break
            else:
                blank_score[0] += 1
                break
        # 左方向
        for i in range(x - 1, x - 5, -1):
            if i <= 0:
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color == color:
                    chess_score[0] += 1
                else:
                    break
            else:
                blank_score[0] += 1
                break
        # 下方向
        for j in range(y, y + 5):
            if j >= 19:
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else:
                blank_score[1] += 1
                break
        # 上方向
        for j in range(y - 1, y - 5, -1):
            if j <= 0:
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else:
                blank_score[1] += 1
                break
        # 右下方向
        j = y
        for i in range(x, x + 5):
            if i >= 19 or j >= 19:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break
            j += 1
        # 左上
        j = y - 1
        for i in range(x - 1, x - 5, -1):
            if i <= 0 or j <= 0:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break
            j -= 1

        # 左下
        j = y
        for i in range(x, x - 5, -1):
            if i <= 0 or j >= 19:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j += 1
        # 右上
        j = y - 1
        for i in range(x + 1, x + 5):
            if i >= 19 or j <= 0:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j -= 1

        # 计算总分:
        for score in chess_score:
            if score > 4:  # 如果某个方向超过4，则此处落子五子连珠
                return 100
        for i in range(0, len(blank_score)):
            if blank_score[i] == 0:  # 说明在这个空白点的附近，没有同色棋子，也没有可继续落子的地方
                blank_score[i] -= 20
        # 四个方向的分数，将两个列表依次相加
        result = [a + b for a, b in zip(chess_score, blank_score)]

        return max(result)  # 返回四个方向其中的最高分值




