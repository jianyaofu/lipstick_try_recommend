# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
from io import BytesIO
from PIL import Image
import random
import re
import json

# get all lipstick links from Sephora, return a list of url
def get_lipstick_links() -> list:
    url = 'https://www.sephora.com/shop/lips-makeup?pageSize=12&currentPage='
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    lipstick_links = list()
    page_number = 1
    while True:
        time.sleep(1)
        try:
            is_valid_page = False
            response = requests.get(url + str(page_number), headers = headers, timeout = 5)
            if not response.status_code == 200:
                return f'Http Errors: {response.status_code}'
            else:
                result_page = BeautifulSoup(response.content, 'lxml')
                all_a_tags = result_page.find_all('a')
                for tag in all_a_tags:
                    if tag.get('href').startswith('/product'):
                        is_valid_page = True
                        link = 'https://www.sephora.com' + tag.get('href')
                        lipstick_links.append(link)
            if is_valid_page:
                page_number += 1
            else:
                return lipstick_links
        except:
            return None

# get the reviews of each lipstick by inputing its sephora link and return a list of reviews
def get_lipstick_reviews(lipstick_link: str) -> list:
    reviews = list()
    pattern = re.compile(r'P\d+')
    product_id = re.search(pattern, string = lipstick_link).group()
    off_set = 0
    while True:
        api_url = ''.join(["https://api.bazaarvoice.com/data/reviews.json?Filter=ProductId%3A",
                          product_id,
                          "&Sort=Helpfulness%3Adesc&Limit=100&Offset=",
                           str(off_set),
                           "&Include=Products%2CComments&Stats=Reviews&passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4"])
        response = requests.get(api_url)
        results = json.loads(response.content, encoding = 'utf-8')['Results']
        if results:
            for review in results:
                reviews.append(review['ReviewText'])
        else:
            break
        off_set += 100
    if len(reviews) < 300:
        return reviews
    else:
        return sorted(reviews, reverse = True)[:300]

# get the lipstick info including product_name(str), brand_name(str), price(float), love_count(int), colors(dict) by inputing its link
def get_lipstick(lipstick_link: str) -> dict:
    time.sleep(random.randint(1,3))
    lipstick = dict()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(lipstick_link, headers = headers, timeout = 10)
    result_page = BeautifulSoup(response.content, 'lxml')
    try:
        product_name = result_page.find('span',class_='css-r4ddnb ').get_text().strip()
    except:
        product_name = np.nan
    try:
        brand_name = result_page.find('img', attrs = {'data-comp': 'BrandLogo Image Box'}).get('alt').strip().upper()
    except:
        brand_name = np.nan
    try:
        if len(list(result_page.find('div', attrs = {'data-comp': 'Price Box'}).children)) > 1:
            price = float(result_page.find('div', attrs = {'data-comp': 'Price Box'}).get_text()[:6].replace('$', ''))
        else:
            price = float(result_page.find('div', attrs = {'data-comp': 'Price Box'}).get_text().strip().replace('$', ''))
    except:
        price = np.nan
    try:
        love_count = int(result_page.find('span', attrs = {'data-at': 'product_love_count'}).get_text().strip())
    except:
        love_count = np.nan
    colors = dict()
    if result_page.find('div', class_ = "css-gth5yg "):
        for tag in result_page.find('div', class_ = "css-gth5yg "):
            if tag.find('img'):
                color = tag.find('div', attrs = {'data-at': 'selected_swatch'})['aria-label']
                img_src = ''.join(["https://www.sephora.com", tag.find('img')['src']])
                response = requests.get(img_src, headers = headers, timeout = 5)
                im = Image.open(BytesIO(response.content))
                pix = im.load()
                width = im.size[0]
                height = im.size[1]
                r, g, b = pix[width / 2, height / 2]
                colors[color] = (r, g, b)
                time.sleep(0.5)

    lipstick['product_name'] = product_name
    lipstick['brand_name'] = brand_name
    lipstick['price'] = price
    lipstick['love_count'] = love_count
    lipstick['colors'] = colors
    lipstick['link'] = lipstick_link
    return lipstick

if __name__ == '__main__':
    lipstick_links = get_lipstick_links()
    
    product_name_l = []
    brand_name_l = []
    price_l = []
    love_count_l = []
    color_l = []
    rgb_l = []
    link_l = []
    for url in lipstick_links:
        try:
            lipstick_info = get_lipstick(url)
            count = len(lipstick_info['colors'])
            product_name_l.extend([lipstick_info['product_name']] * count)
            brand_name_l.extend([lipstick_info['brand_name']] * count)
            price_l.extend([lipstick_info['price']] * count)
            love_count_l.extend([lipstick_info['love_count']] * count)
            color_l.extend(list(lipstick_info['colors'].keys()))
            rgb_l.extend(list(lipstick_info['colors'].values()))
            link_l.extend([url] * count)
        except:
            print(url)
            continue
            
    lipstick_df = pd.DataFrame({'product_name': product_name_l,
                               'brand_name': brand_name_l,
                               'price': price_l,
                               'love_count': love_count_l,
                               'color': color_l,
                               'rgb': rgb_l,
                               'link': link_l})
    lipstick_df.to_csv("lipstick.csv")