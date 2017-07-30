from MusicListUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from MusicAPI import myAPI,myLIST
import sys

class myFunctions(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.LIST = myLIST()
        self.styledict = self.LIST.musicstyle
        # 设置歌单风格选项列表
        self.aboutmsg = "      软件用来批量导出网易云音乐推荐歌单，导出的信息以表格形式存在。表格形成之后建议通过EXCEL的数据透视表功能筛选出推荐歌单的热门歌曲，形成自己的收藏歌单。"
        self.authormsg = "Github：Hopetree\n网易云音乐重度沉迷患者，业余爬虫技术爱好者！\n"
        self.comboBox.addItems([each for each in self.styledict])

        self.actionOpenFile.triggered.connect(QtWidgets.QFileDialog.getOpenFileName)  # 查看当前文件夹
        self.actionQuit.triggered.connect(self.close)  # 菜单栏退出按钮函数
        self.actionAbout.triggered.connect(lambda: self.selectInfo("关于软件", self.aboutmsg))  # 关于软件
        self.actionAuthor.triggered.connect(lambda: self.selectInfo("作者", self.authormsg))  # 关于作者
        self.pushButton.clicked.connect(self.getinfos)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '关闭程序',
                                               "      关闭程序可能导致正在进行的过程终止，请确认\n是否退出并关闭程序？",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 消息框函数，传入2个参数，第1个是标题，第2个是显示内容
    def selectInfo(self, thetitle, megs):
        QtWidgets.QMessageBox.about(self, thetitle, megs)

    def getinfos(self):
        style_name = self.comboBox.currentText()
        style_link = self.styledict[style_name]
        pagenum = self.spinBox.value()
        self.pushButton.setDisabled(True)
        self.textEdit.setText("开始按钮已经按下，程序正在运行...")
        self.mythread = myThread(style_name,style_link,pagenum)
        self.mythread.text_singnal.connect(self.text_print)
        self.mythread.finished.connect(self.openbtn)
        self.mythread.start()

    def text_print(self,astr):
        self.textEdit.append(astr)
    def openbtn(self):
        self.pushButton.setDisabled(False)

class myThread(QtCore.QThread):
    text_singnal = QtCore.pyqtSignal(str)
    def __init__(self,style_name,style_link,pagenum):
        super().__init__()
        self.stylename = style_name
        self.stylelink = style_link
        self.pagenum = pagenum
        self.myapi = myAPI()

    def run(self):
        filename = self.myapi.get_csv(self.stylename)
        links_list = self.myapi.get_song_list(self.stylelink,self.pagenum)
        long = len(links_list)
        self.text_singnal.emit("歌单风格是【{}】,页数是【{}】,总计歌单【{}】个，正在提取歌曲信息".format(self.stylename,self.pagenum,long))
        n = 1
        for each in links_list:
            try:
                self.myapi.get_onestyle(each,filename)
                self.text_singnal.emit("选择歌单总计{}个，成功提取第{}个歌单的歌曲信息".format(long,n))
            except:
                print("miss")
                self.text_singnal.emit("选择歌单总计{}个，第{}个歌单的歌曲信息提取失败".format(long,n))
            n += 1
        self.text_singnal.emit("所有歌单的信息提取完毕,歌曲信息保存在当前文件夹下的表格  {}  中".format(filename))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myui = myFunctions()
    myui.show()
    sys.exit(app.exec_())