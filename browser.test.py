import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://m.blog.naver.com/PostList.nhn?blogId=ezecho',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = (
    ('blogId', 'ezecho'),
    ('categoryNo', '0'),
    ('currentPage', '1'),
    ('logCode', '0'),
)

response = requests.get('https://m.blog.naver.com/rego/PostListInfo.nhn', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://m.blog.naver.com/rego/PostListInfo.nhn?blogId=ezecho&categoryNo=0&currentPage=1&logCode=0', headers=headers, cookies=cookies)
print(response.content)
content = json.loads(response.content)
print(content)