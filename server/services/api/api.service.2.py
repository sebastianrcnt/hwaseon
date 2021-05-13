import requests
import json

headers = {
    'X-Naver-Client-Id': '8VcP69maRqven9qJWV1b',
    'X-Naver-Client-Secret': 'BH21bBnIJz'
}

body = {
    'startDate': '2020-01-01',
    'endDate': '2020-05-01',
    'timeUnit': 'month',
    'keywordGroups': [
        {'groupName': '폼클렌징', 'keywords': ['폼클렌징']}
    ],
}

print(json.dumps(body))
r = requests.post(
    "https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(body))

print(json.dumps(r.json(), ensure_ascii=False, indent=4))
