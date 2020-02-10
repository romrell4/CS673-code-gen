from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from os import path

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/home/bandrus/Documents/text_processing/F18_DIGHT360/chromedriver")

with open ('../resources/valid_edu_websites.csv') as url_list_file:
    urls = [url.strip() for url in url_list_file.read().split(',')]

# urls = ['https://www.byu.edu/']

for i, url in enumerate(urls):
    site_name = url.split('/')[2].split('.')[0]
    screenshot_location = f'../site_screenshots/{site_name}.png'
    screenshot_location_2 = f'../site_screenshots/{site_name}2.png'
    screenshot_location_3 = f'../site_screenshots/{site_name}3.png'

    if path.exists(screenshot_location_3) or site_name == 'nyu':
        continue

    driver.get(url)
    sleep(1)

    driver.save_screenshot(screenshot_location)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    driver.save_screenshot(screenshot_location_2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.save_screenshot(screenshot_location_3)

    print(f'{i} / {len(urls)}')
driver.quit()
