import datetime
import json
import asyncio
from functools import wraps
from server.services.sources.crawl_naver import crawl_product_rank_within_keywords_naver
from server.services.sources.crawl_coupang import crawl_product_rank_within_keywords_coupang
from server.services.api.blog_statistics import fetch_blog_post_hashtags, fetch_blog_post_naver_main_search_rank, fetch_blog_posts

from utils.util import hasattrs
from utils.TimeUnitEnum import TimeUnit
from server.services.sources.official import fetch_related_keywords, fetch_relative_ratio
from server.services.sources.unofficial import fetch_category_shopping_trending_keywords, fetch_naver_shopping_products, fetch_search_category, get_PC_search_section_order, get_blog_post_published_count, get_cafe_post_published_count, get_mobile_search_section_order, fetch_naver_search_autocomplete_keywords, fetch_naver_shopping_autocomplete_keywords
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

"""
- 키워드 검색량(월) - 전월대비
- 키워드 발행량(월) - 전월대비
- 쇼핑별 위치
"""


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped


@app.route("/", methods=['GET'])
def index():
    return "Hello World", 200


@app.route("/api/v1/keyword-services/publish-count", methods=['GET'])
@async_action
async def get_publish_count():
    '''발행량'''
    if not hasattrs(request.args, ['keyword', 'startDate']):
        return "keyword, startDate is required", 400

    keyword = request.args['keyword']
    try:
        start_date_str = request.args['startDate']
        start_date = datetime.date.fromisoformat(start_date_str)
        if request.args['endDate']:
            end_date_str = request.args['endDate']
            end_date = datetime.date.fromisoformat(end_date_str)
        else:
            end_date = datetime.date.today()
        if start_date > end_date:
            return "start date should be before end date", 400
    except:
        return "invalid format", 400
    blog, cafe = await asyncio.gather(
        get_blog_post_published_count(keyword, start_date, end_date),
        get_cafe_post_published_count(keyword, start_date, end_date),
    )

    return json.dumps({
        'keyword': keyword,
        'period': {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
        },
        "blog": blog,
        "cafe": cafe,
    })

# 발행량


@app.route("/api/v1/keyword-services/relkeyword-search-statistics", methods=['GET'])
@async_action
async def get_relkeyword_search_statistics():
    '''연관키워드'''
    if not 'keyword' in request.args or not 'month' in request.args:
        return 'no keyword or month', 400

    keyword = request.args['keyword']
    month = int(request.args['month'])

    related_keywords = await fetch_related_keywords(keyword, month)
    if len(related_keywords) < 1:
        return "error", 400

    return jsonify({
        'keyword': keyword,
        'month': month,
        'data': related_keywords[0],
        'keywords': related_keywords[1:]
    })


@app.route("/api/v1/keyword-services/naver-search-autocomplete", methods=['GET'])
@async_action
async def get_naver_search_autocomplete():
    '''연관키워드'''
    if not hasattrs(request.args, ['keyword']):
        return 'no keyword', 400

    keyword = request.args['keyword']
    related_keywords = await fetch_naver_search_autocomplete_keywords(keyword)

    return jsonify(related_keywords)


@app.route("/api/v1/keyword-services/naver-shopping-autocomplete", methods=['GET'])
@async_action
async def get_naver_shopping_autocomplete():
    '''연관키워드'''
    if not hasattrs(request.args, ['keyword']):
        return 'no keyword', 400

    keyword = request.args['keyword']
    related_keywords = await fetch_naver_shopping_autocomplete_keywords(keyword)

    return jsonify(related_keywords)


@app.route("/api/v1/keyword-services/relative", methods=['GET'])
@async_action
async def get_relative_ratio():
    '''연관키워드'''
    if not hasattrs(request.args, ['keywords', 'startDate']):
        return "keywords, startDate is required", 400
    keywords = [x.strip() for x in request.args['keywords'].split(',')]
    try:
        start_date_str = request.args['startDate']
        start_date = datetime.date.fromisoformat(start_date_str)
        if request.args['endDate']:
            end_date_str = request.args['endDate']
            end_date = datetime.date.fromisoformat(end_date_str)
        else:
            end_date = datetime.date.today()
        if start_date > end_date:
            return "start date should be before end date", 400
    except:
        return "invalid format", 400

    ratio = await fetch_relative_ratio(keywords, start_date, end_date, TimeUnit.DATE)
    return jsonify({
        'keywords': keywords,
        'period': {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
        },
        'ratio': ratio
    })


