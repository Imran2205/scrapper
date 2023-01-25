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
# from pyvirtualdisplay import Display

task_list = [
    2243870,
    2243877,
    2243885,
    2243886,
    2243889,
    2243893,
    2243914,
    2243942,
    2244084,
    2244085,
    2244099,
]

base_url = "https://mantis.tapeout.cso:8088/mantis/v4/#/job-report/view/"

urls = [f"{base_url}{task}" for task in task_list]

output_json_path = r'C:\Users\admin\Desktop\desktop\web\scrapper\json'

proc = CrawlerProcess()
#
# CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# CHROMEDRIVER_PATH = r'C:\chromedriver.exe'
WINDOW_SIZE = "1000,600"

chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# chrome_options.add_argument("--headless")
# chrome_options.binary_location = CHROME_PATH
# chrome_options.add_argument("headless")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_experimental_option("prefs", {"download.default_directory": "/databricks/driver"})
driver = webdriver.Chrome(
    executable_path=r'C:\chromedriver.exe',
    chrome_options=chrome_options
)

for count, url in enumerate(urls):
    # options = webdriver.ChromeOptions()
    # options.binary_location = r'C:\chromedriver.exe'
    # options.add_argument("--log-level=3")

    driver.get(url)
    job_id = url.split("/")[-1]
    html_out_file = f'C:/Users/admin/Desktop/desktop/web/scrapper/html/{job_id}.html'

    # print("##################################################################################")
    # print(driver.page_source)

    if count == 0:
        timeout = 50
        try:
            element_present = EC.presence_of_element_located((By.ID, 'details-button'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

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

    # time.sleep(20)
    while f'>{job_id}</' not in driver.page_source:
        time.sleep(2)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'device-summary-container'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    html = driver.page_source

    html = re.sub(r"reviews_\d", "reviews", html)
    html = re.sub(r"check_\d", "check", html)
    html = re.sub(r"eCellValue_\d", "eCellValue", html)
    html = re.sub(r"hier_error_count_\d", "hier_error_count", html)
    html = re.sub(r"status_\d", "status", html)

    with open(html_out_file, 'w') as f:
        f.write(html)

    proc.crawl(MantisSpider, stat_urls=[f'file://{html_out_file}'], out_path=output_json_path)

    # ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()

driver.close()
driver.quit()
proc.start()

json_files = os.listdir(output_json_path)

master_json = {}

for file in json_files:
    if file.endswith('.json') and 'master' not in file:
        open_json_file = os.path.join(output_json_path, file)
        with open(open_json_file, 'r') as f:
            json_data = json.load(f)
        json_data['url'] = f"{base_url}{file.split('.')[0]}"
        master_json[file.split('.')[0]] = json_data

with open(os.path.join(output_json_path, 'master.json'), 'w') as f:
    json.dump(master_json, f, indent=4)

print(f"Saved all data to {os.path.join(output_json_path, 'master.json')}")


