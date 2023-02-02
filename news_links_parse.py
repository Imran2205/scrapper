import json
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from scrapy.crawler import CrawlerProcess
from mantis_scrapper.mantis_scrapper.spiders.mantis_spider import MantisSpider
from bs4 import BeautifulSoup

news_webs = [
    'https://www.fiercewireless.com',
]

WINDOW_SIZE = "1000,600"

chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

all_urls = []


# #!/usr/bin/python
#
# import threading
# import time
# import os
#
#
# class MyThread(threading.Thread):
#     def __init__(self, thread_id, name, counter, sub_dir):
#         threading.Thread.__init__(self)
#         self.cmd = "find /proj/dtcosg_work/<_DIR_> -type f -print0 | xargs -0 -n 40 -P 40 ls -lash > /proj/dtcosg_work/kkousher/final_size_<_DIR_>.txt"
#         self.threadID = thread_id
#         self.name = name
#         self.counter = counter
#         self.sub_dir = ""
#
#     def run(self):
#         os.system(
#             self.cmd.replace('<_DIR_>', self.sub_dir)
#         )
#
# thread1 = MyThread(1, "Thread-1", 1, "kkouser")
#
# thread1.start()


def link_parser(web_links):
    for count, url in enumerate(web_links):
        if url.endswith('/'):
            url = url[:-1]
        print("loading....", url)
        driver = webdriver.Chrome(
            executable_path=r'C:\chromedriver.exe',
            chrome_options=chrome_options
        )
        driver.get(url)
        html = driver.page_source

        driver.close()
        driver.quit()

        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')

        urls = []
        for link in soup.find_all('a'):
            link_ = link.get('href')
            if link_:
                if not link_.startswith('https://www.'):
                    base_url = "https://" + url.split('//')[1].split('/')[0]
                    link_ = base_url + link_
                website = "https://" + link_.split('//')[1].split('/')[0]
                # print(website)
                if website not in news_webs:
                    continue
                if link_ not in all_urls:
                    urls.append(link_)
                    all_urls.append(link_)

        link_parser(urls)


link_parser(news_webs)
with open('all_urls.txt', 'w') as f:
    f.write("\n".join(all_urls))




