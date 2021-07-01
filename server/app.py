import datetime
import json
import asyncio
from functools import wraps
from utils.TimeUnitEnum import TimeUnit
from server.services.sources.official import fetch_related_keywords, fetch_relative_ratio
from server.services.sources.unofficial import fetch_search_category, get_PC_search_section_order, get_blog_post_published_count, get_cafe_post_published_count, get_mobile_search_section_order
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API SERVER
# @app.route("/api/blog_rank")
# def get_blog_rank():
#     blog_id = request.args.get('blogId')

#     if not blog_id:
#         return 'bad request', 400

#     data = asyncio.run(get_blog_data(blog_id))
#     return json.dumps(data)


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


@app.route("/api/v1/keyword-services/publish-count", methods=['GET'])
@async_action
async def get_publish_count():
    '''발행량'''
    keyword = request.args['keyword']
    try:
        if not request.args['startDate']:
            return "start date not specified", 400
        else:
            start_date_str = request.args['startDate']
            start_date = datetime.date.fromisoformat(start_date_str)
        if request.args['endDate']:
            end_date_str = request.args['endDate']
            end_date = datetime.date.fromisoformat(end_date_str)
        else:
            end_date = datetime.date.today()
        if start_date > end_date:
            return "start date should preceed end date", 400
    except:
        return "invalid format", 400

    blog = await get_blog_post_published_count(keyword, start_date, end_date)
    cafe = await get_cafe_post_published_count(keyword, start_date, end_date)

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

    return jsonify({
        'keyword': keyword,
        'month': month,
        'data': related_keywords[0],
        'keywords': related_keywords[1:]
    })


@app.route("/api/v1/keyword-services/relative", methods=['GET'])
@async_action
async def get_relative_ratio():
    '''연관키워드'''
    keywords = [x.strip() for x in request.args['keywords'].split(',')]

    try:
        if not request.args['startDate']:
            return "start date not specified", 400
        else:
            start_date_str = request.args['startDate']
            start_date = datetime.date.fromisoformat(start_date_str)
        if request.args['endDate']:
            end_date_str = request.args['endDate']
            end_date = datetime.date.fromisoformat(end_date_str)
        else:
            end_date = datetime.date.today()
        if start_date > end_date:
            return "start date should preceed end date", 400
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
    if not 'keyword' in request.args:
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
    if not 'categoryId' in request.args:
        return 'no categoryId', 400

    cid = request.args['categoryId']
    categories = await fetch_search_category(cid)

    return jsonify(categories)
