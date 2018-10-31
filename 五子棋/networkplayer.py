from game import GameWindow,DjrPushButton
import sys
from PyQt5.QtCore import pyqtSignal,Qt
from game import Chess,is_win,biaoshi
from PyQt5.QtGui import QPixmap,QPalette,QFont
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QPushButton,QLabel,QApplication,QWidget,QLineEdit,QHBoxLayout,QListWidget,QVBoxLayout,QMessageBox
import pygame
import socket
import threading
import json
pygame.init()

def recv_sockdata(the_socket):
    #接收完整的数据帧
    total_data = ""
    data = ''
    while True:
        data = the_socket.recv(1024).decode()
        if "END" in data:
            total_data += data[:data.index("END")]
            break
        total_data += data
    return total_data


class NetworkPlayer(GameWindow):
    dataSingal = pyqtSignal(dict)
    back1Singal = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.tcp_socket = None
        #棋盘
        self.chessboard = [[None for i in range(0, 19)] for j in range(0, 19)]
        self.history = []
        self.dataSingal.connect(self.deal_data)
        self.is_w = True
        self.is_over = True
        self.win_label = None
        self.bagin = False
        self.is_connect = True
        self.biaoshi = None


    def setup_ui(self):
        #调用父类的方法
        super().setup_ui()
        font = QtGui.QFont()
        font.setFamily('source/CHILLER.TTF')
        font.setBold(True)
        font.setPixelSize(24)

        self.state_label=QLabel("游戏状态",self)
        self.state_label.setFont(font)
        self.state_label.move(640,110)
        self.setStyleSheet("QLabel{color:rgb(225,22,173,255);}")
        self.setWindowTitle('等待链接进入双人对抗')
        self.cuicu_btn=DjrPushButton("source/催促按钮_normal.png","source/催促按钮_hover.png","source/催促按钮_press.png",self)
        self.cuicu_btn.move(640,450)
        self.cuicu_btn.clicked.connect(self.sound)
    def sound(self):
        if self.bagin:
            return
        if self.is_over:
            return
        self.tcp_socket.sendall((json.dumps({"msg":"sound"}) + "END").encode())
        self.sound1()
    def sound1(selfself):
        sound=pygame.mixer.Sound("source/cuicu.wav")
        sound.set_volume(1)
        sound.play()
    def deal_data(self,data):#处理数据
        if data["msg"] == "pos":
            pos = data['data']
            xx = pos[0]
            yy = pos[1]
            color = data['color']
            self.chess = Chess(color = color ,parent = self)
            #如果此处有棋子点击失效
            if self.chessboard[xx][yy] is not None:
                return
            self.chessboard[xx][yy] = self.chess
            self.history.append((xx, yy))
            x = xx*30+50+30
            y = yy*30+50+30
            self.chess.move(x, y)
            self.state_text.setText("己方下棋")
            self.chess.show()
            if self.biaoshi:
                self.biaoshi.close()
                self.biaoshi = None
            if self.biaoshi == None:
                self.biaoshi = biaoshi(parent=self)
                self.biaoshi.move(x,y)
                self.biaoshi.show()
            sound = pygame.mixer.Sound("source/luozisheng.wav")
            sound.set_volume(1)
            sound.play()
            self.is_w = not self.is_w
            self.bagin = True
        if data["msg"] == "name":
            name = data['data']
            title = '与'+ name + '联机对战中'
            self.bagin = True
            self.setWindowTitle(title)
            self.state_text.setText("请按开始")
        if data["msg"] == "over":
            win = data['color']
            self.win_label = QLabel(self)
            if win == 'b':
                pic = QPixmap("source/黑棋胜利.png")
            else:
                pic = QPixmap("source/白棋胜利.png")
            self.biaoshi.close()
            if self.win_label is None:
                self.win_label.setPixmap(pic)
                self.win_label.move(100, 100)
                self.win_label.show()
            self.state_text.setText("游戏结束")
            self.is_over = True
        if data["msg"] == "restart":
            question = QMessageBox.question(self, "(重新)开始游戏请求","对方请求游戏(重新)开始，是否同意?",QMessageBox.Yes  |  QMessageBox.No )
            if question == QMessageBox.Yes:
                self.restartyes()#同意后向对方发送已同意
                self.restart2()#执行重新开始
                self.state_text.setText("游戏开始")
            if question == QMessageBox.No:
                self.restartno()#不同意向对方发送不同意 继续游戏
        if data["msg"] == "restartyes":
            QMessageBox.information(self, "(重新)开始游戏请求回复", "对方已同意(重新)开始游戏")
            self.restart2()
            self.bagin = True
            self.state_text.setText("游戏开始")
        if data["msg"] == "restartno":
            QMessageBox.information(self, "(重新)开始游戏请求回复","对方拒绝(重新)开始游戏" )
        if data["msg"] == "back":
            QMessageBox.information(self, "游戏中断","对方已退出游戏" )
            self.back1()
        if data["msg"] == "regret":
            question1 = QMessageBox.question(self, "对方悔棋提示","对方悔棋,是否同意",QMessageBox.Yes  |  QMessageBox.No )
            if question1 == QMessageBox.Yes:
                self.regretyes()
                self.regret1()
                self.state_text.setText("对方下棋")
            else:
                self.regretno()
        if data["msg"] == "regretyes":
            QMessageBox.information(self, "悔棋请求回复", "对方已同意悔棋")
            self.regret1()
            self.state_text.setText("己方下棋")
        if data["msg"] == "regretno":
            QMessageBox.information(self, "悔棋请求回复","对方拒绝悔棋" )
        if data["msg"] == "lose":
            QMessageBox.information(self, "对方认输提示","对方已认输" )
            self.lose1()
        if data["msg"] == "sound":
            self.sound1()
        if data["msg"] == "error":
            QMessageBox.information(self,"提示","对方已退出游戏,连接断开，将返回主界面")
            self.backSingal.emit()
            self.close()






    def recv_data(self,sock):
        #收到数据
        while self.is_connect:
            try:
                r_data = recv_sockdata(sock)
                data = json.loads(r_data)
                self.dataSingal.emit(data)  # 处理数据的函数
            except ConnectionResetError as e:
                print(e)
                data = {"msg":"error","data":"disconnect"}
                self.dataSingal.emit(data)
                break
            except ConnectionAbortedError:
                pass


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.is_over:
            return
        print("asd")
        if not self.bagin:
            return
        if a0.x() < 50 or a0.x() > 620:
            return
        if a0.y() < 50 or a0.y() > 620:
            return
        # 通过标识，决定棋子的颜色
        if self.is_w:
            self.chess = Chess('b', self)
        else:
            self.chess = Chess('w', self)

        # 将棋子定位到准确的坐标点
        if (a0.x() - 65) % 30 <= 15:
            x = (a0.x() - 65) // 30 * 30 + 50
        else:
            x = ((a0.x() - 65) // 30 + 1) * 30 + 50

        if (a0.y() - 65) % 30 <= 15:
            y = (a0.y() - 65) // 30 * 30 + 50
        else:
            y = ((a0.y() - 65) // 30 + 1) * 30 + 50
        # 在棋盘数组中，保存棋子对象
        xx = (x - 65) // 30
        yy = (y - 65) // 30
        # 如果此处已经有棋子，点击失效
        if self.chessboard[xx][yy] is not None:
            return

        self.chessboard[xx][yy] = self.chess
        self.history.append((xx, yy))


        self.chess.move(x, y)
        self.chess.show()
        if self.biaoshi:
            self.biaoshi.close()
            self.biaoshi = None
        if self.biaoshi == None:
            self.biaoshi = biaoshi(parent=self)
            self.biaoshi.move(x,y)
            self.biaoshi.show()
        self.state_text.setText("对方下棋")
        sound = pygame.mixer.Sound("source/luozisheng.wav")
        sound.set_volume(1)
        sound.play()
        self.is_w = not self.is_w
        #落之后 发送棋子位置
        colors = self.chess.color
        pos_data = {"msg":"pos","data":(xx,yy),"color":colors}
        self.tcp_socket.sendall((json.dumps(pos_data)+"END").encode())
        self.bagin = False
        color = is_win(self.chessboard)
        if color is False:
            return
        else:
            # QMessageBox.information(self,"消息","{}棋胜利".format(color))
            self.win_label = QLabel(self)
            if color == 'b':
                pic = QPixmap("source/黑棋胜利.png")
            else:
                pic = QPixmap("source/白棋胜利.png")
            pos_data = {"msg": "over","color": color}
            self.tcp_socket.sendall((json.dumps(pos_data) + "END").encode())
            self.win_label.setPixmap(pic)
            self.biaoshi.close()
            self.win_label.move(100, 100)
            self.win_label.show()
            self.state_text.setText("游戏结束")
            self.is_over = True
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.is_connect = False
        self.is_over = True
        if self.tcp_socket:
            self.tcp_socket.close()
        self.back1Singal.emit()
        super().closeEvent(a0)

    def restart(self):#发送重新开始游戏的请求

        self.tcp_socket.sendall((json.dumps({"msg":"restart"}) + "END").encode())
        # 重新开始游戏
    def restart2(self):
        self.is_over = False
        # 清空胜利图片
        if self.win_label is not None:
            self.win_label.close()

        # 清空棋盘
        #self.bagin = True
        self.is_w = True
        self.history = []
        if self.biaoshi:
            self.biaoshi.close()
        for i in range(0, 19):
            for j in range(0, 19):
                if self.chessboard[j][i] is not None:
                    self.chessboard[j][i].close()
                    self.chessboard[j][i] = None
    def restartyes(self):#发送同意重新开始游戏
        self.tcp_socket.sendall((json.dumps({"msg": "restartyes"}) + "END").encode())
    def restartno(self):#发送拒绝重新开始游戏的消息
        self.tcp_socket.sendall((json.dumps({"msg": "restartno"}) + "END").encode())
    def back(self):
        #关闭本窗体 告诉别人我要返回 告诉对方我要结束游戏
        self.tcp_socket.sendall((json.dumps({"msg": "back"}) + "END").encode())
        #发射一个自定义的信号
        self.back1()
    def back1(self):#收到消息后关闭游戏界面
        self.is_connect = False
        self.backSingal.emit()
        self.back1Singal.emit()
        self.close()
        if self.tcp_socket:
            self.tcp_socket.close()

    def regret(self):#向对方发送了悔棋请求
        if self.is_over:
            return
        if  self.bagin:
            return

        self.tcp_socket.sendall((json.dumps({"msg": "regret"}) + "END").encode())
    def regret1(self):
        if self.history:
            # 去最后一个元组
            pos = self.history.pop()
            # 通过元组记录的坐标销毁棋子
            self.chessboard[pos[0]][pos[1]].close()
            self.chessboard[pos[0]][pos[1]] = None
            # 转置棋子颜色

            self.is_w = not self.is_w
            self.bagin = not self.bagin
        if self.history:
            l = self.history[-1]
            x = l[0]
            y = l[1]
            self.biaoshi.move(x*30+80,y*30+80)
            self.biaoshi.show()
        else:
            self.biaoshi.close()

    def regretyes(self):
        self.tcp_socket.sendall((json.dumps({"msg": "regretyes"}) + "END").encode())
    def regretno(self):
        self.tcp_socket.sendall((json.dumps({"msg": "regretno"}) + "END").encode())


    def lose(self):
        if not self.bagin:
            return
        if self.is_over:
            return
        self.tcp_socket.sendall((json.dumps({"msg": "lose"}) + "END").encode())
        self.lose1()
    def lose1(self):

        self.win_label = QLabel(self)
        if not self.is_w:
            pic = QPixmap("source/黑棋胜利.png")
        else:
            pic = QPixmap("source/白棋胜利.png")
        if self.win_label is None:
            self.win_label.setPixmap(pic)
            self.biaoshi.close()
            self.win_label.move(100, 100)
            self.win_label.show()
        self.state_text.setText("游戏结束")

        self.is_over = True

ok = None
class NetworkSercer(NetworkPlayer):
    '''
    运行服务端界面
    '''
    def __init__(self,main_window = None,name="玩家一",parent = None):
        super().__init__(parent)
        self.main_window = main_window
        self.state_text = QLabel(self)
        font = QtGui.QFont()
        font.setFamily('source/CHILLER.TTF')
        font.setBold(True)
        font.setPixelSize(24)
        self.state_text.setFont(font)
        self.state_text.setText("等待链接")
        self.state_text.show()
        self.state_text.move(650, 140)
        #self.setStyleSheet("QLabel{color:rgb(255,241,241,255);}")
        self.name = name
        self.back1Singal.connect(self.backsercer)
        self.ser_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        #self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            global ok
            ok = True
            self.ser_socket.bind(("0.0.0.0",3003))
            self.ser_socket.listen(0)
            # self.ser_socket.accept()#监听假死
            th = threading.Thread(target=self.start_listen)
            th.start()

        except OSError as e:
            ok = False
            print("监听失败： "+ str(e))
            QMessageBox.information(self,"消息","端口已经被占用，请重试")
            self.close2()
    def close2(self):

        self.backSingal.connect(self.main_window.back)
        self.back1()






    def start_listen(self):
        print("start listening")
        while self.is_connect:
            try:
                global ok
                ok = True
                sock,addr = self.ser_socket.accept()#接收到的地址和对象
                self.tcp_socket = sock
                #发送自己的昵称
                self.tcp_socket.sendall((json.dumps({"msg":"name","data":self.name})+"END").encode())
                self.recv_data(self.tcp_socket)#接收数据
            except OSError:
                print("监听失败，socket已经失效")
                QMessageBox.information(self, "消息", "端口已失效，请重试")
                return


    def backsercer(self):
        self.ser_socket.close()



class NetworkClient(NetworkPlayer):
    '''
    运行客户端界面
    '''
    def __init__(self,main_window = None,name="玩家一",ip = "127.0.0.1",parent = None):
        super().__init__(parent)

        self.main_window = main_window
        self.name = name
        font = QtGui.QFont()
        font.setFamily('source/CHILLER.TTF')
        font.setBold(True)
        font.setPixelSize(24)
        self.state_text = QLabel(self)
        self.state_text.setFont(font)
        self.state_text.setText("等待链接")
        self.state_text.show()
        self.state_text.move(650, 140)
        self.setStyleSheet("QLabel{color:rgb(255,241,241,255);}")
        self.back1Singal.connect(self.backsercer)
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr = (ip,3003)
        try:
            global ok
            ok = True
            print(ok)
            self.tcp_socket.connect(addr)
            self.tcp_socket.sendall((json.dumps({"msg": "name", "data": self.name}) + "END").encode())
            th = threading.Thread(target=self.recv_data, args=(self.tcp_socket,))
            # self.recv_data(self.tcp_socket)
            th.start()
        except (ConnectionRefusedError, OSError):
            ok = False
            print(ok)
            print("网络连接失败，请重试")
            QMessageBox.information(self, "消息", "网络链接失败，请重试")
            self.close2()

    def backsercer(self):
        self.tcp_socket.close()

    def close2(self):

        self.backSingal.connect(self.main_window.back)
        self.back1()


class SetWindow(QWidget):
    def __init__(self,main_window = None,parent=None):#父控件 不指定以屏幕作为父窗体
        super().__init__(parent=parent)
        #用变量保存一个主界面的窗体
        self.main_window = main_window
        self.setWindowTitle("网络配置")
        self.name_label = QLabel("昵称",self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText("玩家一")
        #第一行的水平布局
        self.h1=QHBoxLayout()#生成布局管理器
        self.h1.addWidget(self.name_label,3)#把空间加入布局管理器
        self.h1.addWidget(self.name_edit,7)

        self.ip_label=QLabel("主机ip",self)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.setText("127.0.0.1")
        #第二行的水平布局
        self.h2 = QHBoxLayout()  # 生成布局管理器
        self.h2.addWidget(self.ip_label,3)  # 把空间加入布局管理器
        self.h2.addWidget(self.ip_edit,7)

        self.ser_btn = QPushButton("我是主机",self)
        self.con_btn = QPushButton("连接主机",self)
        self.con_btn.clicked.connect(self.client_mode)
        self.ser_btn.clicked.connect(self.server_mode)
        #第三行的水平布局
        self.h3 = QHBoxLayout()  # 生成布局管理器
        self.h3.addWidget(self.ser_btn)  # 把空间加入布局管理器
        self.h3.addWidget(self.con_btn)
        #主布局，垂直布局管理所有的布局
        self.main_layout=QVBoxLayout()#垂直布局
        self.main_layout.addLayout(self.h1)
        self.main_layout.addLayout(self.h2)
        self.main_layout.addLayout(self.h3)
        self.setLayout(self.main_layout)#窗体应用布局管理
        self.game_window = None
    def client_mode(self):
        self.game_window = NetworkClient(main_window=self.main_window,name=self.name_edit.text(),ip=self.ip_edit.text())
        if ok == True:
            self.game_window.show()
        else:
            self.close()
            return
        self.game_window.backSingal.connect(self.main_window.back)
        self.close()

    def server_mode(self):
        self.game_window = NetworkSercer(main_window=self.main_window,name=self.name_edit.text())
        if ok == True:
            self.game_window.show()
        else:
            self.close()
            return
        self.game_window.backSingal.connect(self.main_window.back)
        self.close()




