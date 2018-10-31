import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QCheckBox,QLineEdit,QListWidget,QListWidgetItem,QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
##继承类Class Window(PyQt5.QtWidget):
#主窗体的派生类
class Window(QWidget):
    def __init__(self,parent=None):#父控件 不指定以屏幕作为父窗体
        super().__init__(parent=parent)
        self.setWindowTitle("网络配置")
        self.name_label = QLabel("昵称",self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText("玩家零")
        self.resize(200,250)
        #第一行的水平布局
        self.h1=QHBoxLayout()#生成布局管理器
        self.h1.addWidget(self.name_label)#把空间加入布局管理器
        self.h1.addWidget(self.name_edit)

        self.play_label=QLabel("玩家列表：",self)
        self.refresh_btn = QPushButton("刷新",self)
        #第二行的水平布局
        self.h2 = QHBoxLayout()  # 生成布局管理器
        self.h2.addWidget(self.play_label,5)  # 把空间加入布局管理器
        self.h2.addWidget(self.refresh_btn,5)
        self.player_list=QListWidget(self)

        self.join_btn = QPushButton("加入房间：",self)
        self.battln_btn = QPushButton("选择对战",self)
        self.battln_btn.setEnabled(False)#按钮不可用
        #第三行的水平布局
        self.h3 = QHBoxLayout()  # 生成布局管理器
        self.h3.addWidget(self.join_btn)  # 把空间加入布局管理器
        self.h3.addWidget(self.battln_btn)
        #主布局，垂直布局管理所有的布局
        self.main_layout=QVBoxLayout()#垂直布局
        self.main_layout.addLayout(self.h1)
        self.main_layout.addLayout(self.h2)
        self.main_layout.addWidget(self.player_list)
        self.main_layout.addLayout(self.h3)

        self.setLayout(self.main_layout)#窗体应用布局管理


class Window2(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.is_click = False
        self.resize(400,400)
        self.btn1 = QPushButton("按钮1",self)
        self.btn1.move(100,100)
        self.btn2 = QPushButton("按钮2",self)
        self.btn2.move(200,200)
        self.btn2.setEnabled(False)
        #点击按钮执行一个操作
        self.btn1.clicked.connect(self.func)
        self.btn2.clicked.connect(self.func2)
    def func(self,checked):
        print("enter the function")
        if not self.is_click:
            self.btn1.setText("1按钮")
            self.btn2.setEnabled(True)
        else:
            self.btn1.setText("按钮1")
            self.btn2.setEnabled(False)
        self.is_click = not self.is_click

    def func2(self):
        #界面跳转 新窗体打开 自己关掉
        self.w=Window()
        self.w.show()
        self.close()


if __name__ == '__main__':
    #创建QT应用对象
    app=QApplication(sys.argv)
    w=Window2()
    #w.setFixedSize(800,600)固定大小
    #w.resize(400,400)#重设窗体大小
    w.setWindowTitle('酷炫的五子棋')#设置窗体标题
    w.move(50,50)#移动
    w.show()  # 窗体显示
    # 进入消息循环

    sys.exit(app.exec_())
    #w.close()#关闭窗体

    # #按钮 字符串产生一个按钮标题 父控件不指定 就是屏幕
    #
    # btn=QPushButton(parent=w,text="按钮")
    # btn.move(100,100)#移动
    # btn.setText("加入游戏")
    # btn.show()
    #
    #
    # #复选框
    # check1 = QCheckBox(parent=w, text="111")
    # check2 = QCheckBox(parent=w, text="112")
    # check3 = QCheckBox(parent=w, text="113")
    # check1.move(150,100)
    # check2.move(200,100)
    # check3.move(250,100)
    #
    # #输入框
    # edit = QLineEdit(parent=w)
    # edit.move(100,200)
    # edit.resize(200,30)
    # #列表窗体
    # list_widget=QListWidget(parent=w)
    # list_widget.move(100,250)
    # list_widget.resize(200,200)
    # items1 = QListWidgetItem("条目一")
    # items2 = QListWidgetItem("条目2")
    # items3 = QListWidgetItem("条目3")
    # list_widget.addItem(items1)
    # list_widget.addItem(items2)
    # list_widget.addItem(items3)
