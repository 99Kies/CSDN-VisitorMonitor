import requests
from pyquery import PyQuery as pq
import re
import matplotlib.pyplot as plt
import time
from numpy import *
import csv
import os


def get_read_number(page):
    all_read = 0
    count = 0
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
            for example in project:
                # if project['read'] is '' or '原' not in project['title']:
                if project['read'] is '':
                    flag = 0
            if flag == 1:
                all_read += int(project['read'])
                count += 1
    return str(all_read), time.strftime("%Y/%m/%d",time.localtime(time.time()))

def save_to_mongo_list(msg):
    list_ = list([value for _, value in msg.items()])
    # print(list_)
    for clear in list_:
        # if '' not in clear:
        if clear is '':
            # print(clear)
            list_ = []
    if list_:
        print(list_)

def write_to_file(all_read, date):
    msg_path = 'Read_msg'
    filename = msg_path + os.path.sep +'read_msg.csv'
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


if __name__ == '__main__':
    # print(get_read_number(3))
    # print(get_read_number(3))
    all_read, date = get_read_number(3)
    print(all_read,date)
    write_to_file(all_read, date)