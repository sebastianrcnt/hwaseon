# import requests
# from pprint import pprint

# headers = {
#     'authority': 'apis.naver.com',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
#     'accept': 'application/json, text/plain, */*',
#     'x-cafe-product': 'pc',
#     'sec-ch-ua-mobile': '?0',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#     'content-type': 'application/json;charset=UTF-8',
#     'origin': 'https://cafe.naver.com',
#     'sec-fetch-site': 'same-site',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-dest': 'empty',
#     'referer': 'https://cafe.naver.com/ca-fe/home/search/articles?q=%EA%B0%80%EC%9C%84&pr=3',
#     'accept-language': 'en',
# }

# data = '{"query":"가위","page":1,"sortBy":0,"period":["20210503","20210603"]}'
# response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles',
#                          headers=headers, data=data.encode('utf-8'))
                         
# pprint(response.json()['message']['result']['totalCount'])


from legacy.blog_rank_new import get_blog_data

get_blog_data('woojung357')