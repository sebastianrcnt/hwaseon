# import os
# import sys
# import urllib.request

# client_id = "8VcP69maRqven9qJWV1bs"
# client_secret = "BH21bBnIJz"
# api_url = "https://api.naver.com/keywordstool"

import time
import random
import requests
import json
from . import signature_helper
import pandas as pd


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signature_helper.Signature.generate(
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


def api_get(params):
    return requests.get(BASE_URL + uri, params=params,
                        headers=get_header(method, uri, API_KEY,
                                           SECRET_KEY, CUSTOMER_ID)).json()


def getKeywordStatistics(keyword):
    """
    {
          "relKeyword": "키캡",
          "monthlyPcQcCnt": 6310, // pc 월검색량
          "monthlyMobileQcCnt": 8880, // 모바일 월검색량
          "monthlyAvePcClkCnt": 22.2, // pc 월 광고클릭
          "monthlyAveMobileClkCnt": 207.0, // 모바일 월 광고클릭
          "monthlyAvePcCtr": 0.38, // 
          "monthlyAveMobileCtr": 2.53,
          "plAvgDepth": 15,
          "compIdx": "높음"
    }
    """

    result = api_get({
        'hintKeywords': keyword,
        'showDetail': 1,
        'month': 2
    })

    return result