import server.services.api.KeywordServices as KeywordServices
import server.services.api.ApiServices as ApiServices
import pandas as pd
from pprint import pprint

# test crawler services
# 월간 검색수, 월간 발행수
print(KeywordServices.getMonthlyPublishedBlogPosts('폼클렌징'))
print(KeywordServices.getMonthlyPublishedCafePosts('가위'))

# 네이버 검색 자동완성 키워드 가져오기
# 네이버 쇼핑 자동완성 키워드 가져오기
# print(KeywordServices.getNaverSearchAutocomplteteKeywords('카페'))
# print(KeywordServices.getNaverShoppingAutocomplteteKeywords('카페'))



# #
# abs1 = ApiServices.getKeywordStatistics('폼클렌징')[0]
# rel1 = ApiServices.getKeywordRelativeRatio('폼클렌징', True)


# print(pd.DataFrame([abs1]))
# print(pd.DataFrame(rel1))

# # pprint(dict.keys(res))
# df = pd.DataFrame(res['keywordList'])
# df.to_csv("result2.csv")
