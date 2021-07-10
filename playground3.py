# import asyncio
# from pprint import pprint
# import datetime
# from server.services.sources.unofficial import fetch_category_shopping_trend


# res = asyncio.run(fetch_category_shopping_trend(50000204, datetime.date(2021, 6, 6), datetime.date(2021, 7, 6)))

# pprint(res)
from timeit import default_timer as timer

from server.services.api.blog_statistics import fetch_blog_statistics
import asyncio

start = timer()
res = asyncio.run(fetch_blog_statistics("8075rkdehd"))
end = timer()
print(res)
print(end - start)
