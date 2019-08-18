from csdn_test import *
from flask import Flask, url_for, render_template

app = Flask(__name__)

def echarts_show_pic(filename):
    try:
        xtime = []
        yread = []
        old_msg = {}
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in list(reader)[1:]:
                old_msg[row[1]] = row[0]
                xtime.append(row[1])
                yread.append(row[0])
    except:
        print('Read Error')
    sorted_dict = sorted(old_msg.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_dict[:5])
    # print(xtime)
    # print(yread)
    return xtime,yread,sorted_dict[:5]

@app.route('/')
def index():
    now_time,visitor,title_msg = echarts_show_pic('./Read_msg/read_msg.csv')

    # return render_template("echarts_.html",now_time=now_time,visitor=visitor)
    return render_template("tutorial_.html",title_msg=title_msg)




if __name__ == '__main__':
    app.run()
# if __name__ == '__main__':
#     while 1:
#         update_msg()
#         echarts_show_pic('./Read_msg/read_msg.csv')
#         time.sleep(2)