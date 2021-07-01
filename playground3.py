import requests
import json

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
    ('cid', '0'),
)

response = requests.get('https://datalab.naver.com/shoppingInsight/getCategory.naver', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://datalab.naver.com/shoppingInsight/getCategory.naver?cid=50000205', headers=headers)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))