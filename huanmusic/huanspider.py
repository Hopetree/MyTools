# -*- coding:utf-8 -*-
# date:2017-7-12
# anthor:Alex

'''
二次元音乐幻音网歌单信息爬虫
'''

import requests
import json
import time
from savedata import myExcel

class myspider(object):
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
        self.myexcel = myExcel()
        self.line = 1

    # 提取所有歌单的信息
    def get_playlists(self,url):
        req = requests.get(url,headers=self.headers)
        req.encoding = "utf-8"
        infos = json.loads(req.text)
        big_lists = infos["genres"]
        for each in big_lists:
            small_lists = each["playlists"]
            for anylist in small_lists:
                link = "http://www.huanmusic.com/playlist/{}".format(anylist["_id"])
                anylist["link"] = link
                # 由于请求歌单的信息可能失败，因此使用try语句
                try:
                    the_data = self.get_one_playlist(link)
                    anylist["collect"] = the_data[0]
                    anylist["create_date"] = the_data[1]
                except:
                    anylist["collect"] = "miss"
                    anylist["create_date"] = "miss"
                print(anylist)
                self.myexcel.save_data(self.line,anylist)  #保存信息
                self.line += 1
        self.myexcel.save_excel()
        print("歌单信息保存完毕！")

    # 获取单个歌单的基本信息，主要是获取创建时间和收藏数，返回一个元祖
    def get_one_playlist(self,list_url):
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/57.0.2987.110 Safari/537.36",
            "Host":"www.huanmusic.com"
        }
        req = requests.post(list_url,headers=headers,timeout=5)
        data = json.loads(req.text)
        collect = data["collect"]
        create_date = data["create_date"]
        return (collect,create_date)

if __name__ == '__main__':
    # 更改链接日期可以修改歌单导出日期
    url = "http://net.huanmusic.com/g_v1_20170722"
    t = time.time()
    spider = myspider()
    spider.get_playlists(url)
    tt = time.time()
    print("耗时：{:.2f}秒".format(float(tt-t)))



