import json
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scrapy.crawler import CrawlerProcess
from mantis_scrapper.mantis_scrapper.spiders.mantis_spider import MantisSpider

task_list = [
    '2166972',
    '2166973'
]

base_url = "https://mantis.tapeout.cso:8088/mantis/v4/#/job-report/view/"

urls = [f"{base_url}{task}" for task in task_list]

output_json_path = r'C:\Users\admin\Desktop\desktop\web\scrapper\json'

proc = CrawlerProcess()

for url in urls:
    driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver.get(url)
    job_id = url.split("/")[-1]
    html_out_file = f'C:/Users/admin/Desktop/desktop/web/scrapper/html/{job_id}.html'

    driver.find_element(By.ID, 'details-button').click()
    driver.find_element(By.ID, 'proceed-link').click()

    timeout = 50
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'full-width-input'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.find_element(By.NAME, 'username').send_keys('asad')
    driver.find_element(By.NAME, 'password').send_keys('GFULKA@@@1234')
    driver.find_element(By.CLASS_NAME, 'mat-raised-button').click()

    time.sleep(10)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'device-summary-container'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    html = driver.page_source

    driver.close()
    driver.quit()

    with open(html_out_file, 'w') as f:
        f.write(html)

    proc.crawl(MantisSpider, stat_urls=[f'file://{html_out_file}'], out_path=output_json_path)

proc.start()

json_files = os.listdir(output_json_path)

master_json = {}

for file in json_files:
    if file.endswith('.json') and 'master' not in file:
        open_json_file = os.path.join(output_json_path, file)
        with open(open_json_file, 'r') as f:
            json_data = json.load(f)
        master_json[file.split('.')[0]] = json_data

with open(os.path.join(output_json_path, 'master.json'), 'w') as f:
    json.dump(master_json, f, indent=4)

print(f"Saved all data to {os.path.join(output_json_path, 'master.json')}")


