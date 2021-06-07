# # from bs4 import BeautifulSoup
# # import requests

# # response = requests.get("https://cafe.naver.com/ca-fe/home/search/combinations?q=가상화폐")

# # print(response.text)

# import requests
# import json
# from pprint import pprint

# headers = {
#     'authority': 'datalab.naver.com',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
#     'accept': '*/*',
#     'x-requested-with': 'XMLHttpRequest',
#     'sec-ch-ua-mobile': '?0',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'origin': 'https://datalab.naver.com',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-dest': 'empty',
#     'referer': 'https://datalab.naver.com/shoppingInsight/sKeyword.naver',
#     'accept-language': 'en'
# }

# data = {
#   'cid': '50000000',
#   'timeUnit': 'month',
#   'startDate': '2021-05-01',
#   'endDate': '2021-06-02',
#   'age': '',
#   'gender': '',
#   'device': '',
#   'keyword': '원피스'
# }

# ageRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordAgeRate.naver', headers=headers, data=data).json()['result'][0]['data']
# clickTrendData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordClickTrend.naver', headers=headers, data=data).json()['result'][0]['data']
# genderRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordGenderRate.naver', headers=headers, data=data).json()['result'][0]['data']
# deviceRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordDeviceRate.naver', headers=headers, data=data).json()['result'][0]['data']

# pprint(ageRateData)
# pprint(clickTrendData)
# pprint(genderRateData)
# pprint(deviceRateData)

# # def get

import requests
import json
from pprint import pprint

cookies = {
    'NNB': 'XWDYAEPT7C6WA',
    'BMR': '',
}

headers = {
    'authority': 'blog.like.naver.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': '*/*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://m.blog.naver.com/cafeinfofam',
    'accept-language': 'ko',
    'cookie': 'NNB=XWDYAEPT7C6WA; BMR=',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'image',
    'Referer': 'https://m.blog.naver.com/cafeinfofam',
    'Accept-Language': 'ko',
}

params = (
    ('blogId', 'cafeinfofam'),
    ('categoryNo', '0'),
    ('currentPage', '1'),
    ('logCode', '0'),
)

response = requests.get('https://m.blog.naver.com/rego/ThumbnailPostListInfo.naver', headers=headers, params=params)

pprint(json.loads(response.text[5:])['result'])
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://m.blog.naver.com/rego/ThumbnailPostListInfo.naver?blogId=cafeinfofam&categoryNo=0&currentPage=1&logCode=0', headers=headers, cookies=cookies)
