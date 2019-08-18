
import requests
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
import time
from numpy import *

def get_read_number(page):
    '''
    page指自己csdn博客的页数
    :param page: 自己csdn博客的页数
    :return: {文章主题，访客量，评论量} 时间(时:分:秒)
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
    return all_read, time.strftime("%H:%M:%S",time.localtime())

def plot_show_msg(msg):
    xtime = []
    yread = []
    for xy in msg:
        xtime.append(xy[1])
        yread.append(xy[0])
    print(msg)
    ax = array(xtime)
    ay = array(yread)
    plt.close()
    plt.plot(ax, ay)
    plt.xticks(rotation=70)
    plt.margins(0.08)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel("Date")
    plt.ylabel("Visitors")
    plt.title("Visitor Data Visualization")
    plt.show()
    plt.pause(1)
    plt.close()
    print('----------')

if __name__ == '__main__':
    msg = []
    while 1:
        time.sleep(1)
        all_read, now_time = get_read_number(3)
        msg.append((all_read,now_time))
        plot_show_msg(msg)


