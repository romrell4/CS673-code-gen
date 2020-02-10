'''
This script is meant to be a one-off script that fetches and saves the
html/css for all urls in valid_edu_websites.csv
'''

import os
import urllib
import urllib.request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from webscraping.web_scraper import scraper

with open ('resources/valid_edu_websites.csv') as url_list_file:
    urls = [url.strip() for url in url_list_file.read().split(',')]

for url in urls:
    name = url.split('/')[2].split('.')[0]
    print(name)
    try:
        os.mkdir(f'cached_sites/{name}')
    except:
        print(f'Could not create cached_sites/{name}')
        continue

    soup, css = scraper.scrape(url)
    with open(f'cached_sites/{name}/index.html', 'w') as html_file:
        print(str(soup), file=html_file)

    # with open(f'cached_sites/{name}/style.css', 'w') as css_file:
    #     for rule in css:
    #         print(rule.serialize(), file=css_file)

    #
    request = urllib.request.Request(url,
        headers={'User-Agent': 'Berkeley Andrus bandrus5@byu.edu'})
    try:
        html_doc = urllib.request.urlopen(request).read()
        html_string = html_doc.decode('utf-8')
    except:
        continue

    soup = BeautifulSoup(html_doc, 'html.parser')
    style_links = soup.findAll('link', {'rel': "stylesheet"})
    with open(f'cached_sites/{name}/style.css', 'w') as css_file:
        for link in style_links:
            try:
                css_url = link.get('href')
                if css_url[0] == '/':
                    css_url = url + css_url[1:]
                print(css_url)
                cj = CookieJar()
                css_request = urllib.request.Request(css_url, headers={'User-Agent': 'Berkeley Andrus bandrus5@byu.edu'})
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                css_string = opener.open(css_request).read().decode('utf-8')
                # css_string = urllib.request.urlopen(request).read().decode('utf-8')
                print(css_string, file=css_file)
            except:
                continue
