# -*- coding:utf-8 -*-

import requests
from pyquery import PyQuery as pq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
from numpy import *
import csv
import operator
import sys
import importlib
importlib.reload(sys)
import os
from datetime import datetime

os.environ['NLS_LANG'] = 'Simplified Chinese_CHINA.ZHS16GBK'

#import cx_Oracle as cx

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


def get_read_number(page):
    '''
    爬虫模块，爬取博客主页所有的文章信息
    :param page: 博客共有几页
    :return: 总浏览量，时间，文章标题
    '''
    all_read = 0
    # 记录总浏览量
    count = 0
    # 记录匹配到几篇文章
    title_msg = {}
    # 用于记录文章的标题和他对应的浏览量
    for i in range(1,page+1):
        url = 'https://blog.csdn.net/qq_19381989/article/list/{}'.format(i)
        # print(url)
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        doc = pq(r.text)
        items = doc('#mainBox > main > div.article-list > div').items()
        for item in items:
            project = {
                'title': item.find('h4 > a').text(),
                'read': item.find('div.info-box.d-flex.align-content-center > p:nth-child(3) > span > span').text(),
                'talk':item.find('div.info-box.d-flex.align-content-center > p:nth-child(5) > span > span').text(),
            }
            flag = 1
            for example in project:
                # if project['read'] is '' or '原' not in project['title']:
                if project['read'] is '':
                    flag = 0
            if flag == 1:
                title_msg[project['title']] = project['read']
                all_read += int(project['read'])
                count += 1
    return str(all_read), time.strftime("%Y/%m/%d",time.localtime(time.time())),title_msg

def detail_msg_save(title_msg):
    '''
    这里主要存储每篇文章的信息
    :param title_msg: 匹配到的字典数据
    :return:
    '''
    msg_path = 'Read_msg'
    try:
        if not os.path.exists(msg_path):
            os.mkdir(msg_path)
        filename = msg_path + os.path.sep +'detail_msg.csv'
        with open(filename,'w', encoding='utf-8', errors='ignore') as csvfile:
        # 以覆盖的形式写入,
            writer = csv.writer(csvfile, dialect='unix')
            for title in title_msg:
                writer.writerow((title,title_msg[title]))
    except:
        print('detail_msg_save Error!!!')

def write_to_file(all_read, date):
    '''
    存储总访客量和时间数据
    :param all_read: 总浏览量
    :param date: 时间
    :return:
    '''
    msg_path = 'Read_msg'
    filename = msg_path + os.path.sep +'read_msg.csv'
    if not os.path.exists(msg_path):
        os.mkdir(msg_path)
        with open(filename, 'a', encoding='utf-8', errors="ignore") as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            writer.writerow(['read','date'])
    try:
        with open(filename,'a',encoding='utf-8', errors="ignore") as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            writer.writerow((all_read,date))
    except Exception as e:
        print(e)

def is_yesterday_yn():
    '''
    每次保存时都打开存储访客数据的文件判断一下最后一次保存的是否为昨天，若是则进行爬取
    若没有访客数据的文件时也要进行爬虫
    :param filename: 访客数据文件名
    :return: True/False True：需要爬虫。False：无需爬虫
    '''
    msg_path = 'Read_msg'
    today = time.strftime("%Y/%m/%d",time.localtime(time.time()))
    filename = msg_path + os.path.sep + 'read_msg.csv'
    if not os.path.exists(filename):
        return True
    with open(filename,'r',encoding='utf-8', errors="ignore") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if today in row:
                print('is Today')
                return False

    print("isn\'t today, you need update!")
    return True


def compare_detail_msg(title_msg):
    '''
    :param title_msg: 获得到的每篇文章的访客量
    :return: 返回上次保存和这次更新的变化
    '''
    change_ = {}
    old_msg = {}
    msg_path = './Read_msg'
    filename = msg_path + os.path.sep + 'detail_msg.csv'
    file_compare_day = msg_path + os.path.sep + 'compare_day_msg.csv'
    with open(filename, 'r',encoding='utf-8', errors="ignore") as csvfile:
        res = csv.reader(csvfile)
        for row in list(res):
            old_msg[row[0]] = row[1]
    for title in title_msg:
        # 判断是否有新文章
        if title not in old_msg:
            change_[title] = int(title_msg[title])
        else:
            change_[title] = int(title_msg[title]) - int(old_msg[title])
    sorted_dict = sorted(change_.items(), key=operator.itemgetter(1), reverse=True)
    #对变化过的数据按照访客量进行排序，输出更新变化最大的五篇文章
