# import os
# import sys
# import urllib.request

# client_id = "8VcP69maRqven9qJWV1bs"
# client_secret = "BH21bBnIJz"
# api_url = "https://api.naver.com/keywordstool
# api docs: http://naver.github.io/searchad-apidoc/#/guides

import time
import random
import requests
import json
import pandas as pd
from datetime import datetime


from server.services.signature_helper import Signature
from server.services import CrawlerServices, KeywordServices, SearchResultServices


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(
        timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '01000000001a1cd1c77e64fda7125be469a09d1682cd106a9419fea155f22df2d4261efac4'
SECRET_KEY = 'AQAAAAAaHNHHfmT9pxJb5GmgnRaCZU5NF5wTwLxdGE30+yEYFA=='
CUSTOMER_ID = '2235522'

# ManageCustomerLink Usage Sample

uri = '/keywordstool'
method = 'GET'

x = {
    'hintKeywords': '폼클렌징',
    'month': 12
}


async def api_get(params):
    return requests.get(BASE_URL + uri, params=params,
                        headers=get_header(method, uri, API_KEY,
                                           SECRET_KEY, CUSTOMER_ID)).json()


async def getKeywordStatistics(keyword):
    """
    {
          "relKeyword": "키캡", // 키워드
          "monthlyPcQcCnt": 6310, // pc 월검색량
          "monthlyMobileQcCnt": 8880, // 모바일 월검색량
          "monthlyAvePcClkCnt": 22.2, // pc 월 광고클릭
          "monthlyAveMobileClkCnt": 207.0, // 모바일 월 광고클릭
          "monthlyAvePcCtr": 0.38, // pc 월 클릭전환율
          "monthlyAveMobileCtr": 2.53, // 모바일 월 클릭전환율
          "plAvgDepth": 15,
          "compIdx": "높음" // 경쟁률
    }
    """

    result = await api_get({
        'hintKeywords': keyword,
        'showDetail': 1,
        'month': 2
    })['keywordList']

    keywordStatistics = {
        'monthlyPcQcCnt': result[0]['monthlyPcQcCnt'],  # PC 검색량수
        'monthlyMobileQcCnt': result[0]['monthlyMobileQcCnt'],  # 모바일 검색량수
        'monthlyPublishedBlogPostsCnt': await KeywordServices.getMonthlyPublishedBlogPosts(keyword),
        'monthlyPublishedCafePostsCnt': await KeywordServices.getMonthlyPublishedCafePosts(keyword),
    }

    return keywordStatistics

# 상댓값 가져오기: 데이터랩


async def getKeywordRelativeRatio(keyword, byYear=False):
    month = datetime.now().month
    year = datetime.now().year
    headers = {
        'X-Naver-Client-Id': '8VcP69maRqven9qJWV1b',
        'X-Naver-Client-Secret': 'BH21bBnIJz'
    }

    if byYear:
        body = {
            'startDate': f'{year-1}-{month:02}-01',  # 전월부터
            'endDate': f'{year}-{month:02}-01',  # 이번달까지
            'timeUnit': 'month',
            'keywordGroups': [
                {'groupName': keyword, 'keywords': [keyword]}
            ],
        }
    else:
        body = {
            'startDate': f'{year}-{(month-1):02}-01',  # 전월부터
            'endDate': f'{year}-{month:02}-01',  # 이번달까지
            'timeUnit': 'month',  # 한달간
            'keywordGroups': [
                {'groupName': keyword, 'keywords': [keyword]}
            ],
        }

    r = requests.post(
        "https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(body))

    return r.json()['results'][0]['data']


async def getMonthlySearchCount(keyword):
    """
    {
          "relKeyword": "키캡", // 키워드
          "monthlyPcQcCnt": 6310, // pc 월검색량
          "monthlyMobileQcCnt": 8880, // 모바일 월검색량
          "monthlyAvePcClkCnt": 22.2, // pc 월 광고클릭
          "monthlyAveMobileClkCnt": 207.0, // 모바일 월 광고클릭
          "monthlyAvePcCtr": 0.38, // pc 월 클릭전환율
          "monthlyAveMobileCtr": 2.53, // 모바일 월 클릭전환율
          "plAvgDepth": 15,
          "compIdx": "높음" // 경쟁률
    }
    """

    result = await api_get({
        'hintKeywords': keyword,
        'showDetail': 1,
        'month': 2
    })

    result = result['keywordList']

    keywordStatistics = {
        'totalQcCount': result[0]['monthlyMobileQcCnt'] + result[0]['monthlyPcQcCnt'],
        'monthlyPcQcCnt': result[0]['monthlyPcQcCnt'],  # PC 검색량수
        'monthlyMobileQcCnt': result[0]['monthlyMobileQcCnt'],  # 모바일 검색량수
    }

    return keywordStatistics
