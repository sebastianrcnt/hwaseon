from enum import Enum
from datetime import datetime
from utils.TimeUnitEnum import TimeUnit
import requests
import json
from server.services.tools.officialApiFetcher import fetchOfficialApi


# api: http://naver.github.io/searchad-apidoc/#/operations/GET/~2Fkeywordstool
async def fetchRelKeywords(keyword, month: int):
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

    result = result['keywordList']

    return result



async def getKeywordRelativeRatio(keyword, startDate: datetime.date, endDate: datetime.date, timeUnit: TimeUnit):
    '''get relative ratio'''

    headers = {
        'X-Naver-Client-Id': '8VcP69maRqven9qJWV1b',
        'X-Naver-Client-Secret': 'BH21bBnIJz'
    }

    body = {
        'startDate': startDate.isoformat(),  # 전월부터
        'endDate': endDate.isoformat(),  # 이번달까지
        'timeUnit': timeUnit.value,
        'keywordGroups': [
            {'groupName': keyword, 'keywords': [keyword]}
        ],
    }

    r = requests.post(
        "https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(body))

    return r.json()['results'][0]['data']
