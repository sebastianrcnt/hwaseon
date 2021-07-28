from json.decoder import JSONDecodeError
import time
from utils.TimeUnitEnum import TimeUnit
import pydash
import requests
import json
from datetime import datetime
import bs4
import asyncio
import aiohttp
# 여기서는 연관키워드 추척


async def fetch_naver_shopping_autocomplete_keywords(keyword):
    headers = {
        'authority': 'ac.shopping.naver.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://search.shopping.naver.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('frm', 'shopping'),
        ('q', keyword),
        ('q_enc', 'UTF-8'),
        ('r_enc', 'UTF-8'),
        ('r_format', 'json'),
        ('r_lt', '111111'),
        ('r_unicode', '0'),
        ('st', '111111'),
        ('t_koreng', '1'),
    )

    response = requests.get(
        'https://ac.shopping.naver.com/ac', headers=headers, params=params)
    # print(response.text)
    data = response.json()
    autocomplete_keywords = [x[0][0] for x in data['items'][1]]
    return autocomplete_keywords


async def fetch_naver_search_autocomplete_keywords(keyword):
    headers = {
        'authority': 'ac.search.naver.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://www.naver.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = requests.get(
        'https://ac.search.naver.com/nx/ac', headers=headers, params=(
            ('q', keyword),
            ('frm', 'nv'),
            ('r_format', 'json'),
            ('st', '100'),
        ))
    result = response.json()
    autocomplete_keywords = [item[0] for item in result['items'][0]]
    return autocomplete_keywords


async def fetch_naver_search_related_keywords(keyword):
    params = {
        'query': keyword
    }
    response = requests.get(
        "https://search.naver.com/search.naver", params=params)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    keyword_elements = soup.select(
        '#nx_footer_related_keywords > div > div.related_srch > ul > li.item > a.keyword > .tit')
    keywords = [keyword_element.text for keyword_element in keyword_elements]
    return keywords

# 여기서부터는 발행량 추적


