import json
import asyncio
import concurrent

import aiohttp
from server.services.sources.unofficial import get_blog_post_published_count
from urllib.parse import urlparse
from utils.util import safeget

import requests
from bs4 import BeautifulSoup

import pandas as pd
from pprint import pprint

# CONSTANTS
BLOG_BASE_URL = 'https://m.blog.naver.com/'
NAVER_MOBILE_BLOG_SEARCH_BASE_URL = 'https://m.search.naver.com/search.naver?sm=mtb_hty.top&where=m_view&oquery=4&tqi=h7Lx1wp0JxCssvUuSC0sssssted-488674&query='
MAX_POSTS = 15


# async def fetch_blog_statistics(blog_id):
#     '''
#     블로그 정보 가져오기

#     1) 글 제목, 글별 키워드(해시태그), View 순위, 통합 View 노출 수, Total 검색량, 컨텐츠 발행량
#     '''

#     # post 목록 가져오기
#     post_list_data = await fetch_blog_posts(blog_id)
#     post_list_data = post_list_data[:MAX_POSTS]
#     posts = []

#     # post 데이터 추출
#     for i in range(len(post_list_data)):
#         post = post_list_data[i]
#         url = f"https://m.blog.naver.com/PostView.naver?blogId={blog_id}&logNo={post['logNo']}&navType=tl"
#         posts.append({
#             'id': post['logNo'],
#             'title': post['titleWithInspectMessage'],
#             'url': url,
#             'viewRank': i + 1,
#         })

#     # get hashtags
#     get_hashtag_tasks = [fetch_blog_post_hashtags(post['url']) for post in posts]
#     post_hashtags = await asyncio.gather(*get_hashtag_tasks)
#     for i in range(len(post_hashtags)):
#         post = posts[i]
#         post['hashTags'] = post_hashtags[i]
#         main_hash_tag = safeget(post['hashTags'], 0)
#         post['mainHashTag'] = main_hash_tag
    
#     # get hashtag search rank
#     get_search_rank_tasks = [fetch_blog_post_naver_main_search_rank(post['id'], post['mainHashTag']) for post in posts]
#     post_search_ranks = await asyncio.gather(*get_search_rank_tasks)
#     for i in range(len(post_search_ranks)):
#         post = posts[i]
#         if not post['mainHashTag']:
#             post['searchRank'] = -1
#         else:
#             post['searchRank'] = post_search_ranks[i]

#     return posts


async def fetch_blog_posts(blog_id):
    '''블로그 포스트 가져오기'''

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
        ('blogId', blog_id),
        ('categoryNo', '0'),
        ('currentPage', '1'),
        ('logCode', '0'),
    )

    html = requests.get(
        f'https://m.blog.naver.com/rego/ThumbnailPostListInfo.naver', headers=headers, params=params).text

    return json.loads(html[5:])['result']['postViewList']


async def fetch_blog_post_hashtags(blog_id, post_id):
    '''블로그 포스트가 태그된 해시태그 목록 가져오기'''
    # print(f"[start] crawling post {post_url}")
    url = f'https://m.blog.naver.com/{blog_id}/{post_id}'
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    tags_element = soup.select_one('.post_tag')

    if not tags_element:
        return []

    tags = tags_element.text
    tags = tags.replace('\n', '').split('#')[1:]
    # print(f"[end] crawling post {post_url}")
    return tags

# PART 2: RANK


async def fetch_blog_post_naver_main_search_rank(post_id, keyword):
    '''블로그 포스트가 특정 키워드 하에서 검색순위가 몇위인지?'''
    # search keyword in mobile naver
    # print(f'[start] task {post_id}')
    url = NAVER_MOBILE_BLOG_SEARCH_BASE_URL + keyword
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')

    # print(f'[end] task {post_id}')
    # get all <post> search results
    searched_post_elements = soup.select('.bx._svp_item')

    for searched_post_element in searched_post_elements:
        rank = searched_post_element.attrs['data-cr-rank']
        link = searched_post_element.select_one(
            '.total_wrap > a').attrs['href']
        found_post_id = safeget(urlparse(link).path.split('/'), 2)
        if found_post_id == post_id:
            return int(rank)
    return 0


if __name__ == "__main__":
    res = asyncio.run(fetch_blog_statistics('dotoree0103'))
    print(json.dumps(res, ensure_ascii=False))
