import server.services.api.KeywordServices as KeywordServices
import server.services.api.ApiServices as ApiServices
import pandas as pd

# test crawler services
# 월간 검색수, 월간 발행수
print(KeywordServices.getMonthlyPublishedBlogPosts('카페'))
print(KeywordServices.getMonthlyPublishedCafePosts('카페'))

# 네이버 검색 자동완성 키워드 가져오기
# 네이버 쇼핑 자동완성 키워드 가져오기
print(KeywordServices.getNaverSearchAutocomplteteKeywords('카페'))
print(KeywordServices.getNaverShoppingAutocomplteteKeywords('카페'))


#
res = ApiServices.getKeywordStatistics('폼클렌징')
df = pd.DataFrame(res['keywordList'])
df.to_csv("result2.csv")
