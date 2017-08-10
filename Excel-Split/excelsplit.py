# -*- coding:utf-8 -*-

import xlsxwriter
import threading
import os.path

def title():
    print('使用方法'.center(60))
    print(' '*10+'1、将所有ID复制到txt文件中')
    print(' '*10+'2、输入文件名称，然后输入每个表格需要分配的ID数目')
    print(' '*37+'The author: Alex')

def readtxt(txtname):
    '''读取txt文件，生成一个ID列表'''
    while True:
        if os.path.isfile(txtname):
            break
        else:
            txtname = input('文件名称输入错误，请重新输入:')
    with open(txtname,'r') as f:
        lines = f.readlines()
    id_list = [each.strip() for each in lines if each.strip()]
    # print(id_list)
    return id_list

def write_excel(ids,num):
    '''第一个元素是列表，即要写入表格的ID，第二个元素是编号，用来给表格命名'''
    wk = xlsxwriter.Workbook(filename='ids_{}.xlsx'.format(num))
    sheet = wk.add_worksheet(name=str(num))
    sheet.write_column('A1',ids)
    wk.close()
    print('线程{}写入表格ids_{}.xlsx完毕！'.format(threading.current_thread().name,num))

def run(txtname,n):
    '''2个参数，第一个是读取的txt文件，第二个是每个表格需要写入的个数'''
    id_list = readtxt(txtname)
    new_list = [id_list[i:i+n] for i in range(0,len(id_list),n)]
    pool = []
    for ids,p in zip(new_list,range(1,len(new_list)+1)):
        t = threading.Thread(target=write_excel,args=(ids,p))
        pool.append(t)
    for t in pool:
        t.start()
    for t in pool:
        t.join()

if __name__ == '__main__':
    title()
    filename = input('请输入文件名称（含后缀）：')
    n = input('请输入每个表格需要分配的ID个数：')
    run(filename,int(n))
    input('表格分配完毕，按任意键退出程序！')

