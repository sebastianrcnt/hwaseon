import json
import asyncio
from functools import wraps
from server.services.sources.unofficial import get_monthly_published_blog_posts, get_monthly_published_cafe_posts
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

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


# 발행량
@app.route("/api/v1/keyword-services/monthly-published-count", methods=['GET'])
@async_action
async def get_monthly_published_count():
    keyword = request.args['keyword']
    monthlyPublishedBlogPosts = await get_monthly_published_blog_posts(keyword)
    monthlyPublishedCafePosts = await get_monthly_published_cafe_posts(keyword)

    return json.dumps({
        "cafe": monthlyPublishedCafePosts,
        "blog": monthlyPublishedBlogPosts
    })