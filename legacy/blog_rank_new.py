import json
from os import link, write
import time
from time import sleep

import urllib
from urllib.parse import parse_qs, parse_qsl, urljoin, urlparse
from urllib.request import Request, urlopen
import re
import sys
from utils.util import safeget

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import concurrent.futures
import pandas as pd

# CONSTANTS
BLOG_BASE_URL = 'https://m.blog.naver.com/'
NAVER_MOBILE_BLOG_SEARCH_BASE_URL = 'https://m.search.naver.com/search.naver?sm=mtb_hty.top&where=m_view&oquery=4&tqi=h7Lx1wp0JxCssvUuSC0sssssted-488674&query='


def get_active_html(url):
    '''CSR 완료된 HTML 가져오기'''
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get(url)

    # fetch javascript
    time.sleep(1)
    html = driver.page_source
    driver.close()
    return html

def get_blog_data(blog_id):
    '''블로그 정보 가져오기'''
    url = urljoin(BLOG_BASE_URL, blog_id)
    html = get_active_html(url)
    soup = BeautifulSoup(html,'html.parser')

    nickname = soup.select_one('.user_name').text

    post_elements = soup.select('.card_section')
    posts = []
    for i in range(len(post_elements)):
        post_element = post_elements[i]
        title = post_element.select_one('.tit.ell').text
        url = urljoin(BLOG_BASE_URL, post_element.select_one('a.thumb_link').attrs['href'])
        post_id = parse_qs(urlparse(url).query)['logNo'][0]

        posts.append({
            'id': post_id,
            'title': title,
            'url': url,
            'viewRank': i + 1
        })

    for post in posts:
        post['hashTags'] = get_blog_post_hashtags(post['url'])
        post['searchRank'] = get_blog_post_naver_main_search_rank(post['id'], post['hashTags'][0])

    print(json.dumps(posts, ensure_ascii=False, indent=2))
    

def get_blog_post_hashtags(post_url):
    '''블로그 포스트가 태그된 해시태그 목록 가져오기'''
    soup = BeautifulSoup(requests.get(post_url).text, 'html.parser')
    tags_element = soup.select_one('.post_tag')

    if not tags_element:
        return []

    tags = tags_element.text
    tags = tags.replace('\n', '').split('#')[1:]

    return tags

def get_blog_post_naver_main_search_rank(post_id, keyword):
    '''블로그 포스트가 특정 키워드 하에서 검색순위가 몇위인지?'''
    # search keyword in mobile naver
    url = NAVER_MOBILE_BLOG_SEARCH_BASE_URL + keyword
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    # get all <post> search results
    searched_post_elements = soup.select('.bx._svp_item')
    
    for searched_post_element in searched_post_elements:
        rank = searched_post_element.attrs['data-cr-rank']
        link = searched_post_element.select_one('.total_wrap > a').attrs['href']
        found_post_id = safeget(urlparse(link).path.split('/'), 2)
        if found_post_id == post_id:
            return int(rank)
    return 0



get_blog_data('like5183')