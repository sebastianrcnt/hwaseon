import json
from json.decoder import JSONDecodeError
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

### 알고리즘 ###
# 1. 네이버 쇼핑 > N-pay Click > 특정 검색어 검색!
# 2. 1page 40개 제품 판매량 및 판매금액 등등 가져오기
# 2. AD 구분

# 검색어 입력
keyword = '닭가슴살'

# URL
url = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery=' + keyword + \
    '&pagingIndex=1&pagingSize=40&productSet=checkout&query=닭가슴살&sort=rel&timestamp=&viewType=list'

# 해당 URL 및 정보 긁어오기
req = requests.get(url, headers=headers)
req = req.text
soup = BeautifulSoup(req, 'html.parser')

result = soup.find('script', {'type': 'application/json'})
result = str(result)
result = result.replace(
    '<script id="__NEXT_DATA__" type="application/json">', '')
result = result.replace('</script>', '')
result_json = json.loads(result.strip())
short_url = result_json['props']['pageProps']['initialState']['products']['list']

main_list = []

adrank = 0
non_rank = 0

for i in range(0, len(short_url)):
    sub_list = []
    try:
        sub_list.append(short_url[i]['item']['adcrUrl'])
        sub_list.append(short_url[i]['item']['mallName'])
        sub_list.append(short_url[i]['item']['productName'])
        sub_list.append(short_url[i]['item']['price'])
        sub_list.append(short_url[i]['item']['dlvryCont'].split('|')[0])
        sub_list.append('광고' + str(adrank+1) + '번째')
        sub_list.append(i+1)
        adrank = adrank + 1
    except KeyError:
        sub_list.append(short_url[i]['item']['mallProductUrl'])
        sub_list.append(short_url[i]['item']['mallName'])
        sub_list.append(short_url[i]['item']['productName'])
        sub_list.append(short_url[i]['item']['price'])
        sub_list.append(short_url[i]['item']['dlvryCont'].split('|')[0])
        sub_list.append(str(non_rank+1) + '번째')
        sub_list.append(i+1)
        non_rank = non_rank + 1
    main_list.append(sub_list)


df5 = pd.DataFrame(main_list, columns=[
                   'URL', '쇼핑몰', '제품명', '판매가', '배송비', '순위', '합산순위'])
df5 = df5[['합산순위', '순위', '쇼핑몰', '제품명', '판매가', '배송비', 'URL']]
df5 = df5.sort_values(by=['합산순위'], ascending=True)
df5 = df5.reset_index(drop=True)


# 각 URL들어가서 판매량 가져오기
def get_sales_quantity(link):
    # link 에 제품 페이지 입력. 모바일, PC 상관없음
    page_link = link
    req = requests.get(page_link)
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')

    sub_list = []
    sub_list.append(link)
    try:
        k = soup.find_all('script')[1]
        k = str(k)
        k = k.replace('<script>window.__PRELOADED_STATE__=', '')
        k = k.replace('</script>', '')
        jk = json.loads(k)
        try:
            jk = jk['product']['A']['productDeliveryLeadTimes']
            sumk = 0
            for i in range(0, len(jk)):
                k = jk[i]['leadTimeCount']
                sumk = sumk + k
            # 판매수량 합
            sub_list.append(sumk)
        except KeyError:
            sub_list.append('No Sales data')
    except IndexError:
        sub_list.append('No Storefarm')

    main_list.append(sub_list)
    # return sub_list

ex = get_sales_quantity('https://www.oliveyoung.co.kr/store/common/partner.do?chlNo=1&chlDtlNo=1&sndType=goods&sndVal=A000000113670')
print(ex)

# # 멀티쓰레드
# start_time = time.time()

# u_list = list(df5['URL'])
# main_list = []

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(get_sales_quantity, u_list)

# print("--- %s seconds ---" % (time.time() - start_time))

# # 값 합치기
# df6 = pd.DataFrame(main_list, columns=['URL', '7일간 판매량'])
# df7 = pd.merge(df5, df6, on="URL", how='left')
# df5.to_csv('result_salescount_5.csv')
# df6.to_csv('result_salescount_6.csv')
# df7.to_csv('result_salescount_7.csv')