
import asyncio
from utils.TimeUnitEnum import TimeUnit
from server.services.sources.official import fetch_related_keywords, fetch_relative_ratio
import datetime
from pprint import pprint

res = asyncio.run(fetch_relative_ratio(
    '폼클렌징', datetime.date(2020, 1, 1), datetime.date(2020, 1, 5), TimeUnit.DATE))

datetime.date.today()

res = asyncio.run(fetch_related_keywords('폼클렌징'))
day1 = datetime.date(2000, 1, 1)
pprint(res)