#    print("Day Change:"sorted_dict[:5])
    save_dict_msg(file_compare_day,change_)
    get_last_change_msg(change_)
    #记录文章浏览量总变化

def get_last_change_msg(change_now):
    '''
    为了获得每篇文章的访客变化
    :param change_now: 传入今天增长的访客量
    :return: 返回今天增长的访客量加上从前增长的访客量
    '''
    msg_path = './Read_msg'
    ago_filename = msg_path + os.path.sep + 'compare_day_msg.csv'
    file_compare_all = msg_path + os.path.sep + 'compare_all_msg.csv'
    change_ago = {}
    change_all = {}
    if not os.path.exists(file_compare_all):
        #第一次运行的时候，用于判断是否有compare_all_msg.csv文件，第一次的change_ago取compare_day_msg.csv种的日变化，就是初始化咯
        with open(ago_filename,'r',encoding='gb18030', errors="ignore") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                change_ago[row[0]] = row[1]
    else:
        with open(file_compare_all,'r',encoding='gb18030', errors="ignore") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                change_ago[row[0]] = row[1]
    for title in change_ago:
        if title not in change_now.keys():
            change_all[title] = int(change_ago[title])
        else:
            change_all[title] = int(change_ago[title]) + int(change_now[title])
    sorted_dict = sorted(change_all.items(), key=operator.itemgetter(1), reverse=True)[:5]
#    print('All Change:',sorted_dict)
    print(sorted_dict)
    plot_by_pie(sorted_dict)
    save_dict_msg(file_compare_all,change_all)

def save_dict_msg(filename,msgs):
    '''
    用于其他函数保存字典数据
    :param filename: 文件名
    :param msgs: 字典数据
    :return:
    '''
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            for key in msgs:
                writer.writerow((key, msgs[key]))
    except:
        print('save_dict Error!!!',filename)

def update_msg():
    Detail_path = './Read_msg/read_msg.csv'
    if is_yesterday_yn():
        all_read, date, title_msg = get_read_number(3)
        if os.path.exists(Detail_path):
            print('you_should_compare_your_msg')
            compare_detail_msg(title_msg)
            detail_msg_save(title_msg)
        else:
            print('first_save')
            detail_msg_save(title_msg)
        write_to_file(all_read, date)



def plot_show_msg(filename):
    try:
        xtime = []
        yread = []
        with open(filename,'r',encoding='utf-8', errors="ignore") as csvfile:
            reader = csv.reader(csvfile)
            for row in list(reader):
                xtime.append(datetime.strptime(row[1], "%Y/%m/%d"))
                yread.append(int(row[0]))
    except:
        print('Read Error')
    ax = xtime
    ay = yread
    if len(xtime) > 1:
        # 若只有一条数据或者没有的时候，就不打印图片
        plot_path = 'Images' + os.path.sep + 'plot'
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)
        filename = plot_path + os.path.sep + time.strftime("%Y_%m_%d_plot",time.localtime()) + '.png'
        try:
            plt.close()
            #fig = plt.figure(dpi=128, figsize=(10,6))
            plt.plot(ax,ay, c='red')
            plt.xticks(rotation=70)
            plt.margins(0.08)
            plt.subplots_adjust(bottom=0.15)
            plt.xlabel("Date")
            #fig.autofmt_xdate()
            plt.ylabel("Visitors")
            plt.title("Visitor Data Visualization, 2020")
            plt.savefig(filename)
        except:
            pass
def plot_by_pie(sorted_msg):
    '''
    画张饼图
    :param sorted_msg: 每篇文章的总变化或者日变化的前五位,
    :return:
    '''
    title = []
    read = []
    for msg in sorted_msg:
        if msg[1] != 0:
            # 不统计是 0 的数据
            title.append(msg[0])
            read.append(int(msg[1]))
    if len(title) > 1:
        pie_path = 'Images' + os.path.sep + 'pie_'
        if not os.path.exists(pie_path):
            os.makedirs(pie_path)
        filename = pie_path + os.path.sep + time.strftime("%Y_%m_%d_pie", time.localtime()) + '.png'
        try:
            plt.close()
            plt.pie(read,labels=title)
            plt.title("Visitor Data Visualization")
            plt.savefig(filename)
        except:
            print('pie_plot Error!!!')

def for_Update():
    update_msg()
    plot_show_msg('./Read_msg/read_msg.csv')

if __name__ == '__main__':
    update_msg()
    plot_show_msg('./Read_msg/read_msg.csv')
