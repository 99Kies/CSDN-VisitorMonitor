import os
from git import Repo
from csdn_read_save import for_Update
import time


def Every_day_Update(dirfile):
    cnt = 0
    first_now = int(time.strftime('%d',time.localtime(time.time())))
    now = 100 
    repo = Repo(dirfile)
    g = repo.git

    while 1:
        if first_now != now:
            try:
                print("%d auto push" % first_now)
                for_Update()    
                try:
                    g.add("--all")
                    g.commit("-m auto update")
                    g.push()
                except:
                    pass
                now = int(time.strftime('%d', time.localtime(time.time())))
                first_now = now
            except:
                time.sleep(5)
                Every_day_Update(dirfile)
        else:
            print('is update!')
#            try:
#                g.add('--all')
#                g.commit('-m auto update')
#                g.push()
#                print("something change")
#            except:
#                print("clean")
        now = int(time.strftime("%d", time.localtime(time.time())))
        time.sleep(500)

if __name__ == '__main__':
    dirfile = os.path.abspath('')
    Every_day_Update(dirfile)
