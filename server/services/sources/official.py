from enum import Enum
from datetime import datetime
from utils.util import safeget
from utils.TimeUnitEnum import TimeUnit
import requests
import json
from server.services.tools.officialApiFetcher import fetchOfficialApi
from typing import List


# api: http://naver.github.io/searchad-apidoc/#/operations/GET/~2Fkeywordstool
async def fetch_related_keywords(keyword, month: int):
    """
    get absolute ratio
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

    result = await fetchOfficialApi('/keywordstool', 'GET', {
        'hintKeywords': keyword,
        'showDetail': 1,
        'month': month
    })
    
    if 'keywordList' not in result:
        print(result)

    result = safeget(result, 'keywordList') or []

    return result


async def fetch_relative_ratio(keywords: List[str], start_date: datetime.date, end_date: datetime.date, time_unit: TimeUnit):
    '''get relative ratio'''

    headers = {
        'X-Naver-Client-Id': '8VcP69maRqven9qJWV1b',
        'X-Naver-Client-Secret': 'BH21bBnIJz'
    }

    body = {
        'startDate': start_date.isoformat(),  # 전월부터
        'endDate': end_date.isoformat(),  # 이번달까지
        'timeUnit': time_unit.value,
        'keywordGroups':
            list(map(lambda keyword: {
                'groupName': keyword, 'keywords': [keyword]}, keywords))
    }

    '''  "ratio": [
    {
      "data": [
        {
          "period": "2021-05-01",
          "ratio": 93.98417
        },
        {
          "period": "2021-06-01",
          "ratio": 100
        }
      ],
      "keywords": [
        "샴푸"
      ],
      "title": "샴푸"
    }
  ]'''

    req = requests.post(
        "https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(body))

    raw = req.json()['results']
    result = [{'keyword': d['keywords'][0], 'data': d['data']} for d in raw]

    return result
