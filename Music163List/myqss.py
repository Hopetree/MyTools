class QSS():
    def __init__(self):
        self.qss = '''/**********主界面样式**********/
QWidget#MainWindow {
        font-family:Microsoft YaHei;
        font-size:13px;
        border: 0px solid rgb(111, 156, 207);
        border-image: url("logo/timg.png")
}
QWidget#messageWidget {
        background: rgba(173, 202, 232, 25%);
}
/**********菜单栏**********/
QMenuBar {
        font-size:13px;
        background: transparent;
        border: none;
}
QMenuBar::item {
        font-size:13px;
        font-family:Microsoft YaHei;
        border: 0px solid transparent;
        padding: 5px 10px 5px 10px;
        background: transparent;
}
QMenuBar::item:enabled {
        font-size:13px;
        color: rgb(2, 65, 132);
}
QMenuBar::item:!enabled {
        color: rgb(155, 155, 155);
}
QMenuBar::item:enabled:selected {
        border-top-color: rgb(111, 156, 207);
        border-bottom-color: rgb(111, 156, 207);
        background: rgb(198, 224, 252);
}
/**********按钮**********/
QPushButton{
        border: none;
        width: 75px;
        height: 25px;
}
QPushButton:enabled {
        background: #39c1ff;
        color: white;
}
QPushButton:!enabled {
        background: rgb(180, 180, 180);
        color: white;
}
QPushButton:enabled:hover{
        background: #61cdff;
}
QPushButton:enabled:pressed{
        background: #0291ff;
}
/**********文本编辑框**********/
QTextEdit {
        font-family:Microsoft YaHei;
        font:12px;
        border: none;
        color: #3b3b3b;
        background: rgba(0, 0, 0, 10%);
}
/**********输入框**********/
QLineEdit {
        font-family:Microsoft YaHei;
        border: none;
        height: 22px;
        background: rgba(0, 0, 0, 10%);
}
/**********下拉列表**********/
QComboBox {
        height: 22px;
        border:none;
        background: rgba(0, 0, 0, 10%);
}
QComboBox::drop-down {
        border: none;
        background: transparent;
}
QComboBox::down-arrow {
        image: url("logo/arrowBottom.png");
}
QComboBox QAbstractItemView {
        height: 25px;
        border: none;
        background: white;
        color:gray;
        outline:none;
}

'''