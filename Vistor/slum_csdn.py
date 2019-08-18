from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from multiprocessing.pool import Pool
import re


proxy = [
    '106.12.18.45:8899',
    # '106.15.47.79:8899',
    '106.12.187.224:8899',
    '118.25.113.115:8899',
]

def count_run(i):
    try:

        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=http://' + proxy[i%3])
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(browser, 10)
        # print(proxy[i%4])
        # print('try',i)
        browser.get('https://blog.csdn.net/qq_19381989/article/details/95764431')
        read_count = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'read-count')))
        print(read_count.text)

    except:
        # read_count = browser.find_element_by_class_name('read-count')
        # print(read_count.text)
        print(i)

# count_run()
for i in range(10990):
    count_run(i)

# wait = WebDriverWait(browser,10)
# read_count = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'read-count')))

# print(group)
# if __name__ == '__main__':
#     group = [i for i in range(1000)]
#     pool = Pool()
#     pool.map(count_run,group)
#     pool.close()
#     pool.join()