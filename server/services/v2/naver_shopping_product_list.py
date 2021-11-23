from sys import displayhook
import requests
from bs4 import BeautifulSoup
import pydash as _

from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
import aiohttp
import asyncio
import timeit

### 알고리즘 ###
# 1-1. 제품의 nv_mid 값으로 내가 선택한 키워드들 검색시, 순위 찾기
# 1-2. 키워드별 10page / 묶음상품 구분
# 2. AD 구분

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


async def fetch(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()

MAX_PAGE = 2


class NaverShoppingProductListCrawler:
    # (i)번째 페이지 값 (40개) 가져오기
    async def get_shopping_product_list(self, keyword, max_pages=MAX_PAGE):
        page_urls = []
        for page_index in range(1, max_pages + 1):
            page_url = ('https://search.shopping.naver.com/search/all?frm=NVSCTAB&origQuery=' +
                        keyword + '&pagingIndex=' + str(page_index) + '&pagingSize=40&productSet=total&query=' +
                        keyword + '&sort=rel&timestamp=&viewType=list')
            page_urls.append(page_url)

        shopping_lists = await asyncio.gather(*[self._get_shopping_product_list_for_page(page_url) for page_url in page_urls])
        final_shopping_list = []
        for shopping_list in shopping_lists:
            final_shopping_list += shopping_list
        return final_shopping_list

    async def _get_shopping_product_list_for_page(self, url):
        '''쇼핑리스트 가져오기'''
        print(f'start getting shopping list {url}')

        # 페이지 넘버
        page_numb = url.split('&pagingIndex=')
        page_numb = page_numb[1].split(
            '&pagingSize=40&productSet=total&query=')[0]
        req = await fetch(url, headers=headers)
        # req = req.text()
        soup = BeautifulSoup(req, 'html.parser')
        searchedItems = soup.find('script', {'type': 'application/json'})
        searchedItems = str(searchedItems)
        searchedItems = searchedItems.replace(
            '<script id="__NEXT_DATA__" type="application/json">', '')
        searchedItems = searchedItems.replace('</script>', '')
        result_json = json.loads(searchedItems)

        shopping_list = result_json['props']['pageProps']['initialState']['products']['list']

        def extract(s, i):
            d = _.pick(s['item'], ['id', 'mallProductId',
                       'productTitle', 'imageUrl', 'rank'])
            is_ad = isinstance(d['rank'], str)
            d['isAd'] = is_ad
            d['displayRank'] = i + 1
            if is_ad:
                d['rank'] = int(d['rank'])
            return d

        shopping_list = [extract(shopping_list[i], i) for i in range(len(shopping_list))]

        # actualRank: 실제 표시 랭킹
        return shopping_list
