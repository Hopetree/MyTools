# -*- coding:utf-8 -*-

import datetime
import xlwt

class myExcel(object):
    def __init__(self):
        self.T = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M")
        self.work = xlwt.Workbook(encoding="utf-8")
        self.sheet = self.work.add_sheet(self.T)
        self.get_title()

    def get_title(self):
        # 设置字体
        font = xlwt.Font()
        # font.name = "Arial"    #字体名称
        font.colour_index = 23   #颜色
        font.bold = True    #字体加粗
        font.height = 20*12   #字体决定了行高，后面一个数字可以决定字体型号
        # 设置背景色
        patterni = xlwt.Pattern()
        patterni.pattern = xlwt.Pattern.SOLID_PATTERN
        patterni.pattern_fore_colour = 7
        # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta

        # 设置风格
        style = xlwt.XFStyle()
        style.font = font
        style.pattern = patterni

        for i,title in zip(range(7),["歌单名称","创建者","Popular","收藏人数","简介","创建时间","链接"]):
            self.sheet.write(0,i,title,style)
            self.sheet.col(i).width = 256*15

    def save_data(self,line,data):
        # 这一段是用来防止某些key不存在造成程序报错，因此添加不存在的值
        the_lis = ["name","popular","collect","desc","create_date","_id"]
        for each in the_lis:
            if each not in data:
                data[each] = ""
        if "user" not in data:
            data["user"] = {"name":"","_id":""}

        lis = [
            data["name"],
            data["user"]["name"],
            data["popular"],
            data["collect"],
            data["desc"],
            data["create_date"],
            "http://www.huanmusic.com/playlist/{}".format(data["_id"])
        ]
        for i,info in zip(range(7),lis):
            self.sheet.write(line,i,info)

    def save_excel(self):
        self.work.save(self.T+"_幻音歌单.xls")

if __name__ == '__main__':
    '''以下为测试用'''
    data = {
        "name":"歌单测试",
        "user":{"name":"作者"},
        "popular":"popular",
        "collect":123,
        "desc":1222,
        "create_date":20170713,
        "_id":456
    }
    e = myExcel()
    e.save_data(1,data)
    e.save_excel()