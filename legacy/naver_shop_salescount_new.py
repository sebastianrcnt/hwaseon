import json
import aiohttp
from json.decoder import JSONDecodeError
import time
from utils.util import hasattrs

import requests
from bs4 import BeautifulSoup

from multiprocessing import Process
import concurrent.futures
from concurrent.futures.process import ProcessPoolExecutor
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

async def get_naver_shop_salescount(keyword):
    url = 'https://search.shopping.naver.com/search/all'
    params = {
        'frm': 'NVSHCHK',
        'origQuery': keyword,
        'pagingIndex': 1,
        'pagingSize': 40,
        'productSet': 'checkout',
        'query': keyword,
        'sort': 'rel',
        'viewType': 'list'
    }
    # 해당 URL 및 정보 긁어오기
    req = requests.get(url, headers=headers, params=params)
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')

    result = soup.find('script', {'type': 'application/json'})
    result = str(result)
    result = result.replace(
        '<script id="__NEXT_DATA__" type="application/json">', '')
    result = result.replace('</script>', '')
    result_json = json.loads(result.strip())
    data = result_json['props']['pageProps']['initialState']['products']['list']

    products = []

    ad_rank = 0
    non_ad_rank = 0

    for i in range(0, len(data)):
        p = data[i]['item']
        is_ad = 'adcrUrl' in p
        # has_ad_attrs = (hasattrs(p, ['adcrUrl', 'mallName', 'productName', 'price', 'dlvryCont']))
        # has_non_ad_attrs = (hasattrs(p, ['mallProductUrl', 'mallName', 'productName', 'price', 'dlvryCont']))
        # print(is_ad ,has_ad_attrs, has_non_ad_attrs, hasattr(p, 'mallProductUrl'))
        product = {}
        product['mallName'] = p['mallName'] # 쇼핑몰
        product['productName'] = p['productName'] # 제품명
        product['price'] = int(p['price']) # 판매가
        product['deliveryPrice'] = int(p['dlvryCont'].split('|')[0]) # 배송비
        product['rank'] = ad_rank + 1 # 순위
        product['totalRank'] = i+1 # 합산순위

        if is_ad:
            product['url'] = p['adcrUrl'] 
            ad_rank = ad_rank + 1
        else:
            product['url'] = p['mallProductUrl'] # url
            non_ad_rank = non_ad_rank + 1
        products.append(product)
    for product in products:
        loop = asyncio.get_event_loop()
        salescount = loop.run_until_complete(fetch_sales_count(product))
        # print(salescount)

    return products

# 각 URL들어가서 판매량 가져오기
async def fetch_sales_count(product):
    product_page_url = product['url']
    # link 에 제품 페이지 입력. 모바일, PC 상관없음

    time1 = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(product_page_url) as response:
            req = await response.text()

    soup = BeautifulSoup(req, 'html.parser')

    time2 = time.time()
    sub_list = []
    sub_list.append(product_page_url)
    try:
        k = soup.find_all('script')[1]
        k = str(k)
        k = k.replace('<script>window.__PRELOADED_STATE__=', '')
        k = k.replace('</script>', '')
        jk = json.loads(k)
        try:
            jk = jk['product']['A']['productDeliveryLeadTimes']
            k_sum = 0
            for i in range(0, len(jk)):
                k = jk[i]['leadTimeCount']
                k_sum = k_sum + k
            # 판매수량 합
            sub_list.append(k_sum)
        except KeyError:
            sub_list.append('No Sales data')
    except IndexError:
        sub_list.append('No Storefarm')
    except JSONDecodeError as e:
        # print(e)
        pass

    time3 = time.time()

    print(product['totalRank'], time2-time1, time3-time2)
    return sub_list

import asyncio
start = time.time()
res = asyncio.run(get_naver_shop_salescount('폼클렌징'))
# print(json.dumps(res, ensure_ascii=False, indent=4))
end = time.time()
print(end - start)

# 16.831