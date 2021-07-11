import asyncio
import json
import aiohttp
import time
from time import sleep

import urllib
from urllib.request import Request, urlopen
import re

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver

from multiprocessing import Process
import multiprocessing
import concurrent.futures
from concurrent.futures.process import ProcessPoolExecutor
import pandas as pd


### 알고리즘 ###
# 1-1. 제품의 ID값으로 내가 선택한 키워드들 검색시, 순위 찾기
# 1-2. 키워드별 1page~10page
# 2. AD 구분

# 키워드 직접 입력
# keyword = ['수분에센스', '에센스추천', '촉촉한에센스', '피부붉은기', '얼굴붉은기']

### URLS 생성 및 멀티쓰레드 ###
# coupang_urls = []
# url_maker_coupang(keyword)
# main_list = []

import logging

import http.client
http.client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


async def fetch_coupang_search_products(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    params = {
        'q': keyword,
        'listSize': 72,
        'page': 1
    }

    print('started')
    response = requests.get(
        'https://www.coupang.com/np/search', headers=headers, params=params, timeout=5)
    html = response.text
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('https://www.coupang.com/np/search', headers=headers, params=params) as response:
    #         html = await response.text()
    #         print(html)

    bs = BeautifulSoup(html)
    products = [p['data-products'] for p in bs.select('#productList')]
    print(products)

asyncio.run(fetch_coupang_search_products(keyword="수분에센스"))
