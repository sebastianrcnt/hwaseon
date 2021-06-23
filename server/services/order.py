import requests
import bs4

"""
이런 식으로 어떤 섹션 이름들은 안에 지저분하게 뭐가 들어가있음
주로는 api_title_inner, 아이콘 등이니까 지워버리면 순수한 섹션 제목이 나오게 되어있당

<h2 class="api_title"> <i class="spnew api_ico_shoplogo"></i>네이버쇼핑<div class="api_title_inner"> <a role="button" href="#" class="api_link_help _trigger" aria-pressed="false" title="이 정보가 표시된 이유" onclick="return tCR('a=shp_gui.imark&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew api_ico_alert">이 정보가 표시된 이유</i></a> <div class="ly_api_info _content"> <p class="dsc">네이버가 운영하는 쇼핑 서비스입니다.</p> <button type="button" class="btn_close _trigger" title="안내 레이어 닫기" onclick="return tCR('a=shp_gui.guideclose&amp;r=&amp;i=&amp;u=javascript');"><i class="spnew ico_close">정보확인 레이어 닫기</i></button> </div> </div> </h2>
"""

def getPCSearchSectionOrder(query):
    """
    키워드 검색 시 섹션의 순서 가져오기
    - 예) [파워링크, 네이버쇼핑, VIEW, 지식iN 플레이스, N쇼핑 LIVE]
    """
    response = requests.get(f"https://search.naver.com/search.naver?query={query}")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # 지울 것들 지우기(아이콘)
    deletes = soup.select(".api_title_inner, i")
    for delete in deletes:
        delete.decompose() # 지워버리기

    result = []

    titles = soup.select(".ad_section h2, .api_title")
    for title in titles:
        result.append(title.get_text(strip=True)) 

    return result

def getMobileSearchSectionOrder(query):
    response = requests.get(f"https://m.search.naver.com/search.naver?query={query}")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # 지울 것들 지우기(아이콘)
    deletes = soup.select(".api_title_inner, i")
    for delete in deletes:
        delete.decompose() # 지워버리기

    result = []

    titles = soup.select(".ad_section h2, .api_title")
    for title in titles:
        result.append(title.get_text(strip=True)) 

    return result