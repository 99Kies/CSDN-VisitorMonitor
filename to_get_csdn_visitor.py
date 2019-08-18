import requests
from pyquery import PyQuery as pq
import re
import matplotlib.pyplot as plt
import time
from numpy import *
import os
import csv

def get_read_number(page):
    '''
    page指自己csdn博客的页数
    :param page: 自己csdn博客的页数
    :return: {文章主题，访客量，评论量} 时间(年/月/日)
    '''
    all_read = 0
    #用来存储所有的浏览量
    count = 0
    #用来存储定位到多少篇文章
    for i in range(1,page+1):
        url = 'https://blog.csdn.net/qq_19381989/article/list/{}'.format(i)
        # print(url)
        r = requests.get(url)
        doc = pq(r.text)
        items = doc('#mainBox > main > div.article-list > div').items()
        for item in items:
            project = {
                'title': item.find('h4 > a').text(),
                'read': item.find('div.info-box.d-flex.align-content-center > p:nth-child(3) > span > span').text(),
                'talk':item.find('div.info-box.d-flex.align-content-center > p:nth-child(5) > span > span').text(),
            }
            flag = 1
            #利用flag记录是否为首与末的空div，空的就不存储料
            for example in project:
                # if project['read'] is '' or '原' not in project['title']:
                #若只想统计原创作品时---
                if project['read'] is '':
                    flag = 0
            if flag == 1:
                all_read += int(project['read'])
                count += 1
    print(all_read)
    return all_read, time.strftime("%H:%M:%S",time.localtime(time.time()))

def is_yesterday_yn():
    '''
    每次保存时都打开存储访客数据的文件判断一下最后一次保存的是否为昨天，若是则进行爬取
    若没有访客数据的文件时也要进行爬虫
    :param filename: 访客数据文件名
    :return: True/False True：需要爬虫。False：无需爬虫
    '''
    msg_path = 'Test_msg'
    today = time.strftime("%H:%M:%S",time.localtime(time.time()))
    filename = msg_path + os.path.sep + 'test_msg.csv'
    if not os.path.exists(msg_path):
        return True
    with open(filename,'r',encoding='utf-8') as csvfile:
        reader = str(csvfile.readlines())
        print(reader)
    if today in reader:
        print('is Today')
        return False
    else:
        print('isn\'t today, you need update!')
        return True

def write_to_csvfile(all_read, date):
    msg_path = 'Test_msg'
    filename = msg_path + os.path.sep +'test_msg.csv'
    if not os.path.exists(msg_path):
        os.mkdir(msg_path)
        with open(filename, 'a', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            writer.writerow(['read','date'])
    try:
        with open(filename,'a',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            writer.writerow((all_read,date))
    except Exception as e:
        print(e)

def update_msg():
    if is_yesterday_yn():
        all_read, date = get_read_number(3)
        write_to_csvfile(all_read, date)


def get_msg(filename):
    try:
        xtime = []
        yread = []
        with open(filename,'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in list(reader)[1:]:
                xtime.append(row[1])
                yread.append(row[0])
        return xtime,yread
    except:
        print('Read Error')

def plot_show_msg(xtime,yread):
    ax = array(xtime)
    ay = array(yread)
    # plt.ion()
    plt.close()
    plt.plot(ax,ay)
    plt.xticks(rotation=70)
    plt.margins(0.08)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel("Date")
    plt.ylabel("Visitors")
    #图的标题
    plt.title("Visitor Data Visualization")
    plt.show()
    plt.pause(1)
    plt.close()

if __name__ == '__main__':
    while 1:
        update_msg()
        xtime, yread = get_msg('./Test_msg/test_msg.csv')
        plot_show_msg(xtime, yread)
        time.sleep(2)