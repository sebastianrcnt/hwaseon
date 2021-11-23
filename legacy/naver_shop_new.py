from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
import time
from time import sleep
from pprint import pprint

import urllib
from urllib.request import Request, urlopen
import re


import requests
from bs4 import BeautifulSoup

### 알고리즘 ###
# 1-1. 제품의 nv_mid 값으로 내가 선택한 키워드들 검색시, 순위 찾기
# 1-2. 키워드별 10page / 묶음상품 구분
# 2. AD 구분

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

MAX_PAGE = 2


def getSpecificProductRankAndProduct(keywordSearchData, urlContainingProductId):
    for searchResult in keywordSearchData:
        if (searchResult['productId'] in urlContainingProductId) or (searchResult['shopId'] in urlContainingProductId):
            product = {'rank': searchResult['rank'], 'product': searchResult}
            return product
    product = {'rank': -1, 'product': None}
    return product


# (i)번째 페이지 값 (40개) 가져오기
def getKeywordSearchData(keyword):
    pageUrls = []
    for m in range(1, MAX_PAGE):
        pageUrl = ('https://search.shopping.naver.com/search/all?frm=NVSCTAB&origQuery=' +
                   keyword + '&pagingIndex=' + str(m) + '&pagingSize=40&productSet=total&query=' +
                   keyword + '&sort=rel&timestamp=&viewType=list')
        pageUrls.append(pageUrl)

    keywordSearchData = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_page_url = {executor.submit(
            crawlSearchDataByUrl, pageUrl): pageUrl for pageUrl in pageUrls}
        for future in as_completed(future_to_page_url):
            page_url = future_to_page_url[future]
            keywordSearchData += future.result()

    return keywordSearchData


def crawlSearchDataByUrl(url):
    '''쇼핑리스트 가져오기'''
    ### 검색어 추출 ###
    search_keyword = url.split('&origQuery=')[1].split('&pagingIndex')[0]

    # 페이지 넘버
    page_numb = url.split('&pagingIndex=')
    page_numb = page_numb[1].split('&pagingSize=40&productSet=total&query=')[0]
    req = requests.get(url, headers=headers)
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')
    searchedItems = soup.find('script', {'type': 'application/json'})
    searchedItems = str(searchedItems)
    searchedItems = searchedItems.replace(
        '<script id="__NEXT_DATA__" type="application/json">', '')
    searchedItems = searchedItems.replace('</script>', '')
    result_json = json.loads(searchedItems.strip())

    short_url = result_json['props']['pageProps']['initialState']['products']['list']
    searchedItems = []
    for k in range(0, len(short_url)):
        # 제품명
        productname = short_url[k]['item']['productTitle']
        # 노 묶음 상품
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
                ad_check = True
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
                ad_check = False
                # 묶음상품 순위
                group_rank = '-'
            searchedItems.append({
                'keyword': search_keyword,
                'adType': ad_check,
                'rank': rank,
                'groupRank': group_rank,
                'shopName': shopname,
                'shopId': shopid,
                'productName': productname,
                'productId': nvmid
            })
        # 묶음 상품
        else:
            for m in range(0, len(short_url[k]['item']['lowMallList'])):
                nvmid = short_url[k]['item']['lowMallList'][m]['nvMid']
                shopid = short_url[k]['item']['lowMallList'][m]['mallPid']
                shopname = short_url[k]['item']['lowMallList'][m]['name']
                rank = k+1
                group_rank = m+1
                ad_check = '-'
                searchedItems.append({
                    'keyword': search_keyword,
                    'adType': ad_check,
                    'rank': rank,
                    'groupRank': group_rank,
                    'shopName': shopname,
                    'shopId': shopid,
                    'productName': productname,
                    'productId': nvmid
                })
    return searchedItems


# 키워들 리스트 입력


def getRankAndProduct(keyword, url):
    data = getKeywordSearchData(keyword)
    return getSpecificProductRankAndProduct(data, url)

def crawl_product_rank_within_keywords_naver(keywords, url):
    rank_dict = {}
    with ThreadPoolExecutor() as executor:
        future_to_keyword = {executor.submit(
            getRankAndProduct, keyword, url): keyword for keyword in keywords}
        for future in as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            rank_dict[keyword] = future.result()
    return rank_dict

