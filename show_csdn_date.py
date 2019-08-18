import matplotlib.pyplot as plt
import csv
from numpy import *

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
    print(ax)
    print(ay)
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
    # print(get_msg('./Read_msg/read_msg.csv'))
    xtime, yread = get_msg('./Read_msg/read_msg.csv')
    plot_show_msg(xtime,yread)