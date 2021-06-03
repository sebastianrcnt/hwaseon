# from bs4 import BeautifulSoup
# import requests

# response = requests.get("https://cafe.naver.com/ca-fe/home/search/combinations?q=가상화폐")

# print(response.text)

import requests
import json
from pprint import pprint

headers = {
    'authority': 'datalab.naver.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://datalab.naver.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://datalab.naver.com/shoppingInsight/sKeyword.naver',
    'accept-language': 'en'
}

data = {
  'cid': '50000000',
  'timeUnit': 'month',
  'startDate': '2021-05-01',
  'endDate': '2021-06-02',
  'age': '',
  'gender': '',
  'device': '',
  'keyword': '원피스'
}

ageRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordAgeRate.naver', headers=headers, data=data).json()['result'][0]['data']
clickTrendData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordClickTrend.naver', headers=headers, data=data).json()['result'][0]['data']
genderRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordGenderRate.naver', headers=headers, data=data).json()['result'][0]['data']
deviceRateData = requests.post('https://datalab.naver.com/shoppingInsight/getKeywordDeviceRate.naver', headers=headers, data=data).json()['result'][0]['data']

pprint(ageRateData)
pprint(clickTrendData)
pprint(genderRateData)
pprint(deviceRateData)

# def get