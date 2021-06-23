# import os
# import sys
# import urllib.request

# client_id = "8VcP69maRqven9qJWV1bs"
# client_secret = "BH21bBnIJz"
# api_url = "https://api.naver.com/keywordstool
# api docs: http://naver.github.io/searchad-apidoc/#/guides

from server.services.tools.officialApiFetcher import fetchOfficialApi
import time
import requests
import json
import pandas as pd
from datetime import datetime









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

    result = await fetchOfficialApi({
        'hintKeywords': keyword,
        'showDetail': 1,
        'month': 4
    })

    result = result['keywordList']

    keywordStatistics = {
        'totalQcCount': result[0]['monthlyMobileQcCnt'] + result[0]['monthlyPcQcCnt'],
        'monthlyPcQcCnt': result[0]['monthlyPcQcCnt'],  # PC 검색량수
        'monthlyMobileQcCnt': result[0]['monthlyMobileQcCnt'],  # 모바일 검색량수
    }

    return keywordStatistics
