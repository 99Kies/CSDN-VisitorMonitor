from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from multiprocessing.pool import Pool
import re


proxy = [
    'xxxx.xxxx.xxx:xxx',
    'xxx.xxx.xxx.xx:xxxx'
]

def count_run(i):
    try:

        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=http://' + proxy[i%3])
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(browser, 10)
        browser.get('https://blog.csdn.net/qq_19381989/article/details/95764431')
        read_count = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'read-count')))
        print(read_count.text)

    except:
        # read_count = browser.find_element_by_class_name('read-count')
        # print(read_count.text)
        print(i)

for i in range(10990):
    count_run(i)