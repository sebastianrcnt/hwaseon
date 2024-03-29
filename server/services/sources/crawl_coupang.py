from concurrent.futures.process import ProcessPoolExecutor
import os
import json
from concurrent.futures import as_completed, ProcessPoolExecutor
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.parse


def crawl_product_rank_within_keywords_coupang(keywords, productUrl):
    search_results = {}
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(
            crawl_products, keyword, 1): keyword for keyword in keywords}
        for keyword in as_completed(futures):
            future = futures[keyword]
            data = keyword.result()
            search_results[future] = data

    search_ranks = {}
    # return search_results
    for keyword in keywords:
        products = search_results[keyword]
        for idx in range(len(products)):
            product = products[idx]
            if product['id'] in productUrl:
                search_ranks[keyword] = {
                    'rank': idx,
                    'product': product
                }
                break
        if keyword not in search_ranks:
            search_ranks[keyword] = {
                'product': None,
                'rank': -1
            }

    return search_ranks


def crawl_products(keyword, max_page):
    products = {}
    pages = list(range(1, max_page + 1))
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(
            crawl_page, keyword, page): page for page in pages}
        for page in as_completed(futures):
            future = futures[page]
            data = page.result()
            products[future] = data

    products_list = []
    for page in range(1, max_page + 1):
        products_list += products[page]

    return products_list


