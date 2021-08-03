from server.services.sources.unofficial import fetch_naver_search_related_keywords
import asyncio

result = asyncio.run(fetch_naver_search_related_keywords("소주"))
print(result)