@app.route("/api/v1/keyword-services/search-section-order", methods=['GET'])
@async_action
async def get_search_section_order():
    if not hasattrs(request.args, ['keyword']):
        return 'no keyword', 400
    keyword = request.args['keyword']
    pc_order = get_PC_search_section_order(keyword)
    mobile_order = get_mobile_search_section_order(keyword)

    return jsonify({
        'keyword': keyword,
        'pc': pc_order,
        'mobile': mobile_order,
    })


@app.route("/api/v1/proxy-services/get-search-category", methods=['GET'])
@async_action
async def get_search_category():
    '''검색 카테고리 가져오기'''
    if not 'categoryId' in request.args:
        return 'no categoryId', 400

    cid = request.args['categoryId']
    categories = await fetch_search_category(cid)

    return jsonify(categories)


@app.route('/api/v1/proxy-services/get-category-shopping-trending-keywords', methods=['GET'])
@async_action
async def get_category_shopping_trending_keywords():
    if not hasattrs(request.args, ['categoryId', 'startDate']):
        return "categoryId, startDate is required", 400
    category_id = request.args['categoryId']
    try:
        start_date_str = request.args['startDate']
        start_date = datetime.date.fromisoformat(start_date_str)
        if request.args['endDate']:
            end_date_str = request.args['endDate']
            end_date = datetime.date.fromisoformat(end_date_str)
        else:
            end_date = datetime.date.today()
        if start_date > end_date:
            return "start date should be before end date", 400
    except:
        return "invalid format", 400

    data = await fetch_category_shopping_trending_keywords(category_id, start_date, end_date)
    return jsonify(data)


@app.route("/api/v1/keyword-services/get-naver-shopping-products", methods=['GET'])
@async_action
async def get_naver_shopping_products():
    '''네이버 키워드 상품/판매량 가져오기'''
    if not 'keyword' in request.args:
        return 'no keyword', 400
    keyword = request.args['keyword']
    products = await fetch_naver_shopping_products(keyword)
    return jsonify(products)


@app.route("/api/v1/blog-services/get-blog-posts", methods=['GET'])
@async_action
async def get_blog_posts():
    if not 'blogId' in request.args:
        return 'no blogId', 400
    blog_id = request.args['blogId']
    posts = await fetch_blog_posts(blog_id)
    return jsonify(posts)


@app.route("/api/v1/keyword-services/get-blog-post-naver-main-search-rank", methods=['GET'])
@async_action
async def get_blog_post_naver_main_search_rank():
    if not hasattrs(request.args, ['postId', 'keyword']):
        return 'no postId/keyword', 400
    post_id = request.args['postId']
    keyword = request.args['keyword']
    rank = await fetch_blog_post_naver_main_search_rank(post_id, keyword)
    return jsonify(rank)


@app.route("/api/v1/keyword-services/get-blog-post-hashtags", methods=['GET'])
@async_action
async def get_blog_post_hashtags():
    if not hasattrs(request.args, ['blogId', 'postId']):
        return 'no blogId / postId', 400

    blog_id = request.args['blogId']
    post_id = request.args['postId']

    hashtags = await fetch_blog_post_hashtags(blog_id, post_id)

    return jsonify(hashtags)


@app.route("/api/v1/product-services/get-product-rank-within-keywords/coupang", methods=["POST"])
@async_action
async def get_product_rank_within_keywords_coupang():
    body = request.json
    if not hasattrs(body, ['keywords', 'productUrl']):
        return 'no keywords / productUrl', 400
    result = crawl_product_rank_within_keywords_coupang(
        body['keywords'], body['productUrl'])
    return jsonify(result)


@app.route("/api/v1/product-services/get-product-rank-within-keywords/naver", methods=["POST"])
@async_action
async def get_product_rank_within_keywords_naver():
    body = request.json
    if not hasattrs(body, ['keywords', 'productUrl']):
        return 'no keywords / productUrl', 400
    url = body['productUrl']
    keywords = body['keywords']
    result = crawl_product_rank_within_keywords_naver(keywords, url)
    return jsonify(result)