async def fetch_blog_post_published_count(keyword, start_date: datetime.date, end_date: datetime.date):
    """
    네이버 블로그 월 발행량 가져오기(기간별)
    """
    headers = {
        'authority': 'section.blog.naver.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=%ED%8F%BC%ED%81%B4%EB%A0%8C%EC%A7%95',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = {
        'countPerPage': '7',
        'currentPage': '1',
        'keyword': keyword,
        'orderBy': 'sim',
        'type': 'post',
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat(),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://section.blog.naver.com/ajax/SearchList.nhn', headers=headers, params=params) as response:
            html = await response.text()

    # 월 발행량
    raw = html[6:]  # 앞에 쓸데없는 뭐가 많음
    res = json.loads(raw)
    return int(res['result']['totalCount'])


async def fetch_cafe_post_published_count(keyword, start_date: datetime.date, end_date: datetime.date):
    """
    네이버 카페 월 발행량 가져오기(기간별)
    """
    headers = {
        'authority': 'apis.naver.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, */*',
        'x-cafe-product': 'pc',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://cafe.naver.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://cafe.naver.com/ca-fe/home/search/articles?q=%EA%B0%80%EC%9C%84&pr=3',
        'accept-language': 'en',
    }

    data = {
        "query": keyword,
        "page": 1,
        "sortBy": 0,
        "period": [start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")]
    }

    data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        async with session.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles', headers=headers, data=data.encode('utf-8')) as response:
            res = await response.json()
    return int(res['message']['result']['totalCount'])


# 검색량
# https://datalab.naver.com/shoppingInsight/getCategory.naver?cid=0


"""
이런 식으로 어떤 섹션 이름들은 안에 지저분하게 뭐가 들어가있음
주로는 api_title_inner, 아이콘 등이니까 지워버리면 순수한 섹션 제목이 나오게 되어있당

<h2 class="api_title"> <i class="spnew api_ico_shoplogo"></i>네이버쇼핑<div class="api_title_inner"> <a role="button" href="#" class="api_link_help _trigger" aria-pressed="false" title="이 정보가 표시된 이유" onclick="return tCR('a=shp_gui.imark&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew api_ico_alert">이 정보가 표시된 이유</i></a> <div class="ly_api_info _content"> <p class="dsc">네이버가 운영하는 쇼핑 서비스입니다.</p> <button type="button" class="btn_close _trigger" title="안내 레이어 닫기" onclick="return tCR('a=shp_gui.guideclose&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew ico_close">정보확인 레이어 닫기</i></button> </div> </div> </h2>
"""


def fetch_PC_search_section_order(query):
    """
    키워드 검색 시 섹션의 순서 가져오기
    - 예) [파워링크, 네이버쇼핑, VIEW, 지식iN 플레이스, N쇼핑 LIVE]
    """
    response = requests.get(
        f"https://search.naver.com/search.naver?query={query}")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # 지울 것들 지우기(아이콘)
    deletes = soup.select(".api_title_inner, i")
    for delete in deletes:
        delete.decompose()  # 지워버리기

    result = []

    titles = soup.select(".ad_section h2, .api_title")
    for title in titles:
        result.append(title.get_text(strip=True))

    return result


def fetch_mobile_search_section_order(query):
    '''모바일 섹션 순서'''
    response = requests.get(
        f"https://m.search.naver.com/search.naver?query={query}")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # 지울 것들 지우기(아이콘)
    deletes = soup.select(".api_title_inner, i")
    for delete in deletes:
        delete.decompose()  # 지워버리기

    result = []

    titles = soup.select(".ad_section h2, .api_title")
    for title in titles:
        result.append(title.get_text(strip=True))

    return result


async def fetch_search_category(category_id):
    '''카테고리 정보 가져오기'''
    headers = {
        'authority': 'datalab.naver.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://datalab.naver.com/shoppingInsight/sCategory.naver',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('cid', category_id),
    )

    response = requests.get(
        'https://datalab.naver.com/shoppingInsight/getCategory.naver', headers=headers, params=params)
    res = response.json()

    return res


async def fetch_category_shopping_trending_keywords(category_id, start_date: datetime.date, end_date: datetime.date):
    headers = {
        'authority': 'datalab.naver.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://datalab.naver.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://datalab.naver.com/shoppingInsight/sCategory.naver',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'cid': category_id,
        'timeUnit': 'date',
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat(),
        'age': '',
        'gender': '',
        'device': '',
        'page': '1',
        'count': '100'
    }

    response = requests.post(
        'https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver', headers=headers, data=data)

    # print(response.text)
    data = response.json()['ranks']
    return data


async def fetch_naver_shopping_products(keyword):
    '''판매량 정보 가져오기'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
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
    soup = bs4.BeautifulSoup(req, 'html.parser')

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
        product['mallName'] = p['mallName']  # 쇼핑몰
        product['productName'] = p['productName']  # 제품명
        product['price'] = int(p['price'])  # 판매가
        product['deliveryPrice'] = int(p['dlvryCont'].split('|')[0])  # 배송비
        product['rank'] = ad_rank + 1  # 순위
        product['totalRank'] = i+1  # 합산순위
        product['isAd'] = is_ad

        if is_ad:
            product['url'] = p['adcrUrl']
            ad_rank = ad_rank + 1
        else:
            product['url'] = p['mallProductUrl']  # url
            non_ad_rank = non_ad_rank + 1
        products.append(product)

    tasks = [fetch_sales_count(product) for product in products]
    salescounts = await asyncio.gather(*tasks)
    for i in range(len(products)):
        products[i]['salescounts'] = salescounts[i]
    return products

# 각 URL들어가서 판매량 가져오기


async def fetch_sales_count(product):
    product_page_url = product['url']
    # link 에 제품 페이지 입력. 모바일, PC 상관없음

    async with aiohttp.ClientSession() as session:
        async with session.get(product_page_url) as response:
            html = await response.text()

    soup = bs4.BeautifulSoup(html, 'html.parser')
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
            salescount = k_sum
        except KeyError:
            salescount = '데이터 없음'
    except IndexError:
        salescount = '스토어팜 아님'
    except JSONDecodeError as e:
        salescount = "데이터 없음"
    return salescount


async def fetch_naver_shopping_product_count(keyword):
    '''네이버 쇼핑 키워드 검색된 상품 수'''
    params = {
        'query': keyword
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://search.shopping.naver.com/search/all', params=params) as response:
            html = await response.text()

    soup = bs4.BeautifulSoup(html, 'html.parser')
    element = soup.select_one(".subFilter_num__2x0jq")
    if not element:  # 상품수가 없을 때
        return 0
    # 상품수가 있음
    return int(element.text.replace(',', ''))

async def fetch_naver_shopping_keyword_category(keyword):
    '''키워드의 카테고리 가져오기(categoryId[])'''
    params = {
        'query': keyword
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://search.shopping.naver.com/search/all', params=params) as response:
            html = await response.text()
    
    soup = bs4.BeautifulSoup(html, 'html.parser')
    parent_element = soup.select_one(".basicList_depth__2QIie")
    category_elements = parent_element.select('a')
    categories = []
    for e in category_elements:
        categories.append(int(e['href'].split('=')[-1]))
    return categories


async def fetch_keyword_graph_statistics(keyword, category_id, time_unit: TimeUnit, start_date: datetime.date, end_date: datetime.date):
    '''그래프 그리기용'''
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'referer': 'https://datalab.naver.com/shoppingInsight/sKeyword.naver',
        'origin': 'https://datalab.naver.com'
    }

    data = {
        'cid': category_id,  # category id
        'timeUnit': time_unit,  # time unit date/week/month
        'startDate': start_date.isoformat(),
        'endDate': end_date.isoformat(),
        # 'age': '30,40',  # 10/20/30/40/50/60 in commas
        'age': '',
        # 'gender': 'f',  # f or f,m or m
        'gender': '',
        # 'device': 'pc',  # '' 'pc' 'mo' 'pc,mo'
        'device': '',
        'keyword': keyword
    }

    statistics = {}
    async with aiohttp.ClientSession() as session:
        async with session.post('https://datalab.naver.com/shoppingInsight/getKeywordClickTrend.naver', headers=headers, data=data) as response:
            statistics['clickTrend'] = (await response.json(content_type=None))['result'][0]['data']
        # async with session.post('https://datalab.naver.com/shoppingInsight/getKeywordDeviceRate.naver', headers=headers, data=data) as response:
        #     statistics['deviceRate'] = (await response.json(content_type=None))['result'][0]['data']
        async with session.post('https://datalab.naver.com/shoppingInsight/getKeywordGenderRate.naver', headers=headers, data=data) as response:
            statistics['genderRate'] = (await response.json(content_type=None))['result'][0]['data']
        async with session.post('https://datalab.naver.com/shoppingInsight/getKeywordAgeRate.naver', headers=headers, data=data) as response:
            statistics['ageRate'] = (await response.json(content_type=None))['result'][0]['data']

    return statistics