import json
import time
from time import sleep

import urllib
from urllib.request import Request, urlopen
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from multiprocessing import Process
import multiprocessing
import concurrent.futures
from concurrent.futures.process import ProcessPoolExecutor
import pandas as pd

### 알고리즘 ###
# 1-1. 제품의 nv_mid 값으로 내가 선택한 키워드들 검색시, 순위 찾기
# 1-2. 키워드별 10page / 묶음상품 구분
# 2. AD 구분

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


# URL 만들기
# urls = [] 미리 잡아두기


def url_maker(keyword_list):
    for i in keyword_list:
        for m in range(1, 11):
            naver_shop = ('https://search.shopping.naver.com/search/all?frm=NVSCTAB&origQuery=' +
                          i + '&pagingIndex=' + str(m) + '&pagingSize=40&productSet=total&query=' +
                          i + '&sort=rel&timestamp=&viewType=list')
            urls.append(naver_shop)

# (i)번째 페이지 값 (40개) 가져오기


def get_shop_list(i):

    ### 검색어 추출 ###
    search_keyword = urls[i].split('&origQuery=')[1].split('&pagingIndex')[0]
    # 페이지 넘버
    page_numb = urls[i].split('&pagingIndex=')
    page_numb = page_numb[1].split('&pagingSize=40&productSet=total&query=')[0]

    req = requests.get(urls[i], headers=headers)
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')
    result = soup.find('script', {'type': 'application/json'})
    result = str(result)
    result = result.replace(
        '<script id="__NEXT_DATA__" type="application/json">', '')
    result = result.replace('</script>', '')
    result_json = json.loads(result.strip())

    short_url = result_json['props']['pageProps']['initialState']['products']['list']
    for k in range(0, len(short_url)):
        # 제품명
        productname = short_url[k]['item']['productTitle']
        # 노 묶음 상품
        sub_list = []
        if short_url[k]['item']['lowMallList'] == None:
            # 광고 구분
            if short_url[k]['item']['purchaseConditionInfos'] == None:
                # 광고 맞음
                # NvMid
                nvmid = short_url[k]['item']['id']
                # shopID
                shopid = short_url[k]['item']['mallProductId']
                # 쇼핑몰명
                shopname = short_url[k]['item']['mallName']
                # 랭킹
                rank = k+1
                # ad 구분
                ad_check = 'AD'
                # 묶음상품 순위
                group_rank = '-'
            else:
                # 광고 아님
                # NvMid
                nvmid = short_url[k]['item']['id']
                # shopID
                shopid = short_url[k]['item']['mallProductId']
                # 쇼핑몰명
                shopname = short_url[k]['item']['mallName']
                # 랭킹
                rank = k+1
                # ad 구분
                ad_check = '-'
                # 묶음상품 순위
                group_rank = '-'
            sub_list.append(search_keyword)
            sub_list.append(ad_check)
            sub_list.append(rank)
            sub_list.append(group_rank)
            sub_list.append(shopname)
            sub_list.append(productname)  # 제품명
            sub_list.append(nvmid)
            sub_list.append(shopid)
            sub_list.append(page_numb)
            main_list.append(sub_list)
        # 묶음 상품
        else:
            for m in range(0, len(short_url[k]['item']['lowMallList'])):
                sub_list = []
                nvmid = short_url[k]['item']['lowMallList'][m]['nvMid']
                shopid = short_url[k]['item']['lowMallList'][m]['mallPid']
                shopname = short_url[k]['item']['lowMallList'][m]['name']
                rank = k+1
                group_rank = m+1
                ad_check = '-'
                sub_list.append(search_keyword)
                sub_list.append(ad_check)
                sub_list.append(rank)
                sub_list.append(group_rank)
                sub_list.append(shopname)
                sub_list.append(productname)  # 제품명
                sub_list.append(nvmid)
                sub_list.append(shopid)
                sub_list.append(page_numb)
                main_list.append(sub_list)


# 키워들 리스트 입력
keyword = ['수분에센스', '에센스추천', '촉촉한에센스', '피부붉은기', '얼굴붉은기']

# URLS 생성
urls = []
url_maker(keyword)

# 멀티쓰레드
start_time = time.time()

main_list = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_shop_list, [(i) for i in range(0, len(urls))])

print("--- %s seconds ---" % (time.time() - start_time))

df = pd.DataFrame(main_list, columns=[
                  '키워드', '광고구분', '순위', '묶순', '상점명', '제품명', 'nvmid', 'shopid', '페이지'])
df = df.sort_values(by=['키워드', '페이지', '순위', '묶순'], ascending=True)
df = df.reset_index(drop=True)
df.to_csv('./result2.csv')