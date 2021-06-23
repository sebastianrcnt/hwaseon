import time
import requests

from server.services.tools.signatureHelper import Signature

# SECRETS
BASE_URL = 'https://api.naver.com'
API_KEY = '01000000001a1cd1c77e64fda7125be469a09d1682cd106a9419fea155f22df2d4261efac4'
SECRET_KEY = 'AQAAAAAaHNHHfmT9pxJb5GmgnRaCZU5NF5wTwLxdGE30+yEYFA=='
CUSTOMER_ID = '2235522'


def generateHeader(method, uri, apiKey, secretKey, customerId):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(
        timestamp, method, uri, secretKey)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': apiKey, 'X-Customer': str(customerId), 'X-Signature': signature}


async def fetchOfficialApi(uri, method, params):
    headers = generateHeader(method, uri, API_KEY,
                             SECRET_KEY, CUSTOMER_ID)
    return requests.get(BASE_URL + uri, params=params,
                        headers=headers).json()
