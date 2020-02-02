from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/home/bandrus/Documents/text_processing/F18_DIGHT360/chromedriver")

with open ('../webscraping/valid_edu_websites.csv') as url_list_file:
    urls = [url.strip() for url in url_list_file.read().split(',')]

for i, url in enumerate(urls):
    site_name = url.split('/')[2].split('.')[0]
    screenshot_location = f'../site_screenshots/{site_name}.png'
    driver.get(url)
    screenshot = driver.save_screenshot(screenshot_location)

    print(f'{i} / {len(urls)}')
driver.quit()
