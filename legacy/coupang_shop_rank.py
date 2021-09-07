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


### 알고리즘 ###
# 1-1. 제품의 ID값으로 내가 선택한 키워드들 검색시, 순위 찾기
# 1-2. 키워드별 1page~10page
# 2. AD 구분


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

# deafualt 36개씩 정렬
# URL 만들기
# urls = [] 미리 잡아두기


def url_maker_coupang(keyword_list):
    for i in keyword_list:
        for m in range(1, 11):
            coupang_shop = ('https://www.coupang.com/np/search?component=&q=' +
                            i + '&page=' + str(m))
            coupang_urls.append(coupang_shop)


# 해당페이지 정보 가져오기
def get_shop_list_coupang(i):
    req = requests.get(coupang_urls[i], headers=headers)
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')

    # 광고 구좌 찾기
    # 광고구좌 리스트 만들기
    ad = soup.find_all(class_='search-product search-product__ad-badge')
    ad_soup_list = []
    for k in range(0, len(ad)):
        ad_soup_list.append(ad[k].find(class_='search-product-link').
                            get('data-item-id'))

    # 전체(해당페이지 광고 포함 36개) 가져오기
    total_soup = soup.find_all(class_='search-product-link')

    # 광고 구분 순위
    for j in range(0, len(total_soup)):

        # 상품의 아이템 아이디 가져오기
        item_id = total_soup[j].get('data-item-id')
        # 상품 이름 가져오기
        item_name = total_soup[j].find(class_=('search-product-wrap-img')
                                       ).get('alt')
        # 페이지 저장하기
        now_page = coupang_urls[i].split('&page=')[1]
        # 광고 구좌구분
        if total_soup[j].get('data-item-id') in ad_soup_list:
            ad_check = 'AD'
        else:
            ad_check = '-'
        rank = j+1

        test_list = []
        test_list.append(now_page)
        test_list.append(ad_check)
        test_list.append(rank)
        test_list.append(item_id)
        test_list.append(item_name)
        main_list.append(test_list)


# 키워드 직접 입력
keyword = ['수분에센스', '에센스추천', '촉촉한에센스']

### URLS 생성 및 멀티쓰레드 ###
coupang_urls = []
url_maker_coupang(keyword)
main_list = []

# 멀티쓰레드 구문 설정


def do_thread_crawl(urls: list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_shop_list_coupang, [(i) for i in range(0, len(urls))])


start_time = time.time()
do_thread_crawl(coupang_urls)
print("--- %s seconds ---" % (time.time() - start_time))


# 결과값
df = pd.DataFrame(main_list, columns=['페이지', '광고구분', '순위', 'item_id', '제품명'])
df = df.sort_values(by=['페이지', '순위'], ascending=True)
df = df.reset_index(drop=True)

df.to_csv("./result.csv")
