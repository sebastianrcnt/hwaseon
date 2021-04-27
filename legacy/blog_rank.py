import json
import time
from time import sleep

import urllib
from urllib.request import Request, urlopen
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import concurrent.futures
import pandas as pd

# ### 알고리즘 ###
# 1. 아이디 입력
# 2. 해당 블로거 최신글 10개 가져오기
# 3. 해시태그와 제목 비교. 키워드 자동생성 클릭시, 일치하는 가장 긴 단어를 추출
# 4. 추출 된 단어는 수정 가능해야함.
# 5. 최종으로 수정된 키워드를 검색 클릭시, 모바일view탭에서 몇위인지 안내.(AD 제외 순위)
# 6. 키워드만 변경 후, 클릭시 재동작
# 7. 키워드 자동생성 클릭시, 검색어 값에 다시 값 입력되기.


### 블로그 지수 확인 ###
# 아이디입력
idid = 'like5183'


#### 블로그 최신글 10개 가져오기 ###
#### selenium ###
# 크롬 켜기
# driver = webdriver.Chrome('C:/chromedriver.exe')
driver = webdriver.Chrome("drivers/chromedriver")
# 주소 접속. 꼭 모바일로 접속하기
driver.get('https://m.blog.naver.com/'+idid)
sleep(0.5)
# 나열식으로 보기
driver.find_element_by_class_name("btn_list").click()
sleep(0.5)
# 파싱
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
# 크롬 끄기
driver.close()
# 닉네임가져오기
nickname = ''
nickname = soup.find(class_='user_name').text
# 제목 가져오기
b = soup.find_all(class_='title ell')
sleep(0.5)
# 제목 tlist랑 공백제거 tlist_no_space(키워드자동완성위함)
tlist = []
tlist_no_space = []
for i in range(0, len(b)):
    tlist.append(b[i].text)
    tlist_no_space.append(b[i].text.replace(" ", ""))
########## 링크 linklist ###########
linklist = []
for a in soup.find_all('div', {"class": "postlist"}):
    linklist.append('https://m.blog.naver.com/' +
                    idid + a['id'].replace('pl_', '/'))


### 함수 정의 ###
########## 각 글별 자동키워드(해시태그분석) 가져오기 #########
def find_key_auto(number):
    testlist = []
    testlist.append(nickname)
    testlist.append(str(number) + "번째")
    testlist.append(tlist[number])
    req = requests.get(linklist[number])
    req = req.text
    soup = BeautifulSoup(req, 'html.parser')
    # 태그가져오기
    if soup.find(class_='post_tag') == None:
        testlist.append('-')  # 일치없음 > 공란처리 ****************************
    else:
        tags = soup.find(class_='post_tag').text
        tags = tags.replace("\n", "")
        tags = tags.split("#")
        tags = list(filter(None, tags))
        # 해시 태그와 제목의 중복값 리스트 만들기
        samelist = []
        for i in tags:
            if i in tlist_no_space[number]:
                samelist.append(i)
            else:
                pass

        # 가장 긴 키워드를 메인키워드로 하기
        # 값이 같을시, 먼저 써있는게 우선으로 나옴
        if samelist == []:
            testlist.append('-')  # 일치없음 > 공란처리 ****************************
        else:
            best = 0
            for index in range(len(samelist)):
                if len(samelist[index]) > len(samelist[best]):
                    best = index
            testlist.append(samelist[best])
    testlist.append(linklist[number])

    key_auto_list.append(testlist)


### 멀티쓰레드 ###
key_auto_list = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(find_key_auto, [(i) for i in range(0, len(linklist))])

#### 판다스 df3 / 글10개 + 키워드 등###
df3 = pd.DataFrame(key_auto_list, columns=['닉네임', '최신순', '제목', '키워드', 'URL'])
df3 = df3.sort_values(by=['최신순', ], ascending=True)
df3 = df3.reset_index(drop=True)


####### 키워드별 뷰 30개씩 정보 가져오기 #######
auto_choice = list(df3['키워드'])
### 키워드 입력 ###
### 지금은 오토로 가져온걸로 되게 하기 ###
key_list = auto_choice

# 함수설정


def viewrank(keyword):
    if keyword == '-':  # 수정******************************
        pass

    elif keyword == '':  # 수정******************************
        pass
    elif keyword == None:  # 수정******************************
        pass
    else:
        total_view_count = 'https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query='+keyword
        req = requests.get(total_view_count)
        req = req.text
        soup = BeautifulSoup(req, 'html.parser')
        noad_view_count = len(soup.find_all(class_='bx _svp_item'))
        adview_count = len(soup.find_all(class_='ico_ad spview_bf'))

        key_url = 'https://m.search.naver.com/search.naver?where=m_view&query=' + \
            keyword + '&sm=mtb_viw.all&nso=&mode=normal&main_q=&st_coll=&topic_r_cat='
        req = requests.get(key_url)
        req = req.text
        soup = BeautifulSoup(req, 'html.parser')
        # 첫페이지 40여개 파싱
        search_all = soup.find_all('a', {'class': 'api_txt_lines total_tit'})
        # 랭킹용 숫자
        rank_numb = 0
        ###
        for k in range(0, len(search_all)):
            # 광고는 지나가기
            if 'https://adcr.naver.com' in search_all[k]['href']:
                pass
            else:
                list_sub = []
                # 광고 없을 때의 순위 따로 채크
                rank_numb = rank_numb + 1
                list_sub.append(rank_numb)
                # 제목
                title = search_all[k].text
                list_sub.append(keyword)
                list_sub.append(title)
                list_sub.append(search_all[k]['href'])
                list_sub.append(noad_view_count)
                list_sub.append(adview_count)
                list_main.append(list_sub)


### 멀티쓰레드 ###
list_main = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(viewrank, key_list)

df2 = pd.DataFrame(list_main, columns=[
                   '랭킹', '키워드', '제목', 'URL', '통합View 노출수', '통합View AD수'])
df2 = df2.sort_values(by=['키워드', '랭킹', ], ascending=True)
df2 = df2.reset_index(drop=True)

### 값 체크하기 ###
ranking_list = []
for i in range(0, len(list_main)):
    testlist = []
    if df2['URL'][i] in list(df3['URL']):
        testlist.append(int(df2['랭킹'][i]))
        testlist.append(str(df2['URL'][i]))
        testlist.append(str(df2['통합View 노출수'][i]))
        testlist.append(str(df2['통합View AD수'][i]))
        ranking_list.append(testlist)
    else:
        pass

df4 = pd.DataFrame(ranking_list, columns=[
                   '랭킹', 'URL', '통합View 노출수', '통합View AD수'])
df4 = df4.sort_values(by=['랭킹', 'URL', ], ascending=True)
df4 = df4.reset_index(drop=True)

### 결과 값 ###
df_final = pd.merge(df3, df4, on="URL", how='left')

df_final.to_csv("./result.csv")