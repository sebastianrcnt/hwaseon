import asyncio
import json
from flask import Flask, render_template, request
from legacy.blog_rank_new import get_blog_data

app = Flask(__name__)

# API SERVER
@app.route("/api/blog_rank")
def get_blog_rank():
    blog_id = request.args.get('blogId')

    if not blog_id:
        return 'bad request', 400

    data = asyncio.run(get_blog_data(blog_id))
    return json.dumps(data)
