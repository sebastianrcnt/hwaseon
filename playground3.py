from bs4 import BeautifulSoup
import requests

headers = {
    'authority': 'search.shopping.naver.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://search.shopping.naver.com/search/all?query=%EC%88%98%EB%B6%84%EC%97%90%EC%84%BC%EC%8A%A4&frm=NVSHATC&prevQuery=%EC%88%98%EB%B6%84%EC%97%90%EC%84%BC%EC%8A%A4',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=J7L6CQ53UDQWA; nx_ssl=2; AD_SHP_BID=22; ASID=d3c999830000017a7ce2005200000056; _ga=GA1.2.686722733.1626001005; _gid=GA1.2.2050099600.1626001005; _shopboxeventlog=false; BMR=s=1626013763708&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dtownpharm%26logNo%3D221242852808&r2=https%3A%2F%2Fwww.google.com%2F; sus_val=fwwWHJ2TyMPX9gY/dDV93mXn; spage_uid=',
}

params = (
    ('query', '수분에센스'),
    ('frm', 'NVSHATC'),
)

response = requests.get(
    'https://search.shopping.naver.com/search/all', headers=headers, params=params)
html = response.text
bs = BeautifulSoup(html, features='html.parser')
products = bs.select('#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div li')

for product in products:
    print(product)