def crawl_page(keyword, page):
    LIST_SIZE = 100
    keyword = urllib.parse.quote(keyword, safe="")
    result = os.popen(f"""
    curl 'https://www.coupang.com/np/search?component=&q={keyword}&listSize={LIST_SIZE}&page={page}&channel=user' -s -H 'authority: www.coupang.com' -H 'pragma: no-cache' -H 'cache-control: no-cache' -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' -H 'sec-ch-ua-mobile: ?0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: navigate' -H 'sec-fetch-user: ?1' -H 'sec-fetch-dest: document' -H 'referer: https://www.coupang.com/np/search?rocketAll=false&q=%EC%88%98%EB%B6%84%EC%97%90%EC%84%BC%EC%8A%A4&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=36' -H 'accept-language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7' -H $'cookie: PCID=24484167248594641608131; MARKETID=24484167248594641608131; _fbp=fb.1.1625458542207.1746517345; X-CP-PT-locale=ko; gd1=Y; _gcl_au=1.1.1146918178.1625458747; sid=ae1ceda606244c15bc87171ab40961d0a9ffc532; overrideAbTestGroup=%5B%5D; _abck=0B48471A59ACE77CD65DE292EB4CBDBE~0~YAAQTA3VF6uEZFB6AQAA9GEklQaBfRn1W2dBznRCaFMp3PNJ0/Hnob1u1sAEQY1YWBOFAGYzKfkw02du/7aozeARjl/+AzsEu4QFP4SvdGmq6q2JXer5Pn8szfygqCffLBoUOE2dhKmvMUKOhdeBtkv3/8Y5vimW24Z27+P56bpXWnz1wpsjHH3jgGCvR4vV5+rWln99ZvkCEhvi0QJFb7l4NdQLnvd2NpeJ16YbvxOMvNOY//iId8OUY1Zw9Hax1Fghl6ngXcYbED2Lp2wKg7SIrty1zMJsX7how/dcK0B0DLJTL6xeQoDvi7v2lvpo1NiJbupsigpgQPsoUaByx9u/C6o8vTWWvlsHu6VgTxP+Tw1ieYFEFgHFhs3C+hxqRRltLc6QnWEVpqXhJ611TrdJEMKlKYfbgA==~-1~-1~-1; bm_sz=F3987CC942B76E68BC8A3864084981A3~YAAQTA3VF62EZFB6AQAA9GEklQx1pHVC+hAcJm+Wgiay3bG2PU2MIY5k8fOQA6uwuc94ejbHFZyhCwtj8+ite4yNGVHhymWOR/HL/iPyp74bE0LKqkesYyxgEGemvc9UjQoUfjuPEqKhVOyLwnWPBN7cBu4IeTMUW2/a/WiAfv1cW9yAtpn1EstZ1a8LYwEthsydPAFHlk+diskuXDw5VeW0XJQZ5o+XjlcnuHxwEVztj33n36APzFu4JMRKPzM5fSsfd0KfM+vuvuM9E1k3SpWzfFtAwEE/d+0/7X6ACrswt97o~4338241~3158340; ak_bmsc=41C74C14B5BC779075C2CC87AC4E1EEF~000000000000000000000000000000~YAAQTA3VFxWHZFB6AQAAuGUklQwKfhQWfKctez9hDvs9ZbE+EM9erQ/xsWdQoC1niKfYcOtbFNjxSmiEMhgReE+u81mG/Ax3BWEtpkN++JFt0Ik1movk/wAU0G+Xyqxdb6nt7kB4iQ3FP3RUE42whTArVJSPSi45uzaZlrxaX+IbbQtSDndH7wPWy4V2oPNEpUS3ZK8/f2A6n89Ju5HNYB0kkWxAITiSr7KC/pczX2Zj+XSbrHlMoi7OQC/Xwr1dhMzOS+rDi4UE1XmRBpH9vez6O98HiApQoEYqoYd8Y1AbcvC+I78Kah35aLRAwGQHdSWXMXYllzJAj+IE4SeiAPyNEeZk2CTVEyK9256daLad892MoAl96A//8CXCKQmiZ//xN8hWag3I5SDFNCpbsGKaT3pCdDBywHir04CrxzOxBGbnge2hN5bbRuUl7wh7/oqI3tdr+eJwTUUNTSsdVDXIYV+LdbHeP8c9v1Z69QCt5157dHDKY/Bp2idc; searchKeyword=c%20hdmi%7Chdmi%7Cusb%20%ED%97%88%EB%B8%8C%7Chdmi%20%EC%BC%80%EC%9D%B4%EB%B8%94%7C%EC%88%98%EB%B6%84%EC%97%90%EC%84%BC%EC%8A%A4; searchKeywordType=%7B%22c%20hdmi%22%3A0%7D%7C%7B%22hdmi%22%3A0%7D%7C%7B%22usb%20%ED%97%88%EB%B8%8C%22%3A0%7D%7C%7B%22hdmi%20%EC%BC%80%EC%9D%B4%EB%B8%94%22%3A0%7D%7C%7B%22%EC%88%98%EB%B6%84%EC%97%90%EC%84%BC%EC%8A%A4%22%3A0%7D; FUN="{{\'search\':[{{\'reqUrl\':\'/search.pang\',\'isValid\':true}}]}}"; baby-isWide=small; bm_sv=443481DA99D5F4E25104154846D41F0F~NgH+jQXzIvWnGjoRhNjahSZ8a6/BejvRXllj+IoKPMlALCzEticcalyKibWbgiZFvCgHKF+frcpq6SiP8nAsix3QjTieoOJSpXYEWEIpfUukSMtUWjeIfb/t4JP5z/yVb0eWx+R6leetWsq+CbiZGxPkd3E5JO5ZlViI5vAPGCk=' --compressed
    """).read()
    bs = BeautifulSoup(result, features="html.parser")
    product_elements = bs.select('.search-product')
    products = []
    for product_element in product_elements:
        name = product_element.select_one('.name').text
        product = {
            'id': product_element['id'],
            'name': name
        }
        products.append(product)
    return products

# products = crawl_product_rank_within_keywords(['수분에센스', '에센스추천', '촉촉한에센스', '피부붉은기', '얼굴붉은기'], 4570063730)
# pprint(products)


# essense = crawl_products('선풍기', 1)
# target = '1662414493'

# pprint(essense)
# pprint(len(essense))

# pprint(crawl_product_rank_within_keywords_coupang(
#     ['브리즈킹', '선풍기'], '1662414493'))
