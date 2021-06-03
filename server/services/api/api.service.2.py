import requests
import json
# 상댓값 가져오기: 데이터랩

headers = {
    'X-Naver-Client-Id': '8VcP69maRqven9qJWV1b',
    'X-Naver-Client-Secret': 'BH21bBnIJz'
}

body = {
    'startDate': '2020-04-01',
    'endDate': '2020-05-01',
    'timeUnit': 'month',
    'keywordGroups': [
        {'groupName': '가위', 'keywords': ['가위', '색종이', '마스크']}
    ],
}

print(json.dumps(body))
r = requests.post(
    "https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(body))

print(json.dumps(r.json(), ensure_ascii=False, indent=4))
