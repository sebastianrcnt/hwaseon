import requests
import json
from datetime import datetime
import bs4

# 여기서는 연관키워드 추척
def get_naver_shopping_autocomplete_keywords(keyword):
    headers = {
        'authority': 'ac.shopping.naver.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://shopping.naver.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get(
        'https://ac.shopping.naver.com/ac', headers=headers, params=(
            ('frm', 'shopping'),
            ('st', '111111'),
            ('r_lt', '111111'),
            ('q', keyword),
        ))

    result = response.json()
    autocomplete_keywords = [keyword_obj[0][0]
                             for keyword_obj in result['items'][1]]
    return autocomplete_keywords


def getNaverSearchAutocompleteKeywords(keyword):
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


# 여기서부터는 발행량 추적
async def get_monthly_published_blog_posts(keyword, startDate=None, endDate=None):
    """
    네이버 블로그 월 발행량 가져오기(기간별)
    """

    month = datetime.now().month
    year = datetime.now().year

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
        'startDate': f'{year}-{(month-1):02}-01',
        'endDate': f'{year}-{(month):02}-01',
    }

    response = requests.get(
        'https://section.blog.naver.com/ajax/SearchList.nhn', headers=headers, params=params)

    # 월 발행량
    raw = response.text[6:]  # 앞에 쓸데없는 뭐가 많음
    res = json.loads(raw)
    return int(res['result']['totalCount'])


async def get_monthly_published_cafe_posts(keyword):
    """
    네이버 카페 월 발행량 가져오기(기간별)
    """

    month = datetime.now().month
    year = datetime.now().year

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
        "period": [f"{year}{(month-1):02}01", f"{year}{(month):02}01"]
    }

    data = json.dumps(data)

    response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles',
                             headers=headers, data=data.encode('utf-8'))

    return int(response.json()['message']['result']['totalCount'])


# 검색량
# https://datalab.naver.com/shoppingInsight/getCategory.naver?cid=0


"""
이런 식으로 어떤 섹션 이름들은 안에 지저분하게 뭐가 들어가있음
주로는 api_title_inner, 아이콘 등이니까 지워버리면 순수한 섹션 제목이 나오게 되어있당

<h2 class="api_title"> <i class="spnew api_ico_shoplogo"></i>네이버쇼핑<div class="api_title_inner"> <a role="button" href="#" class="api_link_help _trigger" aria-pressed="false" title="이 정보가 표시된 이유" onclick="return tCR('a=shp_gui.imark&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew api_ico_alert">이 정보가 표시된 이유</i></a> <div class="ly_api_info _content"> <p class="dsc">네이버가 운영하는 쇼핑 서비스입니다.</p> <button type="button" class="btn_close _trigger" title="안내 레이어 닫기" onclick="return tCR('a=shp_gui.guideclose&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew ico_close">정보확인 레이어 닫기</i></button> </div> </div> </h2>
"""


def getPCSearchSectionOrder(query):
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


def getMobileSearchSectionOrder(query):
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
