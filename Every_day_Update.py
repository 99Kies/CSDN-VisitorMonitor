import os
from git import Repo
from csdn_read_save import for_Update
import time


def Every_day_Update(dirfile):
    cnt = 0
    first_now = time.strftime('%d',time.localtime(time.time()))
    now = 100 

    while 1:
        if first_now != now:
            cnt += 1
            repo = Repo(dirfile)
            g = repo.git
            try:
                for_Update()
                 
                g.add("--all")
                g.commit("-m auto update")
                g.push()
            except:
                print('Every, try again ing...')
                time.sleep(4)
                Every_day_Update(dirfile)
            now = time.strftime('%d',time.localtime(time.time()))
        else:
            print('is update!')
            g.add('--all')
            g.commit('-m auto update')
            g.push()
        time.sleep(5)

if __name__ == '__main__':
    dirfile = os.path.abspath('')
    Every_day_Update(dirfile)
