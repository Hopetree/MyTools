# -*- coding: utf-8 -*-
#date:2017-5-28

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PICdownUI import Ui_MainWindow
import os.path
import re
import requests
import datetime
import pickle

class Main(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.aboutmsg = "软件用来批量下载图片"
        self.authormsg = "作者：爱尔兰咖啡\n目前从事电商商务工作，业余爬虫技术爱好者！\n联系QQ：675737972"

        # 链接槽函数-----------------------------------------------------------------------------------------------
        self.setdata()   #设置默认下拉选项
        self.actionOpenfile.triggered.connect(QtWidgets.QFileDialog.getOpenFileName)  # 查看当前文件夹
        self.actionQuit.triggered.connect(self.close)  # 菜单栏退出按钮函数
        self.actionAbout.triggered.connect(lambda: self.selectInfo("关于软件", self.aboutmsg))  # 关于软件
        self.actionAuthor.triggered.connect(lambda: self.selectInfo("作者", self.authormsg))  # 关于作者
        self.pushButton_3.clicked.connect(self.down)      #下载图片线程
        self.pushButton.clicked.connect(self.changeData)  # 更新数据线程
        self.pushButton_2.clicked.connect(self.Read)  # 更新数据线程


        # 重写关闭函数
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '关闭程序',
                                               "关闭程序可能导致正在进行的过程终止，请确认\n是否退出并关闭程序？",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 消息框函数，传入2个参数，第1个是标题，第2个是显示内容
    def selectInfo(self, thetitle, megs):
        QtWidgets.QMessageBox.about(self, thetitle, megs)
    # 读取图片保存的类型
    def getpd(self):
        if self.radioButton.isChecked():
            product = ".jpg"
        if self.radioButton_2.isChecked():
            product = ".ico"
        if self.radioButton_3.isChecked():
            product = ".png"
        return product

# 下载图片槽函数-----------------------------------------------------------
    def down(self):
        self.pushButton_3.setDisabled(True)
        self.textEdit_2.setText("")
        texts = self.textEdit.toPlainText().strip()
        pattern = self.lineEdit_3.text().strip()
        start_url = self.lineEdit_4.text()
        end_url = self.lineEdit_5.text()
        pd = self.getpd()
        filename = self.lineEdit_6.text()
        self.spider = SpiderThread(texts,pattern,start_url,end_url,pd,filename)
        self.spider.progmax_signal.connect(self.setprogmax)
        self.spider.progvalue_signal.connect(self.setprogvalue)
        self.spider.text_signal.connect(self.text_print)
        self.spider.finished.connect(self.openbtn)
        self.spider.start()
    def setprogmax(self,n):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(n)
    def setprogvalue(self,i):
        self.progressBar.setValue(i)
    def text_print(self,astr):
        self.textEdit_2.append(astr)
    def openbtn(self):
        self.pushButton_3.setDisabled(False)

# 更新数据槽函数---------------------------------------------------------
    def changeData(self):
        webname = self.lineEdit.text()
        weblink = self.lineEdit_2.text()
        pattern = self.lineEdit_3.text().strip()
        start_url = self.lineEdit_4.text()
        end_url = self.lineEdit_5.text()
        pd = self.getpd()
        self.savedata = SaveDATA(webname,weblink,pattern,start_url,end_url,pd)
        self.savedata.text_signal.connect(self.text_print)
        self.savedata.combo_signal.connect(self.setdata)
        self.savedata.start()

        # 下载图片线程-----------------------------------------------------------

# 读取数据槽函数-------------------------------------------------------------
#     设置默认下拉框选项
    def setdata(self):
        self.comboBox.clear()    #设置之前先清空，避免形成追加
        try:
            with open("INFOS.dat", "rb") as f:
                data = pickle._load(f)
            self.comboBox.addItems([each for each in data])
        except:
            self.comboBox.insertItem(0, self.tr("默认选项"))
# 读取数据槽函数-------------------------------------------------------------
    def Read(self):
        wedname = self.comboBox.currentText()
        self.Readthread = ReadDATA(wedname)
        self.Readthread.text_signal.connect(self.text_print)
        self.Readthread.infos_signal.connect(self.givedata)
        self.Readthread.start()

    def givedata(self,lis):
        self.lineEdit_3.setText(lis[0])
        self.lineEdit_4.setText(lis[1])
        self.lineEdit_5.setText(lis[2])
        if lis[3] == ".ico":
            self.radioButton_2.setChecked(True)
        elif lis[3] == ".png":
            self.radioButton_3.setChecked(True)
        else:
            self.radioButton.setChecked(True)
        self.lineEdit.setText(lis[5])
        self.lineEdit_2.setText(lis[4])


class SpiderThread(QtCore.QThread):
    progmax_signal = QtCore.pyqtSignal(int)
    progvalue_signal = QtCore.pyqtSignal(int)
    text_signal = QtCore.pyqtSignal(str)

    def __init__(self,texts,pattern,start_url,end_url,pd,filename):
        super().__init__()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                                      " (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
        self.texts = texts
        self.pattern = pattern
        self.start_url = start_url
        self.end_url = end_url
        self.pd = pd
        self.filename = filename

    def run(self):
        T = datetime.datetime.now()
        t = T.strftime("%Y%m%d_%H%M")
        # 创建文件夹---------------------------------------------------------------
        if not os.path.isdir(self.filename):
            try:
                os.mkdir(self.filename)
                self.text_signal.emit("创建一个新的文件夹：{}".format(self.filename))
            except:
                self.filename = "IMGs"
                try:
                    os.mkdir(self.filename)
                except:
                    pass
                finally:
                    self.text_signal.emit("输入的文件夹名称不合规，使用默认文件：{}".format(self.filename))
        else:
            self.text_signal.emit("文件夹存在，不需要重新创建文件夹！")
        # 获取网址-----------------------------------------------------------------
        if "\n" in self.texts:
            urls = self.texts.split("\n")
        else:
            urls = [self.texts]
        # 提取图片链接------------------------------------------------------------------
        links = []
        if self.texts == "":
            self.text_signal.emit("没有输入网址，输入网址后重试！")
        elif self.pattern == "":
            self.text_signal.emit("没有填写正则表达式，请填写后重试！")
        else:
            for url in urls:
                try:
                    html = requests.get(url, headers=self.headers).text
                    midlink = re.findall(self.pattern, html)
                    for each in midlink:
                        imglink = self.start_url + str(each) + str(self.end_url)
                        links.append(imglink.strip())
                except:
                    self.text_signal.emit("{}网址无法提取到图片链接...".format(url))
            long = len(links)
            self.progmax_signal.emit(long)
            self.text_signal.emit("总计提取到图片链接{}个，尝试下载图片".format(long))
            m = 1
            for link in links:
                try:
                    pichtml = requests.get(link, headers=self.headers).content
                    with open(self.filename + "\\" + str(t) + "_" + str(m) + self.pd, "ab") as f:
                        f.write(pichtml)
                except:
                    self.text_signal.emit("图片链接{}下载失败！".format(link))
                self.progvalue_signal.emit(m)
                m += 1
            self.text_signal.emit("操作完毕！")

class SaveDATA(QtCore.QThread):
    text_signal = QtCore.pyqtSignal(str)
    combo_signal = QtCore.pyqtSignal()
    def __init__(self,webname,weblink,pattern,start_url,end_url,pd):
        super().__init__()
        self.webname = webname
        self.weblink = weblink
        self.pattern = pattern
        self.start_url = start_url
        self.end_url = end_url
        self.pd = pd

    def run(self):
        # 网站名称为空的时候不读取文件
        if self.webname == "":
            self.text_signal.emit("网站名称栏是空白，没有信息可以保存！")
        else:
            # 如果文件不存在则读取会报错，所以用try，如果不存在则创建一个文件
            try:
                with open("INFOS.dat","rb") as f:
                    data = pickle._load(f)
            except:
                with open("INFOS.dat","wb") as f:
                    data = ""
            # 是字典类型就追加数据，否则就重建数据
            if isinstance(data,dict):
                if self.webname in data:
                    self.text_signal.emit("网站【{}】在原数据中有记录，现在更新数据...".format(self.webname))
                else:
                    self.text_signal.emit("网站【{}】在原数据中没有记录，现在追加数据...".format(self.webname))
                info = {}
                info["weblink"] = self.weblink
                info["pattern"] = self.pattern
                info["start_url"] = self.start_url
                info["end_url"] = self.end_url
                info["pd"] = self.pd
                data[self.webname] = info
                with open("INFOS.dat","wb") as f:
                    pickle._dump(data,f)
                self.text_signal.emit("更新数据完成！")
            else:
                self.text_signal.emit("读取数据失败，可能是信息文件被破坏，现在新建数据...")
                data = {}
                info = {}
                info["weblink"] = self.weblink
                info["pattern"] = self.pattern
                info["start_url"] = self.start_url
                info["end_url"] = self.end_url
                info["pd"] = self.pd
                data[self.webname] = info
                with open("INFOS.dat","wb") as f:
                    pickle._dump(data,f)
                self.text_signal.emit("新建数据完成！")
            # 把所有的网站名称添加到下拉框中
            self.combo_signal.emit()

class ReadDATA(QtCore.QThread):
    text_signal = QtCore.pyqtSignal(str)
    infos_signal = QtCore.pyqtSignal(list)   #发送一个列表，包含读取的配置信息
    def __init__(self,webname):
        super().__init__()
        self.webname = webname

    def run(self):
        try:
            with open("INFOS.dat", "rb") as f:
                data = pickle._load(f)
        except:
            self.text_signal.emit("数据文件缺失，无法读取配置！")
        else:
            if self.webname in data:
                try:
                    infos = data[self.webname]
                    link = infos["weblink"]
                    pattern = infos["pattern"]
                    start_url = infos["start_url"]
                    end_url = infos["end_url"]
                    pd = infos["pd"]
                    lis = [pattern,start_url,end_url,pd,link,self.webname]
                    self.infos_signal.emit(lis)
                except:
                    self.text_signal.emit("数据文件信息错误，无法生存配置！")
            else:
                self.text_signal.emit("数据文件中没有{}网址的信息，无法进行配置".format(self.webname))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myui = Main()
    myui.show()
    sys.exit(app.exec_())