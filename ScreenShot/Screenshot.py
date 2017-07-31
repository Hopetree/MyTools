# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os.path
import multiprocessing as mp
from numpy import array_split



def readtxt():
    '''读取txt文件，返回一个列表，每个元素都是一个元组;文件的格式是图片保存的名称加英文逗号加网页地址'''
    with open('urls.txt','r') as f:
        lines = f.readlines()
    urls = []
    for line in lines:
        try:
            thelist = line.strip().split(",")
            if len(thelist) == 2 and thelist[0] and thelist[1]:
                urls.append((thelist[0],thelist[1]))
        except:
            pass
    return urls

def get_dir():
    '''判断文件夹是否存在，如果不存在就创建一个'''
    filename = "pics"
    if not os.path.isdir(filename):
        os.makedirs(filename)
    return filename

def webshot(tups):
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = '''function test()
        {
        return document.body.clientHeight;
        }
        return test()'''
    for tup in tups:
        picname = str(tup[0])
        link = tup[1]
        try:
            driver.get(link)
            k = 1
            height = driver.execute_script(js_height)
            while True:
                if k*500 < height:
                    js_move = "window.scrollTo(0,{})".format(k * 500)
                    driver.execute_script(js_move)
                    time.sleep(0.2)
                    height = driver.execute_script(js_height)
                    k += 1
                else:
                    break
            driver.save_screenshot('pics'+"\\"+picname+'.png')
            print("get one pic !!!")
            time.sleep(0.1)
        except Exception as e:
            print(picname,e)

if __name__ == '__main__':
    t = time.time()
    # 读取CUP核数
    cup_num = mp.cpu_count()
    get_dir()
    urls = readtxt()
    long = len(urls)
    # 少于CPU核数用单进程
    if long < cup_num:
        print("链接数量为{},小于CPU核数{}，使用单进程...".format(long,cup_num))
        webshot(urls)
    # 大于CPU核数用最大进程
    else:
        print("链接数量为{},大于CPU核数{}，使用{}进程...".format(long,cup_num,cup_num))
        # 将列表拆分，分给每个进程
        biglist = array_split(urls,cup_num)
        pool = mp.Pool(cup_num)
        for i in range(cup_num):
            pool.apply_async(webshot,args=(biglist[i],))
        pool.close()
        pool.join()
    print("操作结束，耗时：{:.2f}秒".format(float(time.time()-t)))





