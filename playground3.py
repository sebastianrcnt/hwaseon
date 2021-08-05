import json
from utils.util import jsonprint
import requests
import bs4

def parsePage(pageHtml):
    soup = bs4.BeautifulSoup(pageHtml, 'html.parser')
    text = str(soup.select_one("#__NEXT_DATA__"))
    text = text.replace('<script id="__NEXT_DATA__" type="application/json">', '')
    text = text.replace('</script>', '')
    data = json.loads(text)['props']['pageProps']['initialState']['products']['list']

    items = []

    for i in range(len(data)):
        rawItem = data[i]
        item = rawItem['item']
        items.append(item)

    return items


def fetchNaverShoppingProducts(keyword):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    params1 = (
        ('query', keyword),
        ('frm', 'NVSHATC'),
        ('pagingIndex', 1),
        ('pagingSize', 80),
    )

    params2 = (
        ('query', keyword),
        ('frm', 'NVSHATC'),
        ('pagingIndex', 2),
        ('pagingSize', 80),
    )

    response1 = requests.get('https://search.shopping.naver.com/search/all', headers=headers, params=params1)
    response2 = requests.get('https://search.shopping.naver.com/search/all', headers=headers, params=params2)

    page1Items = parsePage(response1.text)
    page2Items = parsePage(response2.text)

    items = page1Items + page2Items
    for i in range(len(items)):
        item = items[i]
        item['rank'] = i + 1
    
    return items

def findProductRankWithinNaverShoppingProductsByUrl(productUrl):
    pass

print(fetchNaverShoppingProducts("폼클렌징"